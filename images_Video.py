# import cv2

# video_path = "E:/Projects/Palm Print Detection/Database/01/L/01_fofc.avi"
# output_directory = "E:/Projects/Palm Print Detection/database/"
# frame_rate = 30  # Desired frame rate
# print(output_directory)

# cap = cv2.VideoCapture(video_path)
# count = 0
# frame_number = 0

# while cap.isOpened():
#     ret, frame = cap.read()
#     if not ret:
#         break

#     if frame_number % frame_rate == 0:
#         output_path = output_directory + "frame{:06d}.jpg".format(count)
#         cv2.imwrite(output_path, frame)
#         count += 1

#     frame_number += 1

# cap.release()
# cv2.destroyAllWindows()

import cv2

video_path = "E:/Projects/Palm Print Detection/Database/01/L/01_fofc.avi"
output_directory = "E:/Projects/Palm Print Detection/database/"
frame_rate = 30  # Desired frame rate

cap = cv2.VideoCapture(video_path)
count = 0
frame_number = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    if frame_number % frame_rate == 0:
        output_path = output_directory + "frame{:06d}.jpg".format(count)
        cv2.imwrite(output_path, frame)
        count += 1

    frame_number += 1

cap.release()
cv2.destroyAllWindows()
