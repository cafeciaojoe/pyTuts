import numpy as np

def _generate_random_line_positions(dtype=np.float32):
    rng = np.random.default_rng()
    pos = np.empty((1, 3), dtype=np.float32)
    pos[:, 0] = rng.random(dtype=dtype)
    pos[:, 1] = rng.random(dtype=dtype)
    pos[:, 2] = rng.random(dtype=dtype)
    return print(pos)

while True:
    _generate_random_line_positions(dtype=np.float32)

    "rng.random(dtype=dtype)"