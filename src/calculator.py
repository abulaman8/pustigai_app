import numpy as np
import warnings


warnings.filterwarnings("ignore")


def landmarks_estimation(detection):
    landmarks = []
    if detection.pose_landmarks:
        for idx, landmark in enumerate(detection.pose_landmarks.landmark):
            landmarks.append(
                [landmark.x, landmark.y, landmark.z, landmark.visibility])
    return landmarks


def angle_estimate(landmarks):
    angles = []
    key_points = [(11, 12, 13), (12, 11, 14), (23, 24, 25), (24, 23, 26)]
    for p1, p2, p3 in key_points:
        if len(landmarks) > max(p1, p2, p3):
            a = np.array([landmarks[p1][0], landmarks[p1][1]])
            b = np.array([landmarks[p2][0], landmarks[p2][1]])
            c = np.array([landmarks[p3][0], landmarks[p3][1]])
            ba = a - b
            bc = c - b
            cosine_angle = np.dot(ba, bc) / \
                (np.linalg.norm(ba) * np.linalg.norm(bc))
            angle = np.arccos(cosine_angle) * 180 / np.pi
            angles.append(angle)
    while len(angles) < 12:
        angles.append(0)
    return angles


def width_distance(landmarks, width):
    if len(landmarks) > 11:
        return abs(landmarks[11][0] - landmarks[12][0]) * width
    return 0


def orie_check(landmarks, wids):
    if len(landmarks) > 11 and wids > 0:
        shoulder_diff = abs(landmarks[11][2] - landmarks[12][2])
        return "front" if shoulder_diff < 0.1 else "side"
    return "unknown"
