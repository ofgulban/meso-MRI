"""Simple layer profile plots"""

import os
import numpy as np
import nibabel as nb
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

# Measurement nifti
MEASURE = "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-05/T2s/12_T2star/sub-05_ses-T2s_part-mag_MEGRE_crop_ups2X_prepped_avg_composite_decayfixed_T2s.nii.gz"

# Depth files
DEPTHS = [
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-05/T1_wholebrain/05_layers_columns/HG_RH/sub-05_ses-T2s_MP2RAGE_uni_segm_rim_reg_v06_rim_HG_RH_metric_equivol.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-05/T1_wholebrain/05_layers_columns/HG_LH/sub-05_ses-T2s_MP2RAGE_uni_segm_rim_reg_v06_rim_HG_LH_metric_equivol.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-05/T1_wholebrain/05_layers_columns/CS_RH/sub-05_ses-T2s_MP2RAGE_uni_segm_rim_reg_v06_rim_CS_RH_metric_equivol.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-05/T1_wholebrain/05_layers_columns/CS_LH/sub-05_ses-T2s_MP2RAGE_uni_segm_rim_reg_v06_rim_CS_LH_metric_equivol.nii.gz",
    ]

# Columns
CHUNKS = [
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-05/T1_wholebrain/05_layers_columns/HG_RH/test_cells.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-05/T1_wholebrain/05_layers_columns/HG_LH/test_cells.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-05/T1_wholebrain/05_layers_columns/CS_RH/test_cells.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-05/T1_wholebrain/05_layers_columns/CS_LH/test_cells.nii.gz",
    ]

TAGS = ["Heschl's Gyrus Right", "Heschl's Gyrus Left",
        "Calcarine Sulcus Right", "Calcarine Sulcus Left"]

OUT_DIR = "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-05/T1_wholebrain/05_layers_columns/"
SUBJ_ID = "sub-05"
FIGURE_TAG = "depth"

RANGE = (20, 50)
DPI = 300
VOXEL_VOLUME = 0.173611 * 0.173611 * 0.175  # mm
VOXEL_VOLUME /= 1000  # cm

# =============================================================================
# Prepare figure
fig, ax = plt.subplots(2, 2,  figsize=(1920*2/DPI, 1080*2/DPI), dpi=DPI)
ax = ax.ravel()
fig.suptitle(SUBJ_ID, x=0.03, y=0.99, color="darkgoldenrod")

for i in range(len(CHUNKS)):
    # Load columns
    nii_cells = nb.load(CHUNKS[i])
    cells = np.asarray(nii_cells.dataobj)
    idx = cells > 0
    cells = np.asarray(nii_cells.dataobj)[idx]  # Reduce memory load
    idx_cells = np.unique(cells)
    idx_cells = idx_cells[1:]  # Remove columns with index 0

    # Load measurement
    nii_measure = nb.load(MEASURE)
    depvar = np.asarray(nii_measure.dataobj)[idx]

    # Load normalized depth metric
    nii_indvar = nb.load(DEPTHS[i])
    indvar = np.asarray(nii_indvar.dataobj)[idx]

    # Compute chunk volume
    nr_voxels = np.sum(idx)
    volume = nr_voxels * VOXEL_VOLUME

    # -------------------------------------------------------------------------
    # 2D histograms
    panel = ax[i].hist2d(indvar, depvar, bins=(200, 200), cmap=plt.cm.Greys,
                         vmin=0, vmax=100)

    cb = fig.colorbar(panel[3], ax=ax[i], pad=0.03, shrink=0.65)
    cb.ax.text(0, -25, "Nr.\nvoxels", rotation=0, color="dimgray",
               multialignment="center")
    ax[i].set_xlim((0, 1))
    ax[i].set_ylim(RANGE)
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
    # line_y = np.linspace(RANGE[0], RANGE[1], 10)
    # line_x = line_y * 0 + indvar_avg
    # ax[i].plot(line_x, line_y, '-', linewidth=1.5, color='dodgerblue',
    #            label=r"Mean depth = {:.1f}°".format(indvar_avg))

    # Plot mean line for dependent variable (y axis)
    depvar_avg = np.mean(depvar)
    line_x = np.linspace(0, 100, 2)
    line_y = line_x * 0 + depvar_avg
    ax[i].plot(line_x, line_y, '-', linewidth=1.5, color='firebrick',
               label=r"Mean T$_2^*$ = {:.2f} ms".format(depvar_avg))

    ax[i].legend(loc = "upper left", frameon=False)

plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "{}_{}".format(SUBJ_ID, FIGURE_TAG)))
# plt.show()

print("Finished.")
