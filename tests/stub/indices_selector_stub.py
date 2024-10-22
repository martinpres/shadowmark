from typing import Callable

from src.indices import IndicesSelector


class IndicesSelectorStub(IndicesSelector):

    def __init__(self, function: Callable[[int, int], list[int]]):
        self._function = function

    def indices(self, n: int, l: int):
        return self._function(n, l)
