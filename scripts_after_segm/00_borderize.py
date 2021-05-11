"""Prepare rim files with borders."""

import os
import subprocess
import nibabel as nb
import numpy as np

RIMS = [
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/segmentation/00_segmentation/HG_RH/sub-01_ses-T2s_segm_rim_HG_RH_v02.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/segmentation/00_segmentation/HG_LH/sub-01_ses-T2s_segm_rim_HG_LH_v02.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/segmentation/00_segmentation/CS_RH/sub-01_ses-T2s_segm_rim_CS_RH_v02.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/segmentation/00_segmentation/CS_LH/sub-01_ses-T2s_segm_rim_CS_LH_v02.nii.gz",
]

OUTDIR = "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/segmentation/01_rim_prep"

# -----------------------------------------------------------------------------
# Output directory
if not os.path.exists(OUTDIR):
    os.makedirs(OUTDIR)
    print("  Output directory: {}\n".format(OUTDIR))

for i in range(4):
    rim = RIMS[i]

    # Determine output basename
    filename = os.path.basename(rim)
    basename, ext = filename.split(os.extsep, 1)
    outname = os.path.join(OUTDIR, "{}_borders.{}".format(basename, ext))

    # Layers and middle gray matter
    command = "/home/faruk/Git/LAYNII/LN2_BORDERIZE "
    command += "-rim {} ".format(rim)
    command += "-output {} ".format(outname)
    print(command)
    subprocess.run(command, shell=True)

    # -------------------------------------------------------------------------
    # Composite initial rim file with borders
    print("  Compositing borders and pure gray matter...")
    nii1 = nb.load(rim)
    data1 = np.asarray(nii1.dataobj)
    nii2 = nb.load(outname)
    data2 = np.asarray(nii2.dataobj)
    data2[data1 == 3] = 3  # gray matter

    outname = os.path.join(OUTDIR, "{}_borderized.{}".format(basename, ext))
    img = nb.Nifti1Image(data2, affine=nii1.affine, header=nii1.header)
    nb.save(img, outname)

print('Finished.\n')
