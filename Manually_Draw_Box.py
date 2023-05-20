import os
import cv2
import csv

# Folder path containing the images
folder_path = 'E:/Projects/Palm Print Detection/1/L'

# Get a list of image files in the folder
image_files = [f for f in os.listdir(folder_path) if f.endswith('.jpg')]

# List to store the annotations
annotations = []

# Iterate over the image files
for image_file in image_files:
    # Load the image
    image_path = os.path.join(folder_path, image_file)
    image = cv2.imread(image_path)

    # Manually label the palm regions
    print('Please draw rectangles around the palm regions. Press enter when finished.')
    bboxes = []
    labels = []

    while True:
        # Prompt the user to draw a rectangle
        rect = cv2.selectROI('Image', image)

        # Get the rectangle coordinates
        x, y, w, h = rect

        # Store the bounding box coordinates
        bboxes.append([x, y, w, h])

        # Prompt the user to enter a label for the palm region
        label = input('Enter the label for the palm region: ')
        labels.append(label)

        # Ask the user if they want to draw another rectangle
        answer = input('Do you want to draw another rectangle? (Y/N): ')
        if answer.lower() == 'n':
            break

    # Add the annotations for the image to the list
    annotations.append({'image': image_file, 'bboxes': bboxes, 'labels': labels})

# Save the annotations in a CSV file
csv_file_path = os.path.join(folder_path, 'annotations.csv')
with open(csv_file_path, 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['image', 'x', 'y', 'width', 'height', 'label'])
    for annotation in annotations:
        image_file = annotation['image']
        bboxes = annotation['bboxes']
        labels = annotation['labels']
        for bbox, label in zip(bboxes, labels):
            x, y, w, h = bbox
            writer.writerow([image_file, x, y, w, h, label])

print('Annotations saved in annotations.csv')
