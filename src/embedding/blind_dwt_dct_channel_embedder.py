import numpy as np

from src.embedder import ChannelEmbedder
from src.exceptions import WatermarkSizeError, ImageChannelError
from src.indices import IndicesSelector
from src.transformation import correlation
from src.transformation import dct, zigzag, dwt
from src.transformation.bipolar import vector_to_bipolar_bits


class BlindDwtDctChannelEmbedder(ChannelEmbedder):
    """
    A class for embedding watermark data into a single channel of an input image.
    """

    def __init__(self, gain: float, selector: IndicesSelector):
        """
        Creates a new instance.

        :param gain: A float value specifying how strong the embedding would be.
        :param selector: An instance of IndicesSelector that is used to spread watermark data across the channel data.
        """
        if gain is None:
            raise TypeError('gain is required')

        if selector is None:
            raise TypeError('selector is required')

        self._gain = gain
        self._selector = selector

    def embed(self, channel: np.ndarray, watermark_values: list[int]) -> np.ndarray:
        """
        Embeds watermark data using the blind DWT-DCT approach.

        :param channel: A 2D numpy array representing image channel and containing pixel values in range 0 - 255.
        :param watermark_values: A list of watermark values in range 0 - 255 that will be embedded to the channel.
        :return: A 2D numpy array representing image channel with embedded watermark.
        """
        if channel is None or channel.size < 1:
            raise ImageChannelError('Empty input image channel provided for embedding')

        if watermark_values is None or len(watermark_values) < 1:
            raise ImageChannelError('Empty watermark provided for embedding')

        if len(watermark_values) > int(channel.size / 64):
            raise WatermarkSizeError(
                'The watermark is too large.'
                'Its total size should be at most 1/64 of the total size of the input image in pixels.'
            )

        ll, hl, lh, hh = dwt.first_level(channel)

        approximation_coefficients = zigzag.scan(ll)

        sub_vector_x1, sub_vector_x2 = correlation.decompose(approximation_coefficients)

        x1_dct = dct.transform(sub_vector_x1)
        x2_dct = dct.transform(sub_vector_x2)

        embedded_x1_dct = x1_dct.copy()
        embedded_x2_dct = x2_dct.copy()

        watermark_bits = vector_to_bipolar_bits(watermark_values)

        embedding_indices = self._selector.indices(int(len(approximation_coefficients) / 2), len(watermark_bits))

        for i, bit in enumerate(watermark_bits):
            j = embedding_indices[i]
            embedded_x1_dct[j] = ((x1_dct[j] + x2_dct[j]) / 2) + (self._gain * bit)
            embedded_x2_dct[j] = ((x1_dct[j] + x2_dct[j]) / 2) - (self._gain * bit)

        embedded_sub_vector_x1 = dct.inverse(embedded_x1_dct)
        embedded_sub_vector_x2 = dct.inverse(embedded_x2_dct)

        embedded_approximation_coefficients = correlation.compose(embedded_sub_vector_x1, embedded_sub_vector_x2)

        ll_embedded = zigzag.inverse(embedded_approximation_coefficients, ll.shape)

        channel_embedded = dwt.first_level_inverse(ll_embedded, hl, lh, hh)

        # Inverse dwt pads channel to be of even size, so we slice it to the original size
        height, width = channel.shape
        return channel_embedded[:height, :width]
