import numpy as np
import pytest

from src.extraction.rgb_watermark_extractor import RGBWatermarkExtractor
from tests.stub.channel_extractor_stub import ChannelExtractorStub

_default_shape = (1, 2)

def _zeros(shape=_default_shape):
    return np.zeros(shape, dtype=np.uint8)

def _255s(shape=_default_shape):
    return np.full(shape, 255, dtype=np.uint8)


class TestRGBWatermarkExtractor:

    @pytest.fixture
    def channel_extractor(self):
        """
        :return: ChannelExtractor instance that returns list of specified watermark_size where all values are 255.
        """

        def _stubbed_extraction(_, watermark_size):
            return [255 for _ in range(0, watermark_size)]

        return ChannelExtractorStub(_stubbed_extraction)

    @pytest.mark.parametrize('channel_spec, expected', [
        ('', (_zeros(), _zeros(), _zeros())),
        ('r', (_255s(), _zeros(), _zeros())),
        ('g', (_zeros(), _255s(), _zeros())),
        ('b', (_zeros(), _zeros(), _255s())),
        ('rg', (_255s(), _255s(), _zeros())),
        ('rb', (_255s(), _zeros(), _255s())),
        ('gb', (_zeros(), _255s(), _255s())),
        ('rgb', (_255s(), _255s(), _255s())),
        ('xyz', (_zeros(), _zeros(), _zeros()))
    ])
    def test_extraction(self, channel_extractor, channel_spec, expected):
        input_shape = (4,4)
        input_channels = (
            np.ones(input_shape, dtype=np.uint8),
            np.ones(input_shape, dtype=np.uint8),
            np.ones(input_shape, dtype=np.uint8)
        )

        rgb_extractor = RGBWatermarkExtractor(channel_extractor, channel_spec)
        actual = rgb_extractor.extract(input_channels, _default_shape)

        assert np.array_equal(actual[0], expected[0])
        assert np.array_equal(actual[1], expected[1])
        assert np.array_equal(actual[2], expected[2])