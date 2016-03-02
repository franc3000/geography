# geography

## Installation:
pip install -e git://github.com/franc3000/geography.git@v0.0.5#egg=geography

## Usage:

### As console command
```bash
neib 32.7858 -96.799 -d neighborhoods
```
```
Features: tx_dallas_48113.geojson, neighborhood: City Center District
```

### As a library
```python
>>> from geography import get_neighborhood, ensure_index
>>> ensure_index()  # Create index to speed up the search.
>>> print get_neighborhood(32.7858, -96.799)
('tx_dallas_48113.geojson', 'City Center District')
```
