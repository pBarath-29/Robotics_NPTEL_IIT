import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import numpy as np
import pytest
from core.edge_detection import threshold, apply_mask, gradient_magnitude, LAPLACIAN_MASK, GX_MASK


def test_threshold_binarizes_correctly():
    image = np.array([[10, 200], [50, 100]])
    result = threshold(image, t=75)
    assert result.tolist() == [[0, 1], [0, 1]]


def test_laplacian_mask_sums_to_zero():
    assert LAPLACIAN_MASK.sum() == 0


def test_uniform_image_gives_zero_laplacian_response():
    image = np.full((5, 5), 100.0)
    result = apply_mask(image, LAPLACIAN_MASK)
    assert result[2, 2] == pytest.approx(0.0)


def test_gradient_detects_a_vertical_edge():
    # Left half dark, right half bright -> a strong response from Gx at the boundary column.
    image = np.zeros((5, 5))
    image[:, 3:] = 100.0
    mag = gradient_magnitude(image)
    assert mag[2, 2] > mag[2, 0]


def test_gx_mask_zero_on_flat_region():
    image = np.full((5, 5), 30.0)
    result = apply_mask(image, GX_MASK)
    assert result[2, 2] == pytest.approx(0.0)
