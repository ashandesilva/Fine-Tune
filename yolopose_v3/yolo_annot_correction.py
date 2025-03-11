"""
This script processes YOLO annotation files to ensure that all bounding box coordinates and keypoints are valid.
It reads annotation files from a specified directory, checks the validity of each coordinate, and corrects or removes invalid annotations.

The code corrects corrupted YOLO pose annotations by ensuring all coordinate values are within a valid, normalized range between 0.0 and 1.0. YOLO expects normalized coordinates in this range, and values outside of it cause corruption warnings.

The best practice for YOLO pose annotation correction is:
    Check each (x, y) pair individually:
        If either x or y is outside [0,1] (negative or > 1.0):
            Set both (x, y) to 0 (or a neutral value within image bounds, usually 0.0).
            Set visibility to 0 for that keypoint.
"""


import os

annotations_path = "C:/Users/UDESIAS/Documents/FYP/Fine-Tune/yolopose_v3/data/labels/train/"
# annotations_path = "C:/Users/UDESIAS/Documents/FYP/Fine-Tune/yolopose_v3/data/labels/test/"
# annotations_path = "C:/Users/UDESIAS/Documents/FYP/Fine-Tune/yolopose_v3/data/labels/val/"

def is_valid_coord(x):
    return 0.0 <= float(x) <= 1.0

for file_name in os.listdir(annotations_path):
    if not file_name.endswith(".txt"):
        continue

    file_path = os.path.join(annotations_path, file_name)
    updated_lines = []
    with open(file_path, 'r') as file:
        lines = file.readlines()

    for line in lines:
        values = line.strip().split()
        if len(values) < 5:
            continue  # skip if format is obviously incorrect

        class_id = values[0]
        box_coords = values[1:5]

        # Check if bbox coordinates are valid first
        box_valid = all(0.0 <= float(coord) <= 1.0 for coord in box_coords)

        keypoints = values[5:]
        new_keypoints = []
        valid_keypoints_exist = False

        # Process keypoints (each keypoint is x,y,v)
        for i in range(0, len(keypoints), 3):
            x, y, v = keypoints[i:i+3]
            x_float = float(x)
            y_float = float(y)

            # Check coordinate validity
            if not (0.0 <= x_float <= 1.0) or not (0.0 <= float(y) <= 1.0):
                # Invalid keypoint found: set visibility=0 and coords=0.0
                new_keypoints.extend(["0.0", "0.0", "0"])
            else:
                # Keypoint is valid; keep as is
                new_keypoints.extend([x, y, v])
                if int(v) != 0:
                    valid_keypoints_exist = True

        if valid_keypoints_exist:
            corrected_line = values[:5] + new_keypoints
            updated_lines.append(' '.join(corrected for corrected in new_keypoints))
        else:
            print(f"❌ Removed invalid annotation from {file_name} (no valid keypoints left).")

        # Rewrite annotation only if valid keypoints remain
        if valid_keypoints_exist:
            with open(file_path, 'w') as f:
                f.write(' '.join(values[:5] + new_keypoints) + '\n')
        else:
            # Optionally remove entirely invalid annotations
            os.remove(file_path)
            print(f"❌ Removed annotation with no valid keypoints: {file_name}")

print("✅ Annotation cleaning and validation completed!")
