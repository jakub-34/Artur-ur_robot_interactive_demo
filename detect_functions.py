import cv2
import time
import mediapipe as mp
from operator import attrgetter

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

def detect_person(infinite = False) -> bool:
    consecutive_detections = 0
    iteration_count = 0
    max_iterations = 15

    # Initialize MediaPipe Face Detection
    mp_face_detection = mp.solutions.face_detection
    face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.5)
    cap = cv2.VideoCapture(0)

    print("Waiting for a person...")
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        # Convert the image to RGB for face detection
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = face_detection.process(image_rgb)

        # Check if a person is detected
        if results.detections:
            consecutive_detections += 1
        else:
            consecutive_detections = 0

        # Display the camera feed
        # cv2.imshow('Person Detection', image)
        # if cv2.waitKey(5) & 0xFF == 27:
        #     break

        if infinite and consecutive_detections >= max_iterations:
            cap.release()
            cv2.destroyAllWindows()
            return True
        
        if not infinite:
            iteration_count += 1
            if iteration_count >= max_iterations:
                return consecutive_detections >= max_iterations


    cap.release()
    cv2.destroyAllWindows()
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

    with mp_face_mesh.FaceMesh(
        max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5, min_tracking_confidence=0.5
    ) as face_mesh:
        print("Detecting head movement...")
        start_time = time.time() if timed else None
        while cap.isOpened():
            if timed and (time.time() - start_time > timer):
                cap.release()
                cv2.destroyAllWindows()
                return "NA"
            
            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                continue

            image.flags.writeable = False
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
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
                            and abs(max(nodding_coordinates, key=attrgetter('y')).y - min(nodding_coordinates, key=attrgetter('y')).y) 
                                <= VERTICAL_ADJUSTMENT * distance_adjustment):
                            cap.release()
                            cv2.destroyAllWindows()
                            return "YES"

                        elif (direction_changes(shaking_coordinates, "z", SHAKING_SENSITIVITY * distance_adjustment) > 0
                              and direction_changes(nodding_coordinates, "z", NODDING_SENSITIVITY * distance_adjustment) == 0
                              and abs(max(shaking_coordinates, key=attrgetter('x')).x - min(shaking_coordinates, key=attrgetter('x')).x) 
                                <= HORIZONTAL_ADJUSTMENT * distance_adjustment):
                            cap.release()
                            cv2.destroyAllWindows()
                            return "NO"
            
            # Display the camera feed
            # cv2.imshow('Head Movement Detection', cv2.flip(image, 1))
            # if cv2.waitKey(5) & 0xFF == 27:
            #    break

    cap.release()
    cv2.destroyAllWindows()
    return None
