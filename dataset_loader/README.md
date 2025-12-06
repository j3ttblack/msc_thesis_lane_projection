# Dataset Loader
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

## Repository Structure
```
msc-thesis-lane-projection/
│
├── README.md
├── .gitignore
│
├── dataset_loader/
│   ├── README.md             ← (this file)
|   ├── requirements.txt
|   ├── config.yaml
│   └── once_loader.ipynb
│
└── lane_projection/
    ...
```
The loader is designed to be self-contained and requires no modification unless dataset paths change or alternate configuration variables are desired.

## Running the Program
Download the datasets, into the appropriate data format (as below). 
Reconfigure the config file to match the data download folders (if applicable).
Install the requirements.
Open the notebook `once_loader.ipynb` in Jupyter (or a Jupyter-compatible environment, such as Visual Studio Code's). <br>
Run all cells in sequential order.

## Dataset Descriptions
### 1. ONCE Dataset
Download page:
```https://once-for-auto-driving.github.io/download.html```

Required components:
- Annotation data
- Lidar roof data
- cam01 data

Any of the dataset splits may be used.

### 2. ONCE-3DLanes Dataset
Download page:
```https://once-3dlanes.github.io/3dlanes```

All components are required:
- Data lists
- cam01 data (containing per-lane sequential 3D lane anchors and a precise calibration matrix).

## Implementation Folder Structure
Below is an example of the folder structure with integrated datasets (as used in the thesis), using the ONCE dataset train/val/test splits.

```
dataset_loader/
├── README.md             ← (this file)
├── requirements.txt
├── config.yaml
├── once_loader.ipynb
├── cam01/                ← (ONCE)
│   ├── train/data/
|   |   └── <run id>/cam01/
|   |       └── <file id>.jpg
│   ├── val/...             (same as train)
│   └── test/...            (same as train)
├── infos/                ← (ONCE)
│   ├── train/data/
|   |   └── <run id>.json
│   ├── val/...             (same as train)
│   ├── test/...            (same as train)
├── lidar/                ← (ONCE)
│   ├── train/data/
|   |   └── <run id>/lidar_roof/
|   |       └── <file id>.bin
│   ├── val/                (same as train)
│   └── test/               (same as train)
├── origin_ONCE_3DLanes/ONCE_3DLanes/  ← (ONCE-3DLanes)
|   ├── list/
|   |   ├── train.txt
|   |   ├── val.txt
|   |   └── test.txt
|   ├── train/
|   |   └── <run id>/cam01/
|   |       └── <file id>.json
│   ├── val/                (same as train)
│   └── test/               (same as train)
└── output/               ← (generated)
    └── <run id>
        ├── calibration.json
        ├── detections_2d/
        |   └── <file id>.txt
        ├── detections_3d/
        |   └── <file id>_<lane index, 0+>.pcd
        ├── images/
        |   └── <file id>.png
        └── lidar/
            └── <file id>.bin
```

Note that the `output/` folder and nested data is generated; thus not needed at runtime.

## Config File Overview (config.yaml)

The YAML file contains four sections:
1. once_data: paths to the ONCE dataset (train/val/test).

2. once_3dlanes_data: path to the root ONCE-3DLanes dataset.

3. ground_plane_ransac: runtime hyperparameters for plane fitting.

4. projection_mapping: runtime hyperparameters for 2D-to-3D mapping.

5. output: output base directory and folders (for lidar, images, detections), and a boolean to overrite existing outtput.

Each entry has a brief inline comment documenting its purpose.
