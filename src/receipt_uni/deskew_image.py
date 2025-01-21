import numpy as np
from skimage.color import rgb2gray
from skimage.transform import rotate
from deskew import determine_skew
import cv2


def deskew(img: np.ndarray) -> np.ndarray:
    """
    Deskew the input image.

    Args:
        img (numpy.ndarray): The input image.

    Yields:
        numpy.ndarray: The deskewed image.
    """
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    grayscale = rgb2gray(img)
    rot_angle = determine_skew(grayscale)
    rotated = rotate(img, rot_angle, resize=True, mode='constant', cval=1.0)
    image_rotated = cv2.cvtColor(np.uint8(rotated * 255), cv2.COLOR_RGB2BGR)
    return image_rotated
