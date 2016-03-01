# -*- coding: utf-8 -*-

import argparse
from six import binary_type
from .__meta__ import __version__


def make_arg_parser():

    parser = argparse.ArgumentParser(
        prog='neib',
        description='Neighborhood search v{}'.format(__version__))

    parser.add_argument('lat', type=float, nargs='?', help='Latitude')
    parser.add_argument('lng', type=float, nargs='?', help='Longitude')
    parser.add_argument('-d', '--directory', nargs=1, type=binary_type, help='Data directory.')
    parser.add_argument('-v', '--version', action='store_true', help='Print version.')

    return parser


def main(args=None):

    if not args:
        parser = make_arg_parser()
        args = parser.parse_args()

    if args.version:
        print('Version: {}'.format(__version__))

    if args.lat and args.lng:
        from .core import get_neighborhood
        features, neighborhood = get_neighborhood(
            float(args.lat), float(args.lng), data_dir=args.directory)
        print('Features: {}, neighborhood: {}'.format(features, neighborhood))


if __name__ == '__main__':
    main()
