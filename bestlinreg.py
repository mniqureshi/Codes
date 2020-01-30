import numpy as np
import nibabel as nib
import os
import subprocess
import pandas

#module load minc-toolkit/1.0.01-new
#module load python/3.6.3


# _____________Function to resample source file to the target file______________________________________________
def mrs(source, target, rsource):
    process = subprocess.run(['mincresample', "-like", target, source, rsource])
    
#______________Function to compute normalized cross correlation between source and traget files________________
def NCC(source, target):
    i1 = nib.load(source); im1 = i1.get_data()
    i2 = nib.load(target); im2 = i2.get_data()
    product = np.mean((im1 - im1.mean()) * (im2 - im2.mean())) #Zero-normalized cross-correlation (ZNCC)
    stds = im1.std() * im2.std()
    if stds == 0:
        return 0
    else:
        product /= stds
        return product

#_____________Function to perform linear registration between source and target__________________________________
def bestlinreg(source, target, output, xfm, metric):
    result = []
    process = subprocess.run(['bestlinreg_s2' ,source, target, xfm, metric, output,'-clobber'], stdout=subprocess.PIPE, universal_newlines=True)
    output = process.stdout
    init = []
    for item in output.split("\n"):
            if "Initial objective function val = " in item:
                    obj = item.strip()
                    ob=obj.split("=")
                    init.append(ob[1])
            if "Final objective function value = " in item:
                    obj1 = item.strip()
                    ob1=obj1.split("=")
    [init.split('\t', 1)[0] for init in init]
    return [init[0],ob1[1]]

#_________________Declear Inputs___________________________________________________________________________________
MPRAGE  = 'CISC-12STX_011-HSC-1_pt_00183_v07_t1gMPR.mnc.gz'
PD      = 'CISC-12STX_011-HSC-1_pt_00183_v07_pdw.mnc.gz'
T2      = 'CISC-12STX_011-HSC-1_pt_00183_v07_t2w.mnc.gz'
MTOFF   = 'CISC-12STX_011-HSC-1_pt_00183_v07_mtOFF.mnc.gz'
MTON    = 'CISC-12STX_011-HSC-1_pt_00183_v07_mtON.mnc.gz'
MTR     = 'CISC-12STX_011-HSC-1_pt_00183_v07_MTR.mnc.gz'

#________________________Process____________________________________________________________________________________
mod = [PD, T2, MTOFF, MTON, MTR]
fun = ["-xcorr","-mi"]
MM  = []
for i in mod:
    for j in fun:
        rs = i.split(".mnc.gz")
        new = (rs[0]+'_resample.mnc')
        registered = (rs[0]+'-MPRAGE'+j+'.mnc')
        transform = (rs[0]+'-MPRAGE'+j+'.xfm')
        mrs(i,MPRAGE,new)
        ncb = NCC(new,MPRAGE)
        res = bestlinreg(i,MPRAGE,registered,transform,j)
        nca = NCC(registered,MPRAGE)
        k = j,ncb,nca,res
        MM.append(k)

#________________________Dispaly output in tabular form
print(pandas.DataFrame(MM, columns=['Cost', 'Initial NCC', 'Final NCC','Initial and Final Objective'], index=['PD', 'PD', 'T2', 'T2', 'MTOFF', 'MTOFF', 'MTON','MTON', 'MTR','MTR']))


