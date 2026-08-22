"""Image pre-processing via masking, from Lecture 5.

A 3x3 mask of coefficients (W1..W9) is centered on each pixel; each
coefficient is multiplied by the raw intensity of the image pixel beneath
it, and the 9 products are summed to give the new, pre-processed pixel
value P(x, y). Mask coefficients that fall outside the image boundary
(at edges/corners) contribute 0.
"""

import numpy as np


def apply_mask(image: np.ndarray, mask: np.ndarray) -> np.ndarray:
    """image: MxN array of pixel intensities. mask: 3x3 array of coefficients."""
    m, n = image.shape
    result = np.zeros_like(image, dtype=float)
    for x in range(m):
        for y in range(n):
            total = 0.0
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    xi, yi = x + dx, y + dy
                    if 0 <= xi < m and 0 <= yi < n:
                        total += mask[dx + 1, dy + 1] * image[xi, yi]
                    # else: outside the boundary, contributes 0
            result[x, y] = total
    return result


SHARPEN_MASK = np.array([
    [-1, -1, -1],
    [-1, 8, -1],
    [-1, -1, -1],
])
