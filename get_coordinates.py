import cv2
import math
import numpy as np
from matplotlib import pyplot as plt
import mediapipe as mp
from typing import List, Optional, Tuple, Union, Mapping
from mediapipe.framework.formats import landmark_pb2
from dataclasses import dataclass
import os
import json

def resize(image):
    DESIRED_HEIGHT = 800
    DESIRED_WIDTH = 800

    h, w = image.shape[:2]
    if h < w:
        return cv2.resize(image, (DESIRED_WIDTH, math.floor(h/(w/DESIRED_WIDTH))))
    else:
        return cv2.resize(image, (math.floor(w/(h/DESIRED_HEIGHT)), DESIRED_HEIGHT))

def import_images(path):
    images = {}
    images_path = path

    for image in os.listdir(images_path):
        f = os.path.join(images_path, image)

        if os.path.isfile(f):
            images[f] = (resize(cv2.imread(f)))

    return images

def get_coordinates(path):
    mp_pose = mp.solutions.pose
    mp_drawing_styles = mp.solutions.drawing_styles

    images = import_images(path)

    json_folder = os.path.join('./coordinates', path.split('\\')[1])

    json_file = os.path.join('./coordinates', path.split('\\')[1], 'pose_coordinates.json')
    json_world_file = os.path.join('./coordinates', path.split('\\')[1], 'pose_world_coordinates.json')
    image_keypoints = {}
    image_world_keypoints = {}

    if not os.path.exists(json_folder):
        os.makedirs(json_folder)

    with mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.7, model_complexity=2) as pose:
        for image in images:
            results = pose.process(cv2.cvtColor(images[image], cv2.COLOR_BGR2RGB))

            image_height, image_width, _ = images[image].shape
            if not results.pose_landmarks:
                continue

            keypoints = []
            keypoint = {}

            for data in results.pose_landmarks.landmark:
                keypoint['x'] = data.x
                keypoint['y'] = data.y
                keypoint['z'] = data.z
                keypoint['visibility'] = data.visibility
                keypoints.append(keypoint)
                keypoint = {}

            image_keypoints[image] = keypoints

            world_keypoints = []
            world_keypoint = {}

            for data in results.pose_world_landmarks.landmark:
                world_keypoint['x'] = data.x
                world_keypoint['y'] = data.y
                world_keypoint['z'] = data.z
                world_keypoint['visibility'] = data.visibility
                world_keypoints.append(world_keypoint)
                world_keypoint = {}

            image_world_keypoints[image] = world_keypoints

    with open(json_file, 'w') as f:
        json.dump(image_keypoints, f)

    with open(json_world_file, 'w') as f:
        json.dump(image_world_keypoints, f)
        