import os
import json
import shutil

# Paths
json_file_path = 'annotations_v3/merged_coco.json'
source_dirs = ['data_v3/correct_extra_frames_proccessed', 'data_v3/lumbar_extra_frames_proccessed']
target_dir = 'data_v3/merged'

# Create target directory if it doesn't exist
os.makedirs(target_dir, exist_ok=True)

# Read JSON file
with open(json_file_path, 'r') as file:
    data = json.load(file)

# Extract image names from JSON
image_names = {img['file_name'] for img in data['images']}

# Function to copy images
def copy_images(source_dirs, target_dir, image_names):
    for source_dir in source_dirs:
        for root, _, files in os.walk(source_dir):
            for file in files:
                if file in image_names:
                    source_file = os.path.join(root, file)
                    target_file = os.path.join(target_dir, file)
                    shutil.copy2(source_file, target_file)
                    print(f'Copied {file} to {target_dir}')

# Copy images
copy_images(source_dirs, target_dir, image_names) 