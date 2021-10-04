"""Flatten T2star values into a chunky disk."""

import os
import subprocess

VALUES = [
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-04/T2s/12_T2star/sub-04_ses-T2s_part-mag_MEGRE_crop_ups2X_prepped_avg_composite_decayfixed_T2s.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-04/T2s/12_T2star/sub-04_ses-T2s_part-mag_MEGRE_crop_ups2X_prepped_avg_composite_decayfixed_T2s.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-04/T2s/12_T2star/sub-04_ses-T2s_part-mag_MEGRE_crop_ups2X_prepped_avg_composite_decayfixed_T2s.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-04/T2s/12_T2star/sub-04_ses-T2s_part-mag_MEGRE_crop_ups2X_prepped_avg_composite_decayfixed_T2s.nii.gz",
]

COORD_UV = [
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-04/segmentation/03_multilaterate/sub-04_ses-T2s_segm_rim_HG_RH_v02_borderized_multilaterate_UV_coordinates.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-04/segmentation/03_multilaterate/sub-04_ses-T2s_segm_rim_HG_LH_v02_borderized_multilaterate_UV_coordinates.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-04/segmentation/03_multilaterate/sub-04_ses-T2s_segm_rim_CS_RH_v02_borderized_multilaterate_UV_coordinates.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-04/segmentation/03_multilaterate/sub-04_ses-T2s_segm_rim_CS_LH_v02_borderized_multilaterate_UV_coordinates.nii.gz",
]

COORD_D = [
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-04/segmentation/02_layers/sub-04_ses-T2s_segm_rim_HG_RH_v02_borderized_metric_equivol.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-04/segmentation/02_layers/sub-04_ses-T2s_segm_rim_HG_LH_v02_borderized_metric_equivol.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-04/segmentation/02_layers/sub-04_ses-T2s_segm_rim_CS_RH_v02_borderized_metric_equivol.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-04/segmentation/02_layers/sub-04_ses-T2s_segm_rim_CS_LH_v02_borderized_metric_equivol.nii.gz",
]

DOMAIN =[
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-04/segmentation/03_multilaterate/sub-04_ses-T2s_segm_rim_HG_RH_v02_borderized_multilaterate_perimeter_chunk.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-04/segmentation/03_multilaterate/sub-04_ses-T2s_segm_rim_HG_LH_v02_borderized_multilaterate_perimeter_chunk.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-04/segmentation/03_multilaterate/sub-04_ses-T2s_segm_rim_CS_RH_v02_borderized_multilaterate_perimeter_chunk.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-04/segmentation/03_multilaterate/sub-04_ses-T2s_segm_rim_CS_LH_v02_borderized_multilaterate_perimeter_chunk.nii.gz",
]

OUTDIR = "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-04/segmentation/08_cakeplot_flats"

BINS_U = 100
BINS_V = 100
BINS_D = 21

TAG = "T2star"

# -----------------------------------------------------------------------------
# Output directory
if not os.path.exists(OUTDIR):
    os.makedirs(OUTDIR)
    print("  Output directory: {}\n".format(OUTDIR))

for i in range(len(DOMAIN)):
    values = VALUES[i]
    coord_uv = COORD_UV[i]
    coord_d = COORD_D[i]
    domain = DOMAIN[i]

    # Determine output basename
    filename = os.path.basename(domain)
    basename, ext = filename.split(os.extsep, 1)
    outname = os.path.join(OUTDIR, "{}_{}.{} ".format(basename, TAG, ext))

    # Layers and middle gray matter
    command = "/home/faruk/Git/LAYNII/LN2_PATCH_FLATTEN "
    command += "-values {} ".format(values)
    command += "-coord_uv {} ".format(coord_uv)
    command += "-coord_d {} ".format(coord_d)
    command += "-domain {} ".format(domain)
    command += "-bins_u {} -bins_v {} -bins_d {} ".format(BINS_U, BINS_V, BINS_D)
    command += "-voronoi "
    command += "-output {} ".format(outname)
    print(command)
    subprocess.run(command, shell=True)
    print()

print('Finished.\n')
