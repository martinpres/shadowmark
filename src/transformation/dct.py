import numpy as np
from scipy.fft import dct, idct


def transform(vector: np.ndarray) -> np.ndarray:
    """
    Applies the Discrete Cosine Transform (DCT) with the 'ortho' normalization to the input vector.

    :param vector: A 1D numpy array to be transformed using the DCT.
    :return: A 1D numpy array containing the DCT coefficients of the input array.
    """
    return dct(vector, norm='ortho')


def inverse(coefficients: np.ndarray) -> np.ndarray:
    """
    Applies the Inverse Discrete Cosine Transform (IDCT) with the 'ortho' normalization to the input vector.

    :param coefficients: A 1D numpy array containing DCT coefficients to be transformed back.
    :return: A 1D numpy array containing the reconstructed vector from the DCT coefficients.
    """
    return idct(coefficients, norm='ortho')
