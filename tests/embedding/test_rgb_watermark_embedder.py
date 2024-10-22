import numpy as np
import pytest

from src.embedding.rgb_watermark_embedder import RGBWatermarkEmbedder
from tests.stub.channel_embedder_stub import ChannelEmbedderStub

_default_shape = (4, 4)


def _zeros(shape=_default_shape):
    return np.zeros(shape, dtype=np.uint8)


def _ones(shape=_default_shape):
    return np.ones(shape, dtype=np.uint8)


class TestRGBWatermarkEmbedder:

    @pytest.fixture
    def channel_embedder(self):
        """
        :return: ChannelEmbedder instance that adds watermark bytes to the values of the input image channel.
        """
        def _stubbed_embedding(channel, watermark_bytes):
            return np.add(channel, np.array(watermark_bytes).reshape(channel.shape))

        return ChannelEmbedderStub(_stubbed_embedding)

    @pytest.mark.parametrize('channel_spec, expected', [
        ('', (_zeros(), _zeros(), _zeros())),
        ('r', (_ones(), _zeros(), _zeros())),
        ('g', (_zeros(), _ones(), _zeros())),
        ('b', (_zeros(), _zeros(), _ones())),
        ('rg', (_ones(), _ones(), _zeros())),
        ('rb', (_ones(), _zeros(), _ones())),
        ('gb', (_zeros(), _ones(), _ones())),
        ('rgb', (_ones(), _ones(), _ones())),
        ('xyz', (_zeros(), _zeros(), _zeros()))
    ])
    def test_embedding(self, channel_embedder, channel_spec, expected):
        input_channels = (_zeros(), _zeros(), _zeros())
        watermark_channels = (_ones(), _ones(), _ones())

        rgb_embedder = RGBWatermarkEmbedder(channel_embedder, channel_spec)
        actual = rgb_embedder.embed(input_channels, watermark_channels)

        assert np.array_equal(actual[0], expected[0])
        assert np.array_equal(actual[1], expected[1])
        assert np.array_equal(actual[2], expected[2])
