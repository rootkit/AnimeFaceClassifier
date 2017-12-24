#Recognize face

import os
import cv2
import sys
import numpy as np

from keras.models import load_model

if len(sys.argv) != 2:
    #print("usage: python predict.py [filename]")
    #sys.exit(1)
	filename = "animeface-character-dataset/thumb/000_hatsune_miku/face_27_136_113.png"
	filename = "images/25631.png"
else:
	filename = sys.argv[1]

print('input:', filename)

classifier = cv2.CascadeClassifier('lbpcascade_animeface.xml')

image = cv2.imread(filename)

gray_image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

faces = classifier.detectMultiScale(gray_image)
#output_dir = 'faces'
#if not os.path.exists(output_dir):
#    os.makedirs(output_dir)

for i, (x,y,w,h) in enumerate(faces):
	margin=w/4

	x2=x-margin
	y2=y-margin
	w2=w+margin
	h2=h+margin

	if(x2<0):
		x2=0
	if(y2<0):
		y2=0
	if(w2>=image.shape[0]):
		w2=image.shape[0]-1
	if(h2>=image.shape[1]):
		h2=image.shape[1]-1

	face_image = image[y2:y2+h2, x2:x2+w2]
	#output_path = os.path.join(output_dir,'{0}.jpg'.format(i))
	#cv2.imwrite(output_path,face_image)

	IMAGE_SIZE = 224
	model = load_model('animeface.hdf5')
	model.summary()

	img = cv2.resize(face_image, (IMAGE_SIZE,IMAGE_SIZE))
	#image.load_img(filename, target_size=(IMAGE_SIZE, IMAGE_SIZE))
	img = img#image.img_to_array(img)
	img = np.expand_dims(img, axis=0)
	img = img / 255.0

	pred = model.predict(img)[0]
	print(pred)

	prob = np.max(pred)
	cls = pred.argmax()

	lines=open('animeface-character-dataset/tools/tag.txt').readlines()
	print prob, cls, lines[cls]

	cv2.rectangle(image, (x2,y2), (x2+w2,y2+h2), color=(0,0,255), thickness=3)
	label=lines[cls]+" "+str(prob)
	cv2.putText(image, label, (x2,y2-8), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8, (0,0,250));

#cv2.imwrite('faces.jpg',image)

cv2.imshow("Faces found", image)
cv2.waitKey(0)

