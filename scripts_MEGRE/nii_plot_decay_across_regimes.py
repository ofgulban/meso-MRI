"""Plot timeseries data based on segmentations."""

import numpy as np
import nibabel as nb
import matplotlib.pyplot as plt

nii1 = nb.load('/media/Data_Drive/ISILON/502_VESSELS_9PT4T/interses/sub-01_interses_avg.nii.gz')
nii2 = nb.load('/media/Data_Drive/ISILON/502_VESSELS_9PT4T/interses/rHG_segmentation_03.nii.gz')
nii3 = nb.load('/media/Data_Drive/ISILON/502_VESSELS_9PT4T/interses/rHG_signal_regimes.nii.gz')

# Load data
ts = nii1.get_data()
segm = nii2.get_data()
regi = nii3.get_data()

# Derivatives
classes = np.unique(segm)
classes = classes[1:]  # discard zeros
nr_classes = len(classes)
regimes = np.unique(regi)
regimes = regimes[1:]  # discard zeros
nr_regimes = len(regimes)

# Separate timeseries
dims = ts.shape
s_avg = np.zeros([nr_regimes, nr_classes, dims[-1]])
s_med = np.zeros(s_avg.shape)
s_std = np.zeros(s_avg.shape)

for j, r in enumerate(regimes):
    # Extract voxels in a regime
    temp1 = segm[regi == r]
    temp2 = ts[regi == r]
    for i, c in enumerate(classes):
        # Extract voxels of a class
        idx = temp1 == c
        # Extract timeseries
        voxels = temp2[idx, :]
        # Compute metrics
        s_avg[j, i, :] = np.nanmean(voxels, axis=0)
        s_med[j, i, :] = np.nanmedian(voxels, axis=0)
        s_std[j, i, :] = np.std(voxels, axis=0)


# =============================================================================
# Figure configuration
plt.ioff()  # turn off interactive mode
plt.style.use('dark_background')

TE = [4.7, 8.7, 12.8, 16.8, 20.8, 24.8]  # Echo times in ms
W = 2
L = [["Gray matter", (0.5, 0.5, 0.5)],
     ["White matter", (0.8, 0.8, 0.8)],
     ["Artery (big)", (1, 0, 0)],
     ["Vein (big)", (0, 0, 1)],
     ["Intracortical vessel", (0, 1, 0)],
     ["Cerebrospinal fluid", (1, 1, 0)]
     ]

# =============================================================================
# Plotting
fig, axes = plt.subplots(nrows=3, ncols=nr_regimes, figsize=(16, 11))
ax = axes.ravel()

ax[0].set_title(r"Coil surface distance = ~2 cm")
ax[1].set_title(r"Coil surface distance = ~2.8 cm")
ax[2].set_title(r"Coil surface distance = ~3.6 cm")
ax[3].set_title(r"Coil surface distance = ~4.4 cm")

# -----------------------------------------------------------------------------
ax[0].set_ylabel('Mean signal intensity')
ax[0].set_xlabel('Echo time (ms)')

for j in range(nr_regimes):
    for i in range(nr_classes):
        ax[j].plot(s_avg[j, i, :], linewidth=W,
                   marker="o", markeredgecolor="white",
                   label=L[i][0], color=L[i][1])
    ax[j].set_xticks(np.arange(nr_classes))
    ax[j].set_xticklabels(TE)
    ax[j].set_ylim(0., 1)
ax[j].legend()
# -----------------------------------------------------------------------------
o = 4  # plot index offset
ax[o].set_ylabel('Median signal intensity')
for j in range(nr_regimes):
    for i in range(nr_classes):
        ax[j+o].plot(s_med[j, i, :], linewidth=W,
                     marker="o", markeredgecolor="white",
                     label=L[i][0], color=L[i][1])
    ax[j+o].set_xticks(np.arange(nr_classes))
    ax[j+o].set_xticklabels(TE)
    ax[j+o].set_ylim(0., 1)

# -----------------------------------------------------------------------------
o = 8
ax[o].set_ylabel('Std. signal intensity')
for j in range(nr_regimes):
    for i in range(nr_classes):
        ax[j+o].plot(s_std[j, i, :], linewidth=W,
                     marker="o", markeredgecolor="white",
                     label=L[i][0], color=L[i][1])
    ax[j+o].set_xticks(np.arange(nr_classes))
    ax[j+o].set_xticklabels(TE)
    ax[j+o].set_ylim(0., 1)

plt.show()
# plt.close("all")
