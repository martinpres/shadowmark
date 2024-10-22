from collections.abc import Callable

from src.extractor import ChannelExtractor


class ChannelExtractorStub(ChannelExtractor):

    def __init__(self, extraction_function: Callable[[any, int], any]):
        self._function = extraction_function

    def extract(self, channel, watermark_size):
        return self._function(channel, watermark_size)