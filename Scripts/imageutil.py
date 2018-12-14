# -*- coding: utf-8 -*-
"""
Utilities for working with images.

@author: Javier Castillo Delgado
@author: Javier Centeno Vega
@author: Manuel Macho Becerra
"""

import numpy
from scipy import misc

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

	return misc.imread(image_path)

def classification_metric(submatrix, tau):
	return numpy.std(submatrix)> tau

def divide_regions(img, s, tau):
	width = len(img)
	height = len(img[0])

	mask = numpy.empty([height // s, width // s])

	width = len(mask)
	height = len(mask[0])

	for i in range(width):
		for j in range(height):
			mask[j][i] = classification_metric(img[j*s:(j+1)*s, i*s:(i+1)*s], tau)

	return mask

def save_image(mask, path):
	misc.toimage(mask).save(path)

def save_mask(mask, path):
	misc.toimage(mask).save(path)