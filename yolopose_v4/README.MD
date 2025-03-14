## How to Fine Tune Yolo Pose with GPU

### ERROR [didnt start training with GPU]

even when
```
import torch
print(torch.cuda.is_available())
print(torch.cuda.get_device_name(0))
print(torch.version.cuda)  # Check CUDA version PyTorch was built with
print(torch.backends.cudnn.version())  # Check cuDNN version
print(torch.cuda.device_count())
```
were
```
True
NVIDIA GeForce RTX 2060
12.6
90501
1
```
---

```
ERROR
OutOfMemoryError: CUDA out of memory. Tried to allocate 20.00 MiB. GPU 0 has a total capacity of 6.00 GiB of which 4.75 GiB is free. Of the allocated memory 193.84 MiB is allocated by PyTorch, and 24.16 MiB is reserved by PyTorch but unallocated. If reserved but unallocated memory is large try setting PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True to avoid fragmentation
```
Explanation:
```
    Reserved vs. Allocated: “Reserved” means PyTorch’s allocator has claimed memory from the OS driver but not given it to a specific tensor. “Allocated” memory is currently in use by tensors.
    Fragmentation: If you see repeated out-of-memory errors with plenty of “reserved but unallocated” memory, fragmentation might be to blame. Turning on expandable_segments:True often helps.
    Normal Behavior: Some amount of “reserved but unallocated” memory is normal and can even improve performance. It’s only a concern if you’re hitting OOM or fragmentation issues regularly.
```

By combining environment variable tweaks, smaller memory demands, and manual cache clearing in your workflow, you can typically avoid or minimize “reserved but unallocated” memory leading to out-of-memory issues.


### Enable Expandable Segments


#### how to set the PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True environment variable manually

### Windows (Persistent via System Settings)

If you’d like to set it permanently in Windows system settings (so that it’s always available, no matter which terminal or environment you open):

    Press Win + R, type SystemPropertiesAdvanced, and press Enter.
    Click Environment Variables.
    Under System variables (or User variables if you only want it for your user account), click New....
    In the dialog, set:
        Variable name: PYTORCH_CUDA_ALLOC_CONF
        Variable value: expandable_segments:True
    Click OK to save.
    Close and reopen any Command Prompt or PowerShell window for the changes to take effect.


### OR Windows (One-Time)
Windows (Command Prompt, One-Time)
If you’re using the classic Command Prompt (cmd.exe), you can do:

    Open cmd.exe.
    Run:

set PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True

Run your Python script from the same Command Prompt window:

    python your_script.py

    Once you close that Command Prompt session, the variable goes away.

Windows (PowerShell, One-Time)

If you’re using PowerShell:

    Open PowerShell.
    Run:

$env:PYTORCH_CUDA_ALLOC_CONF="expandable_segments:True"

Then run your Python code in that same window.


### double check in python

```
import os
print(os.environ.get("PYTORCH_CUDA_ALLOC_CONF"))
```
should be - expandable_segments:True

If you see the correct value, your environment variable has been set successfully. Then PyTorch will enable the “expandable segments” caching strategy, which can help reduce memory fragmentation issues.

- PyTorch provides an option to reduce fragmentation by splitting GPU memory into multiple “expandable segments.” Set this environment variable before starting Python
- This helps reduce fragmentation by letting each segment expand or contract more flexibly.

- nvidia-smi on terminal

#### Clear the Allocator Cache Manually

```
import gc
import torch

# Remove references to any big tensors:
del big_tensor  # or any unneeded large variables
gc.collect()

# Clear PyTorch cache
torch.cuda.empty_cache()
```
    -  del big_tensor ensures that Python itself does not keep references to large tensors.
    - gc.collect() forces Python’s garbage collector to dispose of any unreferenced objects.
    - torch.cuda.empty_cache() tells PyTorch’s caching allocator to release all unused cached memory back to the driver.

- Note: Even after calling torch.cuda.empty_cache(), the next allocation might cause PyTorch to “reserve” memory again. This is normal; the cache system is designed to speed up repeated allocations.


---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---
---



## How to Fine Tune Yolo Pose form new annotaions

#### Create annotations_v3
- add latest json files [ correct and lumbar both] into folder
#### Create data_v3
- add data wchich are being used in cvat task [ all 579 coorect and 467 lumbar]

#### Filter and Merge Annotaion JSON
- Use __merge_annotations.py__ to filter images that are only annotated in coco json files and merge all only annotated data into a new json file __annotations_v3\merged_coco.json__

#### Filter and Merge Images to a new folder
- Use __select_and_copy_images.py__ to filter images that are in the new merged COCO json file which are the only images that ane annotated currently and copy those images from both correct and lumbar folders and paste them into __data_v3\merged__

- annotations_v3\merged details Total annotations: 526 and __data_v3\merged__ image count must be the same

#### Create CVAT task to export annotations in ultralytics_yolo_pose_1.0 format
- Use images in __data_v3\merged__ to create the task 
- Import annotations to the task. Use __annotations_v3\merged_coco.json__
- Export annotation in __ultralytics_yolo_pose_1.0__ format

#### Prepare folder containing both images and labels in yolopose_v3\ultralytics_yolo_pose_1.0_526
- This export has some files and 2 folders, images and labels [images from data_v3\merged and labels from export]
- Manualy create a new folder [yolopose_v3\ultralytics_yolo_pose_1.0_526] and copy paste both images and labels into this folder

#### Split Train Val Test for both images and labels
- Use __split-img-txt-yolo.py__ Split data both images and labels into Train Test Val in seperate folders
- This will create yolopose_v3\data\images and yolopose_v3\data\labels
- save split details

#### Clean annotations
- Since yolo set annotations above 1 and below 0 as corupted this script __yolo_annot_correction.py__ will change any value abouve 1 and below 0 into 0 0 0

#### Fine Tune YOLO
- Run __yolopose_v3\train.ipynb__

