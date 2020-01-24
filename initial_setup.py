import pygame
import random

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    K_a,
    K_w,
    K_s,
    K_d,
    K_SPACE

)
FPS = 60
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
pygame.init()

# Set up the drawing window

pygame.display.set_caption("First Games")
screen = pygame.display.set_mode([800, 600])

clock = pygame.time.Clock()

bullets = pygame.sprite.Group()
shot_image = pygame.image.load('images/shot.jpg').convert()
blood1 = pygame.image.load('img/blood1.jpg').convert()
blood1 = pygame.transform.scale(blood1, (50, 50))
blood2 = pygame.image.load('img/blood2.jpg').convert()
blood2 = pygame.transform.scale(blood2, (50, 50))
shot_image = pygame.transform.scale(shot_image, (50, 50))
hero_image = pygame.image.load('images/wizard.jpg').convert_alpha()
hero_image = pygame.transform.scale(hero_image, (90, 90))
skeleton_image = pygame.image.load('img/enemyskelly.png').convert_alpha()
skeleton_image = pygame.transform.scale(skeleton_image, (90, 90))
wizard_image = pygame.image.load('img/wizard.png').convert_alpha()
wizard_image = pygame.transform.scale(wizard_image, (90, 90))

class Enemy(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        super(Enemy, self).__init__()
        self.surf = pygame.Surface((20, 10))
        self.surf.fill((255, 255, 255))
        self.image = image
        self.pos = [random.randint(20, 30), ]
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(5, 20)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.left < 0:
            self.kill()
        if self.rect.right < 0:
            self.kill()
        if self.rect.top < 0:
            self.kill()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 20))
        self.image = shot_image
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -15
    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            shots_out.pop()
            self.kill()



class Char(pygame.sprite.Sprite):
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.speed = 10
        self.x = 400
        self.y = 475
        self.last_shot = pygame.time.get_ticks()
        self.life = 5
        self.rect.center = [self.x, self.y]
        self.shoot_delay = 270
    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullets.add(Bullet(self.rect.centerx, self.rect.top))
        # sprites.add(Bullet(self.rect.centerx, self.rect.top))
        # bullets.add(Bullet(self.rect.centerx, self.rect.top))
        shots_out.append("pew")
    def update(self, pressed_keys, pos):
            # self.rect.move_ip(pos)
        if pressed_keys[K_UP] or pressed_keys[K_w]:
            self.rect.move_ip(0, -(self.speed))
        if pressed_keys[K_DOWN] or pressed_keys[K_s]:
            self.rect.move_ip(0, self.speed)
        if pressed_keys[K_LEFT] or pressed_keys[K_a]:
            self.rect.move_ip(-(self.speed), 0)
        if pressed_keys[K_RIGHT] or pressed_keys[K_d]:
            self.rect.move_ip(self.speed, 0)
        if pressed_keys[K_SPACE]:
            self.shoot()
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right >= SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
class Monster(pygame.sprite.Sprite):
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.speed = random.randint(1, 7)
        self.x = random.randint(1, 800)
        self.y = random.randint(0, 30)
        self.rect.center = [self.x, self.y]
    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.left > 600:
            self.kill()
class Blood(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = blood1
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 75

def newMonster():
    roll = random.randint(1, 2)
    if roll == 1:
        a = Monster(skeleton_image)
    if roll == 2:
        a = Monster(wizard_image)
    sprites.add(a)
    enemy_sprites.add(a)



player = Char(hero_image)
enemy_sprites = pygame.sprite.Group()
sprites = pygame.sprite.Group()
shot = pygame.sprite.groupcollide(enemy_sprites, bullets, True, True)

sprites.add(player)
shots_out = []
def redrawGameWindow():
    # screen.blit(bg, (0,0))
    sprites.draw(screen)
    bullets.draw(screen)
    bullets.update()
    enemy_sprites.update()
    pygame.display.update()
    player.update(pressed_keys, pos)
    # sprites.update()
level = 1
difficulty = 1
score = 0

running = True
while running:
    
    clock.tick(60)
    for event in pygame.event.get():
        pressed_keys = pygame.key.get_pressed()
        pos = pygame.mouse.get_pos()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        if event.type == pygame.QUIT:
            running = False

    # if pressed_keys[K_SPACE]:
    #     if len(shots_out) <= 5:
    #         player.shoot()
    #         print (len(shots_out))

    hits = pygame.sprite.groupcollide(enemy_sprites, bullets, True, True)
    for hit in hits:
        score += 1
        # blood = Blood(hit.rect.center, blood1)
        # sprites.add(blood)
        if len(shots_out) > 0:
            shots_out.pop()


    hits = pygame.sprite.spritecollide(player, enemy_sprites, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.life -= 1
        if player.life == 0:
            running = False

    random_roll = random.randint(1, 10)
    if random_roll <= difficulty:
        newMonster()      
    
    

    screen.fill((75, 22, 75))

    
    surf = pygame.Surface((50, 50))
    surf.fill((0,0,0))
    
    redrawGameWindow()
    pygame.display.flip()
    
# Done! Time to quit.
pygame.quit()