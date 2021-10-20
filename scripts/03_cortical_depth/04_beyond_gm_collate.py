"""Collate beyond gray matter distances with cortical depth measures."""

import os
import subprocess
import numpy as np
import nibabel as nb

DIST1 = [
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/segmentation/06_beyond_gm_distances/sub-05_ses-T2s_segm_rim_HG_RH_v02_domain-wm_distances.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/segmentation/06_beyond_gm_distances/sub-05_ses-T2s_segm_rim_HG_LH_v02_domain-wm_distances.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/segmentation/06_beyond_gm_distances/sub-05_ses-T2s_segm_rim_CS_RH_v02_domain-wm_distances.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/segmentation/06_beyond_gm_distances/sub-05_ses-T2s_segm_rim_CS_LH_v02_domain-wm_distances.nii.gz",
]

DIST2 = [
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/segmentation/06_beyond_gm_distances/sub-05_ses-T2s_segm_rim_HG_RH_v02_domain-csf_distances.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/segmentation/06_beyond_gm_distances/sub-05_ses-T2s_segm_rim_HG_LH_v02_domain-csf_distances.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/segmentation/06_beyond_gm_distances/sub-05_ses-T2s_segm_rim_CS_RH_v02_domain-csf_distances.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/segmentation/06_beyond_gm_distances/sub-05_ses-T2s_segm_rim_CS_LH_v02_domain-csf_distances.nii.gz",
]

DIST3 = [
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/segmentation/02_layers/sub-05_ses-T2s_segm_rim_HG_RH_v02_borderized_metric_equivol.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/segmentation/02_layers/sub-05_ses-T2s_segm_rim_HG_LH_v02_borderized_metric_equivol.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/segmentation/02_layers/sub-05_ses-T2s_segm_rim_CS_RH_v02_borderized_metric_equivol.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/segmentation/02_layers/sub-05_ses-T2s_segm_rim_CS_LH_v02_borderized_metric_equivol.nii.gz",
]

OUTDIR = "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-05/segmentation/07_beyond_gm_collate"

OUTNAMES = [
    "sub-05_ses-T2s_segm_rim_HG_RH_v02_beyond_gm_distances.nii.gz",
    "sub-05_ses-T2s_segm_rim_HG_LH_v02_beyond_gm_distances.nii.gz",
    "sub-05_ses-T2s_segm_rim_CS_RH_v02_beyond_gm_distances.nii.gz",
    "sub-05_ses-T2s_segm_rim_CS_LH_v02_beyond_gm_distances.nii.gz",
    ]
# -----------------------------------------------------------------------------
# Output directory
if not os.path.exists(OUTDIR):
    os.makedirs(OUTDIR)
    print("  Output directory: {}\n".format(OUTDIR))

for i in range(len(DIST1)):
    dist1 = DIST1[i]
    dist2 = DIST2[i]
    dist3 = DIST3[i]  # gm depth metrics

    nii1 = nb.load(dist1)
    nii2 = nb.load(dist2)
    nii3 = nb.load(dist3)

    data1 = np.asarray(nii1.dataobj)
    data2 = np.asarray(nii2.dataobj)
    data3 = np.asarray(nii3.dataobj)

    # Adjust WM distances to stay below 0
    data1 *= -1
    # Adjust CSF distances to stay above 1
    data2[data2 != 0] = data2[data2 != 0] + 1
    # Collate distances
    data1 += data2
    data1 += data3

    # Save nifti
    outname = os.path.join(OUTDIR, OUTNAMES[i])
    out_img = nb.Nifti1Image(data1, header=nii1.header, affine=nii1.affine)
    nb.save(out_img, outname)

print('Finished.\n')
