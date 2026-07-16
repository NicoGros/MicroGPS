import numpy as np


def compute_affine_matrix(src_pts, dst_pts):
    """
    Compute a 3×3 homogeneous affine transformation matrix.

    Parameters
    ----------
    src_pts : list[(x, y)]
        Image coordinates.

    dst_pts : list[(u, v)]
        Coordinates in the destination system.
    """

    A = []
    B = []

    for (x, y), (u, v) in zip(src_pts, dst_pts):

        A.append([x, y, 1, 0, 0, 0])
        A.append([0, 0, 0, x, y, 1])

        B.append(u)
        B.append(v)

    A = np.asarray(A, dtype=float)
    B = np.asarray(B, dtype=float)

    params = np.linalg.solve(A, B)

    return np.array(
        [
            [params[0], params[1], params[2]],
            [params[3], params[4], params[5]],
            [0.0,       0.0,       1.0],
        ],
        dtype=float,
    )