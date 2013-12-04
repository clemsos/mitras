#!/usr/bin/env python
# -*- coding: utf-8 -*-

import h5py
import numpy as np
import numexpr as ne
from scipy.sparse import *
import cPickle as pickle
import pylab as pl
import tables as tb

def test_save_as_plain_txt():
    z=np.zeros([3,5])
    path="/tmp/test.txt"
    with open(path, 'w') as f:
        # f.write(map(str,[x]) for x in range(0,count))
         f.write("\n".join(" ".join(x for x in (a,b))))
    pass

def test_save_as_npy_file():
    z=np.zeros([3,5])
    path="/tmp/test.npy"
    np.save(path,z)

def test_save_as_npz_file():
    z=np.zeros([3,5])
    path="/tmp/test.npz"
    np.savez(path,z)

def test_dump_as_file():
    z=np.zeros([3,5])
    path="/tmp/test.dump"
    z.dump(path)

def test_linear_combination():
    z=np.zeros([3,5])
    a=np.array([[1, 2, 3, 4, 5],[1, 2, 3, 4, 5],[1, 2, 3, 4, 5]])
    b=np.array([[1, 2, 3, 4, 5],[1, 2, 3, 4, 5],[1, 2, 3, 4, 5]])

    print z
    print

    z[1:3]=a[1:3]*2
    print z

def test_scipy_sparse_with_cPickle():
    z=np.zeros([3,5])
    path="/tmp/test.dat"
    d=csr_matrix(z)
    with open(path, 'wb') as outfile:
        pickle.dump(z, outfile, pickle.HIGHEST_PROTOCOL)
    # d.save(path)

def test_save_as_data_txt():
    z=np.zeros([3,5])
    path="/tmp/test.txt"
    np.savetxt(path, z)

def test_save_using_memmap():
    # z=np.zeros([3,5])
    np.memmap("/tmp/test.float32.memmap", dtype='float32', mode='w+', shape=(3,5))
    np.memmap("/tmp/test.float16.memmap", dtype='float16', mode='w+', shape=(3,5))
    np.memmap("/tmp/test.uint8.memmap", dtype='uint8', mode='w+', shape=(3,5))

def save_complex_data_using_memmap():
    a=np.memmap("/tmp/test2.float16.memmap", dtype='float16', mode='w+', shape=(3,5))
    a=[np.arange(3),np.arange(5)]
    # print a
    # print data

def test_save_using_pylab():
    z=np.zeros([3,5])
    path="/tmp/test.pl"
    pl.save(path, z)

def test_tofile():
    z=np.zeros([3,5])
    path="/tmp/test.file"
    z.tofile(path)

def test_to_hdf5():
    z=np.zeros([3,5])
    path="/tmp/test.h5"
    f = h5py.File(path, 'w')
    f['dset'] = z
    f.close()

def test_large_file_with_hdf5():
    ndim = 60000
    path="/tmp/test.big.h5"
    h5file = tb.openFile(path, mode='w', title="Test Array")
    root = h5file.root
    x = h5file.createCArray(root,'x',tb.Float64Atom(),shape=(ndim,ndim))
    x[:100,:100] = np.random.random(size=(100,100)) # Now put in some data
    h5file.close()

# here you will see a 762MB file created in your working directory    

test_dump_as_file()
test_save_as_npy_file()
test_save_as_npz_file()
test_scipy_sparse_with_cPickle()
test_save_using_memmap()
test_save_as_data_txt()
test_tofile()
test_to_hdf5()
# test_large_file_with_hdf5()
# test_save_using_pylab() # depreciated
# save_complex_data_using_memmap()
# test_save_as_plain_txt()

def benchmark_computation_numexpr():
    z= np.arange([1e6,1e6])
    ne.evaluate(z)