# import yaml
# import csv
# import random
# import os
# from shutil import copyfile


# def convert_csv_to_yaml(csv_file, output_yaml):
#     data = {'train': [], 'val': [], 'nc': 0, 'names': []}
#     class_labels = set()
    
#     with open(csv_file, 'r') as file:
#         reader = csv.reader(file)
#         next(reader)  # Skip the header row if present
#         for row in reader:
            
#             image_path = row[0]
#             x_min = float(row[1])
#             y_min = float(row[2])
#             x_max = float(row[5])
#             y_max = float(row[6])
#             class_label = row[7]
#             class_labels.add(class_label)
            
#             data_row = {
#                 'img': str(image_path),
#                 'bbox': [x_min, y_min, x_max, y_max],
#                 'label': class_label
#             }
#             data['train'].append(data_row)
    
#     class_labels = list(class_labels)
#     class_labels.sort()
#     data['nc'] = len(class_labels)
#     data['names'] = class_labels
    
#     random.shuffle(data['train'])
#     train_size = int(0.6 * len(data['train']))
#     val_size = int(0.2 * len(data['train']))
    
#     data['val'] = data['train'][train_size:train_size+val_size]
#     data['train'] = data['train'][:train_size]
#     data['test'] = data['train'][train_size+val_size:]
    
#     with open(output_yaml, 'w') as yaml_file:
#         yaml.dump(data, yaml_file)
    
#     # Copy images to respective train, val, and test folders
#     output_folder = os.path.dirname(output_yaml)
#     for split in ['train', 'val', 'test']:
#         split_folder = os.path.join(output_folder, split)
#         os.makedirs(split_folder, exist_ok=True)
#         for row in data[split]:
#             image_path = row['img']
#             image_file = os.path.basename(image_path)
#             src_path = os.path.join(os.path.dirname(csv_file), image_path)
#             dst_path = os.path.join(split_folder, image_file)
#             copyfile(src_path, dst_path)


# csv_file = 'E:/Projects/Palm Print Detection/Labled_Database/Final_Database.csv'
# output_yaml = 'E:/Projects/Palm Print Detection/yolov5_data/dataset.yaml'
# convert_csv_to_yaml(csv_file, output_yaml)


import csv
import os
from PIL import Image

# Define the paths
csv_file = 'E:/Projects/Palm_Print_Detection/Labled_Database/Final_Database.csv'
images_folder = 'E:/Projects/Palm_Print_Detection/Labled_Database'
output_folder = 'E:/Projects/Palm_Print_Detection/yolov5_dataset1'
class_names = ['01_left','01_right','02_left','02_right','03_left','03_right','04_left','04_right','05_left','05_right','06_left','06_right','07_left'
                   ,'07_right','08_left','08_right','09_left','09_right','10_left','10_right','11_left','11_right','12_left','12_right','13_left','13_right'
                   ,'14_left','14_right','15_left','15_right','16_left','16_right','17_left','17_right','18_left','18_right','19_left','19_right','20_left'
                   ,'20_right','21_left','21_right','22_left','22_right','23_left','23_right','24_left','24_right','25_left','25_right','26_left','26_right',
                   '27_left','27_right','28_left','28_right','29_left','29_right','30_left','30_right']

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Read the CSV file
with open(csv_file, 'r') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        image_filename = row['image name']
        image_path = os.path.join(images_folder, image_filename)

        # Load the image
        image = Image.open(image_path)
        image_width, image_height = image.size

        # Create the YOLOv5 annotation file
        annotation_filename = os.path.splitext(image_filename)[0] + '.txt'
        annotation_path = os.path.join(output_folder, annotation_filename)

        with open(annotation_path, 'w') as annotation_file:
            for i in range(len(row['xmin'])):
                x_min = float(row['xmin'][i])
                y_min = float(row['ymin'][i])
                x_max = float(row['x_max'][i])
                y_max = float(row['height'][i])

                # Convert to YOLO format
                x_center = (x_min + x_max / 2)
                y_center = (y_min + y_max / 2)
                # width /= image_width
                # height /= image_height

                # Write the annotation to the YOLOv5 format file
                class_index = class_names.index(row['label'][i])
                annotation_file.write(f"{class_index} {x_center} {y_center} \n")

        # Save the image in the output folder
        image.save(os.path.join(output_folder, image_filename))
