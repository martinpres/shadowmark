import numpy as np
import pytest

from src.embedding.blind_dwt_dct_channel_embedder import BlindDwtDctChannelEmbedder
from src.exceptions import ImageChannelError, WatermarkSizeError
from tests.stub.indices_selector_stub import IndicesSelectorStub


class TestBlindDwtDctChannelEmbedder:

    @pytest.fixture
    def selector(self):
        """
        :return: Indices selector that always returns the same indices in interval (0, selection).
        """
        return IndicesSelectorStub(lambda _, selection: list(range(0, selection)))

    @pytest.mark.parametrize('channel', [np.array([[], []]), np.empty((0,)), None])
    def test_embed_empty_channel(self, selector, channel):
        channel_embedder = BlindDwtDctChannelEmbedder(1.0, selector)

        with pytest.raises(ImageChannelError) as _:
            channel_embedder.embed(channel, [])

    @pytest.mark.parametrize('watermark_bits', [[], None])
    def test_embed_empty_watermark(self, selector, watermark_bits):
        channel_embedder = BlindDwtDctChannelEmbedder(1.0, selector)

        with pytest.raises(ImageChannelError) as _:
            channel_embedder.embed(np.array([[0, 255], [255, 0]]), watermark_bits)

    def test_embed_selector_raises_error(self, selector):
        watermark = [0, 255]
        channel = np.array([
            [0, 64, 128, 255],
            [0, 64, 128, 255],
        ])

        channel_embedder = BlindDwtDctChannelEmbedder(1.0, selector)

        with pytest.raises(WatermarkSizeError) as _:
            channel_embedder.embed(channel, watermark)

    @pytest.mark.parametrize('channel, expected', [
        # Rectangular channel, even shape
        (
                np.full((4, 18), 128, dtype=np.uint8),
                np.array([
                    [126, 126, 129, 129, 128, 128, 127, 127, 128, 128, 127, 127, 128, 128, 127, 127, 128, 128],
                    [126, 126, 129, 129, 128, 128, 127, 127, 128, 128, 127, 127, 128, 128, 127, 127, 128, 128],
                    [128, 128, 127, 127, 128, 128, 127, 127, 128, 128, 127, 127, 128, 128, 127, 127, 127, 127],
                    [128, 128, 127, 127, 128, 128, 127, 127, 128, 128, 127, 127, 128, 128, 127, 127, 127, 127]
                ])
        ),

        # Square channel, even shape
        (
                np.full((8, 8), 128, dtype=np.uint8),
                np.array([
                    [127, 127, 128, 128, 127, 127, 128, 128, ],
                    [127, 127, 128, 128, 127, 127, 128, 128, ],
                    [128, 128, 128, 128, 127, 127, 128, 128, ],
                    [128, 128, 128, 128, 127, 127, 128, 128, ],
                    [127, 127, 128, 128, 127, 127, 127, 127, ],
                    [127, 127, 128, 128, 127, 127, 127, 127, ],
                    [127, 127, 128, 128, 128, 128, 127, 127, ],
                    [127, 127, 128, 128, 128, 128, 127, 127, ]
                ])
        ),

        # Channel of odd shape
        (
                np.full((1, 64), 128, dtype=np.uint8),
                np.array([
                    [127, 127, 128, 128, 127, 127, 128, 128, 128, 128, 127, 127, 128, 128, 127, 127, 128, 128,
                     127, 127, 128, 128, 127, 127, 128, 128, 127, 127, 128, 128, 127, 127, 128, 128, 127, 127,
                     128, 128, 127, 127, 128, 128, 127, 127, 128, 128, 127, 127, 128, 128, 127, 127, 128, 128,
                     127, 127, 128, 128, 127, 127, 128, 128, 127, 127, ]
                ])
        )
    ])
    def test_embedding(self, selector, channel, expected):
        watermark = [128]

        actual = BlindDwtDctChannelEmbedder(1.0, selector).embed(channel, watermark)

        # Uses uint8 due to floating-point rounding errors
        assert np.array_equal(actual.astype(np.uint8), expected)
