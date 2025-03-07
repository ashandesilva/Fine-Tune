#!/usr/bin/env python3
"""
train.py

Script for fine-tuning the YOLOPose11 model on a custom COCO keypoint dataset.

Usage:
  python train.py --cfg yolopose11.yaml --data data.yaml --weights yolo11m-pose.pt --batch-size 8 --epochs 50
"""

import argparse
import os
from ultralytics import YOLO

def main():
    parser = argparse.ArgumentParser(description="Train YOLOPose11 on custom pose dataset")
    parser.add_argument('--cfg', type=str, required=True, help='Path to YOLOPose11 config file (yolopose11.yaml)')
    parser.add_argument('--data', type=str, required=True, help='Path to data YAML file (e.g., data.yaml)')
    parser.add_argument('--weights', type=str, default=None, help='Path to pretrained weights (e.g., yolopose11.pt)')
    parser.add_argument('--batch-size', type=int, default=8, help='Training batch size')
    parser.add_argument('--epochs', type=int, default=50, help='Number of training epochs')
    parser.add_argument('--gpu-id', type=int, default=0, help='GPU id to use')
    args = parser.parse_args()

    # Load the configuration file
    cfg = Config.fromfile(args.cfg)
    
    # Update configuration with command-line parameters
    cfg.data.data_yaml = args.data  # the data YAML path is set in the data section
    cfg.train_cfg.epochs = args.epochs
    cfg.train_cfg.optimizer.lr = cfg.train_cfg.optimizer.lr if hasattr(cfg.train_cfg.optimizer, "lr") else 0.0005
    cfg.train_cfg.batch_size = args.batch_size
    if args.weights:
        cfg.model.backbone.pretrained = args.weights

    # Set GPU device if needed (depends on your training library)
    os.environ["CUDA_VISIBLE_DEVICES"] = str(args.gpu_id)

    # Launch training; train_model() should handle model, dataset creation, logging, checkpointing, etc.
    train_model(cfg)

if __name__ == '__main__':
    main()
