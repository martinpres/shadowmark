from argparse import ArgumentParser, ArgumentTypeError
from sys import stderr

from src.embedding.blind_dwt_dct_channel_embedder import BlindDwtDctChannelEmbedder
from src.embedding.rgb_watermark_embedder import RGBWatermarkEmbedder
from src.exceptions import WatermarkSizeError, ImageChannelError
from src.extraction.blind_dwt_dct_channel_extractor import BlindDwtDctChannelExtractor
from src.extraction.rgb_watermark_extractor import RGBWatermarkExtractor
from src.randomization.permutation_indices_selector import PermutationIndicesSelector
from src.transformation.image import image_to_channels, channels_to_image

DEFAULT_SEED = 1234567890
DEFAULT_GAIN = 1.0
DEFAULT_WATERMARK_SHAPE = '32x32'
DEFAULT_CHANNELS = 'rgb'


def _parse_shape(arg: str):
    try:
        width, height = tuple([int(x) for x in arg.split('x', 1)])
    except ValueError:
        raise ArgumentTypeError("Value must be provided in the form WxH, where W is width and H is height")

    # Swap given shape because width x height is more user-friendly and implementation expects height x width
    return height, width


def main():
    argument_parser = ArgumentParser(
        prog='shadowmark',
        description='Embeds/extracts watermark to/from image using blind DWR-DCT approach.'
    )

    argument_parser.add_argument(
        '-i', '--image', required=True, type=str,
        metavar='PATH',
        help='path to input image for watermark embedding/extraction'
    )

    argument_parser.add_argument(
        '-o', '--output', required=True, type=str,
        metavar='PATH',
        help='path where the output image will be stored. '
             'If the -e or --embed option is used, the output is image with embedded watermark. '
             'If the -x or --extract option is used, the output is image of the extracted watermark.'
    )

    argument_parser.add_argument(
        '-e', '--embed', required=False, type=str,
        metavar='PATH',
        help='embeds given watermark to the input image. Value is a path to a watermark image.'
    )

    argument_parser.add_argument(
        '-x', '--extract', required=False, type=_parse_shape,
        default=DEFAULT_WATERMARK_SHAPE, metavar="WxH",
        help='extracts watermark from the input image. '
             'Value is expected shape of the embedded watermark in the form WxH, where W is width and H is height. '
             f'The default is {DEFAULT_WATERMARK_SHAPE}.'
    )

    argument_parser.add_argument(
        '-s', '--seed', required=False, type=int,
        default=DEFAULT_SEED,
        help='integer seed for the pseudorandom number generator (PRNG). '
             'Using the same seed value for embedding and extraction is essential for successful watermark detection. '
             'The seed may be used as a secret key to protect the watermark from tampering, '
             'but bear in mind that it is not strong cryptographic safeguard. '
             f'If not set, the default seed {DEFAULT_SEED} is applied.'
    )

    argument_parser.add_argument(
        '-g', '--gain', required=False, type=float,
        default=DEFAULT_GAIN,
        help='float number specifying strength of the embedding. '
             'Higher values make the watermark more robust and resistant against attacks '
             'but it may decrease quality of the resulting image. '
             'Takes effect only if -e or --embed option is also used. '
             f'Defaults to {DEFAULT_GAIN}.'
    )

    argument_parser.add_argument(
        '-c', '--channels', required=False, type=lambda s: s.lower(),
        default=DEFAULT_CHANNELS,
        help='channels of both input image and watermark that will be used during embedding/extraction. '
             'Allowed values are \'r\' for red, \'g\' for green and \'b\' for blue. Other values are ignored. '
             'You may select just one or any combination of channels, like \'rg\', \'gb\' or \'rb\'. '
             'Order and case of channel letters is not important, \'gbr\' == \'BGR\'.'
             f'Default is {DEFAULT_CHANNELS}.'
    )

    args = argument_parser.parse_args()
    input_image_channels = image_to_channels(args.image)
    indices_selector = PermutationIndicesSelector(args.seed)

    if args.embed:
        embedder = RGBWatermarkEmbedder(BlindDwtDctChannelEmbedder(args.gain, indices_selector), args.channels)
        watermark_channels = image_to_channels(args.embed)

        try:
            embedded_channels = embedder.embed(input_image_channels, watermark_channels)
            channels_to_image(args.output, embedded_channels)

        except (ImageChannelError, WatermarkSizeError) as e:
            print(e, file=stderr)

    elif args.extract:
        extractor = RGBWatermarkExtractor(BlindDwtDctChannelExtractor(indices_selector), args.channels)

        try:
            extracted_watermark_channels = extractor.extract(input_image_channels, args.extract)
            channels_to_image(args.output, extracted_watermark_channels)

        except (ImageChannelError, WatermarkSizeError) as e:
            print(e, file=stderr)


if __name__ == '__main__':
    main()
