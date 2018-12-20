# -*- coding: utf-8 -*-
"""
Utilities for working with matrices.

@author: Javier Castillo Delgado
@author: Javier Centeno Vega
@author: Manuel Macho Becerra
"""

import numpy

def vector(*a):
	"""
	Parameters
	----------
	a : array_like
		One or more objects.
	
	Returns
	-------
	numpy.ndarray
		An array of at least two dimensions containing the elements passed as
		arguments.
		
	Raises
	------
	ValueError
		If it's not passed any arguments.
	"""
	if len(a) == 0:
		raise ValueError
	return numpy.atleast_2d(numpy.array([*a]))
