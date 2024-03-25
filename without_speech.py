import pickle
import cv2
import mediapipe as mp
import numpy as np
import arabic_reshaper
from bidi.algorithm import get_display
from PIL import ImageFont, ImageDraw, Image
import sys
sys.stdout.reconfigure(encoding='utf-8')
# Load the trained model and set up the camera capture
model_dict = pickle.load(open('./model.p', 'rb'))
model = model_dict['model']
cap = cv2.VideoCapture(0)

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

# Dictionary mapping label indices to Arabic words
labels_dict = {
    0: 'مرحبا', 1: 'كيف حالك', 2: 'كم', 3: 'مته', 4: 'مين', 5: 'ملعب', 6: 'ماذا', 7: 'فين', 8: 'شركة', 9: 'احبك'
}

# Load the Arabic font for rendering
fontpath = "arial.ttf"  # Replace with the path to your Arabic font file
font = ImageFont.truetype(fontpath, 50)

while True:
    ret, frame = cap.read()
    H, W, _ = frame.shape
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(frame_rgb)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            x_ = []  # Reset x_ list for each hand
            y_ = []  # Reset y_ list for each hand

            mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())

            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y

                x_.append(x)
                y_.append(y)

            data_aux = []
            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y
                data_aux.append(x - min(x_))
                data_aux.append(y - min(y_))

            prediction = model.predict([np.asarray(data_aux)])
            predicted_character = labels_dict[int(prediction[0])]

            x1 = int(min(x_) * W) - 10
            y1 = int(min(y_) * H) - 10

            x2 = int(max(x_) * W) - 10
            y2 = int(max(y_) * H) - 10

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 4)

            # Render Arabic text onto the frame using the custom font
            reshaped_text = arabic_reshaper.reshape(predicted_character)
            bidi_text = get_display(reshaped_text)
            img_pil = Image.fromarray(frame)
            draw = ImageDraw.Draw(img_pil)
            draw.text((x1, y1 - 50), bidi_text, font=font, fill=(0, 0, 0))
            frame = np.array(img_pil)

            print(reshaped_text)

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
