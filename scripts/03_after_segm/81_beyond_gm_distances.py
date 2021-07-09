"""Measure cortical depths using LayNii LN2_LAYERS."""

import os
import subprocess
import numpy as np
import nibabel as nb

RIMS = [
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/segmentation/05_beyond_gm_prep/sub-05_ses-T2s_segm_rim_HG_RH_v02_domain-wm.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/segmentation/05_beyond_gm_prep/sub-05_ses-T2s_segm_rim_HG_LH_v02_domain-wm.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/segmentation/05_beyond_gm_prep/sub-05_ses-T2s_segm_rim_CS_RH_v02_domain-wm.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/segmentation/05_beyond_gm_prep/sub-05_ses-T2s_segm_rim_CS_LH_v02_domain-wm.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/segmentation/05_beyond_gm_prep/sub-05_ses-T2s_segm_rim_HG_RH_v02_domain-csf.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/segmentation/05_beyond_gm_prep/sub-05_ses-T2s_segm_rim_HG_LH_v02_domain-csf.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/segmentation/05_beyond_gm_prep/sub-05_ses-T2s_segm_rim_CS_RH_v02_domain-csf.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/segmentation/05_beyond_gm_prep/sub-05_ses-T2s_segm_rim_CS_LH_v02_domain-csf.nii.gz",
]

BORDERS = [
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/segmentation/05_beyond_gm_prep/sub-05_ses-T2s_segm_rim_HG_RH_v02_border-wm.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/segmentation/05_beyond_gm_prep/sub-05_ses-T2s_segm_rim_HG_LH_v02_border-wm.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/segmentation/05_beyond_gm_prep/sub-05_ses-T2s_segm_rim_CS_RH_v02_border-wm.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/segmentation/05_beyond_gm_prep/sub-05_ses-T2s_segm_rim_CS_LH_v02_border-wm.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/segmentation/05_beyond_gm_prep/sub-05_ses-T2s_segm_rim_HG_RH_v02_border-csf.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/segmentation/05_beyond_gm_prep/sub-05_ses-T2s_segm_rim_HG_LH_v02_border-csf.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/segmentation/05_beyond_gm_prep/sub-05_ses-T2s_segm_rim_CS_RH_v02_border-csf.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/segmentation/05_beyond_gm_prep/sub-05_ses-T2s_segm_rim_CS_LH_v02_border-csf.nii.gz",
]

OUTDIR = "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/segmentation/06_beyond_gm_distances"

# -----------------------------------------------------------------------------
# Output directory
if not os.path.exists(OUTDIR):
    os.makedirs(OUTDIR)
    print("  Output directory: {}\n".format(OUTDIR))

for i in range(len(RIMS)):
    rim = RIMS[i]
    border = BORDERS[i]

    # Determine output basename
    filename = os.path.basename(rim)
    basename, ext = filename.split(os.extsep, 1)
    outname = os.path.join(OUTDIR, "{}_distances.{}".format(basename, ext))

    # Layers and middle gray matter
    command = "/home/faruk/Git/LAYNII/LN2_GEODISTANCE "
    command += "-domain {} ".format(rim)
    command += "-init {} ".format(border)
    command += "-output {} ".format(outname)
    print(command)
    subprocess.run(command, shell=True)


print('Finished.\n')
