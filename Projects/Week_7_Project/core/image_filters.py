"""Neighborhood averaging and median filtering, from Lecture 1.

Unlike the masking method (which zero-pads out-of-bounds mask cells),
these two filters use only the pixels that actually exist within the
image for a target pixel's neighborhood -- so an edge or corner pixel
averages/medians over fewer pixels (e.g. 4 pixels at a corner), matching
the notes' worked description of that edge case.

Averaging: P(x,y) = round( (1/R) * sum of the neighborhood ), R = the
    actual number of in-bounds neighborhood pixels.
Median: sort the in-bounds neighborhood values; for an odd count the
    middle value is the median, for an even count (e.g. 4 pixels at a
    corner) average the two middle values -- exactly numpy's standard
    median convention.
"""

import numpy as np


def _neighborhood(image: np.ndarray, x: int, y: int):
    m, n = image.shape
    values = []
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            xi, yi = x + dx, y + dy
            if 0 <= xi < m and 0 <= yi < n:
                values.append(image[xi, yi])
    return values


def average_filter(image: np.ndarray) -> np.ndarray:
    m, n = image.shape
    result = np.zeros_like(image, dtype=float)
    for x in range(m):
        for y in range(n):
            values = _neighborhood(image, x, y)
            result[x, y] = round(sum(values) / len(values))
    return result


def median_filter(image: np.ndarray) -> np.ndarray:
    m, n = image.shape
    result = np.zeros_like(image, dtype=float)
    for x in range(m):
        for y in range(n):
            values = _neighborhood(image, x, y)
            result[x, y] = np.median(values)
    return result
