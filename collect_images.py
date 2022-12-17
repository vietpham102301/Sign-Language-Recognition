import cv2
import os
import time
import uuid

IMAGES_PATH = 'Tensorflow/workspace/images/collectedimages'


# create more label to translate (just for reminder)
labels = ['hello', 'hey', 'yes', 'no', 'iloveyou']
# specify the number of images will take
number_imgs = 30

label = 'iloveyou'

if not os.path.exists('Tensorflow\workspace\images\collectedimages\\' + label):
    os.mkdir('Tensorflow\workspace\images\collectedimages\\' + label)

cap = cv2.VideoCapture(0)
print('Start collecting images for {}'.format(label))
time.sleep(5)
for imgnum in range(number_imgs):
    ret, frame = cap.read()
    image_name = os.path.join(IMAGES_PATH, label, label + '.' + '{}.jpg'.format(str(uuid.uuid1())))
    cv2.imwrite(image_name, frame)
    cv2.imshow('frame', frame)
    time.sleep(2)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()

# Cân nhắc làm thủ công bước này cho đơn giản