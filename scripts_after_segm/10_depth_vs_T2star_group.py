"""Simple layer profile plots"""

import os
import numpy as np
import nibabel as nb
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

METRIC_X = [
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-05/T2s/13_nonlinaniso_smooth/sub-05_ses-T2s_part-mag_MEGRE_crop_ups2X_prepped_avg_composite_decayfixed_T2s_CURED_n1_s0pt5_r1pt0_g1.nii.gz",
    ]

METRIC_Y = [
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-05/segmentation/01_layers/sub-05_ses-T2s_segm_rim_HG_RH_v02_metric_equivol.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-05/segmentation/01_layers/sub-05_ses-T2s_segm_rim_HG_LH_v02_metric_equivol.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-05/segmentation/01_layers/sub-05_ses-T2s_segm_rim_CS_RH_v02_metric_equivol.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-05/segmentation/01_layers/sub-05_ses-T2s_segm_rim_CS_LH_v02_metric_equivol.nii.gz",
    ]

CHUNKS = [
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-05/segmentation/02_multilaterate/sub-05_ses-T2s_segm_rim_HG_RH_v02_multilaterate_perimeter_chunk.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-05/segmentation/02_multilaterate/sub-05_ses-T2s_segm_rim_HG_LH_v02_multilaterate_perimeter_chunk.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-05/segmentation/02_multilaterate/sub-05_ses-T2s_segm_rim_CS_RH_v02_multilaterate_perimeter_chunk.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-05/segmentation/02_multilaterate/sub-05_ses-T2s_segm_rim_CS_LH_v02_multilaterate_perimeter_chunk.nii.gz",
    ]

TAGS = ["Heschl's Gyrus Right", "Heschl's Gyrus Left",
        "Calcarine Sulcus Right", "Calcarine Sulcus Left"]

OUTDIR = "/home/faruk/data/DATA_MRI_NIFTI/derived/plots/11_depth_binned"
SUBJ_ID = "sub-05"

RANGE_X = (0, 1)
RANGE_Y = (20, 50)
DPI = 300
VOXEL_VOLUME = 0.173611 * 0.173611 * 0.175  # mm
VOXEL_VOLUME /= 1000  # mm^3 to cm^3
RANGE_CBAR = (0, 100)

# =============================================================================
# Output directory
if not os.path.exists(OUTDIR):
    os.makedirs(OUTDIR)
    print("  Output directory: {}\n".format(OUTDIR))

# for j in range(len(METRIC_X)):
for j in range(1):

    FIGURE_TAG = "depth"

    # Prepare figure
    fig, ax = plt.subplots(2, 2,  figsize=(1920*2/DPI, 1080*2/DPI), dpi=DPI)
    ax = ax.ravel()
    fig.suptitle(SUBJ_ID, x=0.03, y=0.99, color="darkgoldenrod")

    for i in range(len(CHUNKS)):
        # Load mask
        nii_mask = nb.load(CHUNKS[i])
        cells = np.asarray(nii_mask.dataobj)
        idx = cells > 0
        cells = np.asarray(nii_mask.dataobj)[idx]  # Reduce memory load
        nii_mask = np.unique(cells)
        nii_mask = nii_mask[1:]  # Remove columns with index 0

        # Load measurement
        nii_measure = nb.load(METRIC_X[j])
        depvar = np.asarray(nii_measure.dataobj)[idx]

        # Load normalized depth metric
        nii_indvar = nb.load(METRIC_Y[i])
        indvar = np.asarray(nii_indvar.dataobj)[idx]

        # Compute chunk volume
        nr_voxels = np.sum(idx)
        volume = nr_voxels * VOXEL_VOLUME

        # Digitize independent var. based on dependent varianble
        nr_bins = 11
        bins = np.linspace(RANGE_X[0], RANGE_X[1], nr_bins + 1)
        indvar_binned =  np.digitize(indvar, bins)
        idx_indvar = np.arange(nr_bins) + 0.5

        depvar_mean = np.zeros(nr_bins)
        depvar_std = np.zeros(nr_bins)
        for k, l in enumerate(np.unique(indvar_binned)):
            depvar_mean[k] = np.mean(depvar[indvar_binned == l])
            depvar_std[k] = np.std(depvar[indvar_binned == l])

        # -------------------------------------------------------------------------
        # Line plots
        panel = ax[i].errorbar(idx_indvar, depvar_mean, depvar_std, fmt="-o")

        # cb = fig.colorbar(panel[3], ax=ax[i], pad=0.03, shrink=0.65)
        # cb.ax.text(0, -25, "Nr.\nvoxels", rotation=0, color="dimgray",
        #            multialignment="center")
        # ax[i].set_xlim(RANGE_X)
        ax[i].set_ylim(RANGE_Y)
        ax[i].set_xlabel("Normalized cortical depth (equi-volume)"
                         "\n"
                         "0 = white matter border",
                         color="gray")
        ax[i].set_ylabel(r"T$_2^*$ (ms)")
        ax[i].set_title(r"{}, Volume = {:.1f} cm$^3$".format(TAGS[i], volume),
                        color="goldenrod")

        # -------------------------------------------------------------------------
        # # Plot mean line for independent variable (x axis)
        # indvar_avg = np.mean(indvar)
        # line_y = np.linspace(RANGE_Y[0], RANGE_Y[1], 10)
        # line_x = line_y * 0 + indvar_avg
        # ax[i].plot(line_x, line_y, '-', linewidth=1.5, color='dodgerblue',
        #            label=r"Mean depth = {:.1f}°".format(indvar_avg))

        # # Plot mean line for dependent variable (y axis)
        # depvar_avg = np.mean(depvar)
        # line_x = np.linspace(RANGE_X[0], RANGE_X[1], 2)
        # line_y = line_x * 0 + depvar_avg
        # ax[i].plot(line_x, line_y, '-', linewidth=1.5, color='firebrick',
        #            label=r"Mean T$_2^*$ = {:.2f} ms".format(depvar_avg))
        #
        # ax[i].legend(loc = "upper left", frameon=False)

    plt.tight_layout()
    plt.savefig(os.path.join(OUTDIR, "{}_{}".format(SUBJ_ID, FIGURE_TAG)))
    # plt.show()

print("Finished.\n")
