"""Combine echoes for consistent phase encoding.

This script should be run after registration.
"""

import numpy as np
import nibabel as nb

# =============================================================================

# NII_NAMES = [
#     '/home/faruk/Data/ANALYSIS_MESO_MEGRE_7T/MESO_MEGRE_7T/SES04_SUB03/analysis/01_odd_even/sub-03_ses-01_run-01_RL_TE_1_3_5.nii.gz',
#     '/home/faruk/Data/ANALYSIS_MESO_MEGRE_7T/MESO_MEGRE_7T/SES04_SUB03/analysis/02_register/sub-03_ses-01_run-03_LR_TE_2_4_6_reg_RL_TE_1_3_5.nii.gz',
#     ]
# OUT_NAME = "/home/faruk/Data/ANALYSIS_MESO_MEGRE_7T/MESO_MEGRE_7T/SES04_SUB03/analysis/03_consistent_readout/sub-03_ses-01_RL"

# -----------------------------------------------------------------------------

# NII_NAMES = [
#     '/home/faruk/Data/ANALYSIS_MESO_MEGRE_7T/MESO_MEGRE_7T/SES04_SUB03/analysis/02_register/sub-03_ses-01_run-03_LR_TE_1_3_5_reg_RL_TE_2_4_6.nii.gz',
#     '/home/faruk/Data/ANALYSIS_MESO_MEGRE_7T/MESO_MEGRE_7T/SES04_SUB03/analysis/01_odd_even/sub-03_ses-01_run-01_RL_TE_2_4_6.nii.gz',
#     ]
# OUT_NAME = "/home/faruk/Data/ANALYSIS_MESO_MEGRE_7T/MESO_MEGRE_7T/SES04_SUB03/analysis/03_consistent_readout/sub-03_ses-01_LR"

# =============================================================================

# NII_NAMES = [
#     '/home/faruk/Data/ANALYSIS_MESO_MEGRE_7T/MESO_MEGRE_7T/SES04_SUB03/analysis/01_odd_even/sub-03_ses-01_run-02_AP_TE_1_3_5.nii.gz',
#     '/home/faruk/Data/ANALYSIS_MESO_MEGRE_7T/MESO_MEGRE_7T/SES04_SUB03/analysis/02_register/sub-03_ses-01_run-04_PA_TE_2_4_6_reg_AP_TE_1_3_5.nii.gz',
#     ]
# OUT_NAME = "/home/faruk/Data/ANALYSIS_MESO_MEGRE_7T/MESO_MEGRE_7T/SES04_SUB03/analysis/03_consistent_readout/sub-03_ses-01_AP"

# -----------------------------------------------------------------------------

NII_NAMES = [
    '/home/faruk/Data/ANALYSIS_MESO_MEGRE_7T/MESO_MEGRE_7T/SES04_SUB03/analysis/02_register/sub-03_ses-01_run-04_PA_TE_1_3_4_reg_AP_TE_2_4_6.nii.gz',
    '/home/faruk/Data/ANALYSIS_MESO_MEGRE_7T/MESO_MEGRE_7T/SES04_SUB03/analysis/01_odd_even/sub-03_ses-01_run-02_AP_TE_2_4_6.nii.gz',
    ]
OUT_NAME = "/home/faruk/Data/ANALYSIS_MESO_MEGRE_7T/MESO_MEGRE_7T/SES04_SUB03/analysis/03_consistent_readout/sub-03_ses-01_PA"

# =============================================================================

# Insert odd-even echoes orderly
nii1 = nb.load(NII_NAMES[0])
nii2 = nb.load(NII_NAMES[1])

data1 = np.squeeze(np.asanyarray(nii1.dataobj))
data2 = np.squeeze(np.asanyarray(nii2.dataobj))

dims = data1.shape
temp = np.zeros(dims[:-1] + (6,))

temp[..., 0::2] = data1
temp[..., 1::2] = data2

# Save
img = nb.Nifti1Image(temp, affine=nii1.affine, header=nii1.header)
nb.save(img, '{}.nii.gz'.format(OUT_NAME))

print('Finished.')
