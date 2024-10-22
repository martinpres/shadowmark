import numpy as np
import pytest

from src.exceptions import ImageChannelError, WatermarkSizeError
from src.extraction.blind_dwt_dct_channel_extractor import BlindDwtDctChannelExtractor
from tests.stub.indices_selector_stub import IndicesSelectorStub


class TestBlindDwtDctChannelExtractor:
    @pytest.fixture
    def selector(self):
        """
        :return: Indices selector that always returns the same indices in interval (0, selection).
        """
        return IndicesSelectorStub(lambda _, selection: list(range(0, selection)))

    @pytest.mark.parametrize('channel', [np.array([[], []]), np.empty((0,)), None])
    def test_extract_empty_channel(self, selector, channel):
        channel_extractor = BlindDwtDctChannelExtractor(selector)

        with pytest.raises(ImageChannelError) as _:
            channel_extractor.extract(channel, 0)

    def test_extract_selector_raises_error(self, selector):
        channel = np.array([
            [0, 64, 128, 255],
            [0, 64, 128, 255],
        ])

        channel_extractor = BlindDwtDctChannelExtractor(selector)

        with pytest.raises(WatermarkSizeError) as _:
            channel_extractor.extract(channel, 4)

    def test_extract_zero_watermark_size(self, selector):
        actual = BlindDwtDctChannelExtractor(selector).extract(np.array([[0, 255], [255, 0]]), 0)

        assert actual == []

    def test_extract(self, selector):
        channel = np.array([
            [127, 127, 128, 128, 127, 127, 128, 128],
            [127, 127, 128, 128, 127, 127, 128, 128],
            [128, 128, 128, 128, 127, 127, 128, 128],
            [128, 128, 128, 128, 127, 127, 128, 128],
            [127, 127, 128, 128, 127, 127, 127, 127],
            [127, 127, 128, 128, 127, 127, 127, 127],
            [127, 127, 128, 128, 128, 128, 127, 127],
            [127, 127, 128, 128, 128, 128, 127, 127]
        ])

        actual = BlindDwtDctChannelExtractor(selector).extract(channel, 1)

        assert actual == [128]
