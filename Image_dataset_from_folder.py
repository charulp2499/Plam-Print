import os
import cv2
import numpy as np

def process_videos(root_folder, output_folder):
    for root, dirs, files in os.walk(root_folder):
        for folder in dirs:
            folder_path = os.path.join(root, folder)
            output_subfolder = os.path.join(output_folder, os.path.relpath(folder_path, root_folder))

            # Create the output subfolder
            os.makedirs(output_subfolder, exist_ok=True)

            # Iterate through files in the subfolder
            for file in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file)
                if file.endswith(".avi"):
                    # Open the video file
                    cap = cv2.VideoCapture(file_path)
                    count = 0
                    frame_rate = 30
                    frame_number = 0

                    # Iterate through frames
                    while cap.isOpened():
                        ret, frame = cap.read()
                        if not ret:
                            break

                        # Extract one frame per second
                        if frame_number % frame_rate  == 0:

                            # Resize the frame to a scaled size
                            scale_percent = 40 
                            width = int(frame.shape[1] * scale_percent / 100)
                            height = int(frame.shape[0] * scale_percent / 100)
                            resized_frame = cv2.resize(frame, (width, height))
                        
                            # Apply sharpening filter to the resized frame
                            kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
                            sharpened_frame = cv2.filter2D(resized_frame, -1, kernel)

                            output_file = os.path.join(output_subfolder, f"{file}_{count}.jpg")
                            cv2.imwrite(output_file, sharpened_frame)
                            count += 1
                        
                        frame_number += 1

                    cap.release()
        # print(folder)
    print("Image dataset creation complete.")

# Define the paths

root_folder = "E:/Projects/Palm Print Detection/Database/"
output_folder = "E:/Projects/Palm Print Detection/Preprocessed_Dataset"

process_videos(root_folder, output_folder)

