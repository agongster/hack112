import pygame
from pygame.locals import *
import cv2 as cv
from PIL import Image 
import numpy as np
import sys
import time, random, math, os
from util import get_limits

yellow = [0, 255, 255] #yellow in BGR
spaceship = pygame.image.load("C:\\Users\\Monke\\OneDrive\\Desktop\\15-112\\opencvApp\\spaceship.png")

width, height = 800, 800
WIN = pygame.display.set_mode((width, height))
pygame.display.set_caption('kill me')
x, y = 400, 400
FPS = 40


#################

def redrawAll():
    WIN.fill((255, 255, 255))
    WIN.blit(spaceship, (width-aspectRatio*x, aspectRatio*y))
    pygame.display.update()

##############################
cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

capWidth = cv.CAP_PROP_FRAME_WIDTH #4
capHeight = cv.CAP_PROP_FRAME_HEIGHT #3
aspectRatio = capHeight/capWidth if capHeight > capWidth else capWidth/capHeight
print(capWidth, capHeight)


while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    # Our operations on the frame come here
    lowerLimit, upperLimit = get_limits(yellow)
    hsvImage = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    mask = cv.inRange(hsvImage, lowerLimit, upperLimit)
    mask_ = Image.fromarray(mask)

    bbox = mask_.getbbox()
    if bbox is not None:
        x1, y1, x2, y2 = bbox
        x, y = x1, y1
        print(x, y)
        frame = cv.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)

    cv.imshow('frame', cv.flip(frame, 1))
    # Display the resulting frame
    if cv.waitKey(1) == ord('q'):
        break
    
    redrawAll()

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()