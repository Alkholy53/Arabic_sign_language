import os  # Import the OS module to interact with the operating system
import pickle  # Import the pickle module for object serialization
import numpy as np  # Import NumPy for numerical operations
import mediapipe as mp  # Import the MediaPipe library for hand tracking
import cv2  # Import OpenCV for image processing
import matplotlib.pyplot as plt  # Import Matplotlib for visualization

mp_hands = mp.solutions.hands  # Define the MediaPipe hands module
mp_drawing = mp.solutions.drawing_utils  # Utility functions for drawing landmarks
mp_drawing_styles = mp.solutions.drawing_styles  # Drawing styles for landmarks

hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)  # Initialize hand tracking

DATA_DIR = './data'  # Define the directory path containing the collected data

data = []  # Initialize an empty list to store extracted hand landmark data
labels = []  # Initialize an empty list to store corresponding labels (class information)

# Loop through each directory in DATA_DIR (each directory represents a class)
for dir_ in os.listdir(DATA_DIR):
    for img_path in os.listdir(os.path.join(DATA_DIR, dir_)):  # Loop through images in each class directory
        data_aux = []  # Initialize an auxiliary list to temporarily store hand landmark data

        x_ = []  # Temporary list to store x-coordinates of landmarks
        y_ = []  # Temporary list to store y-coordinates of landmarks

        img = cv2.imread(os.path.join(DATA_DIR, dir_, img_path))  # Read the image using OpenCV
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert BGR image to RGB

        results = hands.process(img_rgb)  # Process the image to detect hand landmarks using MediaPipe
        if results.multi_hand_landmarks:  # If hand landmarks are detected
            for hand_landmarks in results.multi_hand_landmarks:  # Loop through detected hand landmarks
                for i in range(len(hand_landmarks.landmark)):  # Loop through each landmark point
                    x = hand_landmarks.landmark[i].x  # Get x-coordinate of the landmark
                    y = hand_landmarks.landmark[i].y  # Get y-coordinate of the landmark

                    x_.append(x)  # Append x-coordinate to temporary list
                    y_.append(y)  # Append y-coordinate to temporary list

                # Normalize the landmark coordinates
                for i in range(len(hand_landmarks.landmark)):
                    x = hand_landmarks.landmark[i].x
                    y = hand_landmarks.landmark[i].y
                    data_aux.append(x - min(x_))  # Normalize x-coordinate
                    data_aux.append(y - min(y_))  # Normalize y-coordinate

            # Check if data_aux is not empty and has the expected length (adjust length as needed)
            if data_aux and len(data_aux) == 42:  # 21 landmarks with x, y coordinates
                data.append(data_aux)  # Append normalized hand landmark data to the main data list
                labels.append(dir_)  # Append corresponding label to the labels list

data = np.array(data)  # Convert the list of lists into a NumPy array for efficiency
labels = np.array(labels)  # Convert the labels list into a NumPy array for efficiency

f = open('data.pickle', 'wb')  # Open a file in binary write mode to store the processed data
pickle.dump({'data': data, 'labels': labels}, f)  # Serialize and store the data and labels in a pickle file
f.close()  # Close the file
