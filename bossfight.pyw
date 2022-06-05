import pygame, random, time, pyquark, pygame.freetype
from configparser import ConfigParser

pygame.freetype.init()

config_object = ConfigParser()
config_object.read("config.ini")

sound_volume = config_object["SOUNDVOLUME"]
scores = config_object["SCORES"]

from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_RIGHT,
    K_LEFT,
    K_SPACE,
    K_ESCAPE,
    K_LSHIFT,
    KEYDOWN,
    QUIT,
)

class Heart(pygame.sprite.Sprite):
    def __init__(self):
        super(Heart, self).__init__()
        self.surf = pygame.image.load("images/hearts.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
            random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
            random.randint(0, SCREEN_HEIGHT),
            ))


        global asteroid_speed
        self.speed = random.randint(asteroid_speed[0], asteroid_speed[1])

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0 or self.rect.top < 45:
            self.kill()

        if player.rect.right > SCREEN_WIDTH:
            self.kill()

        if self.rect.colliderect(player.rect):
            player.lives += 1
            self.kill()

class Heart_empty(pygame.sprite.Sprite):
    def __init__(self):
        super(Heart_empty, self).__init__()
        self.surf = pygame.image.load("images/heart_empty.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("images/ship.png").convert()
        self.rect = self.surf.get_rect()
        self.speed = 7
        self.lives = 3

    # Player movement
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -self.speed)
            move_sound.play()
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, self.speed)
            move_sound.play()
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(self.speed, 0)
            move_sound.play()
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-self.speed, 0)
            move_sound.play()

        # Collision with walls
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

        if self.rect.top <= 55:
            self.rect.top = 55
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

class Boss(pygame.sprite.Sprite):
    def __init__(self):
        super(Boss, self).__init__()
        self.image = pygame.image.load("images/boss.png")
        picture = pygame.transform.scale(self.image, (128, 128))
        self.surf = picture.convert()
        self.rect = self.surf.get_rect()

    def update(self):
        global player_center_x, player_center_y
        player_center_x, player_center_y = player.rect.center
        self_center_x, self_center_y = self.rect.center
        if self.rect.center != player.rect.center:
            if player_center_x > self_center_x:
                self.rect.move_ip(3, 0)
            if player_center_x < self_center_x:
                self.rect.move_ip(-3, 0)
            if player_center_y > self_center_y:
                self.rect.move_ip(0, 3)
            if player_center_y < self_center_y:
                self.rect.move_ip(0, -3)

        # Collision with walls
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

        if self.rect.top <= 55:
            self.rect.top = 55
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

# Define screen width and height constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

pygame.mixer.init()

level = 1

asteroid_speed = [5, 5]

# Set up music & font
pygame.mixer.music.load("sounds/music.wav")
pygame.mixer.music.set_volume(int(sound_volume["music"])/9)
pygame.mixer.music.play(loops=-1)
score_font = pygame.freetype.Font("myfont.ttf", 50)

# Define sfx
win_sound = pygame.mixer.Sound("sounds/game_win.wav")
hit_sound = pygame.mixer.Sound("sounds/hit_sound.wav")
move_sound = pygame.mixer.Sound("sounds/move_sound.wav")
crash_sound = pygame.mixer.Sound("sounds/crash_sound.wav")
up1_sound= pygame.mixer.Sound("sounds/level_up.wav")

hit_sound.set_volume(int(sound_volume["sfx"])/15)
move_sound.set_volume(int(sound_volume["sfx"])/450)
crash_sound.set_volume(int(sound_volume["sfx"])/9)
up1_sound.set_volume(int(sound_volume["music"])/9)
win_sound.set_volume(int(sound_volume["music"])/9)

# Set up the screen
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Planetoids")
icon = pygame.image.load('images/asteroid.png')
pygame.display.set_icon(icon)

# Set up the player
player = Player()
player.rect.move_ip(0, 260)
player.rect.move_ip(70, 0)

boss = Boss()
boss.rect.move_ip(400, 300)

all_sprites = pygame.sprite.Group()
all_sprites.add(boss)
all_sprites.add(player)

# Prepare Hearts
heart1 = Heart()
heart2 = Heart()
heart3 = Heart()
heart_empty = Heart_empty()

# Set up the loop
clock = pygame.time.Clock()
running = True


while running:
    screen.fill((0,0,0)) # Clear display. All sprites should be drawn AFTER this.
    for event in pygame.event.get(): # Check for events
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

        elif event.type == QUIT:
            running = False


    pressed_keys = pygame.key.get_pressed() # Check witch keys have been pressed
    player.update(pressed_keys) # Update the player with said keys
    boss.update()

    # Control Hearts
    if player.lives != 0:
        screen.blit(heart1.surf, (20, 20))
        if player.lives != 1:
            screen.blit(heart2.surf, (60, 20))
            if player.lives != 2:
                screen.blit(heart3.surf, (100, 20))

    if player.lives == 1:
        screen.blit(heart_empty.surf, (60, 20))
        screen.blit(heart_empty.surf, (100, 20))
    elif player.lives == 2:
        screen.blit(heart_empty.surf, (100, 20))

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    if player.rect.colliderect(boss.rect):
        if not player.rect.left.colliderect(boss.rect):
            player.lives -= 1
            boss.rect.move_ip(700, 0)


    score_font.render_to(screen, (700, 25), str(10), (255, 255, 255))
    # Update Display
    pygame.display.flip()   
    clock.tick(30)# Control Frames

scores["latest"] = str(level)
if int(scores["highscore"]) < level:
    scores["highscore"] = str(level)

with open('config.ini', 'w') as conf:
    config_object.write(conf)