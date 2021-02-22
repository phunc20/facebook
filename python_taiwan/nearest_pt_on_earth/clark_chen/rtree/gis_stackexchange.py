"""
Author: Mike T
https://gis.stackexchange.com/questions/22082/how-can-i-use-r-tree-to-find-points-within-a-distance-in-spatialite
"""

from random import randrange
from rtree import index
from math import sqrt

# Create a 3D index
p = index.Property()
p.dimension = 3
idx3d = index.Index(properties=p)

# Make and index random data
coords = []
for id_ in range(13000):
    coord = (randrange( 100000,  500000),
             randrange(1000000, 5000000),
             randrange(      0,    5000))
    coords.append(coord)
    idx3d.add(id_, coord)

# Find closest pair for the first 10 points
for id1 in range(10):
    nearest = list(idx3d.nearest(coords[id1], 2))
    assert id1 == nearest[0]
    id2 = nearest[1]
    c1 = coords[id1]
    c2 = coords[id2]
    # Pythagorean theorem
    dist = sqrt(sum([(a - b)**2 for a, b in zip(c1, c2)]))
    print('%i <-> %i : %.1f' % (id1, id2, dist))
