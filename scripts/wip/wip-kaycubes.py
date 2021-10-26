"""Repeating IDs for each voxel, useful for flattening quality control."""

import os
import subprocess
import nibabel as nb
import numpy as np
import glob

VALUES = [
    "/home/faruk/data2/test-LN_RAGRUG/sub-04_ses-T2s_ragrug12.nii.gz",
    "/home/faruk/data2/test-LN_RAGRUG/sub-04_ses-T2s_ragrug12.nii.gz",
    "/home/faruk/data2/test-LN_RAGRUG/sub-04_ses-T2s_ragrug12.nii.gz",
    "/home/faruk/data2/test-LN_RAGRUG/sub-04_ses-T2s_ragrug12.nii.gz"]

# Make sure that these correspond to images in VALUES
TAG = "kaycubes"

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

OUTDIR = "/home/faruk/data2/test-LN_RAGRUG"

BINS_U = 400
BINS_V = 400
BINS_D = 100

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
    command += "-bins_u {} ".format(BINS_U)
    command += "-bins_v {} ".format(BINS_V)
    command += "-bins_d {} ".format(BINS_D)
    command += "-voronoi "
    command += "-norm_mask "
    command += "-output {} ".format(outname)

    print(command)
    subprocess.run(command, shell=True)
    print()

# Make sform qform of flat niftis identity matrix
nii_files = glob.glob(os.path.join(OUTDIR, "*.nii*"))
for i in nii_files:
    nii = nb.load(i)
    new = nb.Nifti1Image(nii.dataobj, header=nii.header, affine=np.eye(4))
    nb.save(new, i)

# TODO: Use median filter to get rid of patch flatten interpoaltion artifacts
# fslmaths /home/faruk/data2/test-LN_RAGRUG/sub-04_ses-T2s_segm_rim_HG_RH_v02_borderized_multilaterate_perimeter_chunk_curvature_binned_flat_400x400_voronoi.nii.gz
#  -kernel boxv3 5 5 11 -fmedian
# /home/faruk/data2/test-LN_RAGRUG/sub-04_ses-T2s_segm_rim_HG_RH_v02_borderized_multilaterate_perimeter_chunk_curvature_binned_flat_400x400_voronoi_median_boxv_5-5-11.nii.gz

print('Finished.\n')
