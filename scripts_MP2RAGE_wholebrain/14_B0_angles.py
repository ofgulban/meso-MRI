"""B0 angle related stuff"""

import os
import numpy as np
import nibabel as nb

# Scalar file
REF = "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-05/T1_wholebrain/04_segmentation/sub-05_ses-T2s_part-mag_MEGRE_crop_ups2X_prepped_avg_composite_decayfixed_T2s.nii.gz"

# Vector file
VECTORS = [
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-05/T1_wholebrain/05_layers/sub-05_ses-T2s_segm_rim_HG_RH_v02_streamline_vectors.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-05/T1_wholebrain/05_layers/sub-05_ses-T2s_segm_rim_HG_LH_v02_streamline_vectors.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-05/T1_wholebrain/05_layers/sub-05_ses-T2s_segm_rim_CS_RH_v02_streamline_vectors.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-05/T1_wholebrain/05_layers/sub-05_ses-T2s_segm_rim_CS_LH_v02_streamline_vectors.nii.gz",
    ]

OUTDIR = "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-05/T1_wholebrain/07_B0_angles"

# =============================================================================
# Output directory
if not os.path.exists(OUTDIR):
    os.makedirs(OUTDIR)
    print("  Output directory: {}\n".format(OUTDIR))


# Load nifti
nii1 = nb.load(REF)
data = np.asarray(nii1.dataobj)
idx = data != 0
dims = nii1.shape

# Affine
aff = nii1.affine
aff = np.linalg.inv(aff)

ref = np.array([[0, 0, 0], [0, 0, 1]])
new = nb.affines.apply_affine(aff, ref)
new = new[1, :] - new[0, :]
new /= np.linalg.norm(new)

# Prepare 4D nifti
vec_B0 = np.zeros(dims + (3,))
vec_B0[..., 0] = new[0]
vec_B0[..., 1] = new[1]
vec_B0[..., 2] = new[2]
vec_B0[~idx, :] = 0

# Save
filename = os.path.basename(REF)
basename, ext = filename.split(os.extsep, 1)
outname = os.path.join(OUTDIR, "{}_B0vector.{}".format(basename, ext))
img = nb.Nifti1Image(vec_B0, affine=nii1.affine, header=nii1.header)
nb.save(img, outname)

# -----------------------------------------------------------------------------
for i in range(len(VECTORS)):
    # Load vector nifti
    nii2 = nb.load(VECTORS[i])
    vec_local = np.asarray(nii2.dataobj)

    # Angular difference
    term1 = np.sum(vec_B0 ** 2., axis=-1)
    term2 = np.sum(vec_local ** 2., axis=-1)
    temp_dot = np.sum(vec_B0 * vec_local, axis=-1)
    temp_angle = np.arccos(temp_dot / np.sqrt(term1 * term2))
    temp_angle = temp_angle * 180 / np.pi;
    temp_angle[~idx] = 0
    temp_angle[np.isnan(temp_angle)] = 0
    temp_angle[idx] = 90 - np.abs(temp_angle[idx] - 90)

    # Save
    filename = os.path.basename(VECTORS[i])
    basename, ext = filename.split(os.extsep, 1)
    outname = os.path.join(OUTDIR, "{}_B0angdif.{}".format(basename, ext))
    img = nb.Nifti1Image(temp_angle, affine=nii1.affine, header=nii1.header)
    nb.save(img, outname)

print("Finished.")
