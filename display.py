import nibabel as nib
import matplotlib.pyplot as plt
import pylab
import numpy as np


def QCplot(MPRAGE,MTR,DM):
    
    MPRAGE = nib.load(MPRAGE)
    MTR = nib.load(MTR)
    DM = nib.load(DM)
    
    pylab.figure('image'); pylab.clf(); slc=150
    pylab.subplot(331); pylab.imshow(MPRAGE.get_data()[slc,:,:],vmin=0); pylab.title('MPRAGE_FS'); pylab.colorbar();pylab.contour(DM.get_data()[slc,:,:],colors=['r'],alpha=0.5,linewidths=0.5,origin='lower')
    pylab.subplot(332); pylab.imshow(MPRAGE.get_data()[:,slc,:],vmin=0); pylab.colorbar();pylab.contour(DM.get_data()[:,slc,:],colors=['r'],alpha=0.5,linewidths=0.5,origin='lower')
    pylab.subplot(333); pylab.imshow(MPRAGE.get_data()[:,:,slc-30],vmin=0); pylab.colorbar();pylab.contour(DM.get_data()[:,:,slc-30],colors=['r'],alpha=0.5,linewidths=0.5,origin='lower')


    pylab.subplot(334); pylab.imshow(MTR.get_data()[slc,:,:],vmin=0); pylab.title('MTR'); pylab.colorbar();pylab.contour(DM.get_data()[slc,:,:],colors=['r'],alpha=0.5,linewidths=0.5,origin='lower')
    pylab.subplot(335); pylab.imshow(MTR.get_data()[:,slc,:],vmin=0); pylab.colorbar();pylab.contour(DM.get_data()[:,slc,:],colors=['r'],alpha=0.5,linewidths=0.5,origin='lower')
    pylab.subplot(336); pylab.imshow(MTR.get_data()[:,:,slc-30],vmin=0); pylab.colorbar();pylab.contour(DM.get_data()[:,:,slc-30],colors=['r'],alpha=0.5,linewidths=0.5,origin='lower')

    counts, bins = np.histogram(MPRAGE.get_data())
    pylab.subplot(337); plt.hist(bins[:-1], bins, weights=counts); pylab.colorbar();pylab.title('MPRAGE')

    counts, bins = np.histogram(MTR.get_data())
    pylab.subplot(338); plt.hist(bins[:-1], bins, weights=counts); pylab.colorbar();pylab.title('MTR')
        
    counts, bins = np.histogram(DM.get_data())
    pylab.subplot(339); plt.hist(bins[:-1], bins, weights=counts); pylab.colorbar();pylab.title('DD Mask')
    plt.show()

MPRAGE = '/Volumes/glongoni/Montreal_structrural_native/HAM-1_pt_00011_v10.nii'
#MPRAGE = '/Volumes/glongoni/New_Montreal/002-HAM-1/pt_00011/v10/ResampleToStx/1.0.0/CISC-12STX_002-HAM-1_pt_00011_v10_t1gMPR_ISPC-stx152iso.mnc'
MTR = '/Volumes/glongoni/New_Montreal/002-HAM-1/pt_00011/v10/ResampleToStx/1.0.0/CISC-12STX_002-HAM-1_pt_00011_v10_MTR_ISPC-stx152iso.mnc'
Dmask = '/Volumes/glongoni/Montreal_structrural_native/HAM-1_pt_00011_v10.2D.nii'
QCplot(MPRAGE,MTR,Dmask)
