# import cv2

# # Load the pre-trained Haar cascade classifier for palm detection
# palm_cascade = cv2.CascadeClassifier('palm_cascade.xml')

# # Read the input image
# image = cv2.imread('E:/Projects/Palm Print Detection/Database_Image/01/R/01_fwbw.avi_10.jpg')

# # Convert the image to grayscale
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# # Perform palm detection
# palms = palm_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(100, 100))

# # Draw bounding boxes around the detected palms
# for (x, y, w, h) in palms:
#     cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

# # Display the image with palm detection
# cv2.imshow('Palm Detection', image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

import cv2
import numpy as np

# Load pre-trained YOLOv3 model
net = cv2.dnn.readNetFromDarknet('yolov3.cfg', 'yolov3.weights')

# Load class labels
classes = []
with open('coco.names', 'r') as f:
    classes = [line.strip() for line in f.readlines()]

# Set input image and output layers
image = cv2.imread('E:/Projects/Palm Print Detection/Database_Image/01/R/01_fwbw.avi_10.jpg')
height, width, _ = image.shape
blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416), swapRB=True, crop=False)
net.setInput(blob)
layer_names = net.getLayerNames()
output_layers = [layer_names[i-1] for i in net.getUnconnectedOutLayers()]

# Perform object detection
outputs = net.forward(output_layers)

# Process detection results
for output in outputs:
    for detection in output:
        scores = detection[5:]
        class_id = np.argmax(scores)
        confidence = scores[class_id]
        if confidence > 0.5 and classes[class_id] == 'person':
            center_x = int(detection[0] * width)
            center_y = int(detection[1] * height)
            w = int(detection[2] * width)
            h = int(detection[3] * height)
            x = int(center_x - w / 2)
            y = int(center_y - h / 2)
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

# Display the resulting image
cv2.imshow('Palm Detection', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
