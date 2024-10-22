from typing import TypeAlias

import numpy as np

from src.embedder import ChannelEmbedder

RGBChannels: TypeAlias = tuple[np.ndarray, np.ndarray, np.ndarray]


class RGBWatermarkEmbedder:
    """
    A class for embedding RGB channels of a watermark image into RGB channels of the input image.
    """

    def __init__(self, embedder: ChannelEmbedder, channels: str = 'rgb'):
        """
        Creates a new instance.

        :param embedder: A channel embedder that can embed a watermark into an image channel.
        :param channels: A string specifying which image channels should be used for watermark embedding.
        Allowed values are:
        - Character 'r' specifies the red image channel.
        - Character 'g' specifies the green image channel.
        - Character 'b' specifies the blue image channel.
        """
        if embedder is None:
            raise TypeError('embedder is required')

        self._embedder = embedder
        self._channels = channels

    def embed(self, input_channels: RGBChannels, watermark_channels: RGBChannels) -> RGBChannels:
        """
        Embeds a watermark into RGB channels of the input image.

        :param input_channels: A tuple of RGB channels of the input image.
        :param watermark_channels: A tuple of RGB channels if a watermark image.
        :return: Tuple of RGB channels of the input image containing embedded watermark data.
        """
        r, g, b = input_channels
        wr, wg, wb = watermark_channels

        if 'r' in self._channels:
            r = self._embed(r, wr)
        if 'g' in self._channels:
            g = self._embed(g, wg)
        if 'b' in self._channels:
            b = self._embed(b, wb)

        return r, g, b

    def _embed(self, image_channel: np.ndarray, watermark_channel: np.ndarray) -> np.ndarray:
        watermark_bytes = [byte for row in watermark_channel for byte in row]
        return self._embedder.embed(image_channel, watermark_bytes)
