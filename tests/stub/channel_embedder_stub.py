from typing import Callable

from src.embedder import ChannelEmbedder


class ChannelEmbedderStub(ChannelEmbedder):

    def __init__(self, function: Callable[[any, list[int]], any]):
        self._function = function

    def embed(self, channel, watermark_bits):
        return self._function(channel, watermark_bits)
