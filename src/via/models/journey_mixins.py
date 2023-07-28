from collections import defaultdict

import osmnx as ox

from via import settings
from via import logger
from via.utils import (
    filter_nodes_from_geodataframe,
    filter_edges_from_geodataframe,
    update_edge_data,
    get_graph_id,
    area_from_coords,
    get_combined_id,
)
from via.network_cache import network_cache

from via.bounding_graph_gdfs_cache import bounding_graph_gdfs_cache

from via.geojson.utils import geojson_from_graph


class SnappedRouteGraphMixin:
    @property
    def snapped_route_graph(self):
        """ """
        bounding_graph = self.graph

        # TODO: mappymatch here, or bypass all. Just need to update edge data from edgq quality. Maybe use self.edge_data / self.edge_quality_map

        # for all journeys in here get the edges used by them from edge_data? Can't get nodes, just get the combined_ids at the mo

        used_combined_edges = []
        for j in self:
            used_combined_edges.extend(list(j.edge_data.keys()))

        used_edges = []
        used_node_ids = []

        for start, end, _ in bounding_graph.edges:
            graph_edge_id = get_combined_id(start, end)
            if graph_edge_id in used_combined_edges:
                used_node_ids.extend([start, end])
                used_edges.append(tuple([start, end, 0]))

        if bounding_graph_gdfs_cache.get(get_graph_id(bounding_graph)) is None:
            bounding_graph_gdfs_cache.set(
                get_graph_id(bounding_graph),
                ox.graph_to_gdfs(bounding_graph, fill_edge_geometry=True),
            )

        graph_nodes, graph_edges = bounding_graph_gdfs_cache.get(
            get_graph_id(bounding_graph)
        )

        graph = ox.graph_from_gdfs(
            filter_nodes_from_geodataframe(graph_nodes, used_node_ids),
            filter_edges_from_geodataframe(graph_edges, used_edges),
        )

        return update_edge_data(graph, self.edge_quality_map)


class GeoJsonMixin:
    @property
    def geojson(self):
        """
        Write and return a GeoJSON object string of the graph.
        """

        from via.models.journeys import Journeys

        if isinstance(self, Journeys):
            region_map = defaultdict(Journeys)

            for journey in self:
                # use place_2 as place_1 is too specific and a journey that
                # starts in a place_1 could share roads with a journey that
                # starts in a different area nearby
                # This is also a possible issue with place_2 but will happen
                # much less, still a FIXME
                # {'cc': 'IE', 'place_1': 'Rathgar', 'place_2': 'Leinster', 'place_3': 'Dublin City'}
                region_name = journey.origin.gps.reverse_geo["place_2"]
                region_map[region_name].append(journey)

            if len(region_map) > 1:
                geo_features = []
                for region_name, journeys in region_map.items():
                    logger.debug(
                        "Getting geojson features of journeys group in region: %s",
                        region_name,
                    )
                    geo_features.extend(journeys.geojson["features"])

                geo_features = {"type": "FeatureCollection", "features": geo_features}
                return geo_features

            return geojson_from_graph(
                self.snapped_route_graph, must_include_props=["count", "avg", "edge_id"]
            )

        # TODO: Does this *need* to return edge_id (or any other props)?
        # edge_id not used in front end seemingly and other nullables can be
        # handled wherever... edge_id wasn't being returned for any data I
        # tried so this is a hack for now.
        return geojson_from_graph(
            # self.snapped_route_graph, must_include_props=["count", "avg", "edge_id"]
            self.snapped_route_graph,
            must_include_props=None,
        )


class BoundingGraphMixin:
    def get_bounding_graph(self, use_graph_cache: bool = True):
        logger.debug(
            "Plotting bounding graph (n,s,e,w) (%s, %s, %s, %s)",
            self.most_northern,
            self.most_southern,
            self.most_eastern,
            self.most_western,
        )

        if use_graph_cache is False or network_cache.get(self) is None:
            logger.debug("bbox > %s not found in cache, generating...", self.gps_hash)
            network = ox.graph_from_bbox(
                self.most_northern,
                self.most_southern,
                self.most_eastern,
                self.most_western,
                network_type=self.network_type,
                simplify=True,
            )
            network_cache.set(network, self.bbox)

        return network_cache.get(self)

    @property
    def bounding_graph(self):
        """
        Get a rectangular graph which contains the journey
        """
        return self.get_bounding_graph(use_graph_cache=True)

    @property
    def area(self) -> float:
        """
        Get the area of the bounding box in m^2
        """
        return area_from_coords(self.bbox)
