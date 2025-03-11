## How to Fine Tune Yolo Pose form new annotaions

#### Create annotations_v3
- add latest json files [ correct and lumbar both] into folder
#### Create data_v3
- add data wchich are being used in cvat task [ all 579 coorect and 467 lumbar]

#### Filter and Merge Annotaion JSON
- Use __merge_annotations.py__ to filter images that are only annotated in coco json files and merge all only annotated data into a new json file __annotations_v3\merged_coco.json__

#### Filter and Merge Images to a new folder
- Use __select_and_copy_images.py__ to filter images that are in the new merged COCO json file wchich are the only images that and annotated currently and copy those images from both correct and lumbar folders and paste them into __data_v3\merged__

#### Create CVAT task to export annotations in ultralytics_yolo_pose_1.0 format
- Use images in __data_v3\merged__ to create the task 
- Import annotations to the task. Use __annotations_v3\merged_coco.json__
- Export annotation in __ultralytics_yolo_pose_1.0__ format

#### Prepare folder containing both images and labels in yolopose_v3\ultralytics_yolo_pose_1.0_526
- This export has some files and 2 folders, images and labels
- Manualy create a new folder [yolopose_v3\ultralytics_yolo_pose_1.0_526] and copy paste both images and labels into this folder

#### Split Train Val Test for both images and labels
- Use __yolopose_v3\split-img-txt-yolo.py__ Split data both images and labels into Train Test Val in seperate folders
- This will create yolopose_v3\data\images and yolopose_v3\data\labels



