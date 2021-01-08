"""Smartly average across 90 degree phase encoded images."""

import numpy as np
import nibabel as nb

NII_NAMES = [
    '/home/faruk/Data/MESO_MEGRE_7T/SES03_SUB02/analysis/05_sort_across_phase_enc_axes/sorted_0.nii.gz',
    '/home/faruk/Data/MESO_MEGRE_7T/SES03_SUB02/analysis/05_sort_across_phase_enc_axes/sorted_1.nii.gz',
    ]

MASK = "/media/Data_Drive/ISILON/503_VESSELS_7T_MESO/05_consistent_phase_enc_avg/sorted_Tmax_diff_thr1k_bin_close.nii.gz"

OUT_NAME = '/media/Data_Drive/ISILON/503_VESSELS_7T_MESO/05_consistent_phase_enc_avg/composite'

# =============================================================================
nii1 = nb.load(NII_NAMES[0])
nii2 = nb.load(NII_NAMES[1])

data1 = nii1.get_data()
data2 = nii2.get_data()

avg = (data1 + data2) / 2

# Mask stuff
msk = ((nb.load(MASK)).get_data()).astype(np.int)
idx = np.where(msk)

# Selective average with min
avg[idx[0], idx[1], idx[2], :] = data1[idx[0], idx[1], idx[2], :]
img = nb.Nifti1Image(avg, affine=nii1.affine)
nb.save(img, "{}_min.nii.gz".format(OUT_NAME))

# Selective average with max
avg[idx[0], idx[1], idx[2], :] = data2[idx[0], idx[1], idx[2], :]
img = nb.Nifti1Image(avg, affine=nii1.affine)
nb.save(img, "{}_max.nii.gz".format(OUT_NAME))
