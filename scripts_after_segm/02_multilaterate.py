"""Separate scoops of interest (SOI)."""

import os
import subprocess

RIMS = [
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-05/T1_wholebrain/04_segmentation/HG_RH/sub-05_ses-T2s_segm_rim_HG_RH_v02.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-05/T1_wholebrain/04_segmentation/HG_LH/sub-05_ses-T2s_segm_rim_HG_LH_v02.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-05/T1_wholebrain/04_segmentation/CS_RH/sub-05_ses-T2s_segm_rim_CS_RH_v02.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-05/T1_wholebrain/04_segmentation/CS_LH/sub-05_ses-T2s_segm_rim_CS_LH_v02.nii.gz",
]

CENTROIDS = [
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-05/T1_wholebrain/05_layers/sub-05_ses-T2s_segm_rim_HG_RH_v02_midGM_equidist_centroid.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-05/T1_wholebrain/05_layers/sub-05_ses-T2s_segm_rim_HG_LH_v02_midGM_equidist_centroid.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-05/T1_wholebrain/05_layers/sub-05_ses-T2s_segm_rim_CS_RH_v02_midGM_equidist_centroid.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-05/T1_wholebrain/05_layers/sub-05_ses-T2s_segm_rim_CS_LH_v02_midGM_equidist_centroid.nii.gz",
]

OUTDIR = "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-05/T1_wholebrain/06_multilaterate/"

# -----------------------------------------------------------------------------
# Output directory
if not os.path.exists(OUTDIR):
    os.makedirs(OUTDIR)
    print("  Output directory: {}\n".format(OUTDIR))

for i in range(len(RIMS)):
    rim = RIMS[i]
    centroid = CENTROIDS[i]

    # Determine output basename
    filename = os.path.basename(rim)
    basename, ext = filename.split(os.extsep, 1)
    outname = os.path.join(OUTDIR, "{}_multilaterate.{} ".format(basename, ext))

    # Layers and middle gray matter
    command = "/home/faruk/Git/LAYNII/LN2_MULTILATERATE "
    command += "-rim {} ".format(rim)
    command += "-control_points {} ".format(centroid)
    command += "-radius 15 "
    command += "-output {} ".format(outname)
    print(command)
    subprocess.run(command, shell=True)

print('Finished.\n')
