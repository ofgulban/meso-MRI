"""Read CSV to plot scatterplots."""

import csv
import numpy as np
import matplotlib.pyplot as plt
from adjustText import adjust_text

FILE1 = "/home/faruk/gdrive/paper-350_micron/paper_figures/revision-literature/Quantitative Novelty Table - T1 Summary.csv"
FILE2 = "/home/faruk/gdrive/paper-350_micron/paper_figures/revision-literature/Quantitative Novelty Table - T2 Summary.csv"

# =============================================================================
# Load data and prepare for plotting
with open(FILE1, 'r') as f:
    data1 = list(csv.reader(f, delimiter=","))
data1 = np.array(data1)
t1_annotations = list(data1[1:, 0])
t1_contrast = list(data1[1:, 1])
t1_throughput = data1[1:, 2].astype("int")
t1_output = data1[1:, 3].astype("int") / 1000

with open(FILE2, 'r') as f:
    data2 = list(csv.reader(f, delimiter=","))
data2 = np.array(data2)
t2_annotations = list(data2[1:, 0])
t2_contrast = list(data2[1:, 1])
t2_throughput = data2[1:, 2].astype("int")
t2_output = data2[1:, 3].astype("int") / 1000

# =============================================================================
# Plot
px = 1/plt.rcParams['figure.dpi']  # pixel in inches
fig, ax = plt.subplots(1, 2, figsize=(960*px, 540*px))

ax[0].scatter(t1_throughput, t1_output)
ax[0].set_title(r"$T_1$ contrast")
ax[0].set_xlabel("Data Troughput [voxels per ms]")
ax[0].set_ylabel("Data Output [billion voxels]")
ax[0].set_xlim((0, 65))
ax[0].set_ylim((-0.1, 1.1))

annot = []
for i, (j, k) in enumerate(zip(t1_annotations, t1_contrast)):
    annot.append(ax[0].text(t1_throughput[i], t1_output[i], j))
    # ax[0].text(t1_throughput[i]+2, t1_output[i]-0.05, k)

adjust_text(annot, arrowprops=dict(arrowstyle="->", color="#7F7F7F", lw=2),
            ax=fig.axes[0])


ax[1].scatter(t2_throughput, t2_output)
ax[1].set_title(r"$T_2$ contrast")
ax[1].set_xlabel("Data Troughput [voxels per ms]")
ax[1].set_ylabel("Data Output [billion voxels]")
ax[1].set_xlim((0, 65))
ax[1].set_ylim((-0.1, 1.1))

annot = []
for i, (j, k) in enumerate(zip(t2_annotations, t2_contrast)):
    annot.append(ax[1].text(t2_throughput[i], t2_output[i], j))
    # ax[0].text(t2_throughput[i]+2, t2_output[i]-0.05, k)

adjust_text(annot, arrowprops=dict(arrowstyle="->", color="#7F7F7F", lw=2),
            ax=fig.axes[1])

plt.tight_layout()
