"""Measure cortical depths using LayNii LN2_LAYERS."""

import os
import subprocess
import numpy as np
import nibabel as nb

RIMS = [
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/segmentation/00_segmentation/HG_RH/sub-05_ses-T2s_segm_rim_HG_RH_v02.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/segmentation/00_segmentation/HG_LH/sub-05_ses-T2s_segm_rim_HG_LH_v02.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/segmentation/00_segmentation/CS_RH/sub-05_ses-T2s_segm_rim_CS_RH_v02.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/segmentation/00_segmentation/CS_LH/sub-05_ses-T2s_segm_rim_CS_LH_v02.nii.gz",
]

BORDERS = [
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/segmentation/01_rim_prep/sub-05_ses-T2s_segm_rim_HG_RH_v02_borders.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/segmentation/01_rim_prep/sub-05_ses-T2s_segm_rim_HG_LH_v02_borders.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/segmentation/01_rim_prep/sub-05_ses-T2s_segm_rim_CS_RH_v02_borders.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/segmentation/01_rim_prep/sub-05_ses-T2s_segm_rim_CS_LH_v02_borders.nii.gz",
]

CHUNKS = [
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/segmentation/03_multilaterate/sub-05_ses-T2s_segm_rim_HG_RH_v02_borderized_multilaterate_perimeter_chunk.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/segmentation/03_multilaterate/sub-05_ses-T2s_segm_rim_HG_LH_v02_borderized_multilaterate_perimeter_chunk.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/segmentation/03_multilaterate/sub-05_ses-T2s_segm_rim_CS_RH_v02_borderized_multilaterate_perimeter_chunk.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/segmentation/03_multilaterate/sub-05_ses-T2s_segm_rim_CS_LH_v02_borderized_multilaterate_perimeter_chunk.nii.gz",
    ]

MAX_DIST = 0.35 * 2

OUTDIR = "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/segmentation/05_beyond_gm_prep"

# -----------------------------------------------------------------------------
# Output directory
if not os.path.exists(OUTDIR):
    os.makedirs(OUTDIR)
    print("  Output directory: {}\n".format(OUTDIR))

for i in range(len(RIMS)):
    rim = RIMS[i]
    border = BORDERS[i]

    nii1 = nb.load(rim)
    nii2 = nb.load(border)

    # Mask WM
    data1 = np.asarray(nii1.dataobj)
    data2 = np.asarray(nii2.dataobj)
    data1[data1 != 2] = 0
    data1[data1 != 0] = 1
    data2[data2 != 2] = 0
    data2[data2 != 0] = 1

    # Save nifti
    filename = os.path.basename(rim)
    basename, ext = filename.split(os.extsep, 1)
    outname = os.path.join(OUTDIR, "{}_domain-wm.{}".format(basename, ext))
    out_img = nb.Nifti1Image(data1, header=nii1.header, affine=nii1.affine)
    nb.save(out_img, outname)
    outname = os.path.join(OUTDIR, "{}_border-wm.{}".format(basename, ext))
    out_img = nb.Nifti1Image(data2, header=nii2.header, affine=nii2.affine)
    nb.save(out_img, outname)

    # -------------------------------------------------------------------------
    # Mask CSF
    data1 = np.asarray(nii1.dataobj)
    data2 = np.asarray(nii2.dataobj)
    data1[data1 != 1] = 0
    data1[data1 != 0] = 1
    data2[data2 != 1] = 0
    data2[data2 != 0] = 1

    # Save nifti
    filename = os.path.basename(RIMS[i])
    basename, ext = filename.split(os.extsep, 1)
    outname = os.path.join(OUTDIR, "{}_domain-csf.{}".format(basename, ext))
    out_img = nb.Nifti1Image(data1, header=nii1.header, affine=nii1.affine)
    nb.save(out_img, outname)
    outname = os.path.join(OUTDIR, "{}_border-csf.{}".format(basename, ext))
    out_img = nb.Nifti1Image(data2, header=nii2.header, affine=nii2.affine)
    nb.save(out_img, outname)

    # =========================================================================
    # Dilate chunks
    chunk = CHUNKS[i]

    # Determine output basename
    filename = os.path.basename(chunk)
    basename, ext = filename.split(os.extsep, 1)
    outname = os.path.join(OUTDIR, "{}_voronoi_dilated.{}".format(basename, ext))

    # Layers and middle gray matter
    command = "/home/faruk/Git/LAYNII/LN2_VORONOI "
    command += "-domain {} ".format(rim)
    command += "-init {} ".format(chunk)
    command += "-max_dist {} ".format(MAX_DIST)
    command += "-output {} ".format(outname)
    print(command)
    subprocess.run(command, shell=True)

print('Finished.\n')
