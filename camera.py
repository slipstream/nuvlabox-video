#!/usr/bin/env python
import os
import cv2

class Camera(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.video = cv2.VideoCapture(0)
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')
    
    def __del__(self):
        self.video.release()

    def script_path(self):
        return os.path.dirname(os.path.realpath(__file__))

    def identify_faces(self, frame):

        cascade_path = os.path.join(self.script_path(),
                                 'haarcascade_frontalface_default.xml')

        # Create the haar cascade
        faceCascade = cv2.CascadeClassifier(cascade_path)

        # Read the image
        # image = cv2.imread(imagePath)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the image
        faces = faceCascade.detectMultiScale(
           gray,
           scaleFactor=1.1,
           minNeighbors=20,
           minSize=(60, 60),
           flags = cv2.cv.CV_HAAR_SCALE_IMAGE
        )

        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
           cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        return frame

    
    def get_frame(self):
        success, img = self.video.read()
        image =  self.identify_faces(img)
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def gen(self):
        """Video streaming generator function."""
        while True:
            frame = self.get_frame()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def main():
    camera = Camera().gen()
