# 参考ソース
# https://github.com/google/mediapipe/issues/4448#issuecomment-1562674509

# 最新のバージョンではlandmarkを表示するAPIがなさそう。そのため、従来のソリューション(サポート対象外)を使用。
# https://github.com/google/mediapipe/blob/master/docs/solutions/hands.md

import mediapipe as mp
import cv2
import playsound
import glob
import random

BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
VisionRunningMode = mp.tasks.vision.RunningMode

flag = False
counter = 0

# Create a image segmenter instance with the live stream mode:
def get_result(result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
    global counter

    data = result.gestures
    if len(data) != 0:
        gesture = data[0][0].category_name
        detect_score = data[0][0].score
        if gesture == "Thumb_Up":
            counter += 1
        else :
            counter = 0

        print("gesture:%11s, score:%1.3s, counter:%d" % (gesture, detect_score, counter))
    else :
        counter = 0


video = cv2.VideoCapture(0)
timestamp = 0

options = GestureRecognizerOptions(
    base_options=BaseOptions(model_asset_path='gesture_recognizer.task'),
    running_mode=VisionRunningMode.LIVE_STREAM,
    num_hands=1,
    min_hand_detection_confidence=0.1,
    min_hand_presence_confidence=0.1,
    min_tracking_confidence=0.1,
    result_callback=get_result
)

with GestureRecognizer.create_from_options(options) as recognizer:
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_hands = mp.solutions.hands
    with mp_hands.Hands(
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    ) as hands:
        # The recognizer is initialized. Use it here.
        while video.isOpened():
            # Capture frame-by-frame
            ret, frame = video.read()

            if not ret:
                print("Ignoring empty frame")
                break

            timestamp += 1
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
            # Send live image data to perform gesture recognition
            # The results are accessible via the `result_callback` provided in
            # the `GestureRecognizerOptions` object.
            # The gesture recognizer must be created with the live stream mode.
            recognizer.recognize_async(mp_image, timestamp)

            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            frame.flags.writeable = False
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(frame)

            # Draw the hand annotations on the image.
            frame.flags.writeable = True
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        frame,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style()
                    )
            # Flip the image horizontally for a selfie-view display.
            cv2.imshow('MediaPipe Hands', cv2.flip(frame, 1))

            if counter == 5:
                flag = True

            if flag == True:
                flag = False

                file_list = glob.glob('.\wavfiles\*.wav')
                wavfile_fullpath = random.choice(file_list)
                print (wavfile_fullpath)
                playsound.playsound(wavfile_fullpath)

                # 音声再生後、counter が 15 のままだと、音声がループするため
                counter += 1

            if cv2.waitKey(5) & 0xFF == 27:
                break

video.release()
cv2.destroyAllWindows()
