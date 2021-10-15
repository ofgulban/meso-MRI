"""Peak detection after columnar filter."""

import os
import subprocess
import nibabel as nb
import numpy as np
import glob

VALUES = [[
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-01/segmentation/09_columnar_median_filter/sub-01_ses-T2s_segm_rim_HG_RH_v02_borderized_multilaterate_perimeter_chunk_columnar_T2star_UVD_median_filter.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-01/segmentation/09_columnar_median_filter/sub-01_ses-T2s_segm_rim_HG_LH_v02_borderized_multilaterate_perimeter_chunk_columnar_T2star_UVD_median_filter.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-01/segmentation/09_columnar_median_filter/sub-01_ses-T2s_segm_rim_CS_RH_v02_borderized_multilaterate_perimeter_chunk_columnar_T2star_UVD_median_filter.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-01/segmentation/09_columnar_median_filter/sub-01_ses-T2s_segm_rim_HG_LH_v02_borderized_multilaterate_perimeter_chunk_columnar_T2star_UVD_median_filter.nii.gz",
    ], [
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-01/segmentation/09_columnar_median_filter/sub-01_ses-T2s_segm_rim_HG_RH_v02_borderized_multilaterate_perimeter_chunk_columnar_T1_UVD_median_filter.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-01/segmentation/09_columnar_median_filter/sub-01_ses-T2s_segm_rim_HG_LH_v02_borderized_multilaterate_perimeter_chunk_columnar_T1_UVD_median_filter.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-01/segmentation/09_columnar_median_filter/sub-01_ses-T2s_segm_rim_CS_RH_v02_borderized_multilaterate_perimeter_chunk_columnar_T1_UVD_median_filter.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-01/segmentation/09_columnar_median_filter/sub-01_ses-T2s_segm_rim_CS_LH_v02_borderized_multilaterate_perimeter_chunk_columnar_T1_UVD_median_filter.nii.gz",
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

OUTDIR = "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-01/segmentation/10_peak_detect/"

RADIUS = 0.35
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
        command += "-min "
        command += "-output {} ".format(outname)

        print(command)
        subprocess.run(command, shell=True)
        print()

print('Finished.\n')
