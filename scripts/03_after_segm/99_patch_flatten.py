"""Patch flatten"""

import os
import subprocess

VALUES = [
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/segmentation/00_segmentation/sub-01_ses-T2s_part-mag_MEGRE_crop_ups2X_prepped_avg_composite_decayfixed_T2s.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/segmentation/00_segmentation/sub-01_ses-T2s_part-mag_MEGRE_crop_ups2X_prepped_avg_composite_decayfixed_T2s.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/segmentation/00_segmentation/sub-01_ses-T2s_part-mag_MEGRE_crop_ups2X_prepped_avg_composite_decayfixed_T2s.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/segmentation/00_segmentation/sub-01_ses-T2s_part-mag_MEGRE_crop_ups2X_prepped_avg_composite_decayfixed_T2s.nii.gz",
]

COORD_UV = [
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/segmentation/03_multilaterate/sub-01_ses-T2s_segm_rim_HG_RH_v02_borderized_multilaterate_UV_coordinates.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/segmentation/03_multilaterate/sub-01_ses-T2s_segm_rim_HG_LH_v02_borderized_multilaterate_UV_coordinates.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/segmentation/03_multilaterate/sub-01_ses-T2s_segm_rim_CS_RH_v02_borderized_multilaterate_UV_coordinates.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/segmentation/03_multilaterate/sub-01_ses-T2s_segm_rim_CS_LH_v02_borderized_multilaterate_UV_coordinates.nii.gz",
]

COORD_D = [
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/segmentation/02_layers/sub-01_ses-T2s_segm_rim_HG_RH_v02_borderized_metric_equivol.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/segmentation/02_layers/sub-01_ses-T2s_segm_rim_HG_LH_v02_borderized_metric_equivol.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/segmentation/02_layers/sub-01_ses-T2s_segm_rim_CS_RH_v02_borderized_metric_equivol.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/segmentation/02_layers/sub-01_ses-T2s_segm_rim_CS_LH_v02_borderized_metric_equivol.nii.gz",
]

DOMAIN = [
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/segmentation/03_multilaterate/sub-01_ses-T2s_segm_rim_HG_RH_v02_borderized_multilaterate_perimeter_chunk.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/segmentation/03_multilaterate/sub-01_ses-T2s_segm_rim_HG_LH_v02_borderized_multilaterate_perimeter_chunk.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/segmentation/03_multilaterate/sub-01_ses-T2s_segm_rim_CS_RH_v02_borderized_multilaterate_perimeter_chunk.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/segmentation/03_multilaterate/sub-01_ses-T2s_segm_rim_CS_LH_v02_borderized_multilaterate_perimeter_chunk.nii.gz",
]

OUTDIR = "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/segmentation/99_patch_flatten"

# -----------------------------------------------------------------------------
# Output directory
if not os.path.exists(OUTDIR):
    os.makedirs(OUTDIR)
    print("  Output directory: {}\n".format(OUTDIR))

for i in range(len(VALUES)):
    values = VALUES[i]
    coord_uv = COORD_UV[i]
    coord_d = COORD_D[i]
    domain = DOMAIN[i]

    # Determine output basename
    filename = os.path.basename(domain)
    basename, ext = filename.split(os.extsep, 1)
    outname = os.path.join(OUTDIR, "{}.{} ".format(basename, ext))

    # Layers and middle gray matter
    command = "/home/faruk/Git/LAYNII/LN2_PATCH_FLATTEN "
    command += "-values {} ".format(values)
    command += "-coord_uv {} ".format(coord_uv)
    command += "-coord_d {} ".format(coord_d)
    command += "-domain {} ".format(domain)
    command += "-bins_u 500 "
    command += "-bins_v 500 "
    command += "-bins_d 100 "
    command += "-voronoi "
    command += "-output {} ".format(outname)
    print(command)
    subprocess.run(command, shell=True)

print('Finished.\n')
