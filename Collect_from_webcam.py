import csv
import copy
import itertools
import cv2 as cv
import mediapipe as mp

noseTip= [1]
noseBottom= [2]
noseRightCorner= [98]
noseLeftCorner= [327]

rightCheek= [205]
leftCheek= [425]

silhouette= [
10,  338, 297, 332, 284, 251, 389, 356, 454, 323, 361, 288,
397, 365, 379, 378, 400, 377, 152, 148, 176, 149, 150, 136,
172, 58,  132, 93,  234, 127, 162, 21,  54,  103, 67,  109
]

ROI =  silhouette + noseTip + noseBottom + noseRightCorner + noseLeftCorner + rightCheek + leftCheek

def select_mode(key, mode):
    global number
    if number != -1:
        number = prev_number
    if 48 <= key <= 57:  # 0 ~ 9
        number = key - 48
    if key == 110:  # n
        mode = 0
    if key == 107:  # k  # record mode
        mode = 1
        number = -1
    return number, mode


def calc_landmark_list(image, landmarks,ROI):
    image_width, image_height = image.shape[1], image.shape[0]

    landmark_point = []

    # Keypoint
    # for _, landmark in enumerate(landmarks.landmark):
    for i in ROI:
        landmark = landmarks.landmark[i]
        landmark_x = min(int(landmark.x * image_width), image_width - 1)
        landmark_y = min(int(landmark.y * image_height), image_height - 1)

        landmark_point.append([landmark_x, landmark_y])

    return landmark_point


def pre_process_landmark(landmark_list):
    temp_landmark_list = copy.deepcopy(landmark_list)

    # Convert to relative coordinates
    base_x, base_y = 0, 0
    for index, landmark_point in enumerate(temp_landmark_list):
        if index == 0:
            base_x, base_y = landmark_point[0], landmark_point[1]

        temp_landmark_list[index][0] = temp_landmark_list[index][0] - base_x
        temp_landmark_list[index][1] = temp_landmark_list[index][1] - base_y

    # Convert to a one-dimensional list
    temp_landmark_list = list(
        itertools.chain.from_iterable(temp_landmark_list))

    # Normalization
    max_value = max(list(map(abs, temp_landmark_list)))

    def normalize_(n):
        return n / max_value

    temp_landmark_list = list(map(normalize_, temp_landmark_list))

    return temp_landmark_list


def logging_csv(number, mode, landmark_list):
    if mode == 0:
        pass
    if mode == 1 and (0 <= number <= 9):
        csv_path = 'model/keypoint_classifier/keypoint.csv'
        with open(csv_path, 'a', newline="") as f:
            writer = csv.writer(f)
            writer.writerow([number, *landmark_list])
    return


number = -1

cap_device = 1
cap_width = 1920
cap_height = 1080

use_brect = True

# Camera preparation
cap = cv.VideoCapture(cap_device)
cap.set(cv.CAP_PROP_FRAME_WIDTH, cap_width)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, cap_height)

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.5) 

mode = 0

while True:

    # Process Key (ESC: end)
    key = cv.waitKey(10)
    if key == 27:  # ESC
        break
    prev_number = number
    number, mode = select_mode(key, mode)

    # Camera capture 
    ret, image = cap.read()
    if not ret:
        break
    image = cv.flip(image, 1)  # Mirror display
    debug_image = copy.deepcopy(image)

    # Detection implementation 
    image = cv.cvtColor(image, cv.COLOR_BGR2RGB)

    image.flags.writeable = False
    results = face_mesh.process(image)
    image.flags.writeable = True

    if results.multi_face_landmarks is not None:
        for face_landmarks in results.multi_face_landmarks:

            # Landmark calculation
            landmark_list = calc_landmark_list(debug_image, face_landmarks,ROI)

            # Conversion to relative coordinates / normalized coordinates
            pre_processed_landmark_list = pre_process_landmark(
                landmark_list)
            # Write to the dataset file
            logging_csv(number, mode, pre_processed_landmark_list)

    if mode == 1 :
        cv.putText(debug_image, "MODE:" + 'Record keypoints mode', (10, 90),
                cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1,
                cv.LINE_AA)
    cv.imshow('Facial Emotion Recognition', debug_image)

cap.release()
cv.destroyAllWindows()