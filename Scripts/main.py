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

import imageutil

image = imageutil.load_image("../Test/mri1.jpg")
mask = imageutil.divide_regions(image, 10, 0.5)

imageutil.save_mask(mask, "../Test/mask.png")