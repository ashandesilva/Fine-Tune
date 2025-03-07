#!/usr/bin/env python3
"""
merge_annotations.py

Merges multiple CVAT/COCO-format annotation files (keypoints) into one single COCO JSON.

Usage:
python merge_annotations.py --ann_files annotations_v1/Correct_n2_3_7_100.json annotations_v1/lumbar_3_7_dell_111.json --out annotations_v1/merged_coco.json

Next time you add new annotation files (e.g., more frames or more classes), 
just rerun the merge script (possibly with more --ann_files), then rerun the split script. 
You’ll get an updated set of train/val/test JSONs that keep frames from each video ID in the same subset.

  python merge_annotations.py \
    --ann_files annotations_v1/Correct_n2_3_7_100.json annotations_v1/lumbar_3_7_dell_111.json \
    --out annotations_v1/merged_coco.json
"""

import json
import argparse
import copy

def merge_coco_annotations(ann_files, out_file):
    """
    Merges multiple COCO keypoint annotation files into one.
    Offsets image and annotation IDs so they don't conflict.
    """
    merged = {
        "licenses": [],
        "info": {},
        "categories": [],
        "images": [],
        "annotations": []
    }

    current_image_id = 0
    current_ann_id = 0

    # We assume the 'categories' from all files are the same (COCO 17 keypoints).
    # If they differ, you can handle that logic here.
    categories_set = None

    for ann_file in ann_files:
        with open(ann_file, 'r') as f:
            data = json.load(f)

        # If first file, copy over categories
        if categories_set is None or not merged["categories"]:
            merged["categories"] = data.get("categories", [])
            categories_set = True

        images = data.get("images", [])
        annotations = data.get("annotations", [])

        for img in images:
            new_img = copy.deepcopy(img)
            old_id = new_img["id"]
            new_img["id"] = current_image_id + 1
            current_image_id += 1
            merged["images"].append(new_img)

        # We'll create a mapping from old image ID -> new image ID, so that
        # annotations referencing the old IDs are updated to the new IDs.
        image_id_map = {}
        idx = 0
        for img in images:
            old_id = img["id"]
            new_id = merged["images"][idx]["id"]
            image_id_map[old_id] = new_id
            idx += 1

        # Now fix the annotation IDs, and link them to the correct image ID
        for ann in annotations:
            new_ann = copy.deepcopy(ann)
            old_img_id = new_ann["image_id"]
            new_ann["image_id"] = image_id_map[old_img_id]
            # shift ann ID
            current_ann_id += 1
            new_ann["id"] = current_ann_id
            merged["annotations"].append(new_ann)

    # (Optional) Copy over 'licenses' and 'info' from the first file
    # or just leave them empty or consolidated
    # e.g.:
    # merged["licenses"] = data_from_first["licenses"]
    # merged["info"] = data_from_first["info"]

    # Write merged
    with open(out_file, 'w') as f:
        json.dump(merged, f)
    print(f"Merged annotations written to: {out_file}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ann_files", nargs='+', required=True,
                        help="List of COCO annotation JSON files to merge")
    parser.add_argument("--out", required=True, help="Output merged JSON file")
    args = parser.parse_args()

    merge_coco_annotations(args.ann_files, args.out)

if __name__ == "__main__":
    main()
