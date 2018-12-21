# -*- coding: utf-8 -*-
"""
Implementation of an efficient and robust image encryption scheme for medical
applications, as described by A. Kanso and M. Ghebleh.

DOI: 10.1016/j.cnsns.2014.12.005
Bibliographic code: 2015CNSNS..24...98K

@author: Javier Castillo Delgado
@author: Javier Centeno Vega
@author: Manuel Macho Becerra
"""

import numpy
import math
from matrixutil import vector
from byteutil import to_bytes

def a_matrix(a, b, c, d):
	"""
	Parameters
	----------
	a : int
		A parameter used to fill in the matrix.
	b : int
		A parameter used to fill in the matrix.
	c : int
		A parameter used to fill in the matrix.
	d : int
		A parameter used to fill in the matrix.
	
	Returns
	-------
	a : numpy.ndarray
		A two dimensional matrix with dimensions (4, 4) used in pseudorandom
		number generation for the encryption algorithm.
	"""
	return numpy.array(
			[
				[
					(2*b + c)*(d + 1) + 3*d + 1,
					2*(b + 1),
					2*b*c + c + 3,
					4*b + 3
				],
				[
					2*(a + 1)*(d + b*c*(d + 1)) + a*(c + 1)*(d + 1),# E
					2*(a + b + a*b) + 1,
					a*(c + 3) + 2*b*c*(a + 1) + 2,# F
					3*a + 4*b*(a + 1) + 1
				],
				[
					3*b*c*(d + 1) + 3*d,
					3*b + 1,
					3*b*c + 3,
					6*b + 1
				],
				[
					c*(b + 1)*(d + 1) + d,
					b + 1,
					b*c + c + 1,
					2*b + 2
				]
			]
		)

u = vector(2, 3, 5, 1)

def omega_matrix(a, x, height, width):
	"""
	Parameters
	----------
	a : numpy.ndarray
		A two dimensional matrix with dimensions (4, 4).
	x : numpy.ndarray
		A column vector, or two dimensional matrix with dimensions (1, 4).
	height : int
		Height of the resulting matrix.
	width : int
		Width of the resulting matrix.
	
	Returns
	-------
	numpy.ndarray
		A two dimensional matrix representing the omega matrix used in the
		encryption algorithm.
	"""
	l = height*width
	y = []

	for i in range(math.ceil(l/16.0)):
		t = math.floor(numpy.dot(u, x)[0][0]) + 1

		for j in range(t):
			x = a.dot(x) % 1

		n = (numpy.floor(x * (2**32))).T

		y.append(vector(to_bytes(numpy.uint32(n), 4)))

	return numpy.reshape(y, [height, width])
