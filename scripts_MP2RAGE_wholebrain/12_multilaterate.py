"""Separate scoops of interest (SOI)."""

import os
import subprocess

RIMS = [
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/T1_wholebrain/05_layers_columns/HG_RH/sub-01_ses-T2s_MP2RAGE_uni_segm_rim_reg_HG_RH_v04.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/T1_wholebrain/05_layers_columns/HG_LH/sub-01_ses-T2s_MP2RAGE_uni_segm_rim_reg_HG_LH_v04.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/T1_wholebrain/05_layers_columns/CS_RH/sub-01_ses-T2s_MP2RAGE_uni_segm_rim_reg_CS_RH_v04.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/T1_wholebrain/05_layers_columns/CS_LH/sub-01_ses-T2s_MP2RAGE_uni_segm_rim_reg_CS_LH_v04.nii.gz",
]

CENTROIDS = [
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/T1_wholebrain/05_layers_columns/HG_RH/sub-01_ses-T2s_MP2RAGE_uni_segm_rim_reg_HG_RH_v04_midGM_equidist_centroid.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/T1_wholebrain/05_layers_columns/HG_LH/sub-01_ses-T2s_MP2RAGE_uni_segm_rim_reg_HG_LH_v04_midGM_equidist_centroid.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/T1_wholebrain/05_layers_columns/CS_RH/sub-01_ses-T2s_MP2RAGE_uni_segm_rim_reg_CS_RH_v04_midGM_equidist_centroid.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/T1_wholebrain/05_layers_columns/CS_LH/sub-01_ses-T2s_MP2RAGE_uni_segm_rim_reg_CS_LH_v04_midGM_equidist_centroid.nii.gz",
]

OUTDIR = "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/T1_wholebrain/06_multilaterate/"

# -----------------------------------------------------------------------------
# Output directory
if not os.path.exists(OUTDIR):
    os.makedirs(OUTDIR)
    print("  Output directory: {}\n".format(out_target))

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
