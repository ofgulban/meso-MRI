"""Separate scoops of interest (SOI)."""

import os
import subprocess

RIMS = [
    "/home/faruk/Documents/temp_segment/sub-01/05_layers_columns/HG_RH/sub-01_ses-T2s_MP2RAGE_uni_segm_rim_reg_HG_RH_v04.nii.gz",
    "/home/faruk/Documents/temp_segment/sub-01/05_layers_columns/HG_LH/sub-01_ses-T2s_MP2RAGE_uni_segm_rim_reg_HG_LH_v04.nii.gz",
    "/home/faruk/Documents/temp_segment/sub-01/05_layers_columns/CS_RH/sub-01_ses-T2s_MP2RAGE_uni_segm_rim_reg_CS_RH_v04.nii.gz",
    "/home/faruk/Documents/temp_segment/sub-01/05_layers_columns/CS_LH/sub-01_ses-T2s_MP2RAGE_uni_segm_rim_reg_CS_LH_v04.nii.gz",
]

# -----------------------------------------------------------------------------
for i in range(4):
    rim = RIMS[i]
    basename, ext = rim.split(os.extsep, 1)

    # Layers and middle gray matter
    command = "/home/faruk/Git/LAYNII/LN2_LAYERS "
    command += "-rim {} ".format(rim)
    command += "-equivol "
    command += "-nr_layers 5 "
    command += "-curvature "
    print(command)
    subprocess.run(command, shell=True)

    # Connected cluster threshold
    command = "python /home/faruk/Git/phd-mu/Python_Scripts/connected_clusters.py "
    command += "{}_midGM_equidist.nii.gz ".format(basename)
    command += "--cluster_size 100000 "
    print(command)
    subprocess.run(command, shell=True)


print('Finished.')
