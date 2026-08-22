import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import numpy as np
import pytest
from core.vision import apply_mask, SHARPEN_MASK


def test_sharpen_mask_sums_to_zero():
    # Notes: "a common mask... center value of +8, surrounded by eight -1 values", sum = 0.
    assert SHARPEN_MASK.sum() == 0


def test_uniform_image_interior_pixel_is_zero():
    # For a uniform-intensity image, an interior pixel (full 3x3
    # neighborhood in bounds) with a zero-sum mask must come out as 0.
    image = np.full((5, 5), 100.0)
    result = apply_mask(image, SHARPEN_MASK)
    assert result[2, 2] == pytest.approx(0.0)


def test_edge_case_only_counts_in_bounds_pixels():
    # Top-left corner pixel: only the 4 in-bounds cells of the mask
    # (center + 3 neighbors) contribute; out-of-bounds cells contribute 0.
    image = np.zeros((3, 3))
    image[0, 0] = 5.0
    mask = np.array([
        [1, 1, 1],
        [1, 1, 1],
        [1, 1, 1],
    ])
    result = apply_mask(image, mask)
    # Only image[0,0]'s own contribution matters here since it's the only nonzero pixel,
    # and the mask center covering it is always in bounds.
    assert result[0, 0] == pytest.approx(5.0)


def test_identity_like_mask_preserves_image():
    image = np.array([[1.0, 2.0], [3.0, 4.0]])
    identity_mask = np.array([
        [0, 0, 0],
        [0, 1, 0],
        [0, 0, 0],
    ])
    result = apply_mask(image, identity_mask)
    assert result == pytest.approx(image)
