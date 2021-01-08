"""Maximum across echoes to generate artifact mask."""

import numpy as np
import nibabel as nb

NII_NAME = '/home/faruk/Data/MESO_MEGRE_7T/SES03_SUB02/analysis/04_avg_phase_enc_axis/sub-02_350um-mag_RL_LR.nii.gz'

OUT_NAME = '/home/faruk/Data/MESO_MEGRE_7T/SES03_SUB02/analysis/04_avg_phase_enc_axis/sub-02_350um-mag_RL_LR_Tmax'

# =============================================================================
nii = nb.load(NII_NAME)
data = nii.get_data()

t_max = np.max(data, axis=3)

img = nb.Nifti1Image(t_max, affine=nii.affine)
nb.save(img, "{}.nii.gz".format(OUT_NAME))
