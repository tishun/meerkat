'''
<<<<<<< HEAD
Reads camera sensor readings and sends them to a remote location to be stored
'''
from picamera.array import PiRGBArray
from picamera import PiCamera
from .transport import Transport
import RPi.GPIO as GPIO
import argparse
import datetime
import time
import cv2

DEBUG_MODE = False                              # Enables camera renderting for debug purposes

SENSOR_TYPE = 'CAM'                             # Camera sensor

# GPIO for physical debugging
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(13, GPIO.OUT)                        # GREEN led indicating nothing detected
GPIO.setup(11, GPIO.OUT)                        # RED led indicating objects detected


# initialize constants - play with those to achive best results
CAM_FRAMERATE = 24
CAM_RES_WIDTH = 640
CAM_RES_HEIGHT = 480
CAM_WARMUP = 5

DILATE_ITERATIONS = 5                           # 2-50 Large values help to connect blobs. Use large for low light
GAUSIAN_BLUR = 21                               # Blurs contours
DIFF_THRESHOLD = 20                             # Diff between objects and first frame. Lower values for low light
DIFF_ALGO = cv2.THRESH_BINARY+cv2.THRESH_OTSU   # cv2.THRESH_BINARY or cv2.THRESH_OTSU
BLOB_AREA_THRESHHOLD = 500                      # The minimal area of blobs detected in pixels

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (CAM_RES_WIDTH, CAM_RES_HEIGHT)
camera.framerate = CAM_FRAMERATE
rawCapture = PiRGBArray(camera, size=(CAM_RES_WIDTH, CAM_RES_HEIGHT))

# allow the camera to warmup
time.sleep(CAM_WARMUP)
 
# initialize the first frame in the video stream
firstFrame = None
lastReading = None
transport = Transport()

# capture frames from the camera
for myFrame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
        text = "Unoccupied"

        frame = myFrame.array
        # resize the frame, convert it to grayscale, and blur it
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (GAUSIAN_BLUR, GAUSIAN_BLUR), 0)
        
        # if the first frame is None, initialize it
        if firstFrame is None:
                firstFrame = gray
                rawCapture.truncate(0)
                continue

        # compute the absolute difference between the current frame and
        # first frame
        frameDelta = cv2.absdiff(firstFrame, gray)
        adaptivedDiffThreshold, thresh = cv2.threshold(frameDelta, DIFF_THRESHOLD, 255, DIFF_ALGO)
 
        # dilate the thresholded image to fill in holes, then find contours
        # on thresholded image
        thresh = cv2.dilate(thresh, None, iterations=DILATE_ITERATIONS)
        (img, cnts, hierarchy) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)

        # loop over the contours
        for c in cnts:
                
                # if the adaptive threshold is too small or the contour is too small, ignore it
                if adaptivedDiffThreshold < DIFF_THRESHOLD or cv2.contourArea(c) < BLOB_AREA_THRESHHOLD:
                        text = "Unoccupied"
                        continue
 
                # compute the bounding box for the contour, draw it on the frame,
                # and update the text
                (x, y, w, h) = cv2.boundingRect(c)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                text = "Occupied"
                
        # Change LED state and send data when room has changed state from
        # occupied to unoccupied and vice versa
        if(text!=lastReading):
             lastReading = text
             if(text == "Unoccupied"):
                  GPIO.output(11, 0)
                  transport.send(SENSOR_TYPE, 0)
             else:
                  GPIO.output(11, 1)
                  transport.send(SENSOR_TYPE, 1)
 
        # draw the text and timestamp on the frame
        cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
 
        # show the frame and record if the user presses a key
        if(DEBUG_MODE):
             cv2.imshow("Video Feed", frame)
             cv2.imshow("Thresh", thresh)
             cv2.imshow("Frame Delta", frameDelta)

        key = cv2.waitKey(1) & 0xFF
 
        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
             break
        
        # clear the stream in preparation for the next frame
        rawCapture.truncate(0)
         
# cleanup the camera and close any open windows
cv2.destroyAllWindows()
