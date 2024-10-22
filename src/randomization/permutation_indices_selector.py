from typing import Optional

import numpy as np

from src.indices import IndicesSelector


class PermutationIndicesSelector(IndicesSelector):
    """
    A class for selecting a permutation of indices from a specified range.
    """

    def __init__(self, seed: Optional[int]):
        """
        Creates a new instance.

        :param seed: A seed for the random number generator.
        """
        self._rng = np.random.default_rng(seed)

    def indices(self, total_range_size: int, selection_size: int) -> list[int]:
        """
        Randomly selects a list of permuted indices based on the specified range and selection size.

        :param total_range_size: The total size of the range from which to select indices.
        :param selection_size: The number of indices to select. If larger than the total_range_size, the effective
        selection will be adjusted to total_range_size.
        :return: A list of permuted indices selected from the specified range.
        """
        if total_range_size == 0 or selection_size == 0:
            return []

        effective_selection = selection_size
        if selection_size > total_range_size:
            effective_selection = total_range_size

        lower_bound_limit = total_range_size - effective_selection

        lower_bound = self._rng.integers(0, lower_bound_limit, endpoint=True)
        upper_bound = self._rng.integers(lower_bound + effective_selection, total_range_size, endpoint=True)

        permuted_indices = [i.item() for i in self._rng.permutation(list(range(lower_bound, upper_bound)))]
        return permuted_indices[0:effective_selection]
