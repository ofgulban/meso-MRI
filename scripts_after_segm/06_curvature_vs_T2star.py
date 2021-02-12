"""Plot T2star vs B0 angular difference."""

import os
import numpy as np
import nibabel as nb
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

METRIC_Y = "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-03/segmentation/00_segmentation/sub-03_ses-T2s_part-mag_MEGRE_crop_ups2X_prepped_avg_composite_decayfixed_T2s.nii.gz"

METRIC_X = [
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-03/segmentation/01_layers/sub-03_ses-T2s_segm_rim_HG_RH_v02_curvature.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-03/segmentation/01_layers/sub-03_ses-T2s_segm_rim_HG_LH_v02_curvature.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-03/segmentation/01_layers/sub-03_ses-T2s_segm_rim_CS_RH_v02_curvature.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-03/segmentation/01_layers/sub-03_ses-T2s_segm_rim_CS_LH_v02_curvature.nii.gz",
    ]

CHUNKS = [
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-03/segmentation/02_multilaterate/sub-03_ses-T2s_segm_rim_HG_RH_v02_multilaterate_perimeter_chunk.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-03/segmentation/02_multilaterate/sub-03_ses-T2s_segm_rim_HG_LH_v02_multilaterate_perimeter_chunk.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-03/segmentation/02_multilaterate/sub-03_ses-T2s_segm_rim_CS_RH_v02_multilaterate_perimeter_chunk.nii.gz",
    "/home/faruk/data/DATA_MRI_NIFTI/derived/sub-03/segmentation/02_multilaterate/sub-03_ses-T2s_segm_rim_CS_LH_v02_multilaterate_perimeter_chunk.nii.gz",
    ]

TAGS = ["Heschl's Gyrus Right", "Heschl's Gyrus Left",
        "Calcarine Sulcus Right", "Calcarine Sulcus Left"]

OUTDIR = "/home/faruk/data/DATA_MRI_NIFTI/derived/plots/03_curvature"
SUBJ_ID = "sub-03"
FIGURE_TAG = "curvature"

RANGE_X = (-1, 1)
RANGE_Y = (20, 50)
DPI = 300
VOXEL_VOLUME = 0.173611 * 0.173611 * 0.175  # mm
VOXEL_VOLUME /= 1000  # cm

# =============================================================================
# Output directory
if not os.path.exists(OUTDIR):
    os.makedirs(OUTDIR)
    print("  Output directory: {}\n".format(OUTDIR))

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
    nii_depvar = nb.load(METRIC_Y)
    depvar = np.asarray(nii_depvar.dataobj)[idx]

    # Load metric
    nii_indvar = nb.load(METRIC_X[i])
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
    ax[i].set_xlim(RANGE_X)
    ax[i].set_ylim(RANGE_Y)
    ax[i].set_xlabel(r"Curvature"
                     "\n"
                     r"(-1: Sulcal fundi, +1: Gyral crown)",
                     color="gray")
    ax[i].set_ylabel(r"T$_2^*$ (ms)")
    ax[i].set_title(r"{}, Volume = {:.1f} cm$^3$".format(TAGS[i], volume),
                    color="goldenrod")

    # -------------------------------------------------------------------------
    # Plot mean line for independent variable (x axis)
    indvar_avg = np.mean(indvar)
    line_y = np.linspace(RANGE_Y[0], RANGE_Y[1], 10)
    line_x = line_y * 0 + indvar_avg
    ax[i].plot(line_x, line_y, '-', linewidth=1.5, color='dodgerblue',
               label=r"Mean curv. = {:.2f}".format(indvar_avg))

    # Plot mean line for dependent variable (y axis)
    depvar_avg = np.mean(depvar)
    line_x = np.linspace(RANGE_X[0], RANGE_X[1], 2)
    line_y = line_x * 0 + depvar_avg
    ax[i].plot(line_x, line_y, '-', linewidth=1.5, color='firebrick',
               label=r"Mean T$_2^*$ = {:.2f} ms".format(depvar_avg))

    # Draw legend
    ax[i].legend(loc = "upper left", frameon=False)

plt.tight_layout()
plt.savefig(os.path.join(OUTDIR, "{}_{}".format(SUBJ_ID, FIGURE_TAG)))
# plt.show()

print("Finished.")
