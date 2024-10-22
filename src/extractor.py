from abc import ABC, abstractmethod


class ChannelExtractor(ABC):

    @abstractmethod
    def extract(self, channel, watermark_size):
        """
        Extracts watermark data from an image channel.

        :param channel: An image channel.
        :param watermark_size: An expected size of the extracted watermark.
        :return: Extracted watermark data.
        """
        pass
