"""Polish segmentations through morphology and smoothing."""

import os
import nibabel as nb
import numpy as np
from scipy.ndimage import morphology, generate_binary_structure
from scipy.ndimage import gaussian_filter

FILE = '/media/faruk/Seagate Backup Plus Drive/DATA_MRI_NIFTI/derived/sub-05/T1_wholebrain/04_segmentation_reg_to_T2s/sub-05_ses-T2s_MP2RAGE_uni_segm_rim_reg_soi_HG_LH_v02_polished.nii.gz'

# Load data
nii = nb.load(FILE)
data = np.asarray(nii.dataobj)

# Separate tissues
mask = data > 0
gm = data == 1
wm = data == 2
cereb = gm + wm

struct = generate_binary_structure(3, 1)  # 1 jump neighbourbhood

# Polish white matter
wm = morphology.binary_dilation(wm, structure=struct, iterations=2)
wm = gaussian_filter(wm.astype(float), sigma=1)
wm = wm > 0.5
wm = morphology.binary_erosion(wm, structure=struct, iterations=2)

# Polish cerebrum
cereb = morphology.binary_erosion(cereb, structure=struct, iterations=1)
cereb = gaussian_filter(cereb.astype(float), sigma=1)
cereb = cereb > 0.5
cereb = morphology.binary_dilation(cereb, structure=struct, iterations=1)

# Composit output image
out = np.full(data.shape, 3)
out[cereb != 0] = 1
out[wm != 0] += 1
out *= mask

# Save as nifti
basename, ext = nii.get_filename().split(os.extsep, 1)
out = nb.Nifti1Image(out.astype(int), header=nii.header, affine=nii.affine)
nb.save(out, "{}_polished.{}".format(basename, ext))

print('Finished.')
