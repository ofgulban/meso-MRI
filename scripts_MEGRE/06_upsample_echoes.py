"""Upsample echos."""

import os
import subprocess
import numpy as np
import nibabel as nb

# =============================================================================
NII_NAMES = [
    '/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/05_split_echoes/sub-23_ses-T2s_run-01_dir-AP_part-mag_MEGRE_crop_echo1.nii.gz',
    '/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/05_split_echoes/sub-23_ses-T2s_run-01_dir-AP_part-mag_MEGRE_crop_echo2.nii.gz',
    '/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/05_split_echoes/sub-23_ses-T2s_run-01_dir-AP_part-mag_MEGRE_crop_echo3.nii.gz',
    '/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/05_split_echoes/sub-23_ses-T2s_run-01_dir-AP_part-mag_MEGRE_crop_echo4.nii.gz',
    '/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/05_split_echoes/sub-23_ses-T2s_run-01_dir-AP_part-mag_MEGRE_crop_echo5.nii.gz',
    '/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/05_split_echoes/sub-23_ses-T2s_run-01_dir-AP_part-mag_MEGRE_crop_echo6.nii.gz',
    '/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/05_split_echoes/sub-23_ses-T2s_run-02_dir-RL_part-mag_MEGRE_crop_echo1.nii.gz',
    '/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/05_split_echoes/sub-23_ses-T2s_run-02_dir-RL_part-mag_MEGRE_crop_echo2.nii.gz',
    '/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/05_split_echoes/sub-23_ses-T2s_run-02_dir-RL_part-mag_MEGRE_crop_echo3.nii.gz',
    '/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/05_split_echoes/sub-23_ses-T2s_run-02_dir-RL_part-mag_MEGRE_crop_echo4.nii.gz',
    '/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/05_split_echoes/sub-23_ses-T2s_run-02_dir-RL_part-mag_MEGRE_crop_echo5.nii.gz',
    '/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/05_split_echoes/sub-23_ses-T2s_run-02_dir-RL_part-mag_MEGRE_crop_echo6.nii.gz',
    '/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/05_split_echoes/sub-23_ses-T2s_run-03_dir-PA_part-mag_MEGRE_crop_echo1.nii.gz',
    '/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/05_split_echoes/sub-23_ses-T2s_run-03_dir-PA_part-mag_MEGRE_crop_echo2.nii.gz',
    '/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/05_split_echoes/sub-23_ses-T2s_run-03_dir-PA_part-mag_MEGRE_crop_echo3.nii.gz',
    '/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/05_split_echoes/sub-23_ses-T2s_run-03_dir-PA_part-mag_MEGRE_crop_echo4.nii.gz',
    '/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/05_split_echoes/sub-23_ses-T2s_run-03_dir-PA_part-mag_MEGRE_crop_echo5.nii.gz',
    '/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/05_split_echoes/sub-23_ses-T2s_run-03_dir-PA_part-mag_MEGRE_crop_echo6.nii.gz',
    '/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/05_split_echoes/sub-23_ses-T2s_run-04_dir-LR_part-mag_MEGRE_crop_echo1.nii.gz',
    '/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/05_split_echoes/sub-23_ses-T2s_run-04_dir-LR_part-mag_MEGRE_crop_echo2.nii.gz',
    '/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/05_split_echoes/sub-23_ses-T2s_run-04_dir-LR_part-mag_MEGRE_crop_echo3.nii.gz',
    '/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/05_split_echoes/sub-23_ses-T2s_run-04_dir-LR_part-mag_MEGRE_crop_echo4.nii.gz',
    '/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/05_split_echoes/sub-23_ses-T2s_run-04_dir-LR_part-mag_MEGRE_crop_echo5.nii.gz',
    '/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/05_split_echoes/sub-23_ses-T2s_run-04_dir-LR_part-mag_MEGRE_crop_echo6.nii.gz',
    ]

OUTDIR = "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-23/T2s/06_upsample_echos"

# =============================================================================
print("Step_06: Upsample echos.")

# Output directory
if not os.path.exists(OUTDIR):
    os.makedirs(OUTDIR)
print("  Output directory: {}\n".format(OUTDIR))

for i, f in enumerate(NII_NAMES):
    print("  Processing file {}...".format(i+1))
    # Prepare output
    basename, ext = f.split(os.extsep, 1)
    basename = os.path.basename(basename)
    out_file = os.path.join(OUTDIR, "{}_ups2X.nii.gz".format(basename))

    # Prepare command
    command1 = "c3d {} ".format(f)
    command1 += "-interpolation Cubic "
    command1 += "-resample 200% "
    command1 += "-o {}".format(out_file)
    # Execute command
    subprocess.run(command1, shell=True)

print('\n\nFinished.')
