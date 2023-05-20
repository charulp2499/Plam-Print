import cv2

# Load the image
image = cv2.imread('E:/Projects/Palm Print Detection/Database_Image/01/R/01_fwbw.avi_10.jpg')

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply a blur to reduce noise
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Perform edge detection
edges = cv2.Canny(blurred, 50, 150)

# Find contours in the edge-detected image
contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Sort the contours based on their area (largest to smallest)
contours = sorted(contours, key=cv2.contourArea, reverse=True)

# Iterate over the contours
for contour in contours:
    # Compute the convex hull of the contour
    hull = cv2.convexHull(contour)

    # Calculate the area of the hull
    hull_area = cv2.contourArea(hull)

    # Calculate the area of the contour
    contour_area = cv2.contourArea(contour)

    # Calculate the solidity of the contour
    solidity = float(contour_area) / hull_area

    # If the solidity is within a certain range, consider it as the palm area
    if 0.5 <= solidity <= 1.0:
        # Draw a bounding box around the palm area
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        break  # Stop after finding the palm area

# Display the annotated image
cv2.imshow('Annotated Image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
