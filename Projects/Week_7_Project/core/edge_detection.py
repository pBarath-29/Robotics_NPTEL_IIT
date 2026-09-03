"""Thresholding and edge detection, from Lecture 1.

Thresholding converts a pre-processed intensity image into a strict
binary silhouette: for a white object on a dark background, P(x,y) > T
becomes 1 (object), otherwise 0 (background).

Edge detection approximates derivatives with small 3x3 template masks
(mask cells outside the image boundary contribute 0, same convention as
the general masking method):
    Gx: sign change horizontally -- [[-1,0,1],[-1,0,1],[-1,0,1]]
    Gy: sign change vertically   -- [[-1,-1,-1],[0,0,0],[1,1,1]]
    Laplacian: negative center (-4), positive N/S/E/W neighbors (+1), 0 corners.
"""

import numpy as np

GX_MASK = np.array([
    [-1, 0, 1],
    [-1, 0, 1],
    [-1, 0, 1],
])

GY_MASK = np.array([
    [-1, -1, -1],
    [0, 0, 0],
    [1, 1, 1],
])

LAPLACIAN_MASK = np.array([
    [0, 1, 0],
    [1, -4, 1],
    [0, 1, 0],
])


def threshold(image: np.ndarray, t: float) -> np.ndarray:
    return (image > t).astype(int)


def apply_mask(image: np.ndarray, mask: np.ndarray) -> np.ndarray:
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
            result[x, y] = total
    return result


def gradient_magnitude(image: np.ndarray) -> np.ndarray:
    gx = apply_mask(image, GX_MASK)
    gy = apply_mask(image, GY_MASK)
    return np.sqrt(gx ** 2 + gy ** 2)
