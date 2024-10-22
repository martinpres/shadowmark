import numpy as np
import pytest

from src.transformation.zigzag import scan, inverse

test_data = [
    (
        [
            [0, 1, 5, 6],
            [2, 4, 7, 12],
            [3, 8, 11, 13],
            [9, 10, 14, 15]
        ],
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    ),
    (
        [
            [0, 1, 5, 6],
            [2, 4, 7, 10],
            [3, 8, 9, 11]
        ],
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    ),
    (
        [
            [0, 1, 5],
            [2, 4, 6],
            [3, 7, 10],
            [8, 9, 11]
        ],
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    ),
    (
        [
            [0, 1, 4, 5],
            [2, 3, 6, 7]
        ],
        [0, 1, 2, 3, 4, 5, 6, 7]
    ),
    (
        [
            [0, 1],
            [2, 4],
            [3, 5],
            [6, 7]
        ],
        [0, 1, 2, 3, 4, 5, 6, 7]
    ),
    (
        [
            [0, 1, 2, 3]
        ],
        [0, 1, 2, 3]
    ),
    (
        [
            [0],
            [1],
            [2],
            [3]
        ],
        [0, 1, 2, 3]
    ),
    (
        [
            [0, 1],
            [2, 3]
        ],
        [0, 1, 2, 3]
    ),
    (
        [
            [0, 1]
        ],
        [0, 1]
    ),
    (
        [
            [0],
            [1]
        ],
        [0, 1]
    ),
    (
        [[0]],
        [0]
    ),
    (
        [[]],
        []
    )
]


class TestZigzag:

    @pytest.mark.parametrize('matrix, expected', test_data)
    def test_scan(self, matrix, expected):
        actual = scan(np.array(matrix))

        assert np.array_equal(actual, expected)

    @pytest.mark.parametrize('matrix, vector', test_data)
    def test_inverse(self, matrix, vector):
        expected = np.array(matrix)

        actual = inverse(vector, expected.shape)

        assert np.array_equal(actual, expected)

    @pytest.mark.parametrize('matrix, expected_vector', test_data)
    def test_compatibility(self, matrix, expected_vector):
        expected_matrix = np.array(matrix)

        actual_vector = scan(expected_matrix)
        actual_matrix = inverse(actual_vector, expected_matrix.shape)

        assert np.array_equal(actual_vector, expected_vector)
        assert np.array_equal(actual_matrix, expected_matrix)
