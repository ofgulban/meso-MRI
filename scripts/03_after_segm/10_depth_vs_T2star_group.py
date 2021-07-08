"""Simple layer profile plots for group results."""

import os
import numpy as np
import nibabel as nb
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

FIG_DATA = [
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/plots/01_depth/sub-01_depth.npy",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/plots/01_depth/sub-02_depth.npy",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/plots/01_depth/sub-03_depth.npy",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/plots/01_depth/sub-04_depth.npy",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/plots/01_depth/sub-05_depth.npy",
]

TAGS = ["Heschl's Gyrus Right", "Heschl's Gyrus Left",
        "Calcarine Sulcus Right", "Calcarine Sulcus Left"]

OUTDIR = "/home/faruk/data2/DATA_MRI_NIFTI/derived/plots/01_depth"
SUBJ_ID = "group"
FIGURE_TAG = "depth"

RANGE_X = (0, 1)
RANGE_Y = (20, 50)
DPI = 300
NR_BINS = 21

# =============================================================================
# Output directory
if not os.path.exists(OUTDIR):
    os.makedirs(OUTDIR)
    print("  Output directory: {}\n".format(OUTDIR))

# -----------------------------------------------------------------------------
# Prepare figure
fig, ax = plt.subplots(2, 2, facecolor="#e1d89fff", figsize=(1920*2/DPI, 1080*2/DPI), dpi=DPI)
ax = ax.ravel()

for j in range(len(FIG_DATA)):  # Loop across individual subjects
    fig_data = np.load(FIG_DATA[j], allow_pickle=True).item()
    METRIC_X = fig_data["Depth"]
    METRIC_Y = fig_data["T2star"]
    for i in range(len(TAGS)):  # Loop across ROIs
        indvar = METRIC_X[i]
        depvar = METRIC_Y[i]

        # Digitize independent var. based on dependent variable
        bins = np.linspace(RANGE_X[0], RANGE_X[1], NR_BINS + 1)
        indvar_binned =  np.digitize(indvar, bins)
        idx_indvar = np.arange(NR_BINS)

        depvar_mean = np.zeros(NR_BINS)
        depvar_median = np.zeros(NR_BINS)
        depvar_std = np.zeros(NR_BINS)
        depvar_ste = np.zeros(NR_BINS)
        for k, l in enumerate(np.unique(indvar_binned)):
            depvar_mean[k] = np.mean(depvar[indvar_binned == l])
            depvar_median[k] = np.median(depvar[indvar_binned == l])

            depvar_std[k] = np.std(depvar[indvar_binned == l])
            depvar_ste[k] = np.std(depvar[indvar_binned == l]) / np.sqrt(np.size(np.std(depvar[indvar_binned == l])))

        # -------------------------------------------------------------------------
        # Line plots
        # panel = ax[i].errorbar(idx_indvar+j/10, depvar_mean, depvar_ste, fmt="-o")
        panel = ax[i].plot(bins[:-1] + (bins[1] - bins[0]) / 2, depvar_median,
                           linewidth=5)

# Configure plot elements
font = {'family': 'sans-serif',
        'color':  '#2c061fff',
        'weight': 'normal',
        'size': 18,
        }

for i in range(4):
    ax[i].set_ylim(RANGE_Y)
    ax[i].set_title(TAGS[i], fontdict=font)

ax[2].set_xlabel("Normalized cortical depth (equi-volume)"
                 "\n"
                 "0 = white matter border",
                 fontdict=font, fontsize=16)
ax[3].set_xlabel("Normalized cortical depth (equi-volume)"
                 "\n"
                 "0 = white matter border",
                 fontdict=font, fontsize=16)

ax[0].set_ylabel(r"T$_2^*$ (ms)", fontdict=font, fontsize=16)
ax[2].set_ylabel(r"T$_2^*$ (ms)", fontdict=font, fontsize=16)


plt.tight_layout()
plt.savefig(os.path.join(OUTDIR, "{}_{}".format(SUBJ_ID, FIGURE_TAG)),
            facecolor="white")
# plt.show()

print("Finished.\n")
