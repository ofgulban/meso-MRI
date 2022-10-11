"""Median projection across depths/layers."""

import os
import subprocess
import nibabel as nb
import numpy as np
import glob

MAPS = [
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-01/flattening/sub-01_ses-T2s_segm_rim_HG_RH_v02_borderized_multilaterate_perimeter_chunk_curvature_binned_flat_400x400_voronoi.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-01/flattening/sub-01_ses-T2s_segm_rim_HG_LH_v02_borderized_multilaterate_perimeter_chunk_curvature_binned_flat_400x400_voronoi.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-01/flattening/sub-01_ses-T2s_segm_rim_CS_RH_v02_borderized_multilaterate_perimeter_chunk_curvature_binned_flat_400x400_voronoi.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-01/flattening/sub-01_ses-T2s_segm_rim_CS_LH_v02_borderized_multilaterate_perimeter_chunk_curvature_binned_flat_400x400_voronoi.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-01/flattening/sub-01_ses-T2s_segm_rim_HG_RH_v02_borderized_multilaterate_perimeter_chunk_T2star_flat_400x400_voronoi.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-01/flattening/sub-01_ses-T2s_segm_rim_HG_LH_v02_borderized_multilaterate_perimeter_chunk_T2star_flat_400x400_voronoi.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-01/flattening/sub-01_ses-T2s_segm_rim_CS_RH_v02_borderized_multilaterate_perimeter_chunk_T2star_flat_400x400_voronoi.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-01/flattening/sub-01_ses-T2s_segm_rim_CS_LH_v02_borderized_multilaterate_perimeter_chunk_T2star_flat_400x400_voronoi.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-01/flattening/sub-01_ses-T2s_segm_rim_HG_RH_v02_borderized_multilaterate_perimeter_chunk_T1_flat_400x400_voronoi.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-01/flattening/sub-01_ses-T2s_segm_rim_HG_LH_v02_borderized_multilaterate_perimeter_chunk_T1_flat_400x400_voronoi.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-01/flattening/sub-01_ses-T2s_segm_rim_CS_RH_v02_borderized_multilaterate_perimeter_chunk_T1_flat_400x400_voronoi.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-01/flattening/sub-01_ses-T2s_segm_rim_CS_LH_v02_borderized_multilaterate_perimeter_chunk_T1_flat_400x400_voronoi.nii.gz",
]

OUTDIR = "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-01/median_maps"

# -----------------------------------------------------------------------------
# Output directory
if not os.path.exists(OUTDIR):
    os.makedirs(OUTDIR)
print("  Output directory: {}\n".format(OUTDIR))

for i in range(len(MAPS)):
    # Determine output basename
    filename = os.path.basename(MAPS[i])
    basename, ext = filename.split(os.extsep, 1)
    outname = os.path.join(OUTDIR, "{}_median_projection.{}".format(basename, ext))

    nii = nb.load(MAPS[i])
    data = np.asarray(nii.dataobj)

    data = np.median(data, axis=2)

    # Repeat to be able to overlay on 3D flat maps
    data = np.repeat(data[:, :, None], nii.shape[2], axis=2)

    # Save
    out = nb.Nifti1Image(data, header=nii.header, affine=nii.affine)
    nb.save(out, outname)

print('Finished.\n')
