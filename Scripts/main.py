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

#Parámetros
image = imageutil.load_image("../Test/mri3.jpg")

a = (crypto.a_matrix(2, 1, 2, 2), matrixutil.vector(0.6, 0.2, 0.8, 0.6).T)
cm1 = (crypto.cat_map(2, 1), matrixutil.vector(0.9, 0.72).T)
cm2 = (crypto.cat_map(3, 2), matrixutil.vector(0.235, 0.821).T)
block_size = 35
std_limit = 3

#Algoritmo
cypheredImage, mask, shape = crypto.cypher_image(image, *a, *cm1, *cm2, block_size, std_limit)
decypheredImage = crypto.decypher_image(cypheredImage, mask, shape, *a, *cm1, *cm2, block_size)

imageutil.save_image(cypheredImage, "../Test/process/cyphered_image.png")
imageutil.save_image(decypheredImage, "../Test/process/decyphered_image.png")