# -*- coding: utf-8 -*-
"""
Utilities for working with images.

@author: Javier Castillo Delgado
@author: Javier Centeno Vega
@author: Manuel Macho Becerra
"""

import numpy
from PIL import Image

def load_image(path):
	"""
	Parameters
	----------
	path : str
		A file path to read an image from.
	
	Returns
	-------
	numpy.ndarray
		A tridimensional array of the values of the channels of the pixels of
		an image that can be accessed by the x index, y index and channel index
		of the value in that order.
	"""
	return numpy.array(Image.open(path).convert("RGB"))

def save_image(image, path):
	"""
	Parameters
	----------
	path : str
		A file path to save the image to.
	image : array_like
		An image represented as a tridimensional array of the values of the
		channels of its pixels that can be accessed by the x index, y index and
		channel index of the value in that order.
	"""
	Image.fromarray(image, "RGB").save(path)

def pad_image(image, block_size):
	paddingH = len(image) % block_size
	paddingW = len(image[0]) % block_size

	paddingH = 0 if paddingH == 0 else block_size - paddingH
	paddingW = 0 if paddingW == 0 else block_size - paddingW

	return numpy.pad(image, ((0, paddingH), (0, paddingW), (0, 0)), 'constant'), image.shape

def unpad_image(image, shape):
	return image[:shape[0], :shape[1]]

def classification_metric(block, threshold):
	"""
	Parameters
	----------
	block : array_like
		A section of a matrix.
	threshold : float
		The threshold of the minimal standard deviation required to consider
		block as part of the region of interest.
	
	Returns
	-------
	boolean
		True if this block can be considered part of the region of interest
		using threshold as a threshold, False otherwise.
	"""
	return numpy.std(block) > threshold

def divide_regions(image, block_size, threshold):
	"""
	Parameters
	----------
	image : array_like
		An image represented as a tridimensional array of the values of the
		channels of its pixels that can be accessed by the x index, y index and
		channel index of the value in that order.
	block_size : int
		The value used for the width and height of the sections this image will
		be divided in.
	threshold : float
		The threshold of the minimal standard deviation required to consider
		a section of the image as part of the region of interest.
	
	Returns
	-------
	mask : numpy.ndarray
		A two dimensional array containing 1 if the indices correspond to a
		block in the region of interest and 0 otherwise.
	"""
	s = block_size
	width = len(image[0]) // block_size
	height = len(image) // block_size

	mask = numpy.empty([height, width])

	for i in range(width):
		for j in range(height):
			mask[j][i] = classification_metric(image[j*s:(j+1)*s, i*s:(i+1)*s], threshold)

	return mask