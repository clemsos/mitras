#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

z=np.zeros([3,5])
a=np.array([[1, 2, 3, 4, 5],[1, 2, 3, 4, 5],[1, 2, 3, 4, 5]])
b=np.array([[1, 2, 3, 4, 5],[1, 2, 3, 4, 5],[1, 2, 3, 4, 5]])

print z
print

z[1:3]=a[1:3]*2
print z

# a = numpy.memmap('test.mymemmap', dtype='float32', mode='w+', shape=(707425,707425))
# here you will see a 762MB file created in your working directory    