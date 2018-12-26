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

def cat_map(a, b):
	return numpy.array([[1, a], [b, a*b + 1]])

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
	z = []
	u = vector(2, 3, 5, 1)

	for i in range(math.ceil(l/16.0)):
		t = math.floor(numpy.dot(u, x)[0][0]) + 1

		for j in range(t):
			x = a.dot(x) % 1

		n = (numpy.floor(x * (2**32))).T

		y.append(x)
		z.append(vector(to_bytes(numpy.uint32(n), 4)))

	return (numpy.reshape(numpy.reshape(numpy.array(z), [math.ceil(l/16.0)*16])[:l], [height, width]), 
		numpy.reshape(numpy.array(y), [math.ceil(l/16.0)*4]))

def shuffling_sequence(a, x, n):
	r1 = []
	r2 = []
	u = vector(2, 3)

	for i in range(n):
		t = math.floor(numpy.dot(u, x)[0][0]) + 1

		for j in range(t):
			x = a.dot(x) % 1

		r1.append(x[0][0])
		r2.append(x[1][0])

	r1 = [i[0] for i in sorted(enumerate(r1), key = lambda x : x[1])]
	r2 = [i[0] for i in sorted(enumerate(r2), key = lambda x : x[1])]

	return r1, r2

def shuffle(i, omega, l, a1, x1, a2, x2):
	s1 = shuffling_sequence(a1, x1, l)
	s2 = shuffling_sequence(a2, x2, l)

	#Shuffling de columnas
	i = numpy.array([[i[1] for i in sorted(enumerate(j), key = lambda x : s1[0][x[0]])] for j in i])
	omega = numpy.array([[i[1] for i in sorted(enumerate(j), key = lambda x : s1[1][x[0]])] for j in omega])

	#Shuffling de filas
	i = numpy.array([i[1] for i in sorted(enumerate(i), key = lambda x : s2[0][x[0]])])
	omega = numpy.array([i[1] for i in sorted(enumerate(omega), key = lambda x : s2[1][x[0]])])

	return i, omega

def unshuffle(i, omega, l, a1, x1, a2, x2):
	s1 = shuffling_sequence(a1, x1, l)
	s2 = shuffling_sequence(a2, x2, l)

	#Shuffling de columnas
	i = numpy.array([[i[1] for i in sorted(zip(numpy.argsort(s1[0]), j), key = lambda x : x[0])] for j in i])
	omega = numpy.array([[i[1] for i in sorted(zip(numpy.argsort(s1[1]), j), key = lambda x : x[0])] for j in omega])

	#Shuffling de filas
	i = numpy.array([i[1] for i in sorted(zip(numpy.argsort(s2[0]), i), key = lambda x : x[0])])
	omega = numpy.array([i[1] for i in sorted(zip(numpy.argsort(s2[1]), i), key = lambda x : x[0])])

	return i, omega

def mask(i, omega, l, y):
	p = 1

	for j in range(l):
		o = 1 + (omega.T[j].dot(numpy.array([numpy.product(i) for i in numpy.transpose(i, (1, 0, 2))])) % math.floor((l*l)/4))
		numpy.roll(omega.T[j], -p)
		p = 1 + math.floor(l*y[o])

		for k in range(l):
			i[k][j] = (i[k][j] + omega[j][k]) % 256


	return i

def block_shuffle(image, mask, omega, a1, x1, a2, x2):
	s = len(image) // len(mask)
	res = numpy.zeros_like(image)

	for i in range(len(mask[0])):
		for j in range(len(mask)):
			if not mask[j][i]:
				res[j*s:(j+1)*s, i*s:(i+1)*s] = image[j*s:(j+1)*s, i*s:(i+1)*s]

			else:
				res[j*s:(j+1)*s, i*s:(i+1)*s] = shuffle(image[j*s:(j+1)*s, i*s:(i+1)*s], 
														omega, s, a1, x1, a2, x2)[0]

	return res

def block_unshuffle(image, mask, omega, a1, x1, a2, x2):
	s = len(image) // len(mask)
	res = numpy.zeros_like(image)

	for i in range(len(mask[0])):
		for j in range(len(mask)):
			if not mask[j][i]:
				res[j*s:(j+1)*s, i*s:(i+1)*s] = image[j*s:(j+1)*s, i*s:(i+1)*s]

			else:
				res[j*s:(j+1)*s, i*s:(i+1)*s] = unshuffle(image[j*s:(j+1)*s, i*s:(i+1)*s], 
														omega, s, a1, x1, a2, x2)[0]

	return res

def block_mask(image, _mask, omega, y):
	s = len(image) // len(_mask)
	res = numpy.zeros_like(image)

	for i in range(len(_mask[0])):
		for j in range(len(_mask)):
			if not _mask[j][i]:
				res[j*s:(j+1)*s, i*s:(i+1)*s] = image[j*s:(j+1)*s, i*s:(i+1)*s]

			else:
				res[j*s:(j+1)*s, i*s:(i+1)*s] = mask(image[j*s:(j+1)*s, i*s:(i+1)*s], omega, s, y)

	return res