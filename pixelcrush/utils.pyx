#cython: language_level=3

cdef unsigned char count_leading_ones_byte(unsigned char hash_byte):
    """ Determines the amount of leading set bits in a byte, starting from the most significant (assuming little endian)

    Parameters
    ----------
    hash_byte
        a single byte / an integer with values between 0 and 255

    Returns
    -------
        the amount of leading ones, counting from most significant
    """
    cdef unsigned char comparator = 1 << 7
    cdef unsigned char count = 0
    while comparator > 0:
        if comparator & hash_byte:
            count += 1
            comparator = comparator >> 1
        else:
            break
    return count


cpdef unsigned short count_leading_ones(bytes hash_value):
    """ Determines the amount of leading set bits in a byte array,
    starting from most significant (assuming little endian)

    Parameters
    ----------
    hash_value: bytes

    Returns
    -------
        the amount of leading ones, counting from most significant
    """
    cdef unsigned short count = 0
    cdef unsigned char byte_count = 0
    for b in hash_value:
        byte_count = count_leading_ones_byte(b)
        count += byte_count
        if byte_count < 8:
            break
    return count


def heat_gradient(unsigned char hardness, rgb: bool = True):
    """ returns an rgb value for a provided heat value between 0 and 255

    Parameters
    ----------
    hardness
        the hardness value
    rgb
        True: convert to an rgb gradient, False: return a greyscale

    Returns
    -------

    """
    if not rgb:
        # return greyscale for UIs to interpret
        return hardness, hardness, hardness
    else:
        # return a gradient (green -> red -> yellow -> white -> black, viable until 64)
        return max(0, min(255, hardness * 32 - 256) - max(0, hardness - 40) * 10), \
               max(0, min(255, abs(256 - 16 * hardness)) - max(0, hardness - 40) * 10), \
               max(0, min(255, hardness * 32 - 1024) - max(0, hardness - 40) * 10)
