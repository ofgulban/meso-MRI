"""Push upwards chunks of cake like a wedding cake."""

import os
import numpy as np
import nibabel as nb

# Scalars (e.g. T2*)
FILE1 = "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-04/cakeplots/sub-04_ses-T2s_segm_rim_CS_LH_v02_borderized_multilaterate_perimeter_chunk_T2star_flat_400x400_voronoi_curv_icing.nii.gz"
# Norm
FILE2 = "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-04/flattening/sub-04_ses-T2s_segm_rim_CS_LH_v02_borderized_multilaterate_perimeter_chunk_norm_L2_flat_400x400_voronoi.nii.gz"

OUTDIR = "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-04/cakeplots/"

NR_CAKE_LAYERS = 2

# -----------------------------------------------------------------------------
nii1 = nb.load(FILE1)
dims = nii1.shape
data = nii1.get_fdata()

# Quantize norm
norm = nb.load(FILE2).get_fdata()
norm /= norm.max()
norm *= NR_CAKE_LAYERS
norm = np.ceil(norm).astype("int")

# Make space on z axis for cake layers using an extra dimension
new = np.zeros((dims[0], dims[1], NR_CAKE_LAYERS, dims[2]))

# Elevate norm bins center to outwards
nr_layers = dims[2]
for i, j in enumerate(range(NR_CAKE_LAYERS, 0, -1)):
    temp = np.zeros(dims)
    temp[norm == j] = data[norm == j]
    new[:, :, i, :] = temp

# Flatten the extra dimension onto 3rd
new = new.reshape((dims[0], dims[1], NR_CAKE_LAYERS * dims[2]))

# -----------------------------------------------------------------------------
# Determine output basename
filename = os.path.basename(FILE1)
basename, ext = filename.split(os.extsep, 1)
outname = os.path.join(OUTDIR, "{}_cake.{}".format(basename, ext))

# Save as nifti
out = nb.Nifti1Image(new, affine=nii1.affine, header=nii1.header)
nb.save(out, outname)

print("Finished.")
