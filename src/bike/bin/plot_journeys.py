import argparse

from bike.utils import get_journeys


def main():
    '''
    Plot the map of journeys
    '''

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--condition',
        action='store_true',
        dest='condition',
        help='Show the condition of the roads, otherwise just plot the paths'
    )
    parser.add_argument(
        '--closest-edge',
        action='store_true',
        dest='closest_edge',
        help='Use the closest route to the coordinates plotted on the actual journey. If no, similar journeys are not likely to overlap'
    )
    parser.add_argument(
        '--place',
        dest='place',
        default='Dublin, Ireland',
        help='What place to limit the data to (so you don\'t try to visualize too big an area). Must be an osmnx recognised place / format for example "Dublin, Ireland"'
    )
    args = parser.parse_args()

    journeys = get_journeys(source='remote', place=args.place)

    journeys.plot_routes(
        use_closest_edge_from_base=args.closest_edge,
        apply_condition_colour=args.condition,
        plot_kwargs={
            'bgcolor': 'w',
            'edge_linewidth': 5,
            'show': True
        }
    )


if __name__ == '__main__':
    main()
