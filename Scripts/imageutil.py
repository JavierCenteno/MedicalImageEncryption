# -*- coding: utf-8 -*-
"""
Utilities for working with images.

@author: Javier Castillo Delgado
@author: Javier Centeno Vega
@author: Manuel Macho Becerra
"""

import numpy
import PIL

def load_image(image_path):
	"""
        Parameters
        ----------
        image_path : str
            Path to an image file.

        Returns
        -------
        numpy.ndarray
            A tridimensional array of the values of the channels of the pixels 
            of an image that can be accessed by the x index, y index and
            channel index of the value in that order.
        """
    image = PIL.Image.open(image_path);
    (width, height) = image.size
    return numpy.array(list(image.getdata())).reshape((height, width, 3))

