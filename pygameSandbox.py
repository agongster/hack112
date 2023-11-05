import pygame
import os

WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('kill me')
x, y = 400, 400
FPS = 30

spaceship = pygame.image.load(os.path.join('opencvApp', 'spaceship.png'))

def redrawAll():
    WIN.fill((255, 255, 255))
    WIN.blit(spaceship, (x, y))
    # for fjfjfj:
    #     draw(spaceship, (x1, y1))
    pygame.display.update()

def main():
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        keysPressed = pygame.key.get_pressed()
        if keysPressed[pygame.K_a]:
            x -= 50

        
        redrawAll()

    pygame.quit()

if __name__ == "__main__":
    main()
