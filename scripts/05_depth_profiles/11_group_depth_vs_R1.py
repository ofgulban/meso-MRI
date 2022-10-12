"""Simple layer profile plots for group results."""

import os
import numpy as np
import nibabel as nb
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

FIG_DATA = [
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/plots/24_depth_vs_R1/sub-01_depth_vs_R1.npy",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/plots/24_depth_vs_R1/sub-02_depth_vs_R1.npy",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/plots/24_depth_vs_R1/sub-03_depth_vs_R1.npy",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/plots/24_depth_vs_R1/sub-04_depth_vs_R1.npy",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/plots/24_depth_vs_R1/sub-05_depth_vs_R1.npy",
    ]

TAGS = ["Heschl's Gyrus Right", "Heschl's Gyrus Left",
        "Calcarine Sulcus Right", "Calcarine Sulcus Left"]

OUTDIR = "/home/faruk/data2/DATA_MRI_NIFTI/derived/plots/24_depth_vs_R1"
SUBJ_ID = "group"
FIGURE_TAG = "depth_vs_R1"

RANGE_X = (-0.7, 1.7)
RANGE_Y = (0.2, 1.2)
DPI = 300
NR_BINS = 48

# =============================================================================
# Output directory
if not os.path.exists(OUTDIR):
    os.makedirs(OUTDIR)
    print("  Output directory: {}\n".format(OUTDIR))

# -----------------------------------------------------------------------------
# Prepare figure
plt.style.use('dark_background')
fig, ax = plt.subplots(2, 2, figsize=(1920*2/DPI, 1080*2/DPI), dpi=DPI)
ax = ax.ravel()

for j in range(len(FIG_DATA)):  # Loop across individual subjects
    fig_data = np.load(FIG_DATA[j], allow_pickle=True).item()
    for i in range(len(TAGS)):  # Loop across ROIs

        # Collate measurements
        indvar = fig_data[TAGS[i]]["WM"]["Metric_x"]
        indvar = np.hstack([indvar, fig_data[TAGS[i]]["GM"]["Metric_x"]])
        indvar = np.hstack([indvar, fig_data[TAGS[i]]["CSF"]["Metric_x"]])

        depvar = fig_data[TAGS[i]]["WM"]["Metric_y"]
        depvar = np.hstack([depvar, fig_data[TAGS[i]]["GM"]["Metric_y"]])
        depvar = np.hstack([depvar, fig_data[TAGS[i]]["CSF"]["Metric_y"]])

        # Digitize independent var. based on dependent variable
        bins = np.linspace(RANGE_X[0], RANGE_X[1], NR_BINS + 1)
        depvar_median = np.zeros(NR_BINS)
        depvar_lobo = np.zeros(NR_BINS)
        depvar_hibo = np.zeros(NR_BINS)
        depvar_std = np.zeros(NR_BINS)
        depvar_ste = np.zeros(NR_BINS)
        for k in range(NR_BINS):
            idx1 = indvar > bins[k]
            idx2 = indvar < bins[k+1]
            idx3 = idx1 * idx2
            if np.sum(idx3) > 2000:
                depvar_median[k] = np.median(depvar[idx3])
                depvar_lobo[k], depvar_hibo[k] = np.percentile(depvar[idx3],
                                                               [5, 95])
                depvar_std[k] = np.std(depvar[idx3])
                depvar_ste[k] = (np.std(depvar[idx3])
                                 / np.sqrt(np.size(np.std(depvar[idx3]))))
            else:
                depvar_median[k] = None
                depvar_lobo[k] = None
                depvar_hibo[k] = None
                depvar_std[k] = None
                depvar_ste[k] = None

        # ---------------------------------------------------------------------
        # Line plots
        ax[i].plot(bins[:-1] + (bins[1] - bins[0]) / 2, depvar_lobo,
                   linewidth=0.5, color=[66/255, 122/255, 183/255])
        ax[i].plot(bins[:-1] + (bins[1] - bins[0]) / 2, depvar_hibo,
                   linewidth=0.5, color=[66/255, 122/255, 183/255])
        ax[i].plot(bins[:-1] + (bins[1] - bins[0]) / 2, depvar_median,
                   linewidth=0.5, color="white")

for i in range(4):
    ax[i].set_title(r"{}".format(TAGS[i]), color="white")
    ax[i].set_title(TAGS[i])
    ax[i].set_ylabel(r"R$_1$ [ms]")
    ax[i].set_ylim(RANGE_Y)

    # X axis break points
    ax[i].plot((0, 0), (0, 4000), '-', linewidth=1.5,
               color=[100/255, 149/255, 237/255])
    ax[i].plot((1, 1), (0, 4000), '-', linewidth=1.5,
               color=[255/255, 102/255, 0/255])

    # Custom tick labels
    ax[i].set_xticks([-0.7, -0.35, -0.01, 0.01, 0.5, 0.99, 1.01, 1.35, 1.7])
    ax[i].set_xticklabels([0.7, 0.35, None, 0, 0.5, 1, None, 0.35, 0.7])
    yticks = np.linspace(RANGE_Y[0], RANGE_Y[1], 6, dtype=np.float32)
    ax[i].set_yticks(yticks)
    ax[i].set_yticklabels(yticks)

    # Add text (positions are in data coordinates)
    ypos = yticks[-2]
    ax[i].text(-0.7 + 0.025, ypos, 'Below\ngray matter\n(White matter)',
               fontsize=10, color="white")
    ax[i].text(0 + 0.025, ypos, 'Gray matter\n\n',
               fontsize=10, color="white")
    ax[i].text(1 + 0.025, ypos, 'Above\ngray matter\n(CSF & vessels)',
               fontsize=10, color="white")

    # Add text (units)
    ypos = yticks[0] + (yticks[1] - yticks[0]) / 10
    ax[i].text(-0.7 + 0.025, ypos, 'Distance [mm]',
               fontsize=10, color="white")
    ax[i].text(0 + 0.025, ypos, 'Equi-volume depths',
               fontsize=10, color="white")
    ax[i].text(1 + 0.025, ypos, 'Distance [mm]',
               fontsize=10, color="white")

plt.tight_layout()
plt.savefig(os.path.join(OUTDIR, "{}_{}".format(SUBJ_ID, FIGURE_TAG)))

print("Finished.\n")
