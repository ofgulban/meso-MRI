"""Used for rendering frames as png files."""

import numpy as np
import nibabel as nb

FILE1 = "/home/faruk/data2/ISMRM-2022/anim-bigbrain/data/full16_100um_optbal_roi_roi_flat_150x150_voronoi_median_filter_11-11-1.nii.gz"

OUTFILE = "/home/faruk/data2/ISMRM-2022/anim-bigbrain/anim_prep/scene-bigbrain_staircase_shot-1.nii.gz"

# Data range
NR_STEPS = 24*2
NR_SECTIONS = 7

# =============================================================================
# Get data
nii = nb.load(FILE1)
data = nii.get_fdata()

# Prepare coordinates
dims = data.shape
nr_layers = dims[2]
coords_xyz = np.asarray(np.indices(dims))
coords_xyz = np.transpose(coords_xyz, [1, 2, 3, 0])

# Mask interpolation residuals
mask = np.min(data, axis=2)
mask = mask > 0
data[~mask, :] = 0

# -----------------------------------------------------------------------------
# Generate voxel indices
x = np.arange(0, dims[0])
y = np.arange(0, dims[1])
i, j = np.meshgrid(x, y)
i = (i - np.min(i[mask])) / (np.max(i[mask]) - np.min(i[mask]))
j = (j - np.min(j[mask])) / (np.max(j[mask]) - np.min(j[mask]))

# Compute dist
indices = np.stack((i, j), axis=2)
dist = indices[..., 0]  # select x
# dist = indices[..., 1]  # select y
dist[dist == 0] = np.min(dist[dist > 0])
dist[~mask] = 0

# Quantize dist
dist /= dist.max()
dist *= -NR_SECTIONS
dist = np.floor(dist)
dist[mask] = dist[mask] + NR_SECTIONS
dist = np.repeat(dist[..., None], dims[2], axis=2)

# -----------------------------------------------------------------------------
# New z coordinates
coords_new = np.copy(coords_xyz)
for i in range(1, NR_SECTIONS+1):
    coords_new[dist == i, 2] += i * nr_layers
coords_new = np.round(coords_new)

# -----------------------------------------------------------------------------
# Interpolate voxel particle tractories
print("Interpolating voxel particle trajectories...")
flat_xyz = np.reshape(coords_xyz, [np.prod(dims), 3])
flat_new = np.reshape(coords_new, [np.prod(dims), 3])
nr_voxels = np.prod(dims)

traj = np.zeros((nr_voxels, NR_STEPS, 3))
for i in range(nr_voxels):
    print("  {}/{}".format(i+1, nr_voxels), end="\r")
    traj[i, :, 0] = np.linspace(flat_xyz[i, 0], flat_new[i, 0], NR_STEPS)
    traj[i, :, 1] = np.linspace(flat_xyz[i, 1], flat_new[i, 1], NR_STEPS)
    traj[i, :, 2] = np.linspace(flat_xyz[i, 2], flat_new[i, 2], NR_STEPS)
print()

# -----------------------------------------------------------------------------
# Transform volume data
print("Transforming volume data...")
new_data = np.zeros([dims[0], dims[1], dims[2]*NR_SECTIONS, NR_STEPS])
count = np.copy(new_data)
for i in range(nr_voxels):
    print("  {}/{}".format(i+1, nr_voxels), end="\r")
    idx0 = int(traj[i, 0, 0])
    idx1 = int(traj[i, 0, 1])
    idx2 = int(traj[i, 0, 2])

    for j in range(NR_STEPS):
        new_idx0 = int(traj[i, j, 0])
        new_idx1 = int(traj[i, j, 1])
        new_idx2 = int(traj[i, j, 2])
        # Move voxels like particles
        new_data[new_idx0, new_idx1, new_idx2, j] += data[idx0, idx1, idx2]
        count[new_idx0, new_idx1, new_idx2, j] += 1
print()

# Normalize summed values with counts to attain mean
new_data[count != 0] /= count[count != 0]

# Save as nifti
img = nb.Nifti1Image(new_data, affine=nii.affine, header=nii.header)
nb.save(img, OUTFILE)

print("Finished.")
