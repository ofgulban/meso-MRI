"""Resample to 0.7 iso to be able to use BrainVoyager DNN segmentation."""

import os
import subprocess
import numpy as np
import nibabel as nb

# =============================================================================
NII_NAMES = [
    '/home/faruk/data/DATA_MRI_NIFTI/src/sub-01_ses-T2s/MP2RAGE_650micron/sub-01_ses-T2s_MP2RAGE_inv1.nii.gz',
    '/home/faruk/data/DATA_MRI_NIFTI/src/sub-01_ses-T2s/MP2RAGE_650micron/sub-01_ses-T2s_MP2RAGE_inv2.nii.gz',
    '/home/faruk/data/DATA_MRI_NIFTI/src/sub-01_ses-T2s/MP2RAGE_650micron/sub-01_ses-T2s_MP2RAGE_uni.nii.gz',
    '/home/faruk/data/DATA_MRI_NIFTI/src/sub-01_ses-T2s/MP2RAGE_650micron/sub-01_ses-T2s_MP2RAGE_T1.nii.gz',
    ]

OUTDIR = "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/T1_wholebrain/00_resample_to_pt7/"

# =============================================================================
print("Step_00: Resample to 0.7 mm iso.")

# Output directory
if not os.path.exists(OUTDIR):
    os.makedirs(OUTDIR)
print("  Output directory: {}\n".format(OUTDIR))
# -----------------------------------------------------------------------------

# Resample
for f in NII_NAMES:
    # Prepare output
    basename, ext = f.split(os.extsep, 1)
    basename = os.path.basename(basename)
    out_file1 = os.path.join(OUTDIR, "{}_pt7.nii.gz".format(basename))

    # Prepare command
    command1 = "c3d {} ".format(f)
    command1 += "-interpolation Cubic "
    command1 += "-resample-mm 0.7x0.7x0.7mm "
    command1 += "-o {}".format(out_file1)
    # Execute command
    subprocess.run(command1, shell=True)

    # -------------------------------------------------------------------------
    # Zero-pad to reframe into BV DNN applicable array shape
    nii = nb.load(out_file1)
    data = np.asarray(nii.dataobj)
    source_dims = data.shape
    target_dims = (320, 320, 224)
    print("Source shape: {}".format(source_dims))
    print("Target shape: {}".format(target_dims))

    new_data = np.zeros(target_dims)
    # Find x range
    if source_dims[0] < target_dims[0]:
        diff = int(target_dims[0] - source_dims[0])
        idx_x_start = diff // 2 + 1
        if diff % 2 == 0:  # even
            idx_x_end = target_dims[0] - (diff // 2)
        else:  # odd
            idx_x_end = target_dims[0] - (diff // 2)

    # Find y range
    if source_dims[1] < target_dims[1]:
        diff = int(target_dims[1] - source_dims[1])
        idx_y_start = diff // 2 + 1
        if diff % 2 == 0:  # even
            idx_y_end = target_dims[1] - (diff // 2)
        else:  # odd
            idx_y_end = target_dims[1] - (diff // 2)

    # Find z range
    if source_dims[2] < target_dims[2]:
        diff = int(target_dims[2] - source_dims[2])
        idx_z_start = diff // 2 + 1
        if diff % 2 == 0:  # even
            idx_z_end = target_dims[2] - (diff // 2)
        else:  # odd
            idx_z_end = target_dims[2] - (diff // 2)


    print("  x start-end: {} | {}".format(idx_x_start, idx_x_end))
    print("  y start-end: {} | {}".format(idx_y_start, idx_y_end))
    print("  z start-end: {} | {}".format(idx_z_start, idx_z_end))
    print("  x range: {}".format(idx_x_end - idx_x_start))
    print("  y range: {}".format(idx_y_end - idx_y_start))
    print("  z range: {}".format(idx_z_end - idx_z_start))

    # Zero-pad input array
    new_data[idx_x_start:idx_x_end,
             idx_y_start:idx_y_end,
             idx_z_start:idx_z_end] = data
    out_file2 = os.path.join(OUTDIR, "{}_pt7_reframed.nii.gz".format(basename))
    img = nb.Nifti1Image(new_data, affine=nii.affine)
    nb.save(img, out_file2)

print('\n\nFinished.')
