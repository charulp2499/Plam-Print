import os
import cv2
import csv
import xml.etree.ElementTree as ET

folder_path = 'E:/Projects/Palm Print Detection/Preprocessed_Dataset/01/L'

# Get a list of image files in the folder
image_files = [f for f in os.listdir(folder_path) if f.endswith('.jpg')]
annotation_root = ET.Element('Database')
annotations = []

# Iterate over the image files
for image_file in image_files:
    
    image_path = os.path.join(folder_path, image_file)
    image = cv2.imread(image_path)

    bboxes = []
    labels = []

    rect = cv2.selectROI('Image', image)

    x, y, w, h = rect

    bboxes.append([x, y, w, h])

    # Prompt the user to enter a label for the palm region
    label = "01_left"
    labels.append(label)
    
    annotations.append({'image': image_file, 'bboxes': bboxes, 'labels': labels})

    # Create the annotation entry for the image
    annotation_element = ET.SubElement(annotation_root, 'annotation')
    filename_element = ET.SubElement(annotation_element, 'image')
    filename_element.text = image_file
    
    # Iterate over the bounding boxes
    for bbox, label in zip(bboxes, labels):
        xmin, ymin, width, height = bbox
        xmax = xmin + width
        ymax = ymin + height

        object_element = ET.SubElement(annotation_element, 'object')
        name_element = ET.SubElement(object_element, 'name')
        name_element.text = label
        bndbox_element = ET.SubElement(object_element, 'bndbox')
        xmin_element = ET.SubElement(bndbox_element, 'xmin')
        xmin_element.text = str(xmin)
        ymin_element = ET.SubElement(bndbox_element, 'ymin')
        ymin_element.text = str(ymin)
        xmax_element = ET.SubElement(bndbox_element, 'xmax')
        xmax_element.text = str(xmax)
        ymax_element = ET.SubElement(bndbox_element, 'ymax')
        ymax_element.text = str(ymax)

# Create the XML tree and save to file
xml_tree = ET.ElementTree(annotation_root)
xml_file_path = os.path.join(folder_path, 'Database.xml')
xml_tree.write(xml_file_path)

# Save the annotations in a CSV file
csv_file_path = os.path.join(folder_path, 'Database.csv')
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

print('Annotations saved in annotations csv and XML')


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