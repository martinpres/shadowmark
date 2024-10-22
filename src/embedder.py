from abc import ABC, abstractmethod


class ChannelEmbedder(ABC):

    @abstractmethod
    def embed(self, channel, watermark_data):
        """
        Embeds watermark data to an image channel.

        :param channel: An image channel.
        :param watermark_data: A watermark data for embedding.
        :return: An image channel with embedded watermark data.
        """
        pass
