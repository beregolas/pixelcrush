import hashlib
import json
import math
import string
from os import getenv
from typing import Union
import numpy as np
import pyximport
pyximport.install()
from pixelcrush.utils import set_leading_ones, count_leading_ones


hash_function = hashlib.new(getenv('HASH_ALGORITHM', 'sha256'))
hash_length = hash_function.digest_size

starting_hardness = int(getenv('STARTING_HARDNESS', '0'))


class CrusherData:

    name: string

    # width, height
    size: tuple[int, int]

    # data stores
    image: np.ndarray
    hashes: np.ndarray
    hardness: np.ndarray

    def __init__(self, name: string):
        self.name = name
        try:
            # initialize from save files
            with open(self.file_name('image'), 'rb') as image_file, \
                    open(self.file_name('hashes'), 'rb') as hashes_file, \
                    open(self.file_name('meta'), 'r', encoding='utf-8') as meta_file:
                meta = json.load(meta_file)
                self.size = tuple(meta['size'])
                self.image = np.fromfile(image_file, dtype=np.uint8, count=-1)\
                    .reshape((self.size[0], self.size[1], 3))
                self.hashes = np.fromfile(hashes_file, dtype=np.uint8, count=-1)\
                    .reshape((self.size[0], self.size[1], hash_length))
                self.hardness = np.zeros((self.size[0], self.size[1]))
                for i in range(self.size[0]):
                    for j in range(self.size[1]):
                        self.hardness[i, j] = count_leading_ones(self.hashes[i, j].tobytes())
            pass
        except FileNotFoundError:
            # some files could not be loaded. Restart with new files
            self._new_data(list(map(lambda x: int(x), getenv('IMAGE_SIZE').split(','))))
            # save the metadata
            meta = {
                'size': self.size
            }
            with open(self.file_name('meta'), 'w', encoding='utf-8') as meta_file:
                json.dump(meta, meta_file, ensure_ascii=False, indent=4)
            # save the actual data
            self.save()
            pass
        pass

    def save(self):
        self.image.tofile(self.file_name('image'))
        self.hashes.tofile(self.file_name('hashes'))

    def file_name(self, file_type):
        return f'{self.name}-{file_type}.data'

    def _new_data(self, size: Union[tuple[int, int], list[int]]):
        # check sizes
        if not 0 < size[0] < 65536 or not 0 < size[1] < 65536:
            raise ValueError('The size must be greater than zero, and must not exceed 65535 in any dimension')

        # assign variables
        self.size = size[0], size[1]

        self.image = np.zeros((self.size[0], self.size[1], 3), dtype=np.uint8)
        self.hashes = np.full(
            (self.size[0], self.size[1], hash_length),
            np.frombuffer(set_leading_ones(starting_hardness, hash_length), dtype=np.uint8),
            dtype=np.uint8
        )
        self.hardness = np.full(
            (self.size[0], self.size[1]),
            starting_hardness,
            dtype=np.uint8
        )


class Crusher:

    _data: CrusherData

    def __init__(self, name):

        self._data = CrusherData(name)

        pass

    def set_pixel(self, position, color, new_hash=None):
        # TODO
        pass

    def overwrite(self, position, color=None, hardness=None):
        # TODO
        pass
