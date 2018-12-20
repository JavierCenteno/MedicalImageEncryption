import numpy
import math

#OPERACIONES DE BITS
def first_num(n):
	mask = 0b11111111000000000000000000000000
	return (n & mask) >> 24

def second_num(n):
	mask = 0b00000000111111110000000000000000
	return (n & mask) >> 16

def third_num(n):
	mask = 0b00000000000000001111111100000000
	return (n & mask) >> 8

def fourth_num(n):
	mask = 0b00000000000000000000000011111111
	return n & mask

#MATRICES

def a_matrix(a, b, c, d):
	return numpy.array(
			[
				[(2*b + c)*(d + 1) + 3*d + 1, 2*(b + 1), 2*b*c + c + 3, 4*b + 3],
				[2*(a + 1)*(d + b*c*(d + 1)) + a*(c + 1)*(d + 1), 2*(a + b + a*b) + 1, a*(c + 3) + 2*b*c*(a + 1) + 2, 3*a + 4*b*(a + 1) + 1],
				[3*b*c*(d + 1) + 3*d, 3*b + 1, 3*b*c + 3, 6*b + 1],
				[c*(b + 1)*(d + 1) + d, b + 1, b*c + c + 1, 2*b + 2]
			]
		)

def vector(*a):
	return numpy.atleast_2d(numpy.array([*a]))

def omega_matrix(a, x, h, w):
	l = h*w
	u = vector(2, 3, 5, 1)
	y = []

	for i in range(math.ceil(l/16.0)):
		t = math.floor(numpy.dot(u, x)[0][0]) + 1

		for j in range(t):
			x = a.dot(x) % 1

		n = (numpy.floor(x * (2**32))).T

		y.append(vector(first_num(numpy.int64(n)),
						second_num(numpy.int64(n)),
						third_num(numpy.int64(n)),
						fourth_num(numpy.int64(n))))

	return numpy.reshape(y, [h, w])

omega = omega_matrix(a_matrix(2, 1, 2, 2), vector(0.6, 0.2, 0.8, 0.6).T, 8, 8)

print(omega)