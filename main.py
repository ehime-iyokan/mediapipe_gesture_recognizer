# 参考ソース
# https://github.com/google/mediapipe/issues/4448#issuecomment-1562674509

# 最新のバージョンではlandmarkを表示するAPIがなさそう。そのため、従来のソリューション(サポート対象外)を使用。
# https://github.com/google/mediapipe/blob/master/docs/solutions/hands.md
# ↓：tasks.vision.GestureRecognizer と solutions.hands 両方で座標を取得することとなるため修正
# landmark を表示する処理は以下を参考に作成
# https://qiita.com/akira2768922/items/c660129cc45cce384e90


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

Flag = False
Counter = 0
Result = None

# Create a image segmenter instance with the live stream mode:
def get_result(result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
    global Counter, Result

    Result = result

    data = result.gestures
    if len(data) != 0:
        gesture = data[0][0].category_name
        detect_score = data[0][0].score
        if gesture == "Thumb_Up":
            Counter += 1
        else :
            Counter = 0

        print("gesture:%11s, score:%1.3s, counter:%d" % (gesture, detect_score, Counter))
    else :
        Counter = 0


video = cv2.VideoCapture(0)
timestamp = 0

# landmarkの繋がり表示用
landmark_line_ids = [
    (0, 1), (1, 5), (5, 9), (9, 13), (13, 17), (17, 0),  # 掌
    (1, 2), (2, 3), (3, 4),         # 親指
    (5, 6), (6, 7), (7, 8),         # 人差し指
    (9, 10), (10, 11), (11, 12),    # 中指
    (13, 14), (14, 15), (15, 16),   # 薬指
    (17, 18), (18, 19), (19, 20),   # 小指
]

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
        # The recognizer is initialized. Use it here.
        while video.isOpened():
            # Capture frame-by-frame
            ret, frame = video.read()

            if not ret:
                print("Ignoring empty frame")
                break

            frame = cv2.flip(frame, 1)          # 画像を左右反転
            frame_h, frame_w, _ = frame.shape     # サイズ取得

            timestamp += 1
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
            # Send live image data to perform gesture recognition
            # The results are accessible via the `result_callback` provided in
            # the `GestureRecognizerOptions` object.
            # The gesture recognizer must be created with the live stream mode.
            recognizer.recognize_async(mp_image, timestamp)

            if Result:
                # 検出した手の数分繰り返し
                for hand_landmark in Result.hand_landmarks:
                    # landmarkの繋がりをlineで表示
                    for line_id in landmark_line_ids:
                        # 1点目座標取得
                        lm = hand_landmark[line_id[0]]
                        lm_pos1 = (int(lm.x * frame_w), int(lm.y * frame_h))
                        # 2点目座標取得
                        lm = hand_landmark[line_id[1]]
                        lm_pos2 = (int(lm.x * frame_w), int(lm.y * frame_h))
                        # line描画
                        cv2.line(frame, lm_pos1, lm_pos2, (128, 0, 0), 1)

                        # landmarkをcircleで表示
                        z_list = [lm.z for lm in hand_landmark]
                        z_min = min(z_list)
                        z_max = max(z_list)
                        for lm in hand_landmark:
                            lm_pos = (int(lm.x * frame_w), int(lm.y * frame_h))
                            lm_z = int((lm.z - z_min) / (z_max - z_min) * 255)
                            cv2.circle(frame, lm_pos, 3, (255, lm_z, lm_z), -1)

            cv2.imshow("camera", frame)

            if Counter == 5:
                Flag = True

            if Flag == True:
                Flag = False

                file_list = glob.glob('.\wavfiles\*.wav')
                wavfile_fullpath = random.choice(file_list)
                print (wavfile_fullpath)
                playsound.playsound(wavfile_fullpath)

                # 音声再生後、counter が 15 のままだと、音声がループするため
                Counter += 1

            if cv2.waitKey(5) & 0xFF == 27:
                break

video.release()
cv2.destroyAllWindows()
