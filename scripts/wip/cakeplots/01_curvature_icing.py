"""Overlay median bnned curvature as the top layer."""

import os
import sys
import numpy as np
import nibabel as nb

# Icing (e.g. binned curvature)
FILE1 = "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-04/cakeplots/sub-04_ses-T2s_segm_rim_CS_LH_v02_borderized_multilaterate_perimeter_chunk_curvature_binned_flat_400x400_voronoi_median_projection_customized.nii.gz"
# Values (e.g. T2*)
FILE2 = "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-04/flattening/sub-04_ses-T2s_segm_rim_CS_LH_v02_borderized_multilaterate_perimeter_chunk_T2star_flat_400x400_voronoi.nii.gz"

OUTDIR = "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-04/cakeplots"

MIN, MAX = 20, 45

# =============================================================================
# Output directory
if not os.path.exists(OUTDIR):
    os.makedirs(OUTDIR)
    print("  Output directory: {}\n".format(OUTDIR))

# =============================================================================
# Get data
nii1 = nb.load(FILE1)
curv = np.squeeze(nii1.get_fdata())

nii2 = nb.load(FILE2)
data = nii2.get_fdata()

# -----------------------------------------------------------------------------
# Truncate data range (useful for visualization later)
idx = data!= 0
temp = data[idx]
temp[temp > MAX] = MAX
temp[temp < MIN] = MIN
data[idx] = temp

# Match binned curvature with min max of the values
idx = curv != 0
temp = curv[idx]
temp /= 2  # Pull to 0-1 range
temp *= MAX - MIN
temp += MIN
curv[idx] = temp

# -----------------------------------------------------------------------------
# Smooth sides of the cake (fix projection overfills)
data[~idx, :] = 0

# -----------------------------------------------------------------------------
# Swap top layer with curvature
data[:, :, -1] = curv

# Determine output basename
filename = os.path.basename(FILE2)
basename, ext = filename.split(os.extsep, 1)
outname = os.path.join(OUTDIR, "{}_curv_icing.{}".format(basename, ext))

# Save as nifti
out = nb.Nifti1Image(data, affine=nii2.affine, header=nii2.header)
nb.save(out, outname)

print("Finished.")
