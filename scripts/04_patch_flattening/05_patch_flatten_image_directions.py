"""Flatten several values into a cylinder (aka virtual Petri dish)."""

import os
import subprocess
import nibabel as nb
import numpy as np
import glob

VALUES = [[
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/segmentation/11_encode_directions/sub-05_ses-T2s_segm_rim_HG_RH_v02_borderized_curvature_binned_RL.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/segmentation/11_encode_directions/sub-05_ses-T2s_segm_rim_HG_RH_v02_borderized_curvature_binned_RL.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/segmentation/11_encode_directions/sub-05_ses-T2s_segm_rim_HG_RH_v02_borderized_curvature_binned_RL.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/segmentation/11_encode_directions/sub-05_ses-T2s_segm_rim_HG_RH_v02_borderized_curvature_binned_RL.nii.gz",
    ], [
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/segmentation/11_encode_directions/sub-05_ses-T2s_segm_rim_HG_RH_v02_borderized_curvature_binned_PA.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/segmentation/11_encode_directions/sub-05_ses-T2s_segm_rim_HG_RH_v02_borderized_curvature_binned_PA.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/segmentation/11_encode_directions/sub-05_ses-T2s_segm_rim_HG_RH_v02_borderized_curvature_binned_PA.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/segmentation/11_encode_directions/sub-05_ses-T2s_segm_rim_HG_RH_v02_borderized_curvature_binned_PA.nii.gz",
    ], [
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/segmentation/11_encode_directions/sub-05_ses-T2s_segm_rim_HG_RH_v02_borderized_curvature_binned_IS.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/segmentation/11_encode_directions/sub-05_ses-T2s_segm_rim_HG_RH_v02_borderized_curvature_binned_IS.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/segmentation/11_encode_directions/sub-05_ses-T2s_segm_rim_HG_RH_v02_borderized_curvature_binned_IS.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/segmentation/11_encode_directions/sub-05_ses-T2s_segm_rim_HG_RH_v02_borderized_curvature_binned_IS.nii.gz",
    ]
]

# Make sure that these correspond to images in VALUES
TAGS = ["ImgDirRL", "ImgDirPA", "ImgDirIS"]

COORD_UV = [
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/segmentation/03_multilaterate/sub-05_ses-T2s_segm_rim_HG_RH_v02_borderized_multilaterate_UV_coordinates.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/segmentation/03_multilaterate/sub-05_ses-T2s_segm_rim_HG_LH_v02_borderized_multilaterate_UV_coordinates.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/segmentation/03_multilaterate/sub-05_ses-T2s_segm_rim_CS_RH_v02_borderized_multilaterate_UV_coordinates.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/segmentation/03_multilaterate/sub-05_ses-T2s_segm_rim_CS_LH_v02_borderized_multilaterate_UV_coordinates.nii.gz",
]

COORD_D = [
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/segmentation/02_layers/sub-05_ses-T2s_segm_rim_HG_RH_v02_borderized_metric_equivol.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/segmentation/02_layers/sub-05_ses-T2s_segm_rim_HG_LH_v02_borderized_metric_equivol.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/segmentation/02_layers/sub-05_ses-T2s_segm_rim_CS_RH_v02_borderized_metric_equivol.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/segmentation/02_layers/sub-05_ses-T2s_segm_rim_CS_LH_v02_borderized_metric_equivol.nii.gz",
]

DOMAIN =[
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/segmentation/03_multilaterate/sub-05_ses-T2s_segm_rim_HG_RH_v02_borderized_multilaterate_perimeter_chunk.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/segmentation/03_multilaterate/sub-05_ses-T2s_segm_rim_HG_LH_v02_borderized_multilaterate_perimeter_chunk.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/segmentation/03_multilaterate/sub-05_ses-T2s_segm_rim_CS_RH_v02_borderized_multilaterate_perimeter_chunk.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/segmentation/03_multilaterate/sub-05_ses-T2s_segm_rim_CS_LH_v02_borderized_multilaterate_perimeter_chunk.nii.gz",
]

OUTDIR = "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/flattening"
LAYNIIDIR = "/home/faruk/Git/LAYNII/"

BINS_U = 400
BINS_V = 400
BINS_D = 100

# -----------------------------------------------------------------------------
# Output directory
if not os.path.exists(OUTDIR):
    os.makedirs(OUTDIR)
    print("  Output directory: {}\n".format(OUTDIR))

for j in range(len(VALUES)):
    tag = TAGS[j]
    for i in range(len(DOMAIN)):
        values = VALUES[j][i]
        coord_uv = COORD_UV[i]
        coord_d = COORD_D[i]
        domain = DOMAIN[i]

        # Determine output basename
        filename = os.path.basename(domain)
        basename, ext = filename.split(os.extsep, 1)
        outname = os.path.join(OUTDIR, "{}_{}.{} ".format(basename, tag, ext))

        # Layers and middle gray matter
        command = os.path.join(LAYNIIDIR, "LN2_PATCH_FLATTEN ")
        command += "-values {} ".format(values)
        command += "-coord_uv {} ".format(coord_uv)
        command += "-coord_d {} ".format(coord_d)
        command += "-domain {} ".format(domain)
        command += "-bins_u {} ".format(BINS_U)
        command += "-bins_v {} ".format(BINS_V)
        command += "-bins_d {} ".format(BINS_D)
        command += "-voronoi "
        command += "-norm_mask "
        command += "-output {} ".format(outname)

        print(command)
        subprocess.run(command, shell=True)
        print()

print('Finished.\n')
