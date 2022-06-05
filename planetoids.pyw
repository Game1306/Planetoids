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
        self.speed = 5
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
            enemies.update()
            pygame.mixer.music.pause()
            move_sound.stop()
            up1_sound.play()
            time.sleep(2)
            global asteroid_speed, level
            self.rect.move_ip(-740, 0)
            asteroid_speed[1] += 1
            level += 1
            if self.lives != 3:
                self.lives += 1
            pygame.mixer.music.unpause()

        if self.rect.top <= 55:
            self.rect.top = 55
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        super(Asteroid, self).__init__()
        self.textures = ["images/asteroid.png", "images/asteroid2.png"]
        self.surf = pygame.image.load(self.textures[random.randint(0, 1)]).convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
            random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
            random.randint(0, SCREEN_HEIGHT),
            )
        )
        
        global asteroid_speed
        self.speed = random.randint(asteroid_speed[0], asteroid_speed[1])
        self.collided_with_player = False

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0 or self.rect.top < 45:
            self.kill()

        if player.rect.right > SCREEN_WIDTH:
            self.kill()

        if self.rect.colliderect(player.rect):
            player.lives -= 1
            hit_sound.play()
            self.kill()

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
heart_up = pygame.mixer.Sound("sounds/gain_heart.wav")

hit_sound.set_volume(int(sound_volume["sfx"])/15)
move_sound.set_volume(int(sound_volume["sfx"])/450)
crash_sound.set_volume(int(sound_volume["sfx"])/9)
heart_up.set_volume(int(sound_volume["sfx"])/9)
up1_sound.set_volume(int(sound_volume["music"])/9)
win_sound.set_volume(int(sound_volume["music"])/9)
# Set up the screen
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Planetoids")
icon = pygame.image.load('images/asteroid.png')
pygame.display.set_icon(icon)

# Set up the addenemy custom event
ADDENEMY = pygame.USEREVENT + 1
ADDHEART = pygame.USEREVENT + 2
pygame.time.set_timer(ADDENEMY, 250)
pygame.time.set_timer(ADDHEART, random.randint(500, 10000))

# Set up the player
player = Player()
player.rect.move_ip(0, 260)
player.rect.move_ip(70, 0)

# Set up sprite groups
enemies = pygame.sprite.Group()
helpers = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Prepare Hearts
heart1 = Heart()
heart2 = Heart()
heart3 = Heart()
heart_empty = Heart_empty()

# Set up the loop
clock = pygame.time.Clock()
running = True

def bossfight():
    while True:
        screen.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_LSHIFT:
                    return


while running:
    screen.fill((0,0,0)) # Clear display. All sprites should be drawn AFTER this.

    #if level % 10 == 0:
        #bossfight()
    for event in pygame.event.get(): # Check for events
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

        elif event.type == QUIT:
            running = False

        elif event.type == ADDENEMY:
            new_Asteroid = Asteroid()
            enemies.add(new_Asteroid)
            all_sprites.add(new_Asteroid)

        elif event.type == ADDHEART:
            new_Heart = Heart()
            helpers.add(new_Heart)
            all_sprites.add(new_Heart)


    pressed_keys = pygame.key.get_pressed() # Check witch keys have been pressed
    player.update(pressed_keys) # Update the player with said keys
    helpers.update() # Update helpers
    enemies.update() # Update asteroids


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

    # If there are no lives left
    if player.lives == 0:
        pygame.mixer.music.stop()
        player.kill()
        crash_sound.play()
        time.sleep(2)
        running = False
        pyquark.filestart("title.pyw")


    score_font.render_to(screen, (700, 25), str(level), (255, 255, 255))
    # Update Display
    pygame.display.flip()   
    clock.tick(30)# Control Frames

scores["latest"] = str(level)
if int(scores["highscore"]) < level:
    scores["highscore"] = str(level)

with open('config.ini', 'w') as conf:
    config_object.write(conf)