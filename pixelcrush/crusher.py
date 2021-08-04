import hashlib
import json
import string
from os import getenv
from typing import Union
import numpy as np
import pyximport
from PIL import Image
pyximport.install()
from pixelcrush.utils import set_leading_ones, count_leading_ones

hash_function = hashlib.new('sha256')
hash_length = hash_function.digest_size

starting_hardness = int(getenv('STARTING_HARDNESS', '0'))


class Crusher:

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
                self.hardness = np.zeros((self.size[0], self.size[1]), dtype=np.int32)
                for i in range(self.size[0]):
                    for j in range(self.size[1]):
                        self.hardness[i, j] = count_leading_ones(self.hashes[i, j].tobytes())
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
        self.image[::] = 255

        self.hashes = np.full(
            (self.size[0], self.size[1], hash_length),
            np.frombuffer(set_leading_ones(starting_hardness, hash_length), dtype=np.uint8),
            dtype=np.uint8
        )
        self.hardness = np.full(
            (self.size[0], self.size[1]),
            starting_hardness,
            dtype=np.int32
        )

    # interactions

    def set_pixel(self, position, color=None, new_hash: bytes = None, overwrite: bool = False):
        if not (0 <= position[0] < self.size[0] and 0 <= position[1] < self.size[1]):
            raise ValueError(f'The position must not be negative and must be smaller than the image size: '
                             f'{self.size}')
        if color is None and new_hash is None:
            raise ValueError('Nothing to set')
        if overwrite:
            if new_hash:
                self.hashes[position] = np.frombuffer(new_hash, dtype=np.uint8)
            if color:
                self.image[position] = color
            return True
        else:
            # check hash
            old_hash = self.hashes[position].tobytes()
            if new_hash > old_hash:
                self.image[position] = color
                self.hashes[position] = new_hash
                self.hardness[position] = count_leading_ones(new_hash)
                return True
            else:
                return False

    def get_image(self):
        return Image.fromarray(self.image)

    def get_heatmap(self, bw=False):
        heat = np.repeat(self.hardness, 3, 1)
        heat = np.reshape(heat, (*self.size, 3))
        if bw:
            return Image.fromarray(heat.astype(dtype=np.uint8))
        else:
            # return a gradient (green -> red -> yellow -> white -> black, viable until ~64)
            heat -= starting_hardness
            fade = np.clip(self.hardness - 40, a_max=None, a_min=0) * 10
            heat[:, :, 0] = np.clip(np.clip(self.hardness * 32 - 256, a_min=0, a_max=255) - fade, a_min=0, a_max=255)
            heat[:, :, 1] = np.clip(np.clip(np.abs(256 - 16 * self.hardness), a_min=0, a_max=255) - fade, a_min=0, a_max=255)
            heat[:, :, 2] = np.clip(np.clip(self.hardness * 32 - 1024, a_min=0, a_max=255) - fade, a_min=0, a_max=255)
            return Image.fromarray(heat.astype(dtype=np.uint8))
        pass
