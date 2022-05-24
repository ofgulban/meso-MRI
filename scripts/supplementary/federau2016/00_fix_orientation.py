"""GRE and TSE images are flipped compared to MP2RAGE UNI image.py

Therefore the data arrays must be flipped over along right-left axis before
further analyses. Here I assumed MP2RAGE image ahs the right right left
orientation.
"""

import os
import nibabel as nb
import numpy as np

# =============================================================================
NII_NAMES = [
    "/home/faruk/data2/DATA_MRI_NIFTI/data-federau2016/source/sub-federau2016_GRE380.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/data-federau2016/source/sub-federau2016_TSE380.nii.gz",
    ]

OUTDIR = "/home/faruk/data2/DATA_MRI_NIFTI/data-federau2016/source"

# =============================================================================
# Output directory
if not os.path.exists(OUTDIR):
    os.makedirs(OUTDIR)
print("  Output directory: {}\n".format(OUTDIR))

for i, f in enumerate(NII_NAMES):
    # Prepare output
    basename, ext = f.split(os.extsep, 1)
    basename = os.path.basename(basename)
    out_file = os.path.join(OUTDIR, "{}_flipX.nii.gz".format(basename))

    # Flip data array along RL-LR axis
    nii = nb.load(f)
    data = np.asarray(nii.dataobj)
    data = data[::-1, :, :]
    img = nb.Nifti1Image(data, header=nii.header, affine=nii.affine)
    nb.save(img, out_file)

print("Finished.")
