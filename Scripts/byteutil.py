# -*- coding: utf-8 -*-
"""
Utilities for working with bytes and integers.

@author: Javier Castillo Delgado
@author: Javier Centeno Vega
@author: Manuel Macho Becerra
"""

byte_mask = 0xFF

def to_bytes(n, byte_number):
	"""
	Parameters
	----------
	n : int
		A number to break down into bytes.
	byte_number : int
		The number of bytes to break n into.
	
	Returns
	-------
	list
		A list of numbers in the range [0, 256) representing the bytes this
		number is divided into, starting by the lowermost bytes.
	
	Examples
	--------
	>>> [hex(byte) for byte in to_bytes(0x01234567, 4)]
	['0x1', '0x23', '0x45', '0x67']
	"""
	return [((byte_mask << shift) & n) >> shift for shift in reversed(range(0, byte_number * 8, 8))]
