import os
import random
from collections import defaultdict

# Set the folder path where your .txt files are located
folder_path = 'obj_train_data'  # update this to your actual folder path

# List all .txt files in the folder
txt_files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]

# Group files by video id (assumes filename format: videoID_someOtherPart.txt)
video_groups = defaultdict(list)
for file in txt_files:
    # Remove the extension and split on underscore.
    base_name = os.path.splitext(file)[0]  # e.g. "52807_1_44"
    parts = base_name.split('_')
    if len(parts) < 2:
        continue  # skip if filename doesn't match expected format
    video_id = "_".join(parts[:2])  # e.g. "52807_1"
    video_groups[video_id].append(file)

# Get a list of unique video ids
video_ids = list(video_groups.keys())

# Shuffle video ids to randomize splitting
random.shuffle(video_ids)

total_videos = len(video_ids)
train_videos = int(total_videos * 0.70)
val_videos = int(total_videos * 0.15)
# Assign remaining videos to test
test_videos = total_videos - train_videos - val_videos

# Split video ids into three sets
train_video_ids = video_ids[:train_videos]
val_video_ids = video_ids[train_videos:train_videos+val_videos]
test_video_ids = video_ids[train_videos+val_videos:]

# Build filename lists for each set
train_files = []
for vid in train_video_ids:
    train_files.extend(video_groups[vid])

val_files = []
for vid in val_video_ids:
    val_files.extend(video_groups[vid])

test_files = []
for vid in test_video_ids:
    test_files.extend(video_groups[vid])

# Save lists to their respective txt files in the folder
with open(os.path.join(folder_path, 'train.txt'), 'w') as f:
    for name in train_files:
        f.write(name + '\n')

with open(os.path.join(folder_path, 'val.txt'), 'w') as f:
    for name in val_files:
        f.write(name + '\n')

with open(os.path.join(folder_path, 'test.txt'), 'w') as f:
    for name in test_files:
        f.write(name + '\n')

# Print counts: number of files and number of videos for each set
print("Train set: {} files from {} videos".format(len(train_files), len(train_video_ids)))
print("Validation set: {} files from {} videos".format(len(val_files), len(val_video_ids)))
print("Test set: {} files from {} videos".format(len(test_files), len(test_video_ids)))
