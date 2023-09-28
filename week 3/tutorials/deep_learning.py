import cv2
import numpy as np

# read the ImageNet class names
with open('../../input/classification_classes_ILSVRC2012.txt', 'r') as f:
   image_net_names = f.read().split('\n')
# final class names (just the first word of the many ImageNet names for one image)
class_names = [name.split(',')[0] for name in image_net_names]

# load the neural network model
model = cv2.dnn.readNet(model='../../input/DenseNet_121.caffemodel', config='../../input/DenseNet_121.prototxt', framework='Caffe')

# load the image from disk
image = cv2.imread('../../input/image_1.jpg')
# create blob from image
blob = cv2.dnn.blobFromImage(image=image, scalefactor=0.01, size=(224, 224), mean=(104, 117, 123))
