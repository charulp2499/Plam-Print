import os
import csv

def create_csv_dataset(data_dir, output_file):
    with open(output_file, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Image_Path', 'Label'])  # Writing the header row

        for person_id in range(1, 31):  # Assuming 30 persons in the dataset
            left_hand_dir = os.path.join(data_dir, f'{person_id}/L')
            right_hand_dir = os.path.join(data_dir, f'{person_id}/R')

            # Get the filenames of left and right hand images
            left_hand_files = os.listdir(left_hand_dir)
            right_hand_files = os.listdir(right_hand_dir)

            # Create rows for left hand images
            for left_hand_file in left_hand_files:
                image_path = os.path.join(left_hand_dir, left_hand_file)
                csvwriter.writerow([image_path, 'palm'])  # Assuming all left hand images have a palm label

            # Create rows for right hand images
            for right_hand_file in right_hand_files:
                image_path = os.path.join(right_hand_dir, right_hand_file)
                csvwriter.writerow([image_path, 'non_palm'])  # Assuming all right hand images do not have a palm label

# Set the path to the directory containing the left and right hand images
data_directory = "E:/Projects/Palm Print Detection/Database_Image"

# Set the path for the output CSV file
output_csv_file = "E:/Projects/Palm Print Detection/output/dataset.csv"

# Create the CSV dataset
create_csv_dataset(data_directory, output_csv_file)
