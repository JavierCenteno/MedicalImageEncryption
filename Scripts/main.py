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

omega = crypto.omega_matrix(crypto.a_matrix(2, 1, 2, 2), matrixutil.vector(0.6, 0.2, 0.8, 0.6).T, 8, 8)
print(omega)
