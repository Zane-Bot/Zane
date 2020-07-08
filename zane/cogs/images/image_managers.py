import abc
import io
import numpy as np

import matplotlib.pyplot as plt
from wand.image import Image
import skimage.io


__all__ = ('Wand', 'Numpy')


class ImageManager(metaclass=abc.ABCMeta):

    @staticmethod
    @abc.abstractmethod
    def input(image_bytes, *args, **kwargs):
        raise NotImplementedError

    @staticmethod
    @abc.abstractmethod
    def output(image_object, *args, **kwargs):
        raise NotImplementedError


class Wand(ImageManager):

    @staticmethod
    def input(image_bytes, *args, **kwargs) -> Image:
        image = Image(blob=image_bytes.getvalue())
        print(image.format)
        image_bytes.close()
        return image

    @staticmethod
    def output(image_object, *args, **kwargs) -> io.BytesIO:
        image_bytes = io.BytesIO()
        print(image_object.format)
        image_object.save(image_bytes)
        image_bytes.seek(0)
        return image_bytes


class Numpy(ImageManager):

    @staticmethod
    def input(image_bytes, *args, **kwargs) -> np.ndarray:
        image_bytes.seek(0)
        return skimage.io.imread(image_bytes, plugin='matplotlib')

    @staticmethod
    def output(arr, *args, **kwargs) -> io.BytesIO:
        image_bytes = io.BytesIO()
        plt.imsave(image_bytes, arr, cmap=kwargs.pop("cmap"))
        image_bytes.seek(0)
        return image_bytes