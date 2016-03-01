import json
import logging
import os

from rtree import index
from shapely.geometry import shape, Point

logger = logging.getLogger(__name__)

# all indexed directories. Key is directory, value is index.Index()
indexes = {}

this_dir = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DATA_DIR = os.path.normpath(os.path.join(this_dir, 'data'))


def ensure_index(data_dir=None):
    """ Creates rtree index for all *.geojson files found in given directory. """
    if not data_dir:
        data_dir = DEFAULT_DATA_DIR

    if data_dir not in indexes:
        # Populate index
        idx = index.Index()
        i = 0
        for identity, features in _generate_features(data_dir):

            for feature in features:
                polygon = shape(feature['geometry'])
                if 'neighbourhood' not in feature.get('properties', {}):
                    logger.warning('No neighborhood for {}. Do not include to index.'.format(identity))
                    continue
                minx, miny, maxx, maxy = polygon.bounds
                idx.insert(i, (minx, miny, maxx, maxy),
                           obj=(identity, polygon, feature['properties']['neighbourhood']))
                i += 1

        # update cache.
        indexes[data_dir] = idx


def get_neighborhood(lat, lng, data_dir=None):
    """ Returns features file short name and neighborhood for given point.

    Args:
        lat (float):
        lng (float):
        data_dir (str, optional): directory with *.geojson files.

    Returns:
        (str, float)

    """
    if not data_dir:
        data_dir = DEFAULT_DATA_DIR

    point = Point(lat, lng)

    idx = indexes.get(data_dir)

    if idx:
        for identity, polygon, neighborhood in [n.object for n in idx.intersection(point.bounds, objects=True)]:
            if polygon.contains(point):
                return identity, neighborhood
    else:
        print('{} directory is not indexed. Using slow iteration method...'.format(data_dir))
        for identity, features in _generate_features(data_dir):
            for feature in features:
                if 'neighbourhood' not in feature.get('properties', {}):
                    logger.warning('No neighborhood for {}. Do not include to index.'.format(identity))
                    continue
                polygon = shape(feature['geometry'])
                if polygon.contains(point):
                    return identity, feature['properties']['neighbourhood']
    return (None, None)


def _generate_features(data_dir):
    """ Generates (identity, features) tuples found in data_dir.

    Args:
        data_dir (str):

    Yields:
        (str, dict):
    """

    for (dirpath, dirnames, filenames) in os.walk(data_dir):
        for filename in filenames:
            if not filename.endswith('.geojson'):
                continue

            # Get the name relative to data dir.
            identity = os.path.join(dirpath.replace(data_dir, ''), filename)
            with open(os.path.join(dirpath, filename), 'r') as f:
                features = json.load(f)
                yield identity, features['features']
