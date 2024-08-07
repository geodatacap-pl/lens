# Face and Person Detection Algorithm

## Introduction

This repository contains the implementation of a face and person detection algorithm using the YOLOv4 framework. The goal of this project is to provide an efficient and accurate method for detecting faces and people in various conditions, including different orientations and real-world scenarios.

The algorithm has been trained on a comprehensive dataset and optimized for high performance and accuracy. This README file provides a detailed overview of the algorithm, installation instructions, and how to run the provided code.

## Features

- Detection of faces and persons from images and video streams.
- Supports different YOLOv4 models: full and tiny versions.
- Optimized for both GPU and CPU environments.
- Can process images from various sources including local files, folders, and live camera feeds.

## Installation

To set up the environment and run the algorithm, follow these steps:

### Prerequisites

- Docker installed on your system.
- Python 3.7 or later.
- CUDA and cuDNN (for GPU support).

### Building Docker Images

1. Build the Docker images for GPU and/or CPU:

```bash
sudo docker build -t yoloapigpu ./ -f yolo_api_gpu_dockerfile
sudo docker build -t yoloapicpu ./ -f yolo_api_cpu_dockerfile
```

### Running the Docker Container

## GPU Environment

To run the Docker container with GPU support, use the following command:

```bash
sudo docker run --gpus all --shm-size=16g --rm -ti -v /local/folder/:/data yoloapigpu /bin/bash
```

## CPU Environment

To run the Docker container with CPU support, use the following command:

```bash
sudo docker run --rm -ti -v /local/folder/:/data yoloapicpu /bin/bash
```

## Accessing the Camera

To allow the container to access the camera, use this command:

```bash
sudo docker run --device=/dev/video0:/dev/video0 --shm-size=16g --rm -ti --net=host --ipc=host -e DISPLAY=$DISPLAY --privileged -v /local/folder/:/data -p 0.0.0.0:6006:6006 yoloapicpu /bin/bash
```

## Running Detection on a Single File

To run the detection algorithm on a single file, use the following command:

```bash
python3 detect_cont.py --config_file /yolo/models/front_side_person/yolov4.cfg --data_file /yolo/models/front_side_person/obj.data --weights /yolo/models/front_side_person/model.weights
```

## Running Detection on a Folder

To run the detection on all images in a folder, use the following command:

```bash
python3 detect_folder.py --config_file /yolo/models/face_person/yolov4.cfg --data_file /yolo/models/face_person/obj.data --weights /yolo/models/face_person/model.weights --input=/data/datasets/ --output=/data/testy/ --makejpg=True
```

To run detection on a folder with different models, use these commands:

```bash
python3 detect_folder.py --config_file /yolo/models/face_person_tiny_608/yolov4.cfg --data_file /yolo/models/face_person_tiny_608/obj.data --weights /yolo/models/face_person_tiny_608/model.weights --input=/data/input/ --output=/data/output/ --makejpg=True

python3 detect_folder.py --config_file /yolo/models/front_side_person/yolov4.cfg --data_file /yolo/models/front_side_person/obj.data --weights /yolo/models/front_side_person/model.weights --input=/data/input/ --output=/data/output/ --makejpg=True

python3 detect_folder.py --config_file /yolo/models/front_side_person_tiny_608/yolov4.cfg --data_file /yolo/models/front_side_person_tiny_608/obj.data --weights /yolo/models/front_side_person_tiny_608/model.weights --input=/data/input/ --output=/data/output/ --makejpg=True
```

### Models

Four models have been developed:

- Full 608x608 for detecting faces (front and side) and persons.
- Full 608x608 for detecting faces and persons.
- Tiny 608x608 for detecting faces (front and side) and persons.
- Tiny 608x608 for detecting faces and persons.

Each model varies in terms of accuracy and speed, with full models being more accurate but slower, and tiny models being faster but less accurate.
