import os
import pygame

dir = os.path.dirname(os.path.abspath(__file__))


width = 800
heigh = 600
FPS = 60

epi = []

eHP=2

MouseSteering = False

#inicjajca
screen = pygame.display.set_mode((width,heigh))
pygame.display.set_caption('Space Invaders: Closing Up')
clock = pygame.time.Clock()

#wczytanie grafik
img_bullet = pygame.image.load(dir + '/textures/shots/bullet.png')

explosions = []
for i in range (9):
    explosions.append(pygame.image.load(dir + '/textures/explosions/regularExplosion0{}.png'.format(i)))

enemies = []
for e in range (14):
    enemies.append(pygame.image.load(dir + '/textures/enemies/ufo{}.png'.format(e)))

class Player(pygame.sprite.Sprite):
    def __init__(self):
        self.hp = 3
        self.hp_changed = False
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(dir + '/textures/jet.png')
        self.rect = self.image.get_rect()
        self.rect.center = (width/2, heigh*3/4)
    def update(self):
        ##if self.hp >= 0:
        ##    explode
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
        self.image = img_bullet
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        if player.vy < 0:
            self.speed = -7 + player.vy
        else:
            self.speed = -7
    def update(self):
        self.rect.y += self.speed
        if self.rect.colliderect(enemy):
            if enemy.hp > 0:
                enemy.hp -= 1
                enemy.hp_changed = True
            self.kill()
        elif self.rect.colliderect(player):
            if player.hp > 0:
                player.hp -= 1
                player.hp_changed = True
            self.kill()
        elif self.rect.bottom < 0:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        self.hp = eHP
        self.hp_changed = False
        pygame.sprite.Sprite.__init__(self)
        self.image = enemies[self.hp]
        self.rect = self.image.get_rect()
        if player.rect.x > width/2:
            self.rect.center = (width/4, heigh/8)
        else:
            self.rect.center = (width*3/4, heigh/8)
    def update(self):
        if self.hp_changed == True:
            self.image = enemies[self.hp]
            self.hp_changed = False
        if self.hp <= 0:
            epi.append(self.rect.center)
            self.kill()
            expl = Explosion()
            all_sprites.add(expl)

class Explosion(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = explosions[0]
        self.rect = self.image.get_rect()
        self.rect.center = epi[-1]
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosions):
                self.kill()
                epi.pop(0)
            else:
                self.image = explosions[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = epi[-1]


class Background(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(dir + '/textures/background.png')
        self.w, self.h = self.image.get_rect().size
        self.y = 0
    def scroll(self, screen):
        self.y += 1
        if self.y > self.h:
            self.y = 0
        screen.blit(self.image, (0, self.y))
        screen.blit(self.image, (0, self.y - self.h))


class Hp_counter(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(dir + '/textures/counters/hp' + str(player.hp) + '.png')
        self.rect = self.image.get_rect()
        self.x = self.y = 15
    def update(self):
        if player.hp_changed == True:
            self.image = pygame.image.load(dir + '/textures/counters/hp' + str(player.hp) + '.png')
            player.hp_changed = False



hud = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
players = pygame.sprite.Group()
enemises = pygame.sprite.Group()
bullets = pygame.sprite.Group()

background = Background()


player = Player()
hp_counter = Hp_counter()
enemy = Enemy()

all_sprites.add(hp_counter)
all_sprites.add(player)
all_sprites.add(enemy)

players.add(player)
enemises.add(enemy)

hud.add(hp_counter)

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
