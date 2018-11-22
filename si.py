import pygame
import random

width = 474
heigh = 456
FPS = 60

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)

MouseSteering = False

#inicjajca
screen = pygame.display.set_mode((width,heigh))
pygame.display.set_caption('Space Invaders: Closing Up')
clock = pygame.time.Clock()


class Fighter(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('/home/remo/coding/python3/SI-ClosingUp/jet.png')
        self.rect = self.image.get_rect()
        self.rect.center = (width/2, heigh/2)
    def update(self):
        self.vx, self.vy = 0, 0
        self.b = 5
        self.w, self.h = self.image.get_rect().size
        if not MouseSteering:
            keystate = pygame.key.get_pressed()
            if keystate[pygame.K_UP] and self.rect.y - self.b > 0:
                self.vy = -5
            if keystate[pygame.K_DOWN] and self.rect.y + self.b < heigh - self.h:
                self.vy = 5
            if keystate[pygame.K_LEFT] and self.rect.x - self.b > 0:
                self.vx = -5
            if keystate[pygame.K_RIGHT] and self.rect.x + self.b < width - self.w:
                self.vx = 5
            self.rect.x += self.vx
            self.rect.y += self.vy
        else:
            mouseposition = pygame.mouse.get_pos()
            if self.w < mouseposition[0] + self.w/2 < width:
                self.rect.x = mouseposition[0] - self.w/2
            if self.h < mouseposition[1] + self.h/2 < heigh:
                self.rect.y = mouseposition[1] - self.h/2

class Background(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('/home/remo/coding/python3/SI-ClosingUp/background.png').convert()
        self.w, self.h = self.image.get_rect().size
        self.y = 0
    def scroll(self, screen):
        self.y += 1
        if self.y > self.h:
            self.y = 0
        screen.blit(self.image, (0, self.y))
        screen.blit(self.image, (0, self.y - self.h))


vehicle_sprites = pygame.sprite.Group()

background = Background()
fighter = Fighter()

vehicle_sprites.add(fighter)

#petla gry
crashed = False
while not crashed:
    clock.tick(FPS)
    # input/eventy
    for event in pygame.event.get():
        #sprawdzamy zamkniecie okna
        if event.type == pygame.QUIT:
            crashed = True
    #update
    background.scroll(screen)
    vehicle_sprites.update()
    #draw
    vehicle_sprites.draw(screen)
    #flip/display
    pygame.display.flip()


pygame.quit()
quit()
