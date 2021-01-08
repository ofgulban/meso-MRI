"""Plot timeseries data based on segmentations."""

import numpy as np
import nibabel as nb
import matplotlib.pyplot as plt

nii1 = nb.load('/media/Data_Drive/ISILON/502_VESSELS_9PT4T/interses/sub-01_interses_avg.nii.gz')
nii2 = nb.load('/media/Data_Drive/ISILON/502_VESSELS_9PT4T/interses/rHG_segmentation_03.nii.gz')

# Load data
ts = nii1.get_data()
segm = nii2.get_data()

# Derivatives
classes = np.unique(segm)
classes = classes[1:]  # discard zeros
nr_classes = len(classes)

# Separate timeseries
dims = ts.shape
s_avg = np.zeros([classes.size, dims[-1]])
s_med = np.zeros(s_avg.shape)
s_std = np.zeros(s_avg.shape)

for i, c in enumerate(classes):
    idx = segm == c
    voxels = ts[idx, :]
    s_avg[i, :] = np.nanmean(voxels, axis=0)
    s_med[i, :] = np.nanmedian(voxels, axis=0)
    s_std[i, :] = np.std(voxels, axis=0)


# =============================================================================
plt.ioff()  # turn off interactive mode
plt.style.use('dark_background')

L = [["Gray matter", (0.5, 0.5, 0.5)],
     ["White matter", (0.8, 0.8, 0.8)],
     ["Artery (big)", (1, 0, 0)],
     ["Vein (big)", (0, 0, 1)],
     ["Intracortical vessel", (0, 1, 0)],
     ["Cerebrospinal fluid", (1, 1, 0)]
     ]

W = 3
TE = [4.7, 8.7, 12.8, 16.8, 20.8, 24.8]  # Echo times in ms

# -----------------------------------------------------------------------------
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(16, 11))
ax = axes.ravel()

for i in range(nr_classes):
    ax[0].plot(s_avg[i, :], linewidth=W, marker="o", markeredgecolor="white",
               label=L[i][0], color=L[i][1])
ax[0].set_xticks(np.arange(nr_classes))
ax[0].set_xticklabels(TE)
ax[0].set_xlabel('Echo time (ms)')
ax[0].set_ylabel('Signal intensity')
ax[0].set_ylim(0., 0.75)
ax[0].set_title("Mean")
ax[0].legend()
# -----------------------------------------------------------------------------
# for i in range(len(classes)):
#     ax[1].plot(s_med[i, :], linewidth=W, marker="o", markeredgecolor="white",
#                label=L[i][0], color=L[i][1])
# ax[1].set_xticks(np.arange(nr_classes))
# ax[1].set_xticklabels(TE)
# ax[1].set_xlabel('Echo time (ms)')
# ax[1].set_ylabel('Signal intensity')
# ax[1].set_ylim(0., 0.75)
# ax[1].set_title("Median")

# -----------------------------------------------------------------------------
for i in range(len(classes)):
    ax[1].plot(s_std[i, :], linewidth=W, marker="o", markeredgecolor="white",
               label=L[i][0], color=L[i][1])
ax[1].set_xticks(np.arange(nr_classes))
ax[1].set_xticklabels(TE)
ax[1].set_xlabel('Echo time (ms)')
ax[1].set_ylabel('Signal intensity')
ax[1].set_ylim(0., 0.75)
ax[1].set_title("Standard deviation")

plt.show()
# plt.close("all")
