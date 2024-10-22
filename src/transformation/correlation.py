from itertools import zip_longest

import numpy as np


def decompose(vector: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """
    Decomposes a 1D numpy array into two separate arrays containing the even-indexed and odd-indexed elements.

    :param vector: A 1D numpy array to be decomposed.
    :return: Tuple of two numpy arrays. The first array contains elements from the even indices and the second array
    contains elements from the odd indices of the input array.
    """
    return vector[0::2], vector[1::2]


def compose(even_items: np.ndarray, odd_items: np.ndarray) -> list:
    """
    Combines two numpy arrays of even-indexed and odd-indexed items into a single list, maintaining the original order.

    The function interleaves elements from both arrays, filling in gaps from the shorter array with `None`, which are
    then excluded from the final output.

    :param even_items: A numpy array containing the even-indexed items.
    :param odd_items: A numpy array containing the odd-indexed items.
    :return: A list of integers formed by interleaving the elements of `even_items` and `odd_items`.
    """
    return [
        item
        for zipped in zip_longest(even_items, odd_items)
        for item in zipped
        if item is not None
    ]
