from src.transformation.bipolar import vector_to_bipolar_bits, bipolar_bits_to_vector


class TestBipolar:

    def test_vector_to_bits_empty(self):
        assert vector_to_bipolar_bits([]) == []

    def test_bits_to_vector_empty(self):
        assert bipolar_bits_to_vector([]) == []

    def test_vector_to_bits(self):
        expected = [
            -1, -1, -1, -1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1, -1, 1, -1,
            -1, -1, -1, -1, -1, 1, -1, -1,
            -1, -1, -1, -1, 1, -1, -1, -1,
            1, 1, 1, 1, 1, 1, 1, 1
        ]
        assert vector_to_bipolar_bits([0, 2, 4, 8, 255]) == expected

    def test_bits_to_vector(self):
        bipolar_bits = [
            -1, -1, -1, -1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1, -1, 1, -1,
            -1, -1, -1, -1, -1, 1, -1, -1,
            -1, -1, -1, -1, 1, -1, -1, -1,
            1, 1, 1, 1, 1, 1, 1, 1
        ]
        assert bipolar_bits_to_vector(bipolar_bits) == [0, 2, 4, 8, 255]
