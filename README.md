# MSc Thesis Lane Rotation
This repository contains code written in partial fulfilment of the requirements for the degree of Master of Science for the Graduate Program in Geomatics Engineering at the University of Calgary.

Thesis Title: A Robust Structure-Aware Arc-Length Parameterization Framework for 3D Lane Reconstruction <br>
Author: Jett Douglas Penner <br>
Supervisor: Dr. Naser El-Sheimy <br>
Date: December 2025 <br>
Version: 1.0 <br>

## Repository Details
This repository contains the full implementation used for my Master’s thesis on projecting 2D lane detections into 3D space using camera intrinsics and LiDAR depth sampling, based on the ONCE and 
ONCE-3DLanes public datasets.

The codebase is divided into two primary components:
1. Dataset Loader & Preprocessing (`dataset_loader/`)
    - Loads ONCE and ONCE-3DLanes datasets
    - Performs preprocessing steps
    - Generates unified output folders for downstream operation

2. Lane Projection & Thesis Implementation (`lane_projection/`)
    - Loads the unified output data
    - Contains the full mathematical framework for 2D-to-3D projection (for thesis and comparative approaches)
    - Perform analysis for evaluation in the thesis

## Repository Structure
```
msc-thesis-lane-projection/
│
├── README.md                 ← (this file)
├── .gitignore
│
├── dataset_loader/
│   ├── README.md
|   ├── requirements.txt
|   ├── config.yaml
│   └── once_loader.ipynb
│
└── lane_projection/
    ├── README.md
    ├── requirements.txt
    ├── once_config.yaml
    ├── main_runner.ipynb
    ├── postfilter_outliers.ipynb
    ├── results_compiler.ipynb
    ├── analysis.ipynb
    └── logger.py
```

No dataset files are included in this repository. <br>
Users must download ONCE and ONCE-3DLanes separately due to size constraints. <br>
Dataset installation and integration can be found in `dataset_loader/README.md`

## Dataset Descriptions
### 1. ONCE Dataset
Download page:
```https://once-for-auto-driving.github.io/download.html```

Required components:
- Annotation data
- Lidar roof data
- cam01 data

Any of the dataset splits may be used. This thesis was performed using the test, validation, and train dataset splits. <br>
The unlabeled splits were not used in the thesis investigation, as the existing splits were sufficient. 

Camera data is only used for visualization. Only cam01 data is needed from the camera sets (only cam01 data is used in the ONCE-3DLanes dataset).

### 2. ONCE-3DLanes Dataset
Download page:
```https://once-3dlanes.github.io/3dlanes```

All components are required:
- Data lists
- cam01 data (containing per-lane sequential 3D lane anchors and a precise calibration matrix).

## Running the Program
First, the dataset loader is run to perform loading and preprocessing operations. Details can be found in `dataset_loader/README.md`. 
Afterwards, the lane projection is run to perform lane projection operations and various analytics. Details can be found in `lane_projection/README.md`.

### Dataset Loader
This code:
- Validates the downloads and datastructure
- Loads the data
- Performs preprocessing tasks (including reconfiguring 3D GT data)
- Generates 2D detection inputs
- Outputs the files:
  - preprocessed 3D GT achors
  - generated 2D anchors
  - generated calibration files
  - converted camera images
  - duplicated lidar files

### Lane Projection
This code:
- Loads the data (from the output of dataset loader)
- Performs 2D-to-3D lane projection
  - Thesis-based projection
  - Pinhole camera + constant height projection
  - Pinhole camera + ground plane projection
  - LiDAR matching
  - Pinhole camera + ground plane + LiDAR interpolation projection
- (Optional) analyzes runtime metrics
- Performs postfiltering (removing inaccurate detections across all solutions)
- Compiles results (for computational ease of analysis)
- Performs analysis, generating various reports and graphs (hard-coded to thesis results)

## Citation
This code cannot be used for commercial purposes without explicit permission from the author, Jett Penner. <br>
This code may be used for research purposes provided that the following citation is included:

```
ERROR: Undefined Reference
```

Additionally, if this code is used, please cite the ONCE and ONCE-3DLanes datasets as required by their licenses.
