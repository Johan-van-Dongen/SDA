import numpy as np
import cv2

img = cv2.imread('shapes.png')
imgGrey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_, thrash = cv2.threshold(imgGrey, 240, 255, cv2.THRESH_BINARY)
contours, _ = cv2.findContours(thrash, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

cv2.imshow("img", img)
for contour in contours:
    approx = cv2.approxPolyDP(contour, 0.01* cv2.arcLength(contour, True), True)
    cv2.drawContours(img, [approx], 0, (0, 0, 0), 5)
    x = approx.ravel()[0]
    y = approx.ravel()[1] - 5
    if len(approx) == 3:
        cv2.putText(img, "Triangle", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))
    elif len(approx) == 4:
        x1 ,y1, w, h = cv2.boundingRect(approx)
        aspectRatio = float(w)/h
        print(aspectRatio)
        if aspectRatio >= 0.95 and aspectRatio <= 1.05:
          cv2.putText(img, "square", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))
        else:
          cv2.putText(img, "rectangle", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))
    elif len(approx) == 5:
        cv2.putText(img, "Pentagon", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))
    elif len(approx) == 6:
        cv2.putText(img, "hexagon", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))
    else:
        cv2.putText(img, "Circle", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))

# Initialize a list to store centroid coordinates
centroids = []
colors = []

# Loop over the contours and calculate centroids
for contour in contours:
    # Calculate moments
    M = cv2.moments(contour)

    # Check if the contour has a valid area to avoid division by zero
    if M['m00'] != 0:
        # Calculate centroid coordinates
        Cx = int(M['m10'] / M['m00'])
        Cy = int(M['m01'] / M['m00'])

        color2 = img[Cy, Cx]     
      
        #append the color to the list
        colors.append(color2)

         # Append the centroid coordinates to the list
        centroids.append((Cx, Cy))

        
for i, color in enumerate(colors):   
    print(f"Color at Centroid {i+1} (B, G, R):", color)

# Print the centroid coordinates for all shapes
for i, centroid in enumerate(centroids):
    print(f"Centroid {i+1} Coordinates (x, y):", centroid)
    cv2.circle(img, centroid, 5, (0, 0, 0), -1)  # zwart circle
# Draw a circle at the centroid
    

cv2.imshow ("Centroids",img)
##cv2.imshow("shapes", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
