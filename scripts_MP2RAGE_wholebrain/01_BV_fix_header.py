"""Header swap."""

import os
import subprocess
import numpy as np
import nibabel as nb

# =============================================================================
NII_NAMES = [
    '/home/faruk/data/temp_BV_DNN/sub-01/derivatives/sub-01_ses-T2s_MP2RAGE_uni_pt7_reframed_tissue-probs-slow_map-1_Background.nii.gz',
    '/home/faruk/data/temp_BV_DNN/sub-01/derivatives/sub-01_ses-T2s_MP2RAGE_uni_pt7_reframed_tissue-probs-slow_map-2_White matter.nii.gz',
    '/home/faruk/data/temp_BV_DNN/sub-01/derivatives/sub-01_ses-T2s_MP2RAGE_uni_pt7_reframed_tissue-probs-slow_map-3_Grey matter.nii.gz',
    '/home/faruk/data/temp_BV_DNN/sub-01/derivatives/sub-01_ses-T2s_MP2RAGE_uni_pt7_reframed_tissue-probs-slow_map-4_CSF (extra-cerebral).nii.gz',
    '/home/faruk/data/temp_BV_DNN/sub-01/derivatives/sub-01_ses-T2s_MP2RAGE_uni_pt7_reframed_tissue-probs-slow_map-5_Ventricles (Lateral, 5th.nii.gz',
    '/home/faruk/data/temp_BV_DNN/sub-01/derivatives/sub-01_ses-T2s_MP2RAGE_uni_pt7_reframed_tissue-probs-slow_map-6_Subcortical structures.nii.gz',
    '/home/faruk/data/temp_BV_DNN/sub-01/derivatives/sub-01_ses-T2s_MP2RAGE_uni_pt7_reframed_tissue-probs-slow_map-7_Blood vessels.nii.gz',
    '/home/faruk/data/temp_BV_DNN/sub-01/derivatives/sub-01_ses-T2s_MP2RAGE_uni_pt7_reframed_tissue-probs-slow_map-8_Sagittal sinus.nii.gz',
    ]

NII_ORIG = "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/T1_wholebrain/00_resample_to_pt7/sub-01_ses-T2s_MP2RAGE_uni_pt7_reframed.nii.gz"

OUTDIR = "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/T1_wholebrain/01_DNN_Segmentator"

# =============================================================================
print("Step_01: Fix BV VMP to Nifti headers.")

# Output directory
if not os.path.exists(OUTDIR):
    os.makedirs(OUTDIR)
print("  Output directory: {}\n".format(OUTDIR))
# -----------------------------------------------------------------------------

nii_orig = nb.load(NII_ORIG)

for f in NII_NAMES:
    nii = nb.load(f)
    # Reorder voxels
    data = np.transpose(nii.get_fdata(), [1, 2, 0])
    data = data[::-1, :, :]

    # Save
    basename, ext = nii.get_filename().split(os.extsep, 1)
    basename = os.path.basename(basename)
    basename = basename.replace("(", "")
    basename = basename.replace(")", "")
    basename = basename.replace(",", "")
    basename = basename.replace(" ", "_")
    out_name = os.path.join(OUTDIR, basename)
    img = nb.Nifti1Image(data, affine=nii_orig.affine, header=nii_orig.header)
    nb.save(img, '{}.{}'.format(out_name, ext))

print('\n\nFinished.')
