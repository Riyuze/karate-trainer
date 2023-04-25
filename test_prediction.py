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
    pose_reference_coordinates, pose_user_coordinates = import_data(path, world)

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

def plot(path, index, world=False): 
    pose_reference_coordinates, pose_user_coordinates = import_data(path, world)

    WHITE_COLOR = (224, 224, 224)
    BLACK_COLOR = (0, 0, 0)
    RED_COLOR = (0, 0, 255)
    BLUE_COLOR = (255, 0, 0)
    GREY_COLOR = (105, 105, 105)

    _PRESENCE_THRESHOLD = 0.001
    _VISIBILITY_THRESHOLD = 0.001

    mp_pose = mp.solutions.pose

    @dataclass
    class DrawingSpec:
        color: Tuple[int, int, int] = WHITE_COLOR
        thickness: int = 2
        circle_radius: int = 2

    def _normalize_color(color):
        return tuple(v / 255. for v in color)

    def _normalized_to_pixel_coordinates(
            normalized_x: float, normalized_y: float, image_width: int,
            image_height: int) -> Union[None, Tuple[int, int]]:
        """Converts normalized value pair to pixel coordinates."""

        # Checks if the float value is between 0 and 1.
        def is_valid_normalized_value(value: float) -> bool:
            return (value > 0 or math.isclose(0, value)) and (value < 1 or math.isclose(1, value))
            
        x_px = min(math.floor(normalized_x * image_width), image_width - 1)
        y_px = min(math.floor(normalized_y * image_height), image_height - 1)
        return x_px, y_px
    
    def plot_landmarks(landmark_list_1: landmark_pb2.NormalizedLandmarkList,
                    landmark_list_2: landmark_pb2.NormalizedLandmarkList,
                    connections: Optional[List[Tuple[int, int]]] = None,
                    landmark_drawing_spec: DrawingSpec = DrawingSpec(
                        color=[RED_COLOR, BLUE_COLOR], thickness=5),
                    connection_drawing_spec: DrawingSpec = DrawingSpec(
                        color=[BLACK_COLOR, GREY_COLOR], thickness=5),
                    elevation: int = 10,
                    azimuth: int = 10):

        if not (landmark_list_1 or landmark_list_2):
            return
        plt.figure(figsize=(10, 10))
        ax = plt.axes(projection='3d')
        ax.view_init(elev=elevation, azim=azimuth)
        plotted_landmarks_1 = {}
        for idx, landmark in enumerate(landmark_list_1.landmark):
            if ((landmark.HasField('visibility') and
                landmark.visibility < _VISIBILITY_THRESHOLD) or
                (landmark.HasField('presence') and
                landmark.presence < _PRESENCE_THRESHOLD)):
                continue
            ax.scatter3D(
                xs=[-landmark.z],
                ys=[landmark.x],
                zs=[-landmark.y],
                color=_normalize_color(landmark_drawing_spec.color[0]),
                linewidth=landmark_drawing_spec.thickness)
            plotted_landmarks_1[idx] = (-landmark.z, landmark.x, -landmark.y)
        if connections:
            num_landmarks = len(landmark_list_1.landmark)
            # Draws the connections if the start and end landmarks are both visible.
            for connection in connections:
                start_idx = connection[0]
                end_idx = connection[1]
                if not (0 <= start_idx < num_landmarks and 0 <= end_idx < num_landmarks):
                    raise ValueError(f'Landmark index is out of range. Invalid connection '
                                    f'from landmark #{start_idx} to landmark #{end_idx}.')
                if start_idx in plotted_landmarks_1 and end_idx in plotted_landmarks_1:
                    landmark_pair = [
                        plotted_landmarks_1[start_idx], plotted_landmarks_1[end_idx]
                    ]
                    ax.plot3D(
                        xs=[landmark_pair[0][0], landmark_pair[1][0]],
                        ys=[landmark_pair[0][1], landmark_pair[1][1]],
                        zs=[landmark_pair[0][2], landmark_pair[1][2]],
                        color=_normalize_color(
                            connection_drawing_spec.color[1]),
                        linewidth=connection_drawing_spec.thickness)

        plotted_landmarks_2 = {}
        for idx, landmark in enumerate(landmark_list_2.landmark):
            if ((landmark.HasField('visibility') and
                landmark.visibility < _VISIBILITY_THRESHOLD) or
                (landmark.HasField('presence') and
                landmark.presence < _PRESENCE_THRESHOLD)):
                continue
            ax.scatter3D(
                xs=[-landmark.z],
                ys=[landmark.x],
                zs=[-landmark.y],
                color=_normalize_color(landmark_drawing_spec.color[1]),
                linewidth=landmark_drawing_spec.thickness)
            plotted_landmarks_2[idx] = (-landmark.z, landmark.x, -landmark.y)
        if connections:
            num_landmarks = len(landmark_list_2.landmark)
            # Draws the connections if the start and end landmarks are both visible.
            for connection in connections:
                start_idx = connection[0]
                end_idx = connection[1]
                if not (0 <= start_idx < num_landmarks and 0 <= end_idx < num_landmarks):
                    raise ValueError(f'Landmark index is out of range. Invalid connection '
                                    f'from landmark #{start_idx} to landmark #{end_idx}.')
                if start_idx in plotted_landmarks_2 and end_idx in plotted_landmarks_2:
                    landmark_pair = [
                        plotted_landmarks_2[start_idx], plotted_landmarks_2[end_idx]
                    ]
                    ax.plot3D(
                        xs=[landmark_pair[0][0], landmark_pair[1][0]],
                        ys=[landmark_pair[0][1], landmark_pair[1][1]],
                        zs=[landmark_pair[0][2], landmark_pair[1][2]],
                        color=_normalize_color(
                            connection_drawing_spec.color[0]),
                        linewidth=connection_drawing_spec.thickness)
        plt.show()

    landmark_subset_1 = landmark_pb2.NormalizedLandmarkList(
        landmark = pose_reference_coordinates[index]
    )

    landmark_subset_2 = landmark_pb2.NormalizedLandmarkList(
        landmark = pose_user_coordinates[index]
    )

    plot_landmarks(landmark_subset_1, landmark_subset_2, mp_pose.POSE_CONNECTIONS, elevation=0, azimuth=0)
