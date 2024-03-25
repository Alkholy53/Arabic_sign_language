import os  # Import the OS module to interact with the operating system
import cv2  # Import the OpenCV library for image and video processing
import time  # Import the time module for time-related functions

DATA_DIR = './data'  # Define the main directory path to store data
if not os.path.exists(DATA_DIR):  # Check if the main directory exists
    os.makedirs(DATA_DIR)  # Create the main directory if it doesn't exist

number_of_classes = 10  # Define the number of classes or categories for the dataset
dataset_size = 100  # Define the number of images to capture for each class

cap = cv2.VideoCapture(0)  # Initialize a video capture object from the default camera (index 0)
for j in range(number_of_classes):  # Loop through each class
    if not os.path.exists(os.path.join(DATA_DIR, str(j))):  # Check if the class directory exists
        os.makedirs(os.path.join(DATA_DIR, str(j)))  # Create the class directory if it doesn't exist

    print('Collecting data for class {}'.format(j))  # Print the current class being processed

    done = False
    while True:  # Loop until 'q' key is pressed
        ret, frame = cap.read()  # Read a frame from the camera
        cv2.putText(frame, 'Ready? Press "Q" ! :)', (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3,
                    cv2.LINE_AA)  # Put text on the frame to prompt the user to press 'Q'
        cv2.imshow('frame', frame)  # Display the frame
        if cv2.waitKey(25) == ord('q'):  # If 'q' key is pressed, break the loop
            break

    counter = 0
    while counter < dataset_size:  # Loop to capture the specified number of images for the class
        ret, frame = cap.read()  # Read a frame from the camera
        cv2.imshow('frame', frame)  # Display the frame
        cv2.waitKey(25)  # Wait for a short duration
        cv2.imwrite(os.path.join(DATA_DIR, str(j), '{}.jpg'.format(counter)), frame)  # Save the frame as an image

        counter += 1  # Increment the counter for the number of captured images
        time.sleep(.5)  # Add a 0.5-second delay between capturing images

cap.release()  # Release the video capture object
cv2.destroyAllWindows()  # Close all OpenCV windows
