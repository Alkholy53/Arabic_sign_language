from gtts import gTTS  # Import gTTS for text-to-speech
import cv2  # Import OpenCV for video processing
import mediapipe as mp  # Import MediaPipe for hand tracking
import numpy as np
import arabic_reshaper  # For reshaping Arabic text
from bidi.algorithm import get_display  # For handling Arabic text display
from PIL import ImageFont, ImageDraw, Image  # For text rendering
import pickle  # For loading the trained model
import pygame  # For audio playback
import io  # For handling audio data as a stream
import time  # Add the time module

# Initialize pygame mixer for audio playback
pygame.mixer.init()

# Load the trained model and set up the camera capture
model_dict = pickle.load(open('./model.p', 'rb'))  # Load the trained model
model = model_dict['model']  # Retrieve the model from the loaded dictionary
cap = cv2.VideoCapture(0)  # Initialize camera capture (change 0 to your camera index if needed)

# Initialize MediaPipe Hands for hand landmark detection
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)  # Initialize MediaPipe Hands

# Dictionary mapping label indices to Arabic words (for gesture recognition)
labels_dict = {
    0: 'مرحبا', 1: 'كيف حالك', 2: 'كم', 3: 'متى', 4: 'مين',
    5: 'ملعب', 6: 'ماذا', 7: 'فين', 8: 'شركة', 9: 'أحبك'
}

# Load an Arabic font for rendering
fontpath = "arial.ttf"  # Replace with the path to your Arabic font file
font = ImageFont.truetype(fontpath, 50)  # Create an ImageFont object with the Arabic font

while True:
    start_time = time.time()  # Start timing
    ret, frame = cap.read()  # Read a frame from the camera
    H, W, _ = frame.shape  # Get frame dimensions (height, width)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert frame to RGB format

    results = hands.process(frame_rgb)  # Process the frame to detect hand landmarks
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            x_ = []
            y_ = []

            # Draw hand landmarks and connections on the frame
            mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())

            # Extract hand landmark coordinates and normalize
            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y
                x_.append(x)
                y_.append(y)

            # Prepare data for prediction
            data_aux = []
            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y
                data_aux.append(x - min(x_))
                data_aux.append(y - min(y_))

            # Predict gesture using the loaded model
            prediction = model.predict([np.asarray(data_aux)])
            predicted_character = labels_dict[int(prediction[0])]

            # Calculate rectangle coordinates around the detected hand
            x1 = int(min(x_) * W) - 10
            y1 = int(min(y_) * H) - 10
            x2 = int(max(x_) * W) - 10
            y2 = int(max(y_) * H) - 10

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 4)  # Draw rectangle around the hand

            # Convert recognized Arabic text to speech using gTTS
            tts = gTTS(text=predicted_character, lang='ar')
            audio_file = io.BytesIO()
            tts.write_to_fp(audio_file)
            audio_file.seek(0)  # Move the file pointer to the beginning

            # Play the audio using pygame
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()

            # Render Arabic text onto the frame using the custom font
            reshaped_text = arabic_reshaper.reshape(predicted_character)
            bidi_text = get_display(reshaped_text)
            img_pil = Image.fromarray(frame)
            draw = ImageDraw.Draw(img_pil)
            draw.text((x1, y1 - 50), bidi_text, font=font, fill=(0, 0, 0))  # Render text on the frame
            frame = np.array(img_pil)  # Convert back to NumPy array
            end_time = time.time()  # End timing
            execution_time = end_time - start_time
            print(f"Time taken for gesture recognition and speech playback: {execution_time} seconds")


    # Display the frame
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # Break loop on 'q' key press
        break

cap.release()  # Release the camera
cv2.destroyAllWindows()
