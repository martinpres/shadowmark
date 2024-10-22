from typing import TypeAlias

import numpy as np

from src.extractor import ChannelExtractor

RGBChannels: TypeAlias = tuple[np.ndarray, np.ndarray, np.ndarray]


class RGBWatermarkExtractor:
    """
    A class for extracting RGB channels of a watermark image from RGB channels of the input image.
    """

    def __init__(self, extractor: ChannelExtractor, channels: str = 'rgb'):
        """
        Creates a new instance.

        :param extractor: A channel extractor that can extract watermark from an image channel.
        :param channels: A string specifying which image channels should be used for watermark extraction.
        Allowed values are:
        - Character 'r' specifies the red image channel.
        - Character 'g' specifies the green image channel.
        - Character 'b' specifies the blue image channel.
        """
        if extractor is None:
            raise TypeError('ChannelExtractor instance is required')

        self._extractor = extractor
        self._channels = channels

    def extract(self, input_channels: RGBChannels, watermark_shape: tuple[int, int]) -> RGBChannels:
        """
        Extracts a watermark of a given shape from RGB channels of the input image.

        :param input_channels: A tuple of RGB image channels.
        :param watermark_shape: The expected shape of the watermark.
        :return: Tuple of RGB channels of the extracted watermark image.
        """
        r, g, b = input_channels

        wr = self._extract(r, watermark_shape) if 'r' in self._channels else np.zeros(watermark_shape)
        wg = self._extract(g, watermark_shape) if 'g' in self._channels else np.zeros(watermark_shape)
        wb = self._extract(b, watermark_shape) if 'b' in self._channels else np.zeros(watermark_shape)

        return wr, wg, wb

    def _extract(self, image_channel: np.ndarray, watermark_shape: tuple[int, int]) -> np.ndarray:
        watermark_height, watermark_width = watermark_shape
        watermark_bytes = self._extractor.extract(image_channel, watermark_width * watermark_height)

        return np.array(watermark_bytes, dtype=np.uint8).reshape(watermark_shape)
