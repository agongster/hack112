import pygame
import random
import os
import math
import time

level = 0
mouthWidth = 200
foods = []
gravity = 2



WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('kill me')
x, y = 400, 400
FPS = 25

poison = pygame.image.load(os.path.join('opencvApp', 'poison.png'))
meat= pygame.image.load(os.path.join('opencvApp','meat.png'))
heart=pygame.image.load(os.path.join('opencvApp','heart.png'))
dragon=pygame.image.load(os.path.join('opencvApp','dragon.png'))
pat=pygame.image.load(os.path.join('opencvApp', 'pat_virtue.png'))
mike=pygame.image.load(os.path.join('opencvApp', 'mike_taylor.png'))
gates = pygame.image.load(os.path.join('opencvApp', 'gates.jpeg')).convert()
gates.set_alpha(200)

poison = pygame.transform.scale(poison,(100,100))
meat = pygame.transform.scale(meat,(100,100))
heart = pygame.transform.scale(heart,(50,50))
dragon = pygame.transform.scale(dragon,(600,200))
pat = pygame.transform.scale(pat, (175,175))
mike = pygame.transform.scale(mike, (100,100))
gates = pygame.transform.scale(gates, (800,800))

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
    
def launchFood(): #add food data to foods
    if random.random() > 0.5: #launch from left
        x0 = -100 + random.random()*200
    else: #launch from right
        x0 = 900 - random.random()*200
    x1 = (WIDTH - mouthWidth)/2 + random.random()*mouthWidth
    h = 300 + random.random()*400
    t = (2*gravity + math.sqrt(4*gravity**2 + 32*h*gravity))/(2*gravity)
    vx = (x1-x0)/t
    vy = -0.5*gravity*t
    imageList=[mike,pat,mike,meat,pat,meat,mike, pat]
    image=imageList[random.randrange(len(imageList))]
    foods.append((x0, 800, vx, vy,image))

def redrawAll(life):
    print(life)
    WIN.fill((255, 255, 255))
    WIN.blit(gates,(0,0))
    WIN.blit(dragon,(100,600))
    drawBalls()
    for i in range(life):
        WIN.blit(heart,(25*(i+1),25))
    pygame.display.update()

def main():
    gameOver=False
    counter=0
    speed=50
    life = 10
    clock = pygame.time.Clock()
    run = True
    startTime = time.time()
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        keysPressed = pygame.key.get_pressed()
        if keysPressed[pygame.K_r]:
            life=10
            restart()
            gameOver = False

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
                endTime = time.Time()
                elapsedTime = endTime - startTime
            counter+=1
        redrawAll(life)

    pygame.quit()

if __name__ == "__main__":
    main()