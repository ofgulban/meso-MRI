"""Used in thingsonthings.org LN2_MULTILATERATE blog post."""

import numpy as np
import nibabel as nb

# Scalar file (e.g. activtion map or anatomical image)
FILE0 = "/home/faruk/data2/test-LGN/full16_100um_optbal_LGN_RH_roi.nii.gz"

# Flat coordinates (UV) and depth
FILE1 = "/home/faruk/data2/test-LGN/LGN_RH_roi_borders_coord1_zero_crossing_geodistance_signed_pointNormalized.nii.gz"
FILE2 = "/home/faruk/data2/test-LGN/LGN_RH_roi_borders_coord2_zero_crossing_geodistance_signed_pointNormalized.nii.gz"
FILE3 = "/home/faruk/data2/test-LGN/LGN_RH_roi_borders_coord3_zero_crossing_geodistance_signed_pointNormalized.nii.gz"

# Mask
MASK = "/home/faruk/data2/test-LGN/LGN_RH_roi.nii.gz"

OUTFILE = "/home/faruk/data2/test-LGN/anim-test3.nii.gz"

NR_STEPS = 50

# -----------------------------------------------------------------------------
# Load data
nii1 = nb.load(FILE0)

mask = nb.load(MASK).get_fdata()
mask = mask == 1

data0 = nii1.get_fdata() * mask
data1 = nb.load(FILE1).get_fdata() * mask
data2 = nb.load(FILE2).get_fdata() * mask
data3 = nb.load(FILE3).get_fdata() * mask

# Prepare coordinates
dims = data0.shape
coords_xyz = np.asarray(np.indices(dims))
coords_xyz = np.transpose(coords_xyz, [1, 2, 3, 0])

coords_uvd = np.zeros(data0.shape + (3,))
coords_uvd[..., 0] = data2
coords_uvd[..., 1] = data3
coords_uvd[..., 2] = data1

# Adjust UVD coordinate range to fit in the data image matrix
coords_uvd[..., 0] *= 1
coords_uvd[..., 1] *= 1
coords_uvd[..., 2] *= 1

coords_uvd[..., 0] = coords_uvd[..., 0] - np.min(coords_uvd[..., 0])
coords_uvd[..., 1] = coords_uvd[..., 1] - np.min(coords_uvd[..., 1])
coords_uvd[..., 2] = coords_uvd[..., 2] - np.min(coords_uvd[..., 2])

coords_uvd[..., 0] = coords_uvd[..., 0] / (np.max(coords_uvd[..., 0]) + 0.0001)
coords_uvd[..., 1] = coords_uvd[..., 1] / (np.max(coords_uvd[..., 1]) + 0.0001)
coords_uvd[..., 2] = coords_uvd[..., 2] / (np.max(coords_uvd[..., 2]) + 0.0001)

coords_uvd[..., 0] = coords_uvd[..., 0] * dims[0]
coords_uvd[..., 1] = coords_uvd[..., 1] * dims[1]
coords_uvd[..., 2] = coords_uvd[..., 2] * dims[2]

# coords_uvd[..., 0] = coords_uvd[..., 0] / 2 + (dims[0] / 4)
# coords_uvd[..., 1] = coords_uvd[..., 1] / 2 + (dims[1] / 4)
# coords_uvd[..., 2] = coords_uvd[..., 2] / 2 + (dims[2] / 4)

# -----------------------------------------------------------------------------
# Interpolate voxel particle tractories
flat_xyz = coords_xyz[mask]
flat_uvd = coords_uvd[mask]
nr_voxels = np.sum(mask)

traj = np.zeros((nr_voxels, NR_STEPS, 3))
for i in range(nr_voxels):
    traj[i, :, 0] = np.linspace(flat_xyz[i, 0], flat_uvd[i, 0], NR_STEPS)
    traj[i, :, 1] = np.linspace(flat_xyz[i, 1], flat_uvd[i, 1], NR_STEPS)
    traj[i, :, 2] = np.linspace(flat_xyz[i, 2], flat_uvd[i, 2], NR_STEPS)

# -----------------------------------------------------------------------------
# Transform volume data
new_data = np.zeros(dims + (NR_STEPS,))
count = np.copy(new_data)
for i in range(nr_voxels):
    idx0 = int(traj[i, 0, 0])
    idx1 = int(traj[i, 0, 1])
    idx2 = int(traj[i, 0, 2])

    for j in range(NR_STEPS):
        new_idx0 = int(traj[i, j, 0])
        new_idx1 = int(traj[i, j, 1])
        new_idx2 = int(traj[i, j, 2])
        # Move voxels like particles
        new_data[new_idx0, new_idx1, new_idx2, j] += data0[idx0, idx1, idx2]
        count[new_idx0, new_idx1, new_idx2, j] += 1

# Normalize summed values with counts to attain mean
new_data[count != 0] /= count[count != 0]

# Save as nifti
img = nb.Nifti1Image(new_data, affine=nii1.affine, header=nii1.header)
nb.save(img, OUTFILE)

print("Finished.")
