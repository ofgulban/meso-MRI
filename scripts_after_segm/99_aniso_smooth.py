"""Separate scoops of interest (SOI)."""

import os
import subprocess

IMAGES = [
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/T2s/12_T2star/sub-01_ses-T2s_part-mag_MEGRE_crop_ups2X_prepped_avg_composite_decayfixed_T2s.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-02/T2s/12_T2star/sub-02_ses-T2s_part-mag_MEGRE_crop_ups2X_prepped_avg_composite_decayfixed_T2s.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-03/T2s/12_T2star/sub-03_ses-T2s_part-mag_MEGRE_crop_ups2X_prepped_avg_composite_decayfixed_T2s.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-04/T2s/12_T2star/sub-04_ses-T2s_part-mag_MEGRE_crop_ups2X_prepped_avg_composite_decayfixed_T2s.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-05/T2s/12_T2star/sub-05_ses-T2s_part-mag_MEGRE_crop_ups2X_prepped_avg_composite_decayfixed_T2s.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-01/T1/07_register_to_T2s/sub-01_ses-T1_MP2RAGE_uni_crop_ups2X_avg_reg.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-02/T1/07_register_to_T2s/sub-02_ses-T1_MP2RAGE_uni_crop_ups2X_avg_reg.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-03/T1/07_register_to_T2s/sub-03_ses-T1_MP2RAGE_uni_crop_ups2X_avg_reg.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-04/T1/07_register_to_T2s/sub-04_ses-T1_MP2RAGE_uni_crop_ups2X_avg_reg.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-05/T1/07_register_to_T2s/sub-05_ses-T1_MP2RAGE_uni_crop_ups2X_avg_reg.nii.gz",
]

# OUTDIR = "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-05/smooth_test"

# -----------------------------------------------------------------------------
# Output directory
# if not os.path.exists(OUTDIR):
#     os.makedirs(OUTDIR)
#     print("  Output directory: {}\n".format(OUTDIR))

for i in range(IMAGES):
    command = "segmentator_filters "
    command += "-{} ".format(i)
    command += "--noise_scale {} ".format(0.5)
    command += "--feature_scale {} ".format(1.0)
    comamnd += "--nr_iterations 5 "
    command += "--save_every 1 "
    print(command)
    subprocess.run(command, shell=True)

print('Finished.\n')
