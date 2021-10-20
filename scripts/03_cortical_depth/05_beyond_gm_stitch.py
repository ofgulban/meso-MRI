"""Stitch collated distances for continuous distances."""

import os
import subprocess
import numpy as np
import nibabel as nb

INPUTS = [
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/segmentation/07_beyond_gm_collate/sub-05_ses-T2s_segm_rim_HG_RH_v02_beyond_gm_distances.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/segmentation/07_beyond_gm_collate/sub-05_ses-T2s_segm_rim_HG_LH_v02_beyond_gm_distances.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/segmentation/07_beyond_gm_collate/sub-05_ses-T2s_segm_rim_CS_RH_v02_beyond_gm_distances.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/segmentation/07_beyond_gm_collate/sub-05_ses-T2s_segm_rim_CS_LH_v02_beyond_gm_distances.nii.gz",
]

OUTDIR  = "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/segmentation/07_beyond_gm_collate"

# -----------------------------------------------------------------------------
# Output directory
if not os.path.exists(OUTDIR):
    os.makedirs(OUTDIR)
    print("  Output directory: {}\n".format(OUTDIR))

for i in range(len(INPUTS)):
    input = INPUTS[i]

    # Determine output basename
    filename = os.path.basename(input)
    basename, ext = filename.split(os.extsep, 1)
    outname = os.path.join(OUTDIR, "{}_smooth.{}".format(basename, ext))

    # Layers and middle gray matter
    command = "fslmaths "
    command += "{} ".format(input)
    command += "-s 0.35 "
    command += "{} ".format(outname)
    print(command)
    subprocess.run(command, shell=True)


print('Finished.\n')
