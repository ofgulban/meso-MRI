"""Laminar median filter."""

import os
import subprocess
import nibabel as nb
import numpy as np
import glob

VALUES = [[
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-01/T2s/12_T2star/sub-01_ses-T2s_part-mag_MEGRE_crop_ups2X_prepped_avg_composite_decayfixed_T2s.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-01/T2s/12_T2star/sub-01_ses-T2s_part-mag_MEGRE_crop_ups2X_prepped_avg_composite_decayfixed_T2s.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-01/T2s/12_T2star/sub-01_ses-T2s_part-mag_MEGRE_crop_ups2X_prepped_avg_composite_decayfixed_T2s.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-01/T2s/12_T2star/sub-01_ses-T2s_part-mag_MEGRE_crop_ups2X_prepped_avg_composite_decayfixed_T2s.nii.gz",
    ], [
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-01/T1/07_register_to_T2s/sub-01_ses-T1_MP2RAGE_T1_crop_ups2X_avg_reg.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-01/T1/07_register_to_T2s/sub-01_ses-T1_MP2RAGE_T1_crop_ups2X_avg_reg.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-01/T1/07_register_to_T2s/sub-01_ses-T1_MP2RAGE_T1_crop_ups2X_avg_reg.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-01/T1/07_register_to_T2s/sub-01_ses-T1_MP2RAGE_T1_crop_ups2X_avg_reg.nii.gz",
    ]
]

# Make sure that these correspond to images in VALUES
TAGS = ["T2star", "T1"]

COORD_UV = [
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-01/segmentation/03_multilaterate/sub-01_ses-T2s_segm_rim_HG_RH_v02_borderized_multilaterate_UV_coordinates.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-01/segmentation/03_multilaterate/sub-01_ses-T2s_segm_rim_HG_LH_v02_borderized_multilaterate_UV_coordinates.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-01/segmentation/03_multilaterate/sub-01_ses-T2s_segm_rim_CS_RH_v02_borderized_multilaterate_UV_coordinates.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-01/segmentation/03_multilaterate/sub-01_ses-T2s_segm_rim_CS_LH_v02_borderized_multilaterate_UV_coordinates.nii.gz",
]

COORD_D = [
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-01/segmentation/02_layers/sub-01_ses-T2s_segm_rim_HG_RH_v02_borderized_metric_equivol.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-01/segmentation/02_layers/sub-01_ses-T2s_segm_rim_HG_LH_v02_borderized_metric_equivol.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-01/segmentation/02_layers/sub-01_ses-T2s_segm_rim_CS_RH_v02_borderized_metric_equivol.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-01/segmentation/02_layers/sub-01_ses-T2s_segm_rim_CS_LH_v02_borderized_metric_equivol.nii.gz",
]

DOMAIN =[
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-01/segmentation/03_multilaterate/sub-01_ses-T2s_segm_rim_HG_RH_v02_borderized_multilaterate_perimeter_chunk.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-01/segmentation/03_multilaterate/sub-01_ses-T2s_segm_rim_HG_LH_v02_borderized_multilaterate_perimeter_chunk.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-01/segmentation/03_multilaterate/sub-01_ses-T2s_segm_rim_CS_RH_v02_borderized_multilaterate_perimeter_chunk.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-01/segmentation/03_multilaterate/sub-01_ses-T2s_segm_rim_CS_LH_v02_borderized_multilaterate_perimeter_chunk.nii.gz",
]

OUTDIR = "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-01/segmentation/08_median_filter/"

RADIUS = 2
HEIGHT = 0.1

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
        command = "/home/faruk/Git/LAYNII/LN2_UVD_FILTER "
        command += "-values {} ".format(values)
        command += "-coord_uv {} ".format(coord_uv)
        command += "-coord_d {} ".format(coord_d)
        command += "-domain {} ".format(domain)
        command += "-radius {} ".format(RADIUS)
        command += "-height {} ".format(HEIGHT)
        command += "-output {} ".format(outname)

        print(command)
        subprocess.run(command, shell=True)
        print()

print('Finished.\n')
