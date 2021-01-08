"""Merge various segmentations in order."""

import nibabel as nb

nii1 = nb.load('/media/Data_Drive/ISILON/502_VESSELS_9PT4T/interses/rHG_gm_01.nii.gz')
nii2 = nb.load('/media/Data_Drive/ISILON/502_VESSELS_9PT4T/interses/rHG_wm_01.nii.gz')
nii3 = nb.load('/media/Data_Drive/ISILON/502_VESSELS_9PT4T/interses/rHG_arteries_01.nii.gz')
nii4 = nb.load('/media/Data_Drive/ISILON/502_VESSELS_9PT4T/interses/rHG_veins_01.nii.gz')
nii5 = nb.load('/media/Data_Drive/ISILON/502_VESSELS_9PT4T/interses/rHG_vessel_intracort_01.nii.gz')


new_data = nii1.get_data()
new_data[nii2.get_data() > 0] = 2
new_data[nii3.get_data() > 0] = 3
new_data[nii4.get_data() > 0] = 4
new_data[nii5.get_data() > 0] = 5

out = nb.Nifti1Image(new_data, affine=nii1.affine, header=nii1.header)
nb.save(out, '/media/Data_Drive/ISILON/502_VESSELS_9PT4T/interses/rHG_segmentation_02.nii.gz')
