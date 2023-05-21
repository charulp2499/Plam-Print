import os
import cv2
import csv
import xml.etree.ElementTree as ET

folder_path = 'E:/Projects/Palm Print Detection/Preprocessed_Dataset/30/R'

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
    # label = "30_left"
    label = "30_right"
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