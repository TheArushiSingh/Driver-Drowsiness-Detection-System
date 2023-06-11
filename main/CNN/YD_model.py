import cv2
import numpy as np
from PIL import Image
from keras.models import model_from_json

facec = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
model_json_file = r'model.json'
with open(model_json_file, "r") as json_file:
            loaded_model_json = json_file.read()
            model = model_from_json(loaded_model_json)

model.load_weights(r'model_weights.h5')

def img_prep(arg):
     im = Image.fromarray(arg,'RGB')
     img_array = np.array(im)
     img_array = np.expand_dims(img_array, axis=0)
     return img_array

video = cv2.VideoCapture(0)

while True: 
        _, fr = video.read()
        faces = facec.detectMultiScale(fr, 1.3, 5)
        for (x, y, w, h) in faces:
            fc = gray_fr[y:y+h, x:x+w]
            img_array = img_prep(fc)
            prediction = int(model.predict(img_array)[0][0])
            if prediction==1:
               cv2.putText(frame,"Yawning",(10, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255))
            elif prediction==0:
               cv2.putText(frame,"Not Yawning",(10, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0))
        cv2.imshow("Yawn Detection",fr)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
video.release()
cv2.destroyAllWindows()
