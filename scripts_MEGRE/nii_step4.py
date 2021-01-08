"""Compobine for flow artifact mitigated average (composite) image."""

import os
import numpy as np
import nibabel as nb

NII_NAMES = [
    '/home/faruk/Data/ANALYSIS_MESO_MEGRE_7T/MESO_MEGRE_7T/SES03_SUB02/analysis/04_avg_phase_enc_axis/sub-02_ses-01_RL_LR.nii.gz',
    '/home/faruk/Data/ANALYSIS_MESO_MEGRE_7T/MESO_MEGRE_7T/SES03_SUB02/analysis/04_avg_phase_enc_axis/sub-02_ses-01_AP_PA_reg_RL_LR.nii.gz'
    ]

# =============================================================================
nii1 = nb.load(NII_NAMES[0])
nii2 = nb.load(NII_NAMES[1])

data1 = np.squeeze(nii1.get_fdata())
data2 = np.squeeze(nii2.get_fdata())

diff = data1 - data2

idx_neg = diff < 0
idx_pos = diff > 0

data1[idx_pos] -= diff[idx_pos]
data2[idx_neg] += diff[idx_neg]

# out_name = nii1.get_filename().split(os.extsep, 1)[0]
# img = nb.Nifti1Image(data1, affine=nii1.affine)
# nb.save(img, "{}_fix.nii.gz".format(out_name))
#
# out_name = nii2.get_filename().split(os.extsep, 1)[0]
# img = nb.Nifti1Image(data2, affine=nii2.affine)
# nb.save(img, "{}_fix.nii.gz".format(out_name))

# Average
data1 += data2
data1 /= 2.

# Save
out_name = nii1.get_filename().split(os.extsep, 1)[0]
img = nb.Nifti1Image(data1, affine=nii1.affine)
nb.save(img, "{}_flow_artifact_mitigated_avg.nii.gz".format(out_name))

print('Finished.')
