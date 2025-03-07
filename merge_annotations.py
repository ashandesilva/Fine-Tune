#!/usr/bin/env python3
"""
merge_annotations.py

Merges multiple CVAT/COCO-format annotation files (keypoints) into one single COCO JSON,
but EXCLUDES any images that have zero annotations in the final merged output.

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
    Filters out images that have zero annotations.
    """

    # Prepare an empty COCO structure
    merged = {
        "licenses": [],
        "info": {},
        "categories": [],
        "images": [],
        "annotations": []
    }

    current_image_id = 0
    current_ann_id = 0

    # For the first file, we'll copy the categories. 
    categories_copied = False

    for ann_file in ann_files:
        with open(ann_file, 'r') as f:
            data = json.load(f)

        # Copy categories from the first file only (assuming they match across files)
        if not categories_copied:
            merged["categories"] = data.get("categories", [])
            categories_copied = True

        images = data.get("images", [])
        annotations = data.get("annotations", [])

        # We'll store old->new image ID mappings
        image_id_map = {}

        # 1) Add images, offset IDs
        for img in images:
            old_img = copy.deepcopy(img)
            old_id = old_img["id"]

            new_img_id = current_image_id + 1
            current_image_id += 1

            old_img["id"] = new_img_id
            merged["images"].append(old_img)

            image_id_map[old_id] = new_img_id

        # 2) Add annotations, offset IDs, fix image references
        for ann in annotations:
            new_ann = copy.deepcopy(ann)
            old_img_id = ann["image_id"]

            if old_img_id not in image_id_map:
                # Image wasn't added for some reason, skip
                continue

            current_ann_id += 1
            new_ann["id"] = current_ann_id
            new_ann["image_id"] = image_id_map[old_img_id]

            merged["annotations"].append(new_ann)

    # ------------------------------------------------------
    # Now remove images that have zero annotations
    # ------------------------------------------------------

    # 1) Collect all image IDs used by at least one annotation
    annotated_image_ids = set()
    for ann in merged["annotations"]:
        annotated_image_ids.add(ann["image_id"])

    # 2) Filter images
    filtered_images = []
    for img in merged["images"]:
        if img["id"] in annotated_image_ids:
            filtered_images.append(img)

    merged["images"] = filtered_images

    # ------------------------------------------------------
    # (Optionally re-map image/annotation IDs if you want a
    # fresh 1..N range, but that's optional at this point.
    # ------------------------------------------------------

    # Write out the merged data
    with open(out_file, 'w') as f:
        json.dump(merged, f)

    print(f"Merged annotations written to: {out_file}")
    print(f"Total images (with annotations): {len(merged['images'])}")
    print(f"Total annotations: {len(merged['annotations'])}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ann_files", nargs='+', required=True,
                        help="List of COCO annotation JSON files to merge")
    parser.add_argument("--out", required=True, help="Output merged JSON file")
    args = parser.parse_args()

    merge_coco_annotations(args.ann_files, args.out)

if __name__ == "__main__":
    main()
