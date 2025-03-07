#!/usr/bin/env python3
"""
split_train_val_test.py

Splits a merged COCO annotation file into train/val/test sets,
grouping images by 'video ID' so that frames of the same video stay in the same split.

Usage:
python split_train_val_test.py --merged_coco annotations_v1/merged_coco.json --out_dir annotations_v1/split --train_ratio 0.7 --val_ratio 0.15 --test_ratio 0.15 --seed 42

  python split_train_val_test.py \
    --merged_coco annotations_v1/merged_coco.json \
    --out_dir annotations_v1 \
    --train_ratio 0.7 \
    --val_ratio 0.15 \
    --test_ratio 0.15
"""

import json
import argparse
import random
import os
from collections import defaultdict

def get_video_id_from_filename(file_name):
    """
    Extract a 'video ID' from the image filename.
    Example: "52701_1_4.jpg" -> "52701_1"
    Modify this logic as needed to match your naming conventions.
    """
    base = os.path.splitext(file_name)[0]  # "52701_1_4"
    tokens = base.split('_')              # ["52701", "1", "4"]
    if len(tokens) >= 2:
        video_key = tokens[0] + '_' + tokens[1]
    else:
        # fallback if something unexpected
        video_key = base
    return video_key

def split_train_val_test(video_ids, train_ratio, val_ratio, test_ratio):
    """
    Shuffle and split the list of unique video IDs into train/val/test.
    Returns three sets: (train_vids, val_vids, test_vids).
    """
    random.shuffle(video_ids)
    total = len(video_ids)

    train_count = int(total * train_ratio)
    val_count = int(total * val_ratio)
    # test_count = total - train_count - val_count  # or int(total * test_ratio)

    train_vids = set(video_ids[:train_count])
    val_vids = set(video_ids[train_count:train_count + val_count])
    test_vids = set(video_ids[train_count + val_count:])
    return train_vids, val_vids, test_vids

def build_subset_coco(merged_data, image_ids_subset):
    """
    Build a new COCO dict with only the images (and annotations) whose IDs are in image_ids_subset.
    """
    subset = {
        "licenses": merged_data.get("licenses", []),
        "info": merged_data.get("info", {}),
        "categories": merged_data.get("categories", []),
        "images": [],
        "annotations": []
    }

    # Create a quick lookup
    image_ids_subset = set(image_ids_subset)

    # Filter images
    img_id_map = {}
    new_img_id = 1
    for img in merged_data["images"]:
        if img["id"] in image_ids_subset:
            new_img = dict(img)
            new_img["id"] = new_img_id
            img_id_map[img["id"]] = new_img_id
            new_img_id += 1
            subset["images"].append(new_img)

    # Filter annotations
    new_ann_id = 1
    for ann in merged_data["annotations"]:
        if ann["image_id"] in img_id_map:
            new_ann = dict(ann)
            new_ann["image_id"] = img_id_map[ann["image_id"]]
            new_ann["id"] = new_ann_id
            new_ann_id += 1
            subset["annotations"].append(new_ann)

    return subset

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--merged_coco", required=True, help="Path to merged_coco.json")
    parser.add_argument("--out_dir", required=True, help="Where to save train/val/test annotation files")
    parser.add_argument("--train_ratio", type=float, default=0.7)
    parser.add_argument("--val_ratio", type=float, default=0.15)
    parser.add_argument("--test_ratio", type=float, default=0.15)
    parser.add_argument("--seed", type=int, default=42, help="Random seed for reproducibility")
    args = parser.parse_args()

    # Basic checks
    ratio_sum = args.train_ratio + args.val_ratio + args.test_ratio
    if abs(ratio_sum - 1.0) > 1e-6:
        raise ValueError("train_ratio + val_ratio + test_ratio must equal 1.0")

    random.seed(args.seed)

    with open(args.merged_coco, 'r') as f:
        merged_data = json.load(f)

    # 1) Group image IDs by "video ID"
    video_to_image_ids = defaultdict(list)

    for img in merged_data["images"]:
        file_name = img["file_name"]
        vid_key = get_video_id_from_filename(file_name)
        video_to_image_ids[vid_key].append(img["id"])

    # 2) Shuffle and split at video level
    all_video_ids = list(video_to_image_ids.keys())
    train_vids, val_vids, test_vids = split_train_val_test(
        all_video_ids,
        args.train_ratio,
        args.val_ratio,
        args.test_ratio
    )

    # 3) Build sets of image IDs for each split
    train_image_ids = []
    val_image_ids = []
    test_image_ids = []

    for vid_key, img_ids in video_to_image_ids.items():
        if vid_key in train_vids:
            train_image_ids.extend(img_ids)
        elif vid_key in val_vids:
            val_image_ids.extend(img_ids)
        else:
            test_image_ids.extend(img_ids)

    # 4) Build subset COCO for each split
    train_coco = build_subset_coco(merged_data, train_image_ids)
    val_coco = build_subset_coco(merged_data, val_image_ids)
    test_coco = build_subset_coco(merged_data, test_image_ids)

    # 5) Save them
    os.makedirs(args.out_dir, exist_ok=True)

    train_file = os.path.join(args.out_dir, "train_coco.json")
    val_file = os.path.join(args.out_dir, "val_coco.json")
    test_file = os.path.join(args.out_dir, "test_coco.json")

    with open(train_file, 'w') as f:
        json.dump(train_coco, f)
    with open(val_file, 'w') as f:
        json.dump(val_coco, f)
    with open(test_file, 'w') as f:
        json.dump(test_coco, f)

    print(f"Train set: {len(train_coco['images'])} images, {len(train_coco['annotations'])} annotations => {train_file}")
    print(f"Val set: {len(val_coco['images'])} images, {len(val_coco['annotations'])} annotations => {val_file}")
    print(f"Test set: {len(test_coco['images'])} images, {len(test_coco['annotations'])} annotations => {test_file}")

if __name__ == "__main__":
    main()
