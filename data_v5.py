import yaml
import csv
import random
import os
from shutil import copyfile


def convert_csv_to_yaml(csv_file, output_yaml):
    data = {'train': [], 'val': [], 'nc': 0, 'names': []}
    class_labels = set()
    
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row if present
        for row in reader:
            
            image_path = row[0]
            x_min = float(row[1])
            y_min = float(row[2])
            x_max = float(row[5])
            y_max = float(row[6])
            class_label = row[7]
            class_labels.add(class_label)
            
            data_row = {
                'img': str(image_path),
                'bbox': [x_min, y_min, x_max, y_max],
                'label': class_label
            }
            data['train'].append(data_row)
    
    class_labels = list(class_labels)
    class_labels.sort()
    data['nc'] = len(class_labels)
    data['names'] = class_labels
    
    random.shuffle(data['train'])
    train_size = int(0.6 * len(data['train']))
    val_size = int(0.2 * len(data['train']))
    
    data['val'] = data['train'][train_size:train_size+val_size]
    data['train'] = data['train'][:train_size]
    data['test'] = data['train'][train_size+val_size:]
    
    with open(output_yaml, 'w') as yaml_file:
        yaml.dump(data, yaml_file)
    
    # Copy images to respective train, val, and test folders
    output_folder = os.path.dirname(output_yaml)
    for split in ['train', 'val', 'test']:
        split_folder = os.path.join(output_folder, split)
        os.makedirs(split_folder, exist_ok=True)
        for row in data[split]:
            image_path = row['img']
            image_file = os.path.basename(image_path)
            src_path = os.path.join(os.path.dirname(csv_file), image_path)
            dst_path = os.path.join(split_folder, image_file)
            copyfile(src_path, dst_path)


csv_file = 'E:/Projects/Palm Print Detection/Labled_Database/Final_Database.csv'
output_yaml = 'E:/Projects/Palm Print Detection/yolov5_data/dataset.yaml'
convert_csv_to_yaml(csv_file, output_yaml)

