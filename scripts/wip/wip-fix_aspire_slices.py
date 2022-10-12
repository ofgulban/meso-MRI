"""Post-reconstruction fix for random-looking first echo slice artifacts."""

import os
import numpy as np
import nibabel as nb

FILE = "/home/faruk/gdrive/temp_sebastian/sub-04_ses-02_T2s_run-01_dir-AP_echo-1_part-mag_ASPMEGRE.nii.gz"

SLICES = [9, 10, 18, 40, 65, 70, 71, 90, 93, 97]

# =============================================================================
# Load data
nii = nb.load(FILE)
data = nii.get_fdata()
dims = data.shape

# Determine output basename
basename = FILE.split(os.extsep, 1)[0]

# Output slices as a mask for checking if the slices are entered correctly
temp = np.zeros(dims, dtype=np.int8)
for i in SLICES:
    temp[:, i, :] = 1
outname = "{}_slicefix_slices.nii.gz".format(basename)
out = nb.Nifti1Image(temp, header=nii.header, affine=nii.affine)
nb.save(out, outname)

# -----------------------------------------------------------------------------
# Find nearest allowed slices
nearest1, nearest2 = list(), list()
for i in SLICES:
    if i + 1 in SLICES:  # Nearest slice is also artifact effected
        nearest1.append(-1)
    elif i + 1 == dims[2]:  # Nearest slice is out of bounds
        nearest1.append(-1)
    else:
        nearest1.append(i + 1)

    if i - 1 in SLICES:  # Nearest slice is also artifact effected
        nearest2.append(-1)
    elif i - 1 < 0:  # Nearest slice is out of bounds
        nearest2.append(-1)
    else:
        nearest2.append(i - 1)

# -----------------------------------------------------------------------------
# Scale up the voxels using information from the nearest allowed neighbors
data_new = np.copy(data)
for i, (s, n1, n2) in enumerate(zip(SLICES, nearest1, nearest2)):
    for x in range(1, dims[0]-1):
        for z in range(1, dims[2]-1):
            neighbour_val = 0.
            neighbour_count = 0
            if n1 != -1:
                neighbour_count += 1
                neighbour_val += data[x, n1, z] / 9
                neighbour_val += data[x+1, n1, z] / 9
                neighbour_val += data[x-1, n1, z] / 9
                neighbour_val += data[x, n1, z+1] / 9
                neighbour_val += data[x, n1, z-1] / 9
                neighbour_val += data[x+1, n1, z+1] / 9
                neighbour_val += data[x+1, n1, z-1] / 9
                neighbour_val += data[x-1, n1, z+1] / 9
                neighbour_val += data[x-1, n1, z-1] / 9
            if n2 != -1:
                neighbour_count += 1
                neighbour_val += data[x, n2, z] / 9
                neighbour_val += data[x+1, n2, z] / 9
                neighbour_val += data[x-1, n2, z] / 9
                neighbour_val += data[x, n2, z+1] / 9
                neighbour_val += data[x, n2, z-1] / 9
                neighbour_val += data[x+1, n2, z+1] / 9
                neighbour_val += data[x+1, n2, z-1] / 9
                neighbour_val += data[x-1, n2, z+1] / 9
                neighbour_val += data[x-1, n2, z-1] / 9

            if neighbour_count == 0:  # do nothing
                pass
            elif neighbour_count == 1:  # Use one neighbour estimate
                scale_factor = neighbour_val / data[x, s, z]
                data_new[x, s, z] *= scale_factor
            elif neighbour_count == 2:  # Use two neighbour estimate
                scale_factor = (neighbour_val / 2) / data[x, s, z]
                data_new[x, s, z] *= scale_factor

# Save
outname = "{}_slicefix.nii.gz".format(basename)
out = nb.Nifti1Image(data_new, header=nii.header, affine=nii.affine)
nb.save(out, outname)

print("Finished.")
