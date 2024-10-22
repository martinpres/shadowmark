_BITS_IN_BYTE = 8


def vector_to_bipolar_bits(vector: list[int]) -> list[int]:
    """
    Converts a list of integers into a list of bipolar bits.

    Each bit in the input integers is transformed such that:
    - A bit value of 0 is converted to -1
    - A bit value of 1 is converted to 1

    Values less than 256 are padded with leading zeros to 8 decimal places.
    Values equal to or greater than 256 are not padded.

    :param vector: A list of integers.
    :return: A list of bipolar bits where each bit from the input integers is represented as -1 or 1.
    """
    return [
        2 * int(bit) - 1
        for byte in vector
        for bit in list('{0:08b}'.format(byte))
    ]


def bipolar_bits_to_vector(bipolar_bits: list[int]) -> list[int]:
    """
    Converts a list of bipolar bits into a list of integers (bytes).

    Each bipolar bit is transformed such that:
    - A value of -1 is converted to 0
    - A value of 1 is converted to 1

    The resulting bits are then grouped into bytes (8 bits) to form the corresponding integer values.
    This means that there are no numbers greater than 255 in the output.

    :param bipolar_bits: A list of bipolar bits, where each element is either -1 or 1.
    :return: A list of integers created from the bipolar bit values.
    """
    bits = [
        int((bipolar_bit + 1) / 2)
        for bipolar_bit in bipolar_bits
    ]

    return [
        int("".join(map(str, bits[i:i + _BITS_IN_BYTE])), 2)
        for i in range(0, len(bits), _BITS_IN_BYTE)
    ]
