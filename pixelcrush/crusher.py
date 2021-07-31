import json
import math
import string
from dotenv import load_dotenv
from os import getenv
from typing import Union, Any
import numpy as np
import pyximport
pyximport.install()

load_dotenv('.env', override=True)


class CrusherData:

    name: string

    # width, height
    size: tuple[int, int]
    # bits
    color_depth: int
    # bytes
    hash_size: int

    # data stores
    image: np.ndarray
    hardness: np.ndarray

    def __init__(self, name: string):
        self.name = name
        try:
            # initialize from save files
            with open(self.file_name('image'), 'rb') as image_file, \
                    open(self.file_name('hardness'), 'rb') as hardness_file, \
                    open(self.file_name('meta'), 'r', encoding='utf-8') as meta_file:
                meta = json.load(meta_file)
                self.size = tuple(meta['size'])
                self.color_depth = meta['color_depth']
                self.hash_size = meta['hash_size']
                self.image = np.fromfile(image_file, dtype=self.color_type, count=-1)\
                    .reshape((self.size[0], self.size[1], 3))
                self.hardness = np.fromfile(hardness_file, dtype=self.color_type, count=-1)\
                    .reshape((self.size[0], self.size[1], self.hash_size))

            pass
        except FileNotFoundError:
            # some files could not be loaded. Restart with new files
            self._new_data(list(map(lambda x: int(x), getenv('IMAGE_SIZE').split(','))),
                           int(getenv('COLOR_DEPTH')), int(getenv('HASH_LENGTH')))
            self.save()
            pass
        pass

    def save(self):
        meta = {
            'hash_size': self.hash_size,
            'color_depth': self.color_depth,
            'size': self.size
        }
        with open(self.file_name('meta'), 'w', encoding='utf-8') as meta_file:
            json.dump(meta, meta_file, ensure_ascii=False, indent=4)
            self.image.tofile(self.file_name('image'))
            self.hardness.tofile(self.file_name('hardness'))

    @property
    def color_type(self):
        if int(math.ceil(self.color_depth / 8)) == 1:
            return np.uint8
        else:
            return np.uint16

    def file_name(self, file_type):
        return f'{self.name}-{file_type}.data'

    def _new_data(self, size: Union[tuple[int, int], list[int]], color_depth: int, hash_size: int):
        # check sizes
        if not 0 < size[0] < 65536 or not 0 < size[1] < 65536:
            raise ValueError('The size must be greater than zero, and must not exceed 65535 in any dimension')
        if not 0 < color_depth <= 16:
            raise ValueError('The color depth must be greater than zero, and must not exceed 16')
        if not 0 < hash_size < 256:
            raise ValueError('The color depth must be greater than zero, and must not exceed 255')

        # assign variables
        self.size = size[0], size[1]
        self.color_depth = color_depth
        self.hash_size = hash_size

        self.image = np.zeros((self.size[0], self.size[1], 3), dtype=self.color_type)
        self.hardness = np.zeros((self.size[0], self.size[1], self.hash_size), dtype=np.uint8)

    pass


class Crusher:

    _data: CrusherData

    def __init__(self, name):

        self._data = CrusherData(name)

        pass
