from cmu_graphics import *
import math, random

def onAppStart(app):
    app.width = app.height = 800
    app.level = 0
    app.mouthWidth = 200
    app.foods = []
    app.stepsPerSecond = 20
    app.paused = False
    app.gravity = 2
    app.lives=10
    app.gameOver=False
    app.counter=0
    app.speed=50


def onKeyPress(app, key):
    if key == 'space':
        launchFood(app)
    if key == 's':
        takeStep(app)

def launchFood(app): #add food data to app.foods
    if random.random() > 0.5: #launch from left
        x0 = -100 + random.random()*200
    else: #launch from right
        x0 = 900 - random.random()*200
    x1 = (app.width - app.mouthWidth)/2 + random.random()*app.mouthWidth
    h = 300 + random.random()*400
    t = (2*app.gravity + math.sqrt(4*app.gravity**2 + 32*h*app.gravity))/(2*app.gravity)
    vx = (x1-x0)/t
    vy = -0.5*app.gravity*t
    colorList=['black','black','black','black','red','red','black']
    color=colorList[random.randrange(len(colorList))]
    app.foods.append((x0, 800, vx, vy,color))

def onStep(app):
    if not app.gameOver:
        if not app.paused:
            if app.counter%app.speed==0: 
                launchFood(app)
            if app.counter/750==0 and app.speed>5:
                app.speed/=2
            takeStep(app)
            if app.lives<=0:
                app.gameOver=True
            app.counter+=1
def takeStep(app):
    i=0
    while i<len(app.foods):
        (x, y, vx, vy,color) = app.foods[i]
        if y>600 and (x<650) and (x>150):
            app.foods.remove(app.foods[i])
            if color=='black':
                app.lives-=1
        else:
            x += vx
            y += vy
            vy += app.gravity
            app.foods[i] = (x, y, vx, vy,color)
            i+=1
            
        

        

def redrawAll(app):
    if not app.gameOver:
        drawBalls(app)
        for i in range (app.lives):
            drawPolygon((30*i)+100/4,70/4,(30*i)+75/4,50/4,(30*i)+45/4,80/4,(30*i)+100/4,150/4,(30*i)+155/4,80/4,(30*i)+125/4,50/4,fill='red',border='black')
    else:
        drawLabel("Game Over",200,200,size=32,fill='red')
    
    
def drawBalls(app):
    for (x, y, vx, vy,color) in app.foods:
        drawCircle(x, y, 50, border = color, borderWidth = 10, fill = None)
    
def onMousePress(app, mouseX, mouseY):
    print(mouseX, mouseY)


def main():
    runApp()

main()