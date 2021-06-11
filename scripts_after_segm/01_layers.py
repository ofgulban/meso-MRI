"""Measure cortical depths using LayNii LN2_LAYERS."""

import os
import subprocess

RIMS = [
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-01/segmentation/01_rim_prep/sub-01_ses-T2s_segm_rim_HG_RH_v02_borderized.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-01/segmentation/01_rim_prep/sub-01_ses-T2s_segm_rim_HG_LH_v02_borderized.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-01/segmentation/01_rim_prep/sub-01_ses-T2s_segm_rim_CS_RH_v02_borderized.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-01/segmentation/01_rim_prep/sub-01_ses-T2s_segm_rim_CS_LH_v02_borderized.nii.gz",
]

OUTDIR = "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-01/segmentation/02_layers"

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
    outname = os.path.join(OUTDIR, "{}.{} ".format(basename, ext))

    # Layers and middle gray matter
    command = "/home/faruk/Git/LAYNII/LN2_LAYERS "
    command += "-rim {} ".format(rim)
    command += "-equivol "
    command += "-nr_layers 5 "
    command += "-curvature "
    command += "-streamlines "
    command += "-thickness "
    command += "-iter_smooth 100 "
    # command += "-incl_borders "
    command += "-output {} ".format(outname)
    print(command)
    subprocess.run(command, shell=True)

    # Connected cluster threshold
    targetname = os.path.join(OUTDIR, "{}_midGM_equidist.{} ".format(basename, ext))
    command = "python /home/faruk/Git/phd-mu/Python_Scripts/connected_clusters.py "
    command += "{} ".format(targetname)
    command += "--cluster_size 100000 "
    print(command)
    subprocess.run(command, shell=True)

print('Finished.\n')
