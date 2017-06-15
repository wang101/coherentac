import matplotlib.pyplot as plt
import pickle as pkl
import sys
import pdb
import h5py
import numpy as np

hstd = h5py.File('./h5corr/1co/corr1co_lstc0.h5')
h1 = h5py.File('./h5corr/10co/corr10co_lstc0.h5')
h2 = h5py.File('./h5corr/10no/corr10no_lstc0.h5')
acstd = hstd['corr'][()].mean(axis=0)
ac1 = h1['corr'][()]
ac2 = h2['corr'][()]
#ac1 = np.swapaxes(ac1,0,1)
#ac2 = np.swapaxes(ac2,0,1)
#ac1 : num,q,phi
start = 0
print(ac1.shape)
for n in range(20,21):
    cc1 = []
    cc2 = []
    print(ac1[:355][:][:].shape)
    for m in range(1,5000):
        cc1.append(np.corrcoef(np.ravel(acstd[start:]),np.ravel(ac1[:m,start:,:].mean(axis=0)))[0][1])
        cc2.append(np.corrcoef(np.ravel(acstd[start:]),np.ravel(ac2[:m,start:,:].mean(axis=0)))[0][1])
    plt.plot(range(len(cc1)),cc1)
    plt.plot(range(len(cc2)),cc2)
plt.show()
    #print cc
#ac = np.swapaxes(ac,0,2)
#print(ac.shape)
#for q in qs:
#    diffs = []
#    for n in range(1,5000):
#        diffs.append(np.average(ac[dphi][q][:n]))
#    plt.plot(range(len(diffs)),diffs)
#plt.show()
