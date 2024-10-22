import numpy as np
from pywt import wavedec2, waverec2


def first_level(data: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Performs a single-level 2D discrete wavelet decomposition on the input data. This function uses the Haar wavelet
    to decompose the input 2D numpy array into its approximation (low-low) and detail coefficients (high-low,
    low-high, high-high).

    :param data: A 2D numpy array representing the input data to be decomposed.
    :return: A tuple containing:
    - ll: The approximation coefficients (low-low).
    - hl: The horizontal detail coefficients (high-low).
    - lh: The vertical detail coefficients (low-high).
    - hh: The diagonal detail coefficients (high-high).
    """
    ll, detail_coefficients = wavedec2(data, 'haar', level=1)
    hl, lh, hh = detail_coefficients
    return ll, hl, lh, hh,


def first_level_inverse(ll: np.ndarray, hl: np.ndarray, lh: np.ndarray, hh: np.ndarray):
    """
    Reconstruct a 2D data from its first-level wavelet coefficients using the Haar wavelet. The function takes the
    approximation (LL), high-low (HL), low-high (LH), and high-high (HH) coefficients of a wavelet transform and
    reconstructs the original data by applying the inverse wavelet transform.

    :param ll: Approximation coefficients (LL) of the wavelet transform.
    :param hl: High-low coefficients (HL) of the wavelet transform.
    :param lh: Low-high coefficients (LH) of the wavelet transform.
    :param hh: High-high coefficients (HH) of the wavelet transform.
    :return: The reconstructed data as a 2D NumPy array.
    """
    return waverec2((ll, (hl, lh, hh)), 'haar')
