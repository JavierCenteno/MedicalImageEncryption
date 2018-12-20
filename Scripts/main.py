# -*- coding: utf-8 -*-
"""
Driver for the algorithm defined in crypto.

@author: Javier Castillo Delgado
@author: Javier Centeno Vega
@author: Manuel Macho Becerra
"""

import imageutil

image = imageutil.load_image("../Test/mri2.jpg")
mask = imageutil.divide_regions(image, 4, 3)

imageutil.save_mask(mask, "../Test/mask.png")