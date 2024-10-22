import numpy as np

from src.transformation.correlation import decompose, compose


class TestCorrelation:

    def test_decompose_empty(self):
        empty = np.array([])
        actual = decompose(empty)

        for a in actual:
            assert np.array_equal(a, empty)

    def test_compose_empty(self):
        empty = np.array([])
        assert compose(empty, empty) == []

    def test_decompose_odd_length(self):
        actual1, actual2 = decompose(np.array([0, 1, 2, 3, 4]))

        assert np.array_equal(actual1, [0, 2, 4])
        assert np.array_equal(actual2, [1, 3])

    def test_compose_odd_length(self):
        expected = [0, 1, 2, 3, 4]
        actual = compose(np.array([0, 2, 4]), np.array([1, 3]))

        assert actual == expected

    def test_decompose_even_length(self):
        actual1, actual2 = decompose(np.array([0, 1, 2, 3]))

        assert np.array_equal(actual1, [0, 2])
        assert np.array_equal(actual2, [1, 3])

    def test_compose_even_length(self):
        expected = [0, 1, 2, 3]
        actual = compose(np.array([0, 2]), np.array([1, 3]))

        assert actual == expected
