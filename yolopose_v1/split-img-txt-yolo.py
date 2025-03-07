import os
import random
import shutil
from collections import defaultdict

# Update this to the folder that contains both your .txt and image files.
folder_path = 'cvat-export-yolo-210frames'

# Define the output directories for images and labels.
output_images_dir = os.path.join(folder_path, 'images')
output_labels_dir = os.path.join(folder_path, 'labels')

# Create the directory structure: images/train, images/val, images/test,
# and labels/train, labels/val, labels/test.
for split in ['train', 'val', 'test']:
    os.makedirs(os.path.join(output_images_dir, split), exist_ok=True)
    os.makedirs(os.path.join(output_labels_dir, split), exist_ok=True)

# List all .txt files in the folder.
txt_files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]

# Define a list of possible image extensions.
image_extensions = ['.jpg', '.jpeg', '.png']

# Group the files by video id.
# Assumes the file name format is something like: 52807_1_44.txt,
# where "52807_1" is the video id.
video_groups = defaultdict(list)
for txt_file in txt_files:
    base_name = os.path.splitext(txt_file)[0]  # e.g., "52807_1_44"
    parts = base_name.split('_')
    if len(parts) < 2:
        continue  # skip if the format is unexpected
    video_id = "_".join(parts[:2])  # e.g., "52807_1"
    video_groups[video_id].append(txt_file)

# Get unique video IDs and shuffle them for random splitting.
video_ids = list(video_groups.keys())
random.shuffle(video_ids)

total_videos = len(video_ids)
train_count = int(total_videos * 0.70)
val_count = int(total_videos * 0.15)
# Assign the remaining videos to test.
test_count = total_videos - train_count - val_count

# Split the video ids into train, val, and test sets.
train_video_ids = video_ids[:train_count]
val_video_ids = video_ids[train_count:train_count+val_count]
test_video_ids = video_ids[train_count+val_count:]

def copy_files(video_ids, split):
    images_count = 0
    labels_count = 0
    for vid in video_ids:
        # For each video id, get the corresponding label (txt) files.
        for txt_file in video_groups[vid]:
            # Copy the label file.
            src_label = os.path.join(folder_path, txt_file)
            dest_label = os.path.join(output_labels_dir, split, txt_file)
            shutil.copy(src_label, dest_label)
            labels_count += 1

            # Look for the corresponding image file (same base name with a valid extension).
            base_name = os.path.splitext(txt_file)[0]
            found_image = None
            for ext in image_extensions:
                image_file = base_name + ext
                image_path = os.path.join(folder_path, image_file)
                if os.path.exists(image_path):
                    found_image = image_file
                    break
            if found_image:
                src_image = os.path.join(folder_path, found_image)
                dest_image = os.path.join(output_images_dir, split, found_image)
                shutil.copy(src_image, dest_image)
                images_count += 1
            else:
                print(f"Warning: Image file for {txt_file} not found.")
    return images_count, labels_count

# Copy files for each split.
train_images, train_labels = copy_files(train_video_ids, 'train')
val_images, val_labels = copy_files(val_video_ids, 'val')
test_images, test_labels = copy_files(test_video_ids, 'test')

# Print the counts for each split.
print(f"Train set: {train_labels} label files and {train_images} image files from {len(train_video_ids)} videos")
print(f"Validation set: {val_labels} label files and {val_images} image files from {len(val_video_ids)} videos")
print(f"Test set: {test_labels} label files and {test_images} image files from {len(test_video_ids)} videos")
