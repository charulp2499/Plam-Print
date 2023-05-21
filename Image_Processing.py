import os
import cv2
import numpy as np

def process_image(root_folder, output_folder):
    for root, dirs, files in os.walk(root_folder):
        for folder in dirs:
            folder_path = os.path.join(root, folder)
            output_subfolder = os.path.join(output_folder, os.path.relpath(folder_path, root_folder))

            # Create the output subfolder
            os.makedirs(output_subfolder, exist_ok=True)

            # Iterate through files in the subfolder
            for file in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file)
                if file.endswith(".jpg"):
                    
                    image = cv2.imread(file_path)

                    # Apply sharpening filter to the resized image
                    kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
                    sharpened_image = cv2.filter2D(image, -1, kernel)

                    # smoothed = cv2.medianBlur(sharpened_image, 5)

                    subfolder = os.path.basename(folder_path)
                    image_name = os.path.splitext(file)[0]
                    image_name = image_name.replace(".", "_")
                    
                    # output_file = os.path.join(output_subfolder, file)
                    output_file = os.path.join(output_subfolder, f"{root[-1]}_{subfolder}_{image_name}.jpg")
                    print(output_file)
                    cv2.imwrite(output_file, sharpened_image)
        
    print("Image dataset preprocessing complete.")

# Define the paths

root_folder = "E:/Projects/Palm Print Detection/Datasets/Database_Image_Resize"
output_folder = "E:/Projects/Palm Print Detection/Preprocessed_Dataset"

process_image(root_folder, output_folder)

