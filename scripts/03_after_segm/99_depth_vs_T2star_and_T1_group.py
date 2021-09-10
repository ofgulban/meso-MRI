"""Simple layer profile plots for group results."""

import os
import numpy as np
import nibabel as nb
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

FIG_DATA_1 = [
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/plots/20_depth_vs_T2star/sub-01_depth_vs_T2star.npy",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/plots/20_depth_vs_T2star/sub-02_depth_vs_T2star.npy",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/plots/20_depth_vs_T2star/sub-03_depth_vs_T2star.npy",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/plots/20_depth_vs_T2star/sub-04_depth_vs_T2star.npy",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/plots/20_depth_vs_T2star/sub-05_depth_vs_T2star.npy",
    ]

FIG_DATA_2 = [
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/plots/21_depth_vs_T1/sub-01_depth_vs_T1.npy",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/plots/21_depth_vs_T1/sub-02_depth_vs_T1.npy",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/plots/21_depth_vs_T1/sub-03_depth_vs_T1.npy",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/plots/21_depth_vs_T1/sub-04_depth_vs_T1.npy",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/plots/21_depth_vs_T1/sub-05_depth_vs_T1.npy",
    ]


TAGS = ["Heschl's Gyrus Right", "Heschl's Gyrus Left",
        "Calcarine Sulcus Right", "Calcarine Sulcus Left"]

OUTDIR = "/home/faruk/data2/DATA_MRI_NIFTI/derived/plots/99_T2star_T1_all"
SUBJ_ID = "group"
FIGURE_TAG = "depth_vs_T2star_and_T1"

RANGE_X = (-0.7, 1.7)
RANGE_Y_1 = (0, 100)
RANGE_Y_2 = (400, 3800)
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
fig, ax1 = plt.subplots(2, 2, figsize=(1920*2/DPI, 1080*2/DPI), dpi=DPI)
ax1 = ax1.ravel()
ax2 = np.copy(ax1)

for j in range(len(FIG_DATA_1)):  # Loop across individual subjects
    fig_data_1 = np.load(FIG_DATA_1[j], allow_pickle=True).item()
    fig_data_2 = np.load(FIG_DATA_2[j], allow_pickle=True).item()
    for i in range(len(TAGS)):  # Loop across ROIs

        # Collate measurements
        indvar = fig_data_1[TAGS[i]]["WM"]["Metric_x"]
        indvar = np.hstack([indvar, fig_data_1[TAGS[i]]["GM"]["Metric_x"]])
        indvar = np.hstack([indvar, fig_data_1[TAGS[i]]["CSF"]["Metric_x"]])

        depvar1 = fig_data_1[TAGS[i]]["WM"]["Metric_y"]
        depvar1 = np.hstack([depvar1, fig_data_1[TAGS[i]]["GM"]["Metric_y"]])
        depvar1 = np.hstack([depvar1, fig_data_1[TAGS[i]]["CSF"]["Metric_y"]])

        depvar2 = fig_data_2[TAGS[i]]["WM"]["Metric_y"]
        depvar2 = np.hstack([depvar2, fig_data_2[TAGS[i]]["GM"]["Metric_y"]])
        depvar2 = np.hstack([depvar2, fig_data_2[TAGS[i]]["CSF"]["Metric_y"]])

        # Digitize independent var. based on dependent variable
        bins = np.linspace(RANGE_X[0], RANGE_X[1], NR_BINS + 1)
        depvar_median_1 = np.zeros(NR_BINS)
        depvar_median_2 = np.zeros(NR_BINS)
        for k in range(NR_BINS):
            idx1 = indvar > bins[k]
            idx2 = indvar < bins[k+1]
            idx3 = idx1 * idx2
            if np.sum(idx3) > 2000:
                depvar_median_1[k] = np.median(depvar1[idx3])
                depvar_median_2[k] = np.median(depvar2[idx3])
            else:
                depvar_median_1[k] = None
                depvar_median_2[k] = None

        # ---------------------------------------------------------------------
        # Line plots
        ax1[i].plot(bins[:-1] + (bins[1] - bins[0]) / 2, depvar_median_1,
                    linewidth=1, color="white")

        ax2[i] = ax1[i].twinx()  # instantiate a second y axis
        ax2[i].plot(bins[:-1] + (bins[1] - bins[0]) / 2, depvar_median_2,
                 linewidth=1, color="red")

        # NOTE: I dont get why but second y axis labels only work when done here
        ax2[i].set_ylabel(r"T$_1$ [ms]", color="red")
        ax2[i].set_ylim(RANGE_Y_2)
        ax2[i].set_yticks(np.linspace(RANGE_Y_2[0], RANGE_Y_2[1], 6,
                          dtype=np.int))
        ax2[i].set_yticklabels(np.linspace(RANGE_Y_2[0], RANGE_Y_2[1], 6,
                                          dtype=np.int), color="red")


for i in range(4):
    ax1[i].set_title(r"{}".format(TAGS[i]), color="white")
    ax1[i].set_title(TAGS[i])

    ax1[i].set_ylabel(r"T$_2^*$ [ms]")
    ax1[i].set_ylim(RANGE_Y_1)

    # X axis break points
    ax1[i].plot((0, 0), (0, 100), '-', linewidth=1.5,
               color=[100/255, 149/255, 237/255])
    ax1[i].plot((1, 1), (0, 100), '-', linewidth=1.5,
               color=[255/255, 102/255, 0/255])

    # Custom tick labels
    ax1[i].set_xticks([-0.7, -0.35, -0.01, 0.01, 0.5, 0.99, 1.01, 1.35, 1.7])
    ax1[i].set_xticklabels([0.7, 0.35, None, 0, 0.5, 1, None, 0.35, 0.7])

    ax1[i].set_yticks(np.linspace(RANGE_Y_1[0], RANGE_Y_1[1], 6, dtype=np.int))
    ax1[i].set_yticklabels(np.linspace(RANGE_Y_1[0], RANGE_Y_1[1], 6,
                                      dtype=np.int))

    # Add text (positions are in data coordinates)
    ax1[i].text(-0.7 + 0.025, 80, 'Below\ngray matter\n(White matter)',
               fontsize=10, color="white")
    ax1[i].text(0 + 0.025, 80, 'Gray matter\n\n',
               fontsize=10, color="white")
    ax1[i].text(1 + 0.025, 80, 'Above\ngray matter\n(CSF & vessels)',
               fontsize=10, color="white")

    # Add text (units)
    ax1[i].text(-0.7 + 0.025, 2, 'Distance [mm]',
               fontsize=10, color="white")
    ax1[i].text(0 + 0.025, 2, 'Equi-volume depths',
               fontsize=10, color="white")
    ax1[i].text(1 + 0.025, 2, 'Distance [mm]',
               fontsize=10, color="white")


plt.tight_layout()
plt.savefig(os.path.join(OUTDIR, "{}_{}".format(SUBJ_ID, FIGURE_TAG)))

print("Finished.\n")
