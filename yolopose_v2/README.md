# YOLOPose v2

When getting the dataset,
Use both lumbar and corect COCO export jsons and merge them and also merge all the images
then use the merges COCO json and the correct images from both correct and lumbar and create a new task in CVAT
them get an export in yolo format and use that dataset export to fine tune YOLO


This directory contains the implementation and resources for the YOLOPose v2 model, a variant of the YOLO model designed for pose estimation.

## Contents

- **train.ipynb**: A Jupyter Notebook used for training the YOLOPose model. It contains the code and instructions necessary to train the model on a dataset.

- **experiment/**: This directory is intended to store experimental results, configurations, or logs related to the training and evaluation of the model.

- **dataset.yaml**: A configuration file that specifies the dataset parameters, such as paths to training and validation data, class names, and other dataset-specific settings.

- **yolo_annot_correction.py**: A Python script for correcting annotations in the YOLO format. This script can be used to preprocess or adjust the dataset annotations before training.

- **data/**: This directory is expected to contain the datasets used for training and evaluation. It may include images, labels, and other related files.

- **yolo11m-pose.pt**: A pre-trained YOLOPose model file (medium size) in PyTorch format. This model can be used for inference or as a starting point for further training.

- **yolo11n-pose.pt**: A pre-trained YOLOPose model file (small size) in PyTorch format. This model is suitable for environments with limited computational resources.

## Usage

To train the model, open `train.ipynb` in Jupyter Notebook and follow the instructions provided. Ensure that the dataset is correctly configured in `dataset.yaml` and that all necessary dependencies are installed.

## Dependencies

Make sure to install the required Python packages before running the scripts or notebooks. You can typically do this using a `requirements.txt` file or by manually installing the packages listed in the notebook or scripts. 