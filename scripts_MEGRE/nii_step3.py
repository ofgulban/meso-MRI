"""Average the same phase encoding axis data"""

import numpy as np
import nibabel as nb

# =============================================================================

# NII_NAMES = [
#     '/home/faruk/Data/ANALYSIS_MESO_MEGRE_7T/MESO_MEGRE_7T/SES04_SUB03/analysis/03_consistent_readout/sub-03_ses-01_RL.nii.gz',
#     '/home/faruk/Data/ANALYSIS_MESO_MEGRE_7T/MESO_MEGRE_7T/SES04_SUB03/analysis/03_consistent_readout/sub-03_ses-01_LR.nii.gz',
#     ]
# OUT_NAME = "/home/faruk/Data/ANALYSIS_MESO_MEGRE_7T/MESO_MEGRE_7T/SES04_SUB03/analysis/04_avg_phase_enc_axis/sub-03_ses-01_RL_LR"

# -----------------------------------------------------------------------------

NII_NAMES = [
    '/home/faruk/Data/ANALYSIS_MESO_MEGRE_7T/MESO_MEGRE_7T/SES04_SUB03/analysis/03_consistent_readout/sub-03_ses-01_AP.nii.gz',
    '/home/faruk/Data/ANALYSIS_MESO_MEGRE_7T/MESO_MEGRE_7T/SES04_SUB03/analysis/03_consistent_readout/sub-03_ses-01_PA.nii.gz',
    ]
OUT_NAME = "/home/faruk/Data/ANALYSIS_MESO_MEGRE_7T/MESO_MEGRE_7T/SES04_SUB03/analysis/04_avg_phase_enc_axis/sub-03_ses_01-AP_PA"

# =============================================================================

nii1 = nb.load(NII_NAMES[0])
nii2 = nb.load(NII_NAMES[1])

data1 = np.squeeze(np.asanyarray(nii1.dataobj))
data2 = np.squeeze(np.asanyarray(nii2.dataobj))

temp = (data1 + data2)/2.

# Save
img = nb.Nifti1Image(temp, affine=nii1.affine, header=nii1.header)
nb.save(img, '{}.nii.gz'.format(OUT_NAME))

print('Finished.')
