"""A library for describing and applying affine transforms to PIL images."""
'''code from: https://gist.github.com/WChargin/d8eb0cbafc4d4479d004'''

import numpy as np
import PIL.Image


class RGBTransform(object):
    """A description of an affine transformation to an RGB image.
    This class is immutable.
    Methods correspond to matrix left-multiplication/post-application:
    for example,
        RGBTransform().multiply_with(some_color).desaturate()
    describes a transformation where the multiplication takes place first.
    Use rgbt.applied_to(image) to return a converted copy of the given image.
    For example:
        grayish = RGBTransform.desaturate(factor=0.5).applied_to(some_image)
    """

    def __init__(self, matrix=None):
        self._matrix = matrix if matrix is not None else np.eye(4)

    def _then(self, operation):
        return RGBTransform(np.dot(_embed44(operation), self._matrix))


    def mix_with(self, base_color, factor=1.0):
        """Mix an image by a constant base color.
        The base color should be a 1-by-3 array-like object
        representing an RGB color in [0, 255]^3 space.
        For example, to mix with orange,
        the transformation
            RGBTransform().mix_with((255, 127, 0))
        might be used.
        The factor controls the strength of the color to be added.
        If the factor is 1.0, all pixels will be exactly the new color;
        if it is 0.0, the pixels will be unchanged.
        """
        base_color = _to_rgb(base_color, "base_color")
        operation = _embed44((1 - factor) * np.eye(3))
        operation[:3, 3] = factor * base_color

        return self._then(operation)
    #
    def get_matrix(self):
        """Get the underlying 3-by-4 matrix for this affine transform."""
        return self._matrix[:3, :]

    def applied_to(self, image):
        """Apply this transformation to a copy of the given RGB* image.
        The image should be a PIL image with at least three channels.
        Specifically, the RGB and RGBA modes are both supported, but L is not.
        Any channels past the first three will pass through unchanged.
        The original image will not be modified;
        a new image of the same mode and dimensions will be returned.
        """

        # PIL.Image.convert wants the matrix as a flattened 12-tuple.
        # (The docs claim that they want a 16-tuple, but this is wrong;
        # cf. _imaging.c:767 in the PIL 1.1.7 source.)
        matrix = tuple(self.get_matrix().flatten())

        channel_names = image.getbands()
        channel_count = len(channel_names)
        if channel_count < 3:
            raise ValueError("Image must have at least three channels!")
        elif channel_count == 3:
            return image.convert('RGB', matrix)
        else:
            # Probably an RGBA image.
            # Operate on the first three channels (assuming RGB),
            # and tack any others back on at the end.
            channels = list(image.split())
            rgb = PIL.Image.merge('RGB', channels[:3])
            transformed = rgb.convert('RGB', matrix)
            new_channels = transformed.split()
            channels[:3] = new_channels
            return PIL.Image.merge(''.join(channel_names), channels)

#
#
def _embed44(matrix):
    """Embed a 4-by-4 or smaller matrix in the upper-left of I_4."""
    result = np.eye(4)
    r, c = matrix.shape
    result[:r, :c] = matrix
    return result
#
#
def _to_rgb(thing, name="input"):
    """Convert an array-like object to a 1-by-3 numpy array, or fail."""
    thing = np.array(thing)
    assert thing.shape == (3, ), (
        "Expected %r to be a length-3 array-like object, but found shape %s" %
            (name, thing.shape))
    return thing

def array2PIL(arr, size):
    mode = 'RGBA'
    arr = arr.reshape(arr.shape[0]*arr.shape[1], arr.shape[2])
    if len(arr[0]) == 3:
        arr = np.c_[arr, 255*np.ones((len(arr),1), np.uint8)]
    return PIL.Image.frombuffer(mode, size, arr.tostring(), 'raw', mode, 0, 1)