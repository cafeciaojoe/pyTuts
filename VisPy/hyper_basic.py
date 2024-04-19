import numpy as np

def _generate_random_line_positions(num_points, dtype=np.float32):
    rng = np.random.default_rng()
    pos = np.empty((num_points, 3), dtype=np.float32)
    pos[:, 0] = np.arange(num_points)
    pos[:, 1] = rng.random((num_points,), dtype=dtype)
    pos[:, 2] = rng.random((num_points,), dtype=dtype)

    print(pos[-1,0])
    return print(pos)

_generate_random_line_positions(10, dtype=np.float32)