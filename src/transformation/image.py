import numpy as np
from PIL import Image


def image_to_channels(path: str) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Loads an image from the specified file path and splits it into its red, green, and blue (RGB) channels. The image is
    automatically converted to RGB mode if it is not already in that mode. Each channel is returned as a separate 2D
    numpy array.

    :param path: The file path to the image to be loaded.
    :return: A tuple containing three numpy arrays representing the red, green and blue channels of the image.
    """
    with Image.open(path) as input_image:
        r, g, b = input_image.convert('RGB').split()
        return np.array(r), np.array(g), np.array(b)


def channels_to_image(path: str, channels: tuple[np.ndarray, np.ndarray, np.ndarray]):
    """
    Combines the given red, green, and blue (RGB) channels into an image and saves it to the specified file path. The
    input channel values are clipped to the valid range [0, 255].

    :param path: The file path where the resulting image will be saved.
    :param channels: A tuple containing three numpy arrays representing the red, green and blue channels of the image.
    """
    Image.fromarray(np.dstack(channels).clip(0, 255).astype(np.uint8)).save(path)
