"""
This script is to numerically verify the proof we gave
in the Section titled **Misunderstanding** in the
main `README.md` file.

We shall
- choose a few norms (on R^2)
- compute the distance matrices
- compare the near-far relationships btw diff norms
"""

import numpy as np
from numpy.random import MT19937
from numpy.random import RandomState, SeedSequence
rs = RandomState(MT19937(SeedSequence(42)))



def dist_matrix(points, norm):
    n_points = points.shape[0]
    m = np.diag([np.inf]*n_points)
    for i in range(n_points):
        for j in range(i+1, n_points):
            m[i, j] = norm(points[i] - points[j])
    m += np.triu(m, k=1).T
    return m

def near_far_matrix(points, norm):
    m1 = dist_matrix(points, norm)
    print(norm)
    print(f"m1 =\n{m1}")
    #m2 = np.argmin(m1, axis=1)
    m2 = np.argsort(m1, axis=1)
    print(f"m2 =\n{m2}")
    return m2

if __name__ == "__main__":
    n_points = 10
    #xs = rs.randint(low=-n_points, high=n_points, size=(n_points,1), dtype=int)
    #ys = rs.randint(low=-n_points, high=n_points, size=(n_points,1), dtype=int)
    #points = np.hstack([xs, ys])
    points = rs.rand(n_points, 2)
    #points = rs.rand(n_points, 2) * 100
    np.set_printoptions(precision=2)
    #print(f"points =\n{points}")
    
    ##ps = range(1, 4)
    #ps = list(range(1, 4))
    ##norms = { p: (lambda x: np.linalg.norm(x, ord=p)) for p in ps }
    #norms = { p: lambda x: np.linalg.norm(x, ord=p) for p in ps }

    ps = [1,2,3]
    norms = { 1: lambda x: np.linalg.norm(x, ord=1),
              2: lambda x: np.linalg.norm(x, ord=2),
              3: lambda x: np.linalg.norm(x, ord=3),
            }

    # Debug
    a = np.array([3,4])
    b = np.array([-3,7])
    for p in ps:
        print(f"norms[{p}](a-b) = {norms[p](a-b)}")
    
    near_far_matrices = { p: near_far_matrix(points, norms[p]) for p in ps }
    
    from itertools import combinations
    for p1, p2 in combinations(ps, 2):
        print(f"np.array_equal(near_far_matrices[{p1}], near_far_matrices[{p2}]) = {np.array_equal(near_far_matrices[p1], near_far_matrices[p2])}")
        
        
