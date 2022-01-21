# Mesoscopic quantification of cortical architecture in the living human brain

![fig-intro](https://user-images.githubusercontent.com/4668327/143470307-0b281a46-edc0-4e76-8c97-ac85cecceca1.png)

Data processing scripts for [Mesoscopic Quantification of Cortical Architecture in the Living Human Brain](https://doi.org/10.1101/2021.11.25.470023),

See <https://osf.io/n5bj7/> for the _Supplementary Data_, _Figures_, and _Animations_.
  
## Citation
- [Preprint] Gulban, O. F., Bollmann, S., Huber, R., Wagstyl, K., Goebel, R., Poser, B. A., Kay, K., & Ivanov, D. (2021). Mesoscopic Quantification of Cortical Architecture in the Living Human Brain. BioRxiv. <<https://doi.org/10.1101/2021.11.25.470023>>

## Dependencies

| Package                                                 | Tested version |
|---------------------------------------------------------|----------------|
| [LayNii](https://github.com/layerfMRI/LAYNII)           | 2.2.0          |
| [ITK-SNAP](http://www.itksnap.org/pmwiki/pmwiki.php)    | 3.8.0          |
| [c3d](http://www.itksnap.org/pmwiki/pmwiki.php?n=Downloads.C3D) | 1.1.0  |
| [greedy](https://sites.google.com/view/greedyreg/about) | 1.0.1          |
| [Python 3](https://www.python.org/)                     | 3.7.8          |
| - [NumPy](http://www.numpy.org/)                        | 1.15.4         |
| - [NiBabel](http://nipy.org/nibabel/)                   | 2.5.1          |
| - [matplotlib](http://matplotlib.org/)                  | 3.1.1          |

## Data processing overview
Please refer to the Methods section of my paper, and the flowcharts inluded here to see what each python script is doing.

### MEGRE data
![MEGRE](/flowcharts/flowchart-MEGRE.png)

### MP2RAGE data
![MP2RAGE](/flowcharts/flowchart-MP2RAGE.png)

# License
The project is licensed under [BSD-3-Clause](https://opensource.org/licenses/BSD-3-Clause).
