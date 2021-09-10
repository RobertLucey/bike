import os
import hashlib

import fast_json
import shapely

from networkx.readwrite import json_graph
import osmnx as ox

from via import logger
from via.utils import (
    filter_nodes_from_geodataframe,
    filter_edges_from_geodataframe,
    update_edge_data
)
from via.nearest_edge import nearest_edge
from via.network_cache import network_cache
from via.base_cache import BaseCache
from via.constants import GEOJSON_DIR


bounding_graph_gdfs_cache = BaseCache(cache_type='bounding_graph_gdfs_cache')


class SnappedRouteGraphMixin():

    @property
    def snapped_route_graph(self):
        """
        Get the route graph, snapping to the nearest edge
        """
        bounding_graph = self.graph

        nearest_edge.get(bounding_graph, self.all_points)

        edges = []
        used_node_ids = []
        for our_origin in self.all_points:
            nearest_edges = nearest_edge.get(
                bounding_graph,
                [
                    our_origin
                ]
            )
            edge = our_origin.best_edge(nearest_edges)

            edges.append(tuple(edge[0]))
            used_node_ids.extend([edge[0][0], edge[0][1]])

        graph_key = hashlib.md5(str(list(bounding_graph.nodes)).encode()).hexdigest()
        if bounding_graph_gdfs_cache.get(graph_key) is None:
            bounding_graph_gdfs_cache.set(
                graph_key,
                ox.graph_to_gdfs(
                    bounding_graph,
                    fill_edge_geometry=True
                )
            )

        graph_nodes, graph_edges = bounding_graph_gdfs_cache.get(graph_key)

        # Filter only the nodes and edges on the route and ignore the
        # buffer used to get context
        graph = ox.graph_from_gdfs(
            filter_nodes_from_geodataframe(graph_nodes, used_node_ids),
            filter_edges_from_geodataframe(graph_edges, edges)
        )

        return update_edge_data(graph, self.edge_quality_map)


class GeoJsonMixin():

    def save_geojson(self):
        geojson_file = os.path.join(
            GEOJSON_DIR,
            self.content_hash + '.geojson'
        )

        if not os.path.exists(geojson_file):
            logger.debug(f'{geojson_file} not found, generating...')

            data = self.geojson

            if not os.path.exists(geojson_file):
                os.makedirs(
                    os.path.join(GEOJSON_DIR),
                    exist_ok=True
                )

            with open(geojson_file, 'w') as json_file:
                fast_json.dump(
                    data,
                    json_file,
                    indent=4
                )

    @property
    def geojson(self):
        """
        Write and return a GeoJSON object string of the graph.
        """
        geojson_file = os.path.join(
            GEOJSON_DIR,
            self.content_hash + '.geojson'
        )

        logger.debug(f'{geojson_file} generating...')

        json_links = json_graph.node_link_data(
            self.snapped_route_graph
        )['links']

        geojson_features = {
            'type': 'FeatureCollection',
            'features': []
        }

        for link in json_links:
            if 'geometry' not in link:
                continue

            feature = {
                'type': 'Feature',
                'properties': {}
            }

            for k in link:
                if k == 'geometry':
                    feature['geometry'] = shapely.geometry.mapping(
                        link['geometry']
                    )
                else:
                    feature['properties'][k] = link[k]

            geojson_features['features'].append(feature)

        return geojson_features


class BoundingGraphMixin():

    def get_bounding_graph(self, use_graph_cache=True):
        logger.debug(
            'Plotting bounding graph (n,s,e,w) (%s, %s, %s, %s)',
            self.most_northern,
            self.most_southern,
            self.most_eastern,
            self.most_western
        )

        if use_graph_cache is False or network_cache.get('bbox', self, poly=False) is None:
            logger.debug(f'bbox > {self.gps_hash} not found in cache, generating...')
            network = ox.graph_from_bbox(
                self.most_northern,
                self.most_southern,
                self.most_eastern,
                self.most_western,
                network_type=self.network_type,
                simplify=True
            )
            network_cache.set(
                'bbox',
                self,
                network
            )

        return network_cache.get('bbox', self, poly=False)

    @property
    def bounding_graph(self):
        """
        Get a rectangular graph which contains the journey
        """
        return self.get_bounding_graph(use_graph_cache=True)
