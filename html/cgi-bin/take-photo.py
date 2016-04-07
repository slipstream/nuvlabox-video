#!/usr/bin/env python

import cv2

import time
import glob
import os
from string import Template

def script_path():
     return os.path.dirname(os.path.realpath(__file__))

def get_image(camera):
     retval, im = camera.read()
     return im

def capture_frame():

     camera_port = 0
     ramp_frames = 30

     camera = cv2.VideoCapture(camera_port)
     
     for i in xrange(ramp_frames):
          temp = get_image(camera)

     frame = get_image(camera)

     del(camera)

     return frame

def identify_faces(frame):

     cascade_path = os.path.join(script_path(),
                                 'haarcascade_frontalface_default.xml')

     # Create the haar cascade
     faceCascade = cv2.CascadeClassifier(cascade_path)

     # Read the image
     #image = cv2.imread(imagePath)
     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

     # Detect faces in the image
     faces = faceCascade.detectMultiScale(
          gray,
          scaleFactor=1.1,
          minNeighbors=5,
          minSize=(30, 30),
          flags = cv2.cv.CV_HAAR_SCALE_IMAGE
     )

     # Draw a rectangle around the faces
     for (x, y, w, h) in faces:
          cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

     return frame
       
def format_page(refresh, frame_file):
     tpl_path = os.path.join(script_path(), 'template.html')
     basename = "/%s" % os.path.basename(frame_file)
     with open(tpl_path) as x: tpl = Template(x.read())
     return tpl.substitute(refresh=refresh, frame_file=basename)

def current_time():
     return int(round(time.time()))

def new_frame_file():
     parent = os.path.join(script_path(), os.pardir)
     return os.path.join(parent, ("frame_%d.png" % current_time()))

def clean_frames():
     parent = os.path.join(script_path(), os.pardir)
     for frame in glob.glob(os.path.join(parent, "frame*.png")):
          os.remove(frame)

def write_frame(frame, frame_file):
     cv2.imwrite(frame_file, frame)

def main():
     print script_path()

     clean_frames()
     refresh = 3
     frame_file = new_frame_file()

     try:
          frame = capture_frame()
          annotated_frame = identify_faces(frame)
          write_frame(annotated_frame, frame_file)
          print format_page(refresh, frame_file)
     except:
          print format_page(refresh, "error.png")
          frame = capture_frame()


if __name__ == "__main__":
     main()

