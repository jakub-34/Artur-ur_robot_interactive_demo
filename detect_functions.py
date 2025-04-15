# Inspired by: https://github.com/paytonshaltis/head-nod-detection/blob/main/headMovements.py

import cv2
import time
import robot_eyes
import mediapipe as mp
import pygame

# Initialize MediaPipe Face Mesh
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh

# Constants for tweaking the program
FRAMES_TO_ANALYZE = 10
NODDING_SENSITIVITY = 0.025
SHAKING_SENSITIVITY = 0.04
VERTICAL_ADJUSTMENT = 0.2
HORIZONTAL_ADJUSTMENT = 0.12

def detect_person(infinite = False, show_camera = False) -> bool:
    consecutive_detections = 0
    iteration_count = 0
    max_iterations = 15

    # Initialize MediaPipe Face Detection
    mp_face_detection = mp.solutions.face_detection
    face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.5)
    cap = cv2.VideoCapture(0)
    
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            continue

        # If show_camera is True, display the camera feed
        if show_camera:
            image_flipped = cv2.flip(image, 1)
            image_rgb_preview = cv2.cvtColor(image_flipped, cv2.COLOR_BGR2RGB)
            # Create a pygame Surface from the image
            frame_surface = pygame.image.frombuffer(image_rgb_preview.tobytes(), (image_rgb_preview.shape[1], image_rgb_preview.shape[0]), 'RGB')
            with robot_eyes.camera_lock:
                robot_eyes.camera_surface = frame_surface
                robot_eyes.display_camera = True

        # Convert the image to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = face_detection.process(image_rgb)

        # Face detection results
        if results.detections:
            consecutive_detections += 1
        else:
            consecutive_detections = 0

        if infinite and consecutive_detections >= max_iterations:
            cap.release()
            cv2.destroyAllWindows()
            if show_camera:
                with robot_eyes.camera_lock:
                    robot_eyes.display_camera = False
            return True
        
        if not infinite:
            iteration_count += 1
            if iteration_count >= max_iterations:
                cap.release()
                cv2.destroyAllWindows()
                if show_camera:
                    with robot_eyes.camera_lock:
                        robot_eyes.display_camera = False
                return consecutive_detections >= int((2 * max_iterations) / 3)

    cap.release()
    cv2.destroyAllWindows()
    if show_camera:
        with robot_eyes.camera_lock:
            robot_eyes.display_camera = False
    return False


def head_movement(timed = False, timer = 0) -> str:
    cap = cv2.VideoCapture(0)
    nodding_coordinates = []
    shaking_coordinates = []

    def direction_changes(data, coord, sensitivity):
        current_data, prev_data = None, None
        current_direction, prev_direction = None, None
        peak_or_valley = getattr(data[0], coord)
        num_direction_changes = 0

        for i in range(len(data)):
            current_data = getattr(data[i], coord)
            if prev_data and abs(peak_or_valley - current_data) > sensitivity:
                current_direction = 'increasing' if peak_or_valley > current_data else 'decreasing'
                if prev_direction and current_direction != prev_direction:
                    num_direction_changes += 1
                    peak_or_valley = current_data
                elif not prev_direction:
                    prev_direction = current_direction
                    peak_or_valley = current_data
            prev_data = current_data
        return num_direction_changes


    success, image = cap.read()
    if success:
        image = cv2.flip(image, 1)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # Create a pygame Surface from the image
        frame_surface = pygame.image.frombuffer(image_rgb.tobytes(), (image_rgb.shape[1], image_rgb.shape[0]), 'RGB')
        with robot_eyes.camera_lock:
            robot_eyes.camera_surface = frame_surface
            robot_eyes.display_camera = True

    with mp.solutions.face_mesh.FaceMesh(
        max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5, min_tracking_confidence=0.5
    ) as face_mesh:
        start_time = time.time() if timed else None
        while cap.isOpened():
            if timed and (time.time() - start_time > timer):
                break

            success, image = cap.read()
            if not success:
                continue

            image = cv2.flip(image, 1)
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            # Create a pygame Surface from the image
            frame_surface = pygame.image.frombuffer(image_rgb.tobytes(), (image_rgb.shape[1], image_rgb.shape[0]), 'RGB')
            with robot_eyes.camera_lock:
                robot_eyes.camera_surface = frame_surface

            image.flags.writeable = False
            results = face_mesh.process(image_rgb)

            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    chin = face_landmarks.landmark[199]
                    sidehead = face_landmarks.landmark[447]
                    tophead = face_landmarks.landmark[10]
                    bottomhead = face_landmarks.landmark[152]
                    distance_adjustment = (bottomhead.y - tophead.y) / 0.5

                    nodding_coordinates.append(chin)
                    shaking_coordinates.append(sidehead)

                    if len(nodding_coordinates) > FRAMES_TO_ANALYZE and len(shaking_coordinates) > FRAMES_TO_ANALYZE:
                        nodding_coordinates.pop(0)
                        shaking_coordinates.pop(0)
                        if (direction_changes(nodding_coordinates, "z", NODDING_SENSITIVITY * distance_adjustment) > 0
                            and direction_changes(shaking_coordinates, "z", SHAKING_SENSITIVITY * distance_adjustment) == 0
                            and abs(max(nodding_coordinates, key=lambda x: x.y).y - min(nodding_coordinates, key=lambda x: x.y).y) 
                                <= VERTICAL_ADJUSTMENT * distance_adjustment):
                            cap.release()
                            cv2.destroyAllWindows()
                            with robot_eyes.camera_lock:
                                robot_eyes.display_camera = False
                            return "YES"
                        elif (direction_changes(shaking_coordinates, "z", SHAKING_SENSITIVITY * distance_adjustment) > 0
                              and direction_changes(nodding_coordinates, "z", NODDING_SENSITIVITY * distance_adjustment) == 0
                              and abs(max(shaking_coordinates, key=lambda x: x.x).x - min(shaking_coordinates, key=lambda x: x.x).x) 
                                <= HORIZONTAL_ADJUSTMENT * distance_adjustment):
                            cap.release()
                            cv2.destroyAllWindows()
                            with robot_eyes.camera_lock:
                                robot_eyes.display_camera = False
                            return "NO"
    cap.release()
    cv2.destroyAllWindows()
    with robot_eyes.camera_lock:
        robot_eyes.camera_surface = None
        robot_eyes.display_camera = False
    return "NA"
