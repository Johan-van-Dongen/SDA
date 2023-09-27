import cv2 

img_gray = cv2.imread('test.png', 0)
cv2.imshow('Gray Image', img_gray)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imwrite('gray_image.png', img_gray)	
