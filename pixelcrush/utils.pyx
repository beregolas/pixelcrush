#cython: language_level=3

byte_map = [0, 128, 192, 224, 240, 248, 252, 254, 255]

cdef unsigned char[256] _leading_map
cdef unsigned char l = 0
# Fill the leading map with
for i in range(256):
    if i >= byte_map[l+1]:
        l += 1
    _leading_map[i] = l


cpdef unsigned short count_leading_ones(hash_value: bytes):
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
        byte_count = _leading_map[b]
        count += byte_count
        if byte_count < 8:
            break
    return count


cpdef set_leading_ones(unsigned int leading_ones, unsigned int length):
    bytes_out = []
    for b in range(length):
        if leading_ones > 8:
            leading_ones -= 8
            bytes_out.append(byte_map[8])
        elif leading_ones > 0:
            bytes_out.append(byte_map[leading_ones])
            leading_ones = 0
        else:
            bytes_out.append(0)
    return bytes(bytes_out)


cpdef heat_gradient(unsigned char hardness, rgb: bool = True):
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
