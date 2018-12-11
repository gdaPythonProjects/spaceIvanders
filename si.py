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


class Player(pygame.sprite.Sprite):
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
    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('/home/remo/coding/python3/SI-ClosingUp/projectile.png')
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        if player.vy < 0:
            self.speed = -7 + player.vy
        else:
            self.speed = -7
    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

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


all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()

background = Background()
player = Player()

all_sprites.add(player)

#petla gry
crashed = False
while not crashed:
    clock.tick(FPS)
    # input/eventy
    for event in pygame.event.get():
        #sprawdzamy zamkniecie okna
        if event.type == pygame.QUIT:
            crashed = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
    #update
    background.scroll(screen)
    all_sprites.update()
    #draw
    all_sprites.draw(screen)
    #flip/display
    pygame.display.flip()


pygame.quit()
quit()
