"""Simple layer profile plots"""

import os
import numpy as np
import nibabel as nb
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

METRIC_X = "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-02/T2s/12_T2star/sub-02_ses-T2s_part-mag_MEGRE_crop_ups2X_prepped_avg_composite_decayfixed_T2s.nii.gz"

METRIC_Y = [
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-02/segmentation/07_beyond_gm_collate/sub-02_ses-T2s_segm_rim_HG_RH_v02_beyond_gm_distances_smooth.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-02/segmentation/07_beyond_gm_collate/sub-02_ses-T2s_segm_rim_HG_LH_v02_beyond_gm_distances_smooth.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-02/segmentation/07_beyond_gm_collate/sub-02_ses-T2s_segm_rim_CS_RH_v02_beyond_gm_distances_smooth.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-02/segmentation/07_beyond_gm_collate/sub-02_ses-T2s_segm_rim_CS_LH_v02_beyond_gm_distances_smooth.nii.gz",
    ]

CHUNKS = [
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-02/segmentation/05_beyond_gm_prep/sub-02_ses-T2s_segm_rim_HG_RH_v02_borderized_multilaterate_perimeter_chunk_voronoi_dilated.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-02/segmentation/05_beyond_gm_prep/sub-02_ses-T2s_segm_rim_HG_LH_v02_borderized_multilaterate_perimeter_chunk_voronoi_dilated.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-02/segmentation/05_beyond_gm_prep/sub-02_ses-T2s_segm_rim_CS_RH_v02_borderized_multilaterate_perimeter_chunk_voronoi_dilated.nii.gz",
    "/home/faruk/data2/DATA_MRI_NIFTI/derived/sub-02/segmentation/05_beyond_gm_prep/sub-02_ses-T2s_segm_rim_CS_LH_v02_borderized_multilaterate_perimeter_chunk_voronoi_dilated.nii.gz",
    ]

TAGS = ["Heschl's Gyrus Right", "Heschl's Gyrus Left",
        "Calcarine Sulcus Right", "Calcarine Sulcus Left"]

OUTDIR = "/home/faruk/data2/DATA_MRI_NIFTI/derived/plots/20_depth_vs_T2star"
SUBJ_ID = "sub-02"
FIGURE_TAG = "depth_vs_T2star"

RANGE_X = (-0.7, 1.7)
RANGE_Y = (10, 60)
DPI = 300
VOXEL_VOLUME = 0.173611 * 0.173611 * 0.175  # mm
VOXEL_VOLUME /= 1000  # mm^3 to cm^3
RANGE_CBAR = (0, 150)

# =============================================================================
# Output directory
if not os.path.exists(OUTDIR):
    os.makedirs(OUTDIR)
    print("  Output directory: {}\n".format(OUTDIR))

# -----------------------------------------------------------------------------
# Prepare figure data output for group figure
fig_data = dict()
fig_data["T2star"] = []
fig_data["Depth"] = []

# Prepare figure
fig, ax = plt.subplots(2, 2,  figsize=(1920*2/DPI, 1080*2/DPI), dpi=DPI)
ax = ax.ravel()
fig.suptitle(SUBJ_ID, x=0.03, y=0.99, color="darkgoldenrod")

for i in range(len(CHUNKS)):
    # Load columns
    nii_cells = nb.load(CHUNKS[i])
    cells = np.asarray(nii_cells.dataobj)
    idx = cells == 1
    cells = np.asarray(nii_cells.dataobj)[idx]  # Reduce memory load
    idx_cells = np.unique(cells)
    idx_cells = idx_cells[1:]  # Remove columns with index 0

    # Load measurement
    nii_measure = nb.load(METRIC_X)
    depvar = np.asarray(nii_measure.dataobj)[idx]

    # Load normalized depth metric
    nii_indvar = nb.load(METRIC_Y[i])
    indvar = np.asarray(nii_indvar.dataobj)[idx]

    # Compute chunk volume
    nr_voxels = np.sum(idx)
    volume = nr_voxels * VOXEL_VOLUME

    # Store plot data
    fig_data["T2star"].append(depvar)
    fig_data["Depth"].append(indvar)

    # -------------------------------------------------------------------------
    # 2D histograms
    panel = ax[i].hist2d(indvar, depvar, bins=(200, 200), cmap=plt.cm.Greys,
                         vmin=RANGE_CBAR[0], vmax=RANGE_CBAR[1])

    cb = fig.colorbar(panel[3], ax=ax[i], pad=0.03, shrink=0.65)
    cb.ax.text(0, -25, "Nr.\nvoxels", rotation=0, color="dimgray",
               multialignment="center")
    ax[i].set_xlim(RANGE_X)
    ax[i].set_ylim(RANGE_Y)
    ax[i].set_xlabel("Normalized cortical depth (equi-volume)"
                     "\n"
                     "0 = white matter border",
                     color="gray")
    ax[i].set_ylabel(r"T$_2^*$ (ms)")
    ax[i].set_title(r"{}, Volume = {:.1f} cm$^3$".format(TAGS[i], volume),
                    color="goldenrod")

    # -------------------------------------------------------------------------

    # Plot mean line for dependent variable (y axis)
    depvar_avg = np.mean(depvar)
    line_x = np.linspace(RANGE_X[0], RANGE_X[1], 2)
    line_y = line_x * 0 + depvar_avg
    ax[i].plot(line_x, line_y, '-', linewidth=1.5, color='firebrick',
               label=r"Mean T$_2^*$ = {:.2f} ms".format(depvar_avg))

    ax[i].legend(loc="upper left", frameon=False)

plt.tight_layout()
plt.savefig(os.path.join(OUTDIR, "{}_{}".format(SUBJ_ID, FIGURE_TAG)))
# plt.show()

# -------------------------------------------------------------------------
np.save(os.path.join(OUTDIR, "{}_{}".format(SUBJ_ID, FIGURE_TAG)), fig_data)

print("Finished.\n")
