import numpy as np
from numpy.linalg import norm
import math
from mediapipe.framework.formats import landmark_pb2
from dataclasses import dataclass
from typing import List, Optional, Tuple, Union, Mapping
import mediapipe as mp
from matplotlib import pyplot as plt
import json
import os

def import_data(path, world=False):
    pose_reference = json.load(open('./coordinates/reference/pose_coordinates.json')) if world == False else json.load(open('./coordinates/reference/pose_world_coordinates.json'))
    pose_reference_coordinates = []
    for name in pose_reference:
        pose_reference_coordinates.append(pose_reference[name])

    pose_user = json.load(open(os.path.join(path, 'pose_coordinates.json'))) if world == False else json.load(open(os.path.join(path, 'pose_world_coordinates.json')))
    pose_user_coordinates = []
    for name in pose_user:
        pose_user_coordinates.append(pose_user[name])

    return pose_reference_coordinates, pose_user_coordinates

def convert_data(index, pose_reference_coordinates, pose_user_coordinates):
    pose_reference_array = []
    pose_reference_visibility = []
    pose_user_array = []

    pose_reference = pose_reference_coordinates[index]
    pose_user = pose_user_coordinates[index]

    for pose1, pose2 in zip(pose_reference, pose_user):
        pose_reference_array.extend([pose1['x'], pose1['y'], pose1['z']])
        pose_reference_visibility.extend([pose1['visibility']])
        pose_user_array.extend([pose2['x'], pose2['y'], pose2['z']])

    return pose_reference_array, pose_reference_visibility, pose_user_array

def calculate_similarity(path, index, world=False):
    pose_reference_coordinates, pose_user_coordinates = import_data(path, False)

    pose_reference_array, pose_reference_visibility, pose_user_array = convert_data(index, pose_reference_coordinates, pose_user_coordinates)

    A = np.array(pose_reference_array)
    B = np.array(pose_user_array)

    cosine_similarity = np.dot(A,B)/(norm(A)*norm(B))

    sum1 = 1 / np.sum(pose_reference_visibility)
    sum2 = 0

    for i in range(len(pose_reference_array)):
        index = math.floor(i/3)
        sum2 += pose_reference_visibility[index] * abs(pose_reference_array[i] - pose_user_array[i])

    weighted_similarity = 1 - (sum1 * sum2)

    return cosine_similarity, weighted_similarity

    