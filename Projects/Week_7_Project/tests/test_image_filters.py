import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import numpy as np
import pytest
from core.image_filters import average_filter, median_filter


def test_uniform_image_average_is_unchanged():
    image = np.full((5, 5), 42.0)
    result = average_filter(image)
    assert np.all(result == 42.0)


def test_uniform_image_median_is_unchanged():
    image = np.full((5, 5), 42.0)
    result = median_filter(image)
    assert np.all(result == 42.0)


def test_corner_pixel_uses_four_neighbors():
    # A corner pixel's 3x3 neighborhood only has 4 in-bounds pixels
    # (itself + 3 neighbors), matching the notes' worked edge case.
    image = np.array([
        [10.0, 20.0, 0.0],
        [30.0, 40.0, 0.0],
        [0.0, 0.0, 0.0],
    ])
    avg = average_filter(image)
    expected_corner_avg = round((10 + 20 + 30 + 40) / 4)
    assert avg[0, 0] == pytest.approx(expected_corner_avg)


def test_median_filter_removes_salt_and_pepper_spike():
    image = np.full((5, 5), 50.0)
    image[2, 2] = 255.0  # a single "salt" noise spike
    result = median_filter(image)
    assert result[2, 2] == pytest.approx(50.0)
