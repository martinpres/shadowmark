import pytest

from src.randomization.permutation_indices_selector import PermutationIndicesSelector


class TestPermutationIndicesSelector:

    @pytest.fixture
    def seed(self):
        return 1234567890

    def test_total_range_0(self, seed):
        selector = PermutationIndicesSelector(seed)
        assert selector.indices(0, 42) == []

    def test_selection_0(self, seed):
        selector = PermutationIndicesSelector(seed)
        assert selector.indices(42, 0) == []

    def test_selection_too_big(self, seed):
        selector = PermutationIndicesSelector(seed)
        assert len(selector.indices(42, 43)) == 42

    def test_permutation_length(self, seed):
        total_size = 10
        selector = PermutationIndicesSelector(seed)

        for selection_size in range(0, 11):
            assert len(selector.indices(total_size, selection_size)) == selection_size

    def test_consistency(self, seed):
        total_size = 10
        selection_size = 5

        selector1 = PermutationIndicesSelector(seed)
        selector2 = PermutationIndicesSelector(seed)

        assert selector1.indices(total_size, selection_size) == selector2.indices(total_size, selection_size)
