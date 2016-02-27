import json
import os

from shapely.geometry import shape, Point


def get_neighborhood(lat, lng, data_dir=None):
    """ Returns features name and neighborhood for give point.

    Args:
        lat (float):
        lng (float):
        data_dir (str, optional): directory with *.geojson files.

    Returns:
        (str, float)

    """

    # load GeoJSON file containing sectors
    if not data_dir:
        this_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.normpath(os.path.join(this_dir, 'data'))

    for (dirpath, dirnames, filenames) in os.walk(data_dir):
        for filename in filenames:
            if not filename.endswith('.geojson'):
                continue

            # Get the name relative to data dir.
            identity = os.path.join(dirpath.replace(data_dir, ''), filename)
            # TODO: Use logging instead.
            print('Seeking through {} ...'.format(identity))
            with open(os.path.join(dirpath, filename), 'r') as f:
                js = json.load(f)

            # construct point based on lat/long
            point = Point(lat, lng)

            # check each polygon to see if it contains the point
            for feature in js['features']:
                polygon = shape(feature['geometry'])
                if polygon.contains(point):
                    return (os.path.splitext(filename)[0], feature['properties']['neighbourhood'])
    return (None, None)
