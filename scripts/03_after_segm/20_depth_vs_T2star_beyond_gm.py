"""Simple layer profile plots"""

import os
import copy
import numpy as np
import nibabel as nb
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

SUBJ_ID = ["sub-01", "sub-02", "sub-03", "sub-04", "sub-05"]
OUTDIR = "/home/faruk/data2/DATA_MRI_NIFTI/derived/plots/20_depth_vs_T2star"
FIGURE_TAG = "depth_vs_T2star"

# =========================================================================
for s in SUBJ_ID:
    METRIC_X = [
        "/home/faruk/data2/DATA_MRI_NIFTI/derived/{}/segmentation/07_beyond_gm_collate/{}_ses-T2s_segm_rim_HG_RH_v02_beyond_gm_distances_smooth.nii.gz".format(s, s),
        "/home/faruk/data2/DATA_MRI_NIFTI/derived/{}/segmentation/07_beyond_gm_collate/{}_ses-T2s_segm_rim_HG_LH_v02_beyond_gm_distances_smooth.nii.gz".format(s, s),
        "/home/faruk/data2/DATA_MRI_NIFTI/derived/{}/segmentation/07_beyond_gm_collate/{}_ses-T2s_segm_rim_CS_RH_v02_beyond_gm_distances_smooth.nii.gz".format(s, s),
        "/home/faruk/data2/DATA_MRI_NIFTI/derived/{}/segmentation/07_beyond_gm_collate/{}_ses-T2s_segm_rim_CS_LH_v02_beyond_gm_distances_smooth.nii.gz".format(s, s),
        ]

    METRIC_Y = "/home/faruk/data2/DATA_MRI_NIFTI/derived/{}/T2s/12_T2star/{}_ses-T2s_part-mag_MEGRE_crop_ups2X_prepped_avg_composite_decayfixed_T2s.nii.gz".format(s, s)

    CHUNKS = [
        "/home/faruk/data2/DATA_MRI_NIFTI/derived/{}/segmentation/05_beyond_gm_prep/{}_ses-T2s_segm_rim_HG_RH_v02_borderized_multilaterate_perimeter_chunk_voronoi_dilated.nii.gz".format(s, s),
        "/home/faruk/data2/DATA_MRI_NIFTI/derived/{}/segmentation/05_beyond_gm_prep/{}_ses-T2s_segm_rim_HG_LH_v02_borderized_multilaterate_perimeter_chunk_voronoi_dilated.nii.gz".format(s, s),
        "/home/faruk/data2/DATA_MRI_NIFTI/derived/{}/segmentation/05_beyond_gm_prep/{}_ses-T2s_segm_rim_CS_RH_v02_borderized_multilaterate_perimeter_chunk_voronoi_dilated.nii.gz".format(s, s),
        "/home/faruk/data2/DATA_MRI_NIFTI/derived/{}/segmentation/05_beyond_gm_prep/{}_ses-T2s_segm_rim_CS_LH_v02_borderized_multilaterate_perimeter_chunk_voronoi_dilated.nii.gz".format(s, s),
        ]

    TAGS = ["Heschl's Gyrus Right", "Heschl's Gyrus Left",
            "Calcarine Sulcus Right", "Calcarine Sulcus Left"]

    RANGE_X = (-0.7, 1.7)
    RANGE_Y = (10, 60)
    DPI = 300
    VOXEL_VOLUME = 0.173611 * 0.173611 * 0.175  # mm
    VOXEL_VOLUME /= 1000  # mm^3 to cm^3
    RANGE_CBAR = (0, 150)

    # =========================================================================
    # Output directory
    if not os.path.exists(OUTDIR):
        os.makedirs(OUTDIR)
        print("  Output directory: {}\n".format(OUTDIR))

    # -------------------------------------------------------------------------
    # Prepare figure data output for group figure
    temp_data = {"WM": {}, "GM": {}, "CSF": {}}

    # Prepare data for histograms
    fig_data = dict()
    for i in range(len(CHUNKS)):
        # Load chunks to find relevant voxels
        nii_cells = nb.load(CHUNKS[i])
        cells = np.asarray(nii_cells.dataobj)
        idx = cells == 1

        # Load measurements
        nii_x = nb.load(METRIC_X[i])
        metric_x = np.asarray(nii_x.dataobj)[idx]
        nii_y = nb.load(METRIC_Y)
        metric_y = np.asarray(nii_y.dataobj)[idx]

        # Secondary indices to separate tissues
        idx2 = np.zeros((np.sum(idx), 3), dtype=np.bool)
        for j, k in enumerate(metric_x):
            if k < 0:  # WM
                idx2[j, 0] = True
            elif k > 1:  # CSF
                idx2[j, 2] = True
            else:  # GM
                idx2[j, 1] = True

        for j in range(3):
            # Compute sampled tissue volume
            nr_voxels = np.sum(idx2[:, j])
            volume = nr_voxels * VOXEL_VOLUME

            # -----------------------------------------------------------------
            # Prepare data structure that will be plotted
            if j == 0:
                temp_data["WM"]["Metric_x"] = metric_x[idx2[:, 0]]
                temp_data["WM"]["Metric_y"] = metric_y[idx2[:, 0]]
                temp_data["WM"]["Volume"] = volume

                nr_bins = 101
                axis_bins_x = np.linspace(RANGE_X[0], 0, nr_bins)
                axis_bins_y = np.linspace(RANGE_Y[0], RANGE_Y[1], nr_bins)
                axis_range_x = [RANGE_X[0], 0]
                img, xedges, yedges = np.histogram2d(
                    metric_x[idx2[:, 0]], metric_y[idx2[:, 0]],
                    bins=[axis_bins_x, axis_bins_y],
                    range=[axis_range_x, RANGE_Y],
                    density=False)
                temp_data["WM"]["Hist2D"] = img

            # -----------------------------------------------------------------
            elif j == 1:
                temp_data["GM"]["Metric_x"] = metric_x[idx2[:, 1]]
                temp_data["GM"]["Metric_y"] = metric_y[idx2[:, 1]]
                temp_data["GM"]["Volume"] = volume

                nr_bins = 101
                axis_bins_x = np.linspace(0, 1, nr_bins)
                axis_bins_y = np.linspace(RANGE_Y[0], RANGE_Y[1], nr_bins)
                axis_range_x = [0, 1]
                img, xedges, yedges = np.histogram2d(
                    metric_x[idx2[:, 1]], metric_y[idx2[:, 1]],
                    bins=[axis_bins_x, axis_bins_y],
                    range=[axis_range_x, RANGE_Y],
                    density=False)
                temp_data["GM"]["Hist2D"] = img

            # -----------------------------------------------------------------
            elif j == 2:
                temp_data["CSF"]["Metric_x"] = metric_x[idx2[:, 2]]
                temp_data["CSF"]["Metric_y"] = metric_y[idx2[:, 2]]
                temp_data["CSF"]["Volume"] = volume

                nr_bins = 101
                axis_bins_x = np.linspace(1, RANGE_X[1], nr_bins)
                axis_bins_y = np.linspace(RANGE_Y[0], RANGE_Y[1], nr_bins)
                axis_range_x = [1, RANGE_X[1]]
                img, xedges, yedges = np.histogram2d(
                    metric_x[idx2[:, 2]], metric_y[idx2[:, 2]],
                    bins=[axis_bins_x, axis_bins_y],
                    range=[axis_range_x, RANGE_Y],
                    density=False)
                temp_data["CSF"]["Hist2D"] = img

        fig_data[TAGS[i]] = copy.deepcopy(temp_data)

    # -------------------------------------------------------------------------
    # Prepare figure
    fig, ax = plt.subplots(2, 2,  figsize=(1920*2/DPI, 1080*2/DPI), dpi=DPI)
    ax = ax.ravel()
    fig.suptitle(s, x=0.95, y=0.99, color="Black")

    for i in range(len(CHUNKS)):

        img = np.zeros((300, 100))
        img[0:100, :] = fig_data[TAGS[i]]["WM"]["Hist2D"]
        img[100:200, :] = fig_data[TAGS[i]]["GM"]["Hist2D"]
        img[200:300, :] = fig_data[TAGS[i]]["CSF"]["Hist2D"]

        panel = ax[i].imshow(img.T, origin="lower", cmap="Greys",
                             interpolation="none", aspect="auto",
                             vmin=0, vmax=150, extent=(0, 300, 0, 100))

        # ax[i].tick_params(
        #     axis='y',
        #     which='both',  # both major and minor ticks are affected
        #     bottom=False, top=False,
        #     left=False, right=False,
        #     labelbottom=False,
        #     labelleft=False
        #     )

        cb = fig.colorbar(panel, ax=ax[i], pad=0.03, shrink=0.65)
        cb.ax.text(0, -25, "Nr.\nvoxels", rotation=0, color="dimgray",
                   multialignment="center")

        ax[i].set_title(r"{}".format(TAGS[i]),
                        color="gray")

        # ---------------------------------------------------------------------
        # Axis labels
        ax[i].set_ylabel(r"T$_2^*$ (ms)")

        # Plot median lines
        median_x = np.median(fig_data[TAGS[i]]["WM"]["Metric_y"])
        median_line_x = median_x + RANGE_Y[0]
        ax[i].plot((0, 100), (median_line_x, median_line_x),
                   '-', linewidth=1.5, color="red")
        ax[i].text(0+1, median_line_x + 1, '{:.1f}'.format(median_x),
                   fontsize=10, color="red")

        median_x = np.median(fig_data[TAGS[i]]["GM"]["Metric_y"])
        median_line_x = median_x + RANGE_Y[0]
        ax[i].plot((100, 200), (median_line_x, median_line_x),
                   '-', linewidth=1.5, color="red")
        ax[i].text(100+1, median_line_x + 1, '{:.1f}'.format(median_x),
                   fontsize=10, color="red")

        median_x = np.median(fig_data[TAGS[i]]["CSF"]["Metric_y"])
        median_line_x = median_x + RANGE_Y[0]
        ax[i].plot((200, 300), (median_line_x, median_line_x),
                   '-', linewidth=1.5, color="red")
        ax[i].text(200+1, median_line_x + 1, '{:.1f}'.format(median_x),
                   fontsize=10, color="red")

        # X axis break points
        ax[i].plot((100, 100), (0, 100), '-', linewidth=1.5,
                   color=[100/255, 149/255, 237/255])
        ax[i].plot((200, 200), (0, 100), '-', linewidth=1.5,
                   color=[255/255, 102/255, 0/255])

        # Custom tick labels
        ax[i].set_xticks([0, 50, 99, 101, 150, 199, 201, 250, 300])
        ax[i].set_xticklabels([1.4, 0.7, None, 0, 0.5, 1, None, 0.7, 1.4])
        ax[i].set_yticks([0, 20, 40, 60, 80, 100])
        ax[i].set_yticklabels([10, 20, 30, 40, 50, 60])

        # Add text (positions are in data coordinates)
        ax[i].text(0 + 1, 2, 'Below gray matter\n(White matter)', fontsize=10)
        ax[i].text(100 + 1, 2, 'Cortical gray matter\n', fontsize=10)
        ax[i].text(200 + 1, 2, 'Above gray matter\n(CSF and vessels)', fontsize=10)


    plt.tight_layout()
    plt.savefig(os.path.join(OUTDIR, "{}_{}".format(s, FIGURE_TAG)))
    # plt.show()

    # -------------------------------------------------------------------------
    np.save(os.path.join(OUTDIR, "{}_{}".format(s, FIGURE_TAG)), fig_data)

    print("Did it: {}".format(s))

print("Finished.\n")
