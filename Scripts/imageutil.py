# -*- coding: utf-8 -*-
"""
Utilities for working with images.

@author: Javier Castillo Delgado
@author: Javier Centeno Vega
@author: Manuel Macho Becerra
"""

import numpy
from scipy import misc

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
	return misc.imread(path)

def classification_metric(submatrix, threshold):
	"""
	Parameters
	----------
	submatrix : array_like
		A section of a matrix.
	threshold : float
		The threshold of the minimal standard deviation required to consider
		submatrix as part of the region of interest.
	
	Returns
	-------
	boolean
		True if this submatrix can be considered part of the region of interest
		using threshold as a threshold, False otherwise.
	"""
	return numpy.std(submatrix) > threshold

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
	boolean
		True if this submatrix can be considered part of the region of interest
		using threshold as a threshold, False otherwise.
	"""

	s = block_size
	width = len(image[0]) // block_size
	height = len(image) // block_size

	mask = numpy.empty([height, width])

	for i in range(width):
		for j in range(height):
			mask[j][i] = classification_metric(image[j*s:(j+1)*s, i*s:(i+1)*s], threshold)

	return mask

def save_image(mask, path):
	misc.toimage(mask).save(path)

def save_mask(mask, path):
	misc.toimage(mask).save(path)
