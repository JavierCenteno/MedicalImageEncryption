# -*- coding: utf-8 -*-
"""
Driver for the algorithm defined in crypto.

@author: Javier Castillo Delgado
@author: Javier Centeno Vega
@author: Manuel Macho Becerra
"""

import imageutil
import matrixutil
import crypto

#image = imageutil.load_image("../Test/mri2.jpg")
#mask = imageutil.divide_regions(image, 4, 3)
#imageutil.save_mask(mask, "../Test/mask.png")

a = crypto.a_matrix(2, 1, 2, 2)
n = [4, 4]

omega = crypto.omega_matrix(a, matrixutil.vector(0.6, 0.2, 0.8, 0.6).T, *n)
psi = crypto.omega_matrix(a, matrixutil.vector(0.7, 0.1, 0.9, 0.2).T, *n)

print(crypto.shuffle(a, omega, 4, 
	crypto.cat_map(2, 1), matrixutil.vector(0.9, 0.72).T, 
	crypto.cat_map(3, 2), matrixutil.vector(0.235, 0.821).T))

