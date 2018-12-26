# -*- coding: utf-8 -*-
"""
Driver for the algorithm defined in crypto.

@author: Javier Castillo Delgado
@author: Javier Centeno Vega
@author: Manuel Macho Becerra
"""

import numpy

import imageutil
import matrixutil
import crypto

block_size = 20

image = imageutil.load_image("../Test/mri1.jpg")
mask = imageutil.divide_regions(image, block_size, 3)
imageutil.save_image(mask, "../Test/mask.png")

a = crypto.a_matrix(2, 1, 2, 2)
n = [block_size, block_size]

omega, y = crypto.omega_matrix(a, matrixutil.vector(0.6, 0.2, 0.8, 0.6).T, *n)

shuffled_image = crypto.block_shuffle(image, mask, omega,
						crypto.cat_map(2, 1), matrixutil.vector(0.9, 0.72).T, 
						crypto.cat_map(3, 2), matrixutil.vector(0.235, 0.821).T)

unshuffled_image = crypto.block_unshuffle(shuffled_image, mask, omega,
						crypto.cat_map(2, 1), matrixutil.vector(0.9, 0.72).T, 
						crypto.cat_map(3, 2), matrixutil.vector(0.235, 0.821).T)

imageutil.save_image(shuffled_image, "../Test/shuffled_image.png")
imageutil.save_image(unshuffled_image, "../Test/unshuffled_image.png")

masked_image = crypto.block_mask(shuffled_image, mask, omega, y)

imageutil.save_image(masked_image, "../Test/masked_image.png")