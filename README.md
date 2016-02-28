# geography

## Installation:
pip install -e git://github.com/franc3000/geography.git@v0.0.2#egg=geography

## Usage:

### As console command
```bash
neib -97.8904 30.207777
```
```
Features: austin_neighbourhoods, neighborhood: 78739
```

### As a library
```python
>>> from geography import get_neighborhood
>>> print get_neighborhood(-97.8904, 30.207777)
('austin_neighbourhoods', 78739)
```
