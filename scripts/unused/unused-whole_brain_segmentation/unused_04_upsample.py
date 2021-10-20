"""Upsample images."""

import os
import subprocess
import numpy as np
import nibabel as nb

# =============================================================================
NII_NAMES = [
    '/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/T1_wholebrain/01_crop/sub-01_ses-T2s_MP2RAGE_inv1_crop.nii.gz',
    '/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/T1_wholebrain/01_crop/sub-01_ses-T2s_MP2RAGE_inv2_crop.nii.gz',
    '/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/T1_wholebrain/01_crop/sub-01_ses-T2s_MP2RAGE_uni_crop.nii.gz',
    '/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/T1_wholebrain/01_crop/sub-01_ses-T2s_MP2RAGE_T1_crop.nii.gz',
    ]

OUTDIR = "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/T1_wholebrain/02_upsample"

# =============================================================================
print("Step_04: Upsample.")

# Output directory
if not os.path.exists(OUTDIR):
    os.makedirs(OUTDIR)
print("  Output directory: {}\n".format(OUTDIR))

for i, f in enumerate(NII_NAMES):
    print("  Processing file {}...".format(i+1))
    # Prepare output
    basename, ext = f.split(os.extsep, 1)
    basename = os.path.basename(basename)
    out_file = os.path.join(OUTDIR, "{}_ups350um.nii.gz".format(basename))

    # Prepare command
    command1 = "c3d {} ".format(f)
    command1 += "-interpolation Cubic "
    command1 += "-resample-mm 0.35x0.35x0.35mm "
    command1 += "-o {}".format(out_file)
    # Execute command
    subprocess.run(command1, shell=True)

print('\n\nFinished.')
