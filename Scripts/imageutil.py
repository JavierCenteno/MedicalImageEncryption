# -*- coding: utf-8 -*-
"""
Utilities for working with images.

@author: Javier Castillo Delgado
@author: Javier Centeno Vega
@author: Manuel Macho Becerra
"""

import numpy
from PIL import Image
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
	Image.fromarray(image, mode="RGB").save(path)

def save_mask(mask, path):
	"""
	Parameters
	----------
	path : str
		A file path to save the image to.
	mask : array_like
		An image represented as a tridimensional array of the values of the
		channels of its pixels that can be accessed by the x index, y index and
		channel index of the value in that order.
	"""
	Image.fromarray(mask, mode="L").save(path)

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
	return numpy.mean(numpy.std(submatrix)) > threshold

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
	width = len(image)
	height = len(image[0])
	mask = numpy.empty([height // block_size, width // block_size])
	width = len(mask)
	height = len(mask[0])
	for i in range(width):
		for j in range(height):
			block = numpy.ix_([i*block_size, (i+1)*block_size], [j*block_size, (j+1)*block_size])
			mask[i][j] = classification_metric(block, threshold)
	return mask
