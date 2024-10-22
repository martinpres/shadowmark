import numpy as np

from src.transformation.dct import inverse, transform


class TestDct:

    def test_consistency(self):
        expected = np.array([0, 1, 2, 4, 8, 16, 32, 64, 128])
        actual = inverse(transform(expected))

        # Uses uint8 due to floating-point rounding errors
        assert np.array_equal(actual.astype(np.uint8), expected)