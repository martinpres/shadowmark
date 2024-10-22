import numpy as np

from src.transformation.dwt import first_level, first_level_inverse


class TestDwt:

    def test_consistency(self):
        expected = np.array([[0, 1, 2, 4], [8, 16, 32, 64]])
        actual = first_level_inverse(*first_level(expected))

        # Uses uint8 due to floating-point rounding errors
        assert np.array_equal(actual.astype(np.uint8), expected)