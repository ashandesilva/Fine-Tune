

# Fine-Tune Pose Estimation Project

## Getting Started

To get started with this project, follow these steps:

1. **Clone the Repository**: Clone this repository to your local machine using:
   ```bash
   git clone <repository-url>
   ```

2. **Navigate to the Project Directory**: Change into the project directory:
   ```bash
   cd Fine-Tune
   ```

3. **Set Up a Virtual Environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

4. **Install Dependencies**: Install the required Python packages using the `requirements.txt` file:
   ```bash
   pip install -r requirements.txt
   ```

5. **Run Scripts**: You can now run the scripts provided in the repository. For example, to merge annotations, use:
   ```bash
   python merge_annotations.py --ann_files annotations_v1/Correct_n2_3_7_100.json annotations_v1/lumbar_3_7_dell_111.json --out annotations_v1/merged_coco.json
   ```

6. **Train the Model**: Open the `train.ipynb` notebook in Jupyter and follow the instructions to train the YOLOPose model.

Ensure that all paths in the scripts and notebooks are correctly set to your local environment.

This repository contains scripts and data for fine-tuning pose-estimation models on a custom dataset of human exercise frames. The dataset currently has two annotation sets:
- **Correct_n2_3_7_100** for correct form
- **lumbar_3_7_dell_111** for lumbar error

Both are in CVAT/COCO keypoint format.

---

## Folder Structure

```
Fine-Tune/
├── data_v1/
│   ├── Correct_n2_3_7_100/
│   │   ├── 52701_1_4.jpg
│   │   ├── 52701_1_9.jpg
│   │   └── ...
│   ├── lumbar_3_7_dell_111/
│   │   ├── 52701_1_14.jpg
│   │   ├── 52701_1_40.jpg
│   │   └── ...
│   └── README.md  # Documentation related to data
│
├── annotations_v1/
│   ├── Correct_n2_3_7_100.json
│   ├── lumbar_3_7_dell_111.json
│   ├── merged_coco.json          # Generated by merge_annotations.py
│   ├── train_coco.json           # Generated by split_train_val_test.py
│   ├── val_coco.json             # ...
│   ├── test_coco.json            # ...
│   └── README.md                 # Documentation related to annotations
│
├── merge_annotations.py          # Script to merge multiple JSON files
├── split_train_val_test.py       # Script to split into train/val/test
├── README.md                     # (This file)
└── ...
```

---

## Scripts

Since after running 
```bash
python split_train_val_test.py --merged_coco annotations_v1/merged_coco.json --out_dir annotations_v1 --train_ratio 0.7 --val_ratio 0.15 --test_ratio 0.15 --seed 42
```
the output was
```bash
Train set: 712 images, 156 annotations => annotations_v1\train_coco.json
Val set: 165 images, 0 annotations => annotations_v1\val_coco.json
Test set: 166 images, 54 annotations => annotations_v1\test_coco.json
```
Decided to change the merge_annotation.py file to filter out all images not in that set. This ensures that every image in the final JSON has at least one annotation.

### 1. `merge_annotations.py`
- **Purpose**: Merge multiple COCO annotation files into a single “merged_coco.json,” excluding images that have zero annotations.
- **Usage**:
  ```bash
  python merge_annotations.py \
    --ann_files annotations_v1/Correct_n2_3_7_100.json annotations_v1/lumbar_3_7_dell_111.json \
    --out annotations_v1/merged_coco.json
  ```
- **Notes**: 
  - It automatically offsets image/annotation IDs so there are no collisions.
  - It filters out images with zero annotations.
  - Next time you add new annotation files (e.g., more frames or more classes), 
just rerun the merge script (possibly with more --ann_files), then rerun the split script. 
You’ll get an updated set of train/val/test JSONs that keep frames from each video ID in the same subset.
   - __also in the output merge_coco.json the files image id will not go from 1 - 210 even though there are 210 annotaion in both files, since it skips imgs that are not annotated img id number may skip and start at 500.__
   - __From a training perspective: it’s not a problem. The COCO standard only cares that:__
      1. __Each image ID is unique.__
      2. __Each annotation references a valid image ID.__

### 2. `split_train_val_test.py`
- **Purpose**: Split the merged annotation file into train/val/test sets, ensuring all frames from the same video are placed in the same subset.
- **Usage**:
  ```bash
  python split_train_val_test.py \
    --merged_coco annotations_v1/merged_coco.json \
    --out_dir annotations_v1 \
    --train_ratio 0.7 \
    --val_ratio 0.15 \
    --test_ratio 0.15 \
    --seed 42
  ```
- **Notes**:
  - Splitting is based on the “video ID” extracted from the image filename (e.g., `52701_1` in `52701_1_4.jpg`).
  - Generates `train_coco.json`, `val_coco.json`, and `test_coco.json` in `annotations_v1/`.

---

## Usage Workflow

1. **Update or Add Annotations**  
   - Place new `.json` annotation files under `annotations_v1/` and corresponding images in `data_v1/<some_folder>/`.

2. **Merge**  
   - Run `merge_annotations.py` with all relevant `.json` files to create `merged_coco.json`.

3. **Split**  
   - Run `split_train_val_test.py` to produce `train_coco.json`, `val_coco.json`, and `test_coco.json`.  
   - These can be used for training your pose-estimation model (e.g., MMPose, YOLO-Pose, etc.).

---

## Future Planned Work

1. **GCN Classification Model**  
   - Utilize the final pose-estimation model outputs (joint coordinates) as input features for a Graph Convolutional Network to classify each exercise frame (correct form vs. lumbar error).
   - Potentially integrate temporal information (sequences of frames) for better classification accuracy.

2. **Semi-Supervised / Active Learning**  
   - Investigate whether unannotated frames can be used for model pretraining or pseudo-labeling to further increase accuracy.

3. **Additional Error Categories**  
   - Beyond lumbar rounding, incorporate more movement faults or posture misalignments into the annotation scheme.

4. **Real-Time Inference**  
   - Optimize the pose model for on-device or real-time inference, e.g., using ONNX or TensorRT.

5. **3D Pose / Multi-View**  
   - Explore 3D approaches if multiple camera angles become available, potentially improving occlusion handling.


