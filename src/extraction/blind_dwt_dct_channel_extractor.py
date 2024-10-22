import numpy as np

from src.exceptions import WatermarkSizeError, ImageChannelError
from src.extractor import ChannelExtractor
from src.indices import IndicesSelector
from src.transformation import dct, zigzag, dwt
from src.transformation.bipolar import bipolar_bits_to_vector
from src.transformation.correlation import decompose


class BlindDwtDctChannelExtractor(ChannelExtractor):
    """
    A class for extracting watermark data from a single channel of an input image.
    """

    def __init__(self, selector: IndicesSelector):
        """
        Creates a new instance.

        :param selector: An instance of IndicesSelector for collecting spread watermark data from the channel data.
        """
        if selector is None:
            raise TypeError('selector is required')

        self._selector = selector

    def extract(self, channel: np.ndarray, watermark_size: int) -> list[int]:
        """
        Extracts watermark data using the blind DWT-DCT approach.

        :param channel: A 2D numpy array representing image channel and containing pixel values in range 0 - 255.
        :param watermark_size: An expected size of the extracted watermark.
        :return: A list of watermark data values in range 0 - 255.
        """
        if channel is None or channel.size < 1:
            raise ImageChannelError('Empty image channel provided for extraction')

        if watermark_size > int(channel.size / 64):
            raise WatermarkSizeError(
                'The specified size of the watermark is too large. '
                'Its total size should be at most 1/64 of the total size of the input image in pixels.'
            )

        if watermark_size < 1:
            return []

        ll, _, _, _ = dwt.first_level(channel)

        approximation_coefficients = zigzag.scan(ll)

        sub_vector_x1, sub_vector_x2 = decompose(approximation_coefficients)

        x1_dct = dct.transform(sub_vector_x1)
        x2_dct = dct.transform(sub_vector_x2)

        watermark_size_in_bits = watermark_size * 8
        locations = self._selector.indices(int(len(approximation_coefficients) / 2), watermark_size_in_bits)

        watermark_bipolar_bits = []
        for i in range(0, watermark_size_in_bits):
            j = locations[i]
            delta_x = (x1_dct[j] - x2_dct[j])
            watermark_bipolar_bits.append(1 if delta_x >= 0 else -1)

        return bipolar_bits_to_vector(watermark_bipolar_bits)
