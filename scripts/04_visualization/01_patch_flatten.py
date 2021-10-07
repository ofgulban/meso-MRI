"""Flatten several values into a chunky disk."""

import os
import subprocess
import nibabel as nb
import numpy as np
import glob

VALUES = [[
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/T2s/12_T2star/sub-05_ses-T2s_part-mag_MEGRE_crop_ups2X_prepped_avg_composite_decayfixed_T2s.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/T2s/12_T2star/sub-05_ses-T2s_part-mag_MEGRE_crop_ups2X_prepped_avg_composite_decayfixed_T2s.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/T2s/12_T2star/sub-05_ses-T2s_part-mag_MEGRE_crop_ups2X_prepped_avg_composite_decayfixed_T2s.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/T2s/12_T2star/sub-05_ses-T2s_part-mag_MEGRE_crop_ups2X_prepped_avg_composite_decayfixed_T2s.nii.gz",
    ], [
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/T1/07_register_to_T2s/sub-05_ses-T1_MP2RAGE_T1_crop_ups2X_avg_reg.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/T1/07_register_to_T2s/sub-05_ses-T1_MP2RAGE_T1_crop_ups2X_avg_reg.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/T1/07_register_to_T2s/sub-05_ses-T1_MP2RAGE_T1_crop_ups2X_avg_reg.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/T1/07_register_to_T2s/sub-05_ses-T1_MP2RAGE_T1_crop_ups2X_avg_reg.nii.gz",
    ], [
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/segmentation/02_layers/sub-05_ses-T2s_segm_rim_HG_RH_v02_borderized_curvature_binned.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/segmentation/02_layers/sub-05_ses-T2s_segm_rim_HG_LH_v02_borderized_curvature_binned.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/segmentation/02_layers/sub-05_ses-T2s_segm_rim_CS_RH_v02_borderized_curvature_binned.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/segmentation/02_layers/sub-05_ses-T2s_segm_rim_CS_LH_v02_borderized_curvature_binned.nii.gz",
    ], [
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/segmentation/03_multilaterate/sub-05_ses-T2s_segm_rim_HG_RH_v02_borderized_multilaterate_UV_norm_L2.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/segmentation/03_multilaterate/sub-05_ses-T2s_segm_rim_HG_LH_v02_borderized_multilaterate_UV_norm_L2.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/segmentation/03_multilaterate/sub-05_ses-T2s_segm_rim_CS_RH_v02_borderized_multilaterate_UV_norm_L2.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/segmentation/03_multilaterate/sub-05_ses-T2s_segm_rim_CS_LH_v02_borderized_multilaterate_UV_norm_L2.nii.gz",
    ]
]

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

OUTDIR = "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/flattening/"

BINS_U = 400
BINS_V = 400
BINS_D = 100

# Make sure that these correspond to images in VALUES
TAGS = ["T2star", "T1", "curvature_binned", "norm_L2"]

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

print('Finished.\n')
