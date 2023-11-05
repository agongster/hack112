import pygame
import random
import os
import math
import time
import cv2 as cv
from PIL import Image
from util import get_limits

level = 0
mouthWidth = 200
foods = []
gravity = 2
yellow = [0, 255, 255]
cursorX, cursorY = 400, 400
meatBumped = 0



WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('kill me')
x, y = 400, 400
FPS = 25

meat = pygame.image.load(os.path.join('meat.png'))
heart = pygame.image.load(os.path.join('heart.png'))
dragon = pygame.image.load(os.path.join('dragon.png'))
pat = pygame.image.load(os.path.join('pat_virtue.png'))
mike = pygame.image.load(os.path.join('mike_taylor.png'))
cursor = pygame.image.load(os.path.join("cursor.png"))
gates = pygame.image.load(os.path.join('gates.jpeg')).convert()
gates.set_alpha(200)

meat = pygame.transform.scale(meat, (100, 100))
heart = pygame.transform.scale(heart, (50, 50))
dragon = pygame.transform.scale(dragon, (600, 200))
pat = pygame.transform.scale(pat, (175, 175))
mike = pygame.transform.scale(mike, (100, 100))
cursor = pygame.transform.scale(cursor, (50, 50))
cursor = pygame.transform.rotate(cursor, -90)
gates = pygame.transform.scale(gates, (800, 800))


cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()
capWidth = cv.CAP_PROP_FRAME_WIDTH #4
capHeight = cv.CAP_PROP_FRAME_HEIGHT #3
aspectRatio = capHeight/capWidth if capHeight > capWidth else capWidth/capHeight

def restart():
    global foods
    foods = []

def takeStep(life):
    i=0
    while i<len(foods):
        (x, y, vx, vy,image) =foods[i]
        if y>600 and (x<650) and (x>150):
            foods.remove(foods[i])
            if image!=meat and life>=1:
                return (life-1)
        else:
            x += vx
            y += vy
            vy += gravity
            foods[i] = (x, y, vx, vy,image)
            i+=1

def drawBalls():
    for (x, y, vx, vy,image) in foods:
        WIN.blit(image,(x,y))

def drawCursor():
    WIN.blit(cursor, (40+WIDTH-aspectRatio*cursorX, aspectRatio*cursorY))
    
def distance(x1, y1, x2, y2):
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)

def launchFood(): #add food data to foods
    if random.random() > 0.5: #launch from left
        x0 = -100 + random.random()*200
    else: #launch from right
        x0 = 900 - random.random()*200
    x1 = (WIDTH - mouthWidth)/2 + random.random()*mouthWidth
    h = 550 + random.random()*250
    t = (2*gravity + math.sqrt(4*gravity**2 + 32*h*gravity))/(2*gravity)
    vx = (x1-x0)/t
    vy = -0.5*gravity*t
    imageList=[mike,pat,mike,meat,pat,meat,mike, pat]
    image=imageList[random.randrange(len(imageList))]
    foods.append((x0, 800, vx, vy,image))

def checkContact():
    for i in range(len(foods)):
        (x, y, vx, vy, name) = foods[i]
        if distance(x, y, WIDTH-aspectRatio*cursorX, cursorY) < 55:
            bumpFood(i, x)

def bumpFood(bumpedIndex, x):
    (x, y, vx, vy, name) = foods[bumpedIndex]
    if name == meat:
        global meatBumped
        meatBumped += 1
    vx = x-cursorX
    vy = 13
    #foods[i] = (x, y, vx, vy,image)
    foods[bumpedIndex] = (x, y, vx/4, vy, name)

def redrawAll(life):
    #print(life)
    WIN.fill((255, 255, 255))
    WIN.blit(gates,(0,0))
    WIN.blit(dragon,(100,600))
    drawBalls()
    drawCursor()
    for i in range(life):
        WIN.blit(heart,(25*(i+1),25))
    pygame.display.update()

def main():
    gameOver=False
    counter=0
    speed=100
    life = 10
    clock = pygame.time.Clock()
    run = True
    startTime = time.time()

    while run:
        clock.tick(FPS)

        # motion tracking####################################################
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
            global cursorX
            global cursorY
            cursorX = (x2+x1)/2
            cursorY = (y2+y1)/2
            frame = cv.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)

            #update held ball pos
            # if holdingBall:
            #     balls[heldBallIndex] = (80+width-aspectRatio*cursorX, aspectRatio*cursorY)

        cv.imshow('frame', cv.flip(frame, 1))
        # Display the resulting frame
        if cv.waitKey(1) == ord('q'):
            break
        ################################################################

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        keysPressed = pygame.key.get_pressed()
        if keysPressed[pygame.K_r]:
            life=10
            restart()
            gameOver = False

        checkContact()

        if gameOver==False:
            
            if counter%speed==0: 
                launchFood()
            if counter/750==0 and speed>5:
                speed/=2
            result = takeStep(life)
            if isinstance(result,int):
                life=result
            if life<=0:
                gameOver=True
                endTime = time.time()
                elapsedTime = endTime - startTime
            counter+=1
        redrawAll(life)

    pygame.quit()

if __name__ == "__main__":
    main()