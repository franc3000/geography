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
    for geo_file in os.listdir(data_dir):
        if not geo_file.endswith('.geojson'):
            continue

        with open(geo_file, 'r') as f:
            js = json.load(f)

        # construct point based on lat/long returned by geocoder
        point = Point(lat, lng)

        # check each polygon to see if it contains the point
        for feature in js['features']:
            polygon = shape(feature['geometry'])
            if polygon.contains(point):
                return (os.path.splitext(geo_file)[0], feature['properties']['neighbourhood'])
    return (None, None)
