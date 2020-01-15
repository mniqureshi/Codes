import nibabel as nib
import matplotlib.pyplot as plt
import pylab
import numpy as np
MPRAGE = nib.load('/input file1 path')

MT_OFF = nib.load('/input file2 path')
pylab.figure('image'); pylab.clf(); slc=40
pylab.subplot(131); pylab.imshow(MPRAGE.get_data()[slc],vmin=0); pylab.title('MPRAGE'); pylab.colorbar()
pylab.subplot(132); pylab.imshow(MT_OFF.get_data()[slc],vmin=0); pylab.title('MT_OFF'); pylab.colorbar()

def NCC(im1, im2):
    product = np.mean((im1 - im1.mean()) * (im2 - im2.mean())) #Zero-normalized cross-correlation (ZNCC)
    #product = np.mean(im1  * im2)#Normalized cross-correlation (NCC)
    stds = im1.std() * im2.std()
    if stds == 0:
        return 0
    else:
        product /= stds
        return product

print ("MPRAGE shape =", MPRAGE.shape)
print ("MT_OFF shape =", MT_OFF.shape)
d = 1
correlation = np.zeros_like(MPRAGE.get_data())
for k in range(d, MPRAGE.shape[0] - (d + 1)):
    slicemp = MPRAGE.get_data()[k]
    slicemt = MT_OFF.get_data()[k]

    for i in range(d, MPRAGE.shape[1] - (d + 1)):
        for j in range(d, MPRAGE.shape[2] - (d + 1)):
            print(slicemp.shape,k)
            print(k,i,j)
            correlation[k,i,j]=NCC(slicemp[i - d: i + d + 1, j - d: j + d + 1],slicemt[i - d: i + d + 1, j - d: j + d + 1])
            print(correlation.shape)

output = nib.Nifti2Image(correlation,MPRAGE.affine,header=MPRAGE.header)
nib.save(output,'correlate.nii')
pylab.subplot(133); pylab.imshow(correlation[40]); pylab.title('Correlation'); pylab.colorbar()
plt.show()
