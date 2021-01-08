"""Sort multiple runs per echo."""

import numpy as np
import nibabel as nb

NII_NAMES = [
    '/home/faruk/Data/MESO_MEGRE_7T/SES03_SUB02/analysis/04_avg_phase_enc_axis/sub-02_350um-mag_RL_LR.nii.gz',
    '/home/faruk/Data/MESO_MEGRE_7T/SES03_SUB02/analysis/04_avg_phase_enc_axis/sub-02_350um-mag_AP_PA.nii.gz',
    ]

OUT_NAME = '/home/faruk/Data/MESO_MEGRE_7T/SES03_SUB02/analysis/05_sort_across_phase_enc_axes/sorted'

# Prepare data array
for i, nii_name in enumerate(NII_NAMES):
    nii = nb.load(nii_name)

    if i == 0:
        nr_files = len(NII_NAMES)
        temp = np.squeeze(nii.get_data())
        dims, temp = temp.shape, None
        temp = np.zeros(dims + (nr_files,))

    temp[..., i] = np.squeeze(nii.get_data())

# Sort
temp = np.sort(temp, axis=-1, kind='stable')

# Save sorted runs
for i, nii_name in enumerate(NII_NAMES):
    img = nb.Nifti1Image(np.squeeze(temp[..., i]),
                         affine=nii.affine, header=nii.header)
    nb.save(img, '{}_{}.nii.gz'.format(OUT_NAME, i))
