# -*- coding: utf-8 -*-
"""
Created on Fri Jul 15 08:56:24 2016

@author: wang
"""

import numpy as np
import matplotlib.pyplot as plt
import random
import os,re,sys
import h5py

lbd = 1.0e-10
distance = 1.
scr_size = 129
pix_size = 0.0086

hlf_scr = scr_size*pix_size/2.0
theta = np.arctan(hlf_scr/distance)/2.0
q = 4*np.pi*np.sin(theta)/lbd
d = 2*np.pi/q

print d


def readfile(filename):
    f = open(filename,"r")
    allarr = []
    realarr = []
    imagarr = []
    print filename
    for line in f.readlines():
        comp = line.strip().split(',')[:-1]
        linereal = [float(y[0]) for y in [x.split('+') for x in comp]]
        lineimag = [float(y[1]) for y in [x.split('+') for x in comp]]
        realarr.append(linereal)
        imagarr.append(lineimag)
    realarr = np.array(realarr)
    imagarr = np.array(imagarr)
    allarr = realarr + imagarr*1j
    f.close()
    return allarr

def getdim(filename):
    f = open(filename,"r")
    dim1 = 0
    dim2 = 0
    for line in f.readlines():
        dim1 = dim1 + 1
        comp = line.strip().split(',')[:-1]
        dim2 = len(comp)
    print dim1,dim2
    return (dim1,dim2)

def Make_screen(scr_size,dr):
    scr = np.zeros((scr_size,scr_size),dtype=np.complex64)
    z = 1.0 #distance=1.0m
    k = np.pi*2.0/lbd
    for i in range(scr_size):
        for j in range(scr_size):
            x = (i-(scr_size-1)/2.0)*pix_size
            y = (j-(scr_size-1)/2.0)*pix_size
            r = np.sqrt(x**2+y**2+z**2)
            s = k*np.array((x,y,z))/r
    #        print np.dot(s,dr)
#            print 'dr' , dr
 #           print 's', s
            scr[i][j] = np.exp(1.0j*np.dot(s,dr))
            #scr[i][j] = np.exp(1.0j*(i+j)/scr_size*6*2*np.pi)
     #       print 'v', 1.0*(i+j)/scr_size*12*np.pi
    return scr

def read2(dim,filename1,filename2,shift):
    scr = Make_screen(dim,shift)
    arr1 = readfile(filename1)
    arr2 = readfile(filename2)
    arrR = arr1+arr2*scr
    return arrR

def RandVecGen(rmin,rmax):
    e1 = 0
    e2 = 0
    e3 = 0
    while e1**2+e2**2+e3**2>rmax**2 or e1**2+e2**2+e3**2<rmin**2:
        e1 = (np.random.rand()*2-1)*rmax
        e2 = (np.random.rand()*2-1)*rmax
        e3 = (np.random.rand()*2-1)*rmax
#    rr = e1**2+e2**2+e3**2
#    r = np.random.rand()*r
    f = open('log.txt','a+')
    f.write( "%6.2f,%6.2f,%6.2f,%6.2f\n" % (1e9*e1,1e9*e2,1e9*e3,1e9*np.sqrt(e1**2+e2**2+e3**2)) )
    f.close()
    return np.array((e1,e2,e3))


#def show():
#    allarr1 = readfile("tmp1.dat")
#    plt.subplot(5,5,1)
#    plt.imshow(np.log(abs(allarr1)))
#    for i in range(20):
#        r = 1.0e-6*3
#        shift = RandVecGen(r)
#        allarr2 = read2("tmp1.dat","tmp2.dat",shift)
#        plt.subplot(5,5,i+6)
#        plt.imshow(np.log(abs(allarr2)))

def coherent(conum,num,fname):
    '''
    conum: number of coherent
    num: number of patterns
    '''
    rmin = 300e-9
    rmax = 1e-6
    shifts = [(6e-7,6e-7,6e-7),(0,6e-7,6e-7),(6e-7,0,6e-7),(6e-7,6e-7,0),(6e-7,0,0),(0,6e-7,0),(0,0,6e-7),(0,-6e-7,6e-7),(-6e-7,0,6e-7),(6e-7,-6e-7,0)]
    shiftalllist = []
    anglealllist = []
    pcoall = []
    pnoall = []
    out_co = h5py.File(str(conum)+'co_'+fname)
    out_no = h5py.File(str(conum)+'no_'+fname)
    h = h5py.File(fname)
    pattern = h['pattern'][()]
    angle = h['angle'][()]
    inds1 = 0
    n_pattern = len(pattern)
    for i in range(num):
        pco = np.zeros(pattern.shape[-2:],dtype=np.complex64)
        pno = np.zeros(pattern.shape[-2:])
        shiftlst = []
        anglelst = []
        #inds = random.sample(range(len(pattern)),conum)
        inds = [(inds1+113*i)%n_pattern for i in range(conum)]
        inds1 = inds1 + 1
        for coi in range(conum):
            ind = inds[coi]
            anglelst.append(angle[ind])
            if coi != 0:
                #shift = RandVecGen(rmin,rmax)
                shift = shifts[coi]
                shiftlst.append(shift)
                pco = pco + pattern[ind]*Make_screen(pattern.shape[-1],shift)
                pno = pno + abs(pattern[ind])
            else:
                pco = pco + pattern[ind]
                pno = pno + abs(pattern[ind])
        pco = abs(pco)
        shiftalllist.append(shiftlst)
        anglealllist.append(anglelst)
        pcoall.append(pco)
        pnoall.append(pno)
    pcoall=np.array(pcoall)
    pnoall=np.array(pnoall)
    shiftalllist = np.array(shiftalllist)
    anglealllist = np.array(anglealllist)
    out_co.create_dataset('pattern',data=pcoall)
    out_no.create_dataset('pattern',data=pnoall)
    out_co.create_dataset('angle',data=anglealllist)
    out_no.create_dataset('angle',data=anglealllist)
    out_co.create_dataset('shift',data=shiftalllist)
    out_no.create_dataset('shift',data=shiftalllist)
    out_no.close()
    out_co.close()
    h.close()

for i in [1,2,5,10]:
    coherent(i,5000,sys.argv[1])
