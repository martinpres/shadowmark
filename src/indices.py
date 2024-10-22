from abc import ABC, abstractmethod


class IndicesSelector(ABC):

    @abstractmethod
    def indices(self, total_range_size: int, selection_size: int):
        """
        Selects selection_size indices from 0 to total_range_size based on implementation.
        """
        pass
