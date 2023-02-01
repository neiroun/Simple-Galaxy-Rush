import pygame
import random
from os import path

# Getting file directories
img_dir = path.join(path.dirname(__file__), 'PNG')
laser_dir = path.join(path.dirname(__file__), 'Lasers')
meteor_dir = path.join(path.dirname(__file__), 'Meteors')
explosion_dir = path.join(path.dirname(__file__), 'Explosions')
sonic_dir = path.join(path.dirname(__file__), 'SonicExplosions')
bonus_dir = path.join(path.dirname(__file__), 'Bonus')
snd_dir = path.join(path.dirname(__file__), 'snd')

f = open('record.txt', 'r', encoding='utf-8')

# Creating constants and variables
WIDTH = 480
HEIGHT = 600
FPS = 60
POWERUP_TIME = 5000
BEST_SCORE = int(f.readline())
DIFFICULTY = 'easy'
f.close()

# Setting colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)


# Создаем игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Galaxy Rush!")
clock = pygame.time.Clock()

font_name = pygame.font.match_font('Times New Roman')

# function for draw text
def write_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

# function for create new essence
def new_esscense():
    m = Essence()
    all_sprites.add(m)
    mobs.add(m)

# function for drawing the health bar
def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, RED, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

# function to draw the number of lives
def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = 332 + 30 * i
        img_rect.y = 0
        surf.blit(img, img_rect)

# Function to create a pause menu
def pause():
    screen.blit(background, background_rect)
    write_text(screen, "Game on PAUSE", 64, WIDTH / 2, HEIGHT / 4)
    write_text(screen, "Press SPACE to continue", 22, WIDTH / 2, HEIGHT / 2)
    pygame.display.flip()
    waiting = True
    while waiting:
        in_game_background.stop()
        background_sound.play()
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if pygame.key.get_pressed()[pygame.K_SPACE]:
                    waiting = False
                if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                    waiting = False
                    show_go_screen()
    background_sound.stop()
    in_game_background.play()

# Creating a settings screen
def settings_screen():
    global player_img, DIFFICULTY
    background = pygame.image.load(path.join(img_dir, 'settings.jpg')).convert()
    background_rect = background.get_rect()
    screen.blit(background, background_rect)
    write_text(screen, "Settings for quit press ESCAPE", 30, WIDTH / 2, 10)
    write_text(screen, "To choose ship press 1, 2 or 3", 22, WIDTH / 2, 70)
    write_text(screen, f"To choose difficulty press SHIFT", 22, WIDTH / 2, 200)
    pygame.display.flip()
    waiting = True
    while waiting:
        in_game_background.stop()
        background_sound.play()
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                    waiting = False
                    show_go_screen()
                if pygame.key.get_pressed()[pygame.K_1]:
                    player_img = pygame.image.load(path.join(img_dir, "playerShip1_orange.png")).convert()
                if pygame.key.get_pressed()[pygame.K_2]:
                    player_img = pygame.image.load(path.join(img_dir, "playerShip2_red.png")).convert()
                if pygame.key.get_pressed()[pygame.K_3]:
                    player_img = pygame.image.load(path.join(img_dir, "playerShip3_green.png")).convert()
                if pygame.key.get_pressed()[pygame.K_LSHIFT]:
                    if DIFFICULTY == 'easy':
                        DIFFICULTY = 'normal'
                    elif DIFFICULTY == 'normal':
                        DIFFICULTY = 'hard'
                    elif DIFFICULTY == 'hard':
                        DIFFICULTY = 'impossible'
                    elif DIFFICULTY == 'impossible':
                        DIFFICULTY = 'easy'
                    print(DIFFICULTY)


# Creating a home screen
def show_go_screen():
    global score, BEST_SCORE, DIFFICULTY
    if score > BEST_SCORE:
        BEST_SCORE = score
        f = open('record.txt', 'w+', encoding='utf-8')
        f.truncate()
        f.write(str(score))
        f.close()
    screen.blit(background, background_rect)
    write_text(screen, "Galaxy Rush!", 64, WIDTH / 2, HEIGHT / 4)
    write_text(screen, f"Press arrow keys for move, space to fire", 22, WIDTH / 2, HEIGHT / 2)
    write_text(screen, f"Best score: {BEST_SCORE}, DIFFICULTY: {DIFFICULTY}", 26, WIDTH / 2, HEIGHT * 2.49 / 4)
    write_text(screen, "Press SPACE to start, F1 for open settings", 18, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        in_game_background.stop()
        background_sound.play()
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if pygame.key.get_pressed()[pygame.K_SPACE]:
                    waiting = False
                if pygame.key.get_pressed()[pygame.K_F1]:
                    settings_screen()
    background_sound.stop()
    in_game_background.play()

# Class for creating player capabilities
class Player(pygame.sprite.Sprite):
    def __init__(self):
        global DIFFICULTY
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        if DIFFICULTY == 'easy':
            self.shield = 100
            self.shoot_delay = 150
            self.last_shot = pygame.time.get_ticks()
            self.lives = 5
        elif DIFFICULTY == 'normal':
            self.shield = 100
            self.shoot_delay = 250
            self.last_shot = pygame.time.get_ticks()
            self.lives = 3
        elif DIFFICULTY == 'hard':
            self.shield = 100
            self.shoot_delay = 550
            self.last_shot = pygame.time.get_ticks()
            self.lives = 2
        elif DIFFICULTY == 'impossible':
            self.shield = 100
            self.shoot_delay = 750
            self.last_shot = pygame.time.get_ticks()
            self.lives = 1
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1
        self.power_time = pygame.time.get_ticks()

    def update(self):
        # timeout for powerups
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()

        # show if hidden
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10

        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        if keystate[pygame.K_UP]:
            self.speedy = -8
        if keystate[pygame.K_DOWN]:
            self.speedy = 8
        if keystate[pygame.K_SPACE]:
            self.shoot()
        if keystate[pygame.K_ESCAPE]:
            pause()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
            if self.power >= 2:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_sound.play()

    def hide(self):
        # временно скрыть игрока
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)

# Class that configures non-game entities
class Essence(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # kill if it goes beyond the top of the screen
        if self.rect.bottom < 0:
            self.kill()


class Bonus(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun'])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 2

    def update(self):
        self.rect.y += self.speedy
        # kill if it slides off the bottom of the screen
        if self.rect.top > HEIGHT:
            self.kill()


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


# Download all game graphics
background = pygame.image.load(path.join(img_dir, 'starfield.jpg')).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir, "playerShip1_orange.png")).convert()
player_mini_img = pygame.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(BLACK)
bullet_img = pygame.image.load(path.join(laser_dir, "laserRed16.png")).convert()
# print(meteor_dir)
meteor_images = list()
meteor_list = ['meteorBrown_big1.png', 'meteorBrown_med1.png', 'meteorBrown_med1.png',
               'meteorBrown_med3.png', 'meteorBrown_small1.png', 'meteorBrown_small2.png',
               'meteorBrown_tiny1.png']
for img in meteor_list:
    meteor_images.append(pygame.image.load(path.join(meteor_dir, img)).convert())

explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['player'] = []
for i in range(9):
    filename = 'regularExplosion0{0}.png'.format(i)
    img = pygame.image.load(path.join(explosion_dir, filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_anim['sm'].append(img_sm)
    filename = 'sonicExplosion0{0}.png'.format(i)
    img = pygame.image.load(path.join(sonic_dir, filename)).convert()
    img.set_colorkey(BLACK)
    explosion_anim['player'].append(img)
powerup_images = dict()
powerup_images['shield'] = pygame.image.load(path.join(bonus_dir, 'shield_gold.png')).convert()
powerup_images['gun'] = pygame.image.load(path.join(bonus_dir, 'bolt_gold.png')).convert()


# Download game ringtones
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'pew.wav'))
shield_sound = pygame.mixer.Sound(path.join(snd_dir, 'pow4.wav'))
power_sound = pygame.mixer.Sound(path.join(snd_dir, 'pow5.wav'))
background_sound = pygame.mixer.Sound(path.join(snd_dir, 'background.wav'))
in_game_background = pygame.mixer.Sound(path.join(snd_dir, 'background_in_game.wav'))
expl_sounds = []
for snd in ['expl3.wav', 'expl6.wav']:
    expl_sounds.append(pygame.mixer.Sound(path.join(snd_dir, snd)))

all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
powerups = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(8):
    new_esscense()

if __name__ == '__main__':
    # Game cycle
    score = 0
    game_over = True
    running = True
    while running:
        if game_over:
            show_go_screen()
            game_over = False
            all_sprites = pygame.sprite.Group()
            mobs = pygame.sprite.Group()
            bullets = pygame.sprite.Group()
            powerups = pygame.sprite.Group()
            player = Player()
            all_sprites.add(player)
            if DIFFICULTY == 'easy':
                for i in range(2):
                    new_esscense()
            elif DIFFICULTY == 'normal':
                for i in range(8):
                    new_esscense()
            elif DIFFICULTY == 'hard':
                for i in range(10):
                    new_esscense()
            elif DIFFICULTY == 'impossible':
                for i in range(20):
                    new_esscense()
            score = 0

        # Keeping the cycle at the right speed
        clock.tick(FPS)
        # Process input
        for event in pygame.event.get():
            # проверка для закрытия окна
            if event.type == pygame.QUIT:
                running = False
        # Update
        all_sprites.update()

        # checking if the bullet hit the entity
        hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
        for hit in hits:
            score += 50 - hit.radius
            random.choice(expl_sounds).play()
            expl = Explosion(hit.rect.center, 'lg')
            all_sprites.add(expl)
            if random.random() > 0.9:
                pow = Bonus(hit.rect.center)
                all_sprites.add(pow)
                powerups.add(pow)
            new_esscense()

        # Checking if the entity hit the player
        hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
        for hit in hits:
            player.shield -= hit.radius * 2
            expl = Explosion(hit.rect.center, 'sm')
            all_sprites.add(expl)
            new_esscense()
            if player.shield <= 0:
                death_explosion = Explosion(player.rect.center, 'player')
                all_sprites.add(death_explosion)
                player.hide()
                player.lives -= 1
                player.shield = 100

        # Player Collision Check and Improvements
        hits = pygame.sprite.spritecollide(player, powerups, True)
        for hit in hits:
            if hit.type == 'shield':
                player.shield += random.randrange(10, 30)
                shield_sound.play()
                if player.shield >= 100:
                    player.shield = 100
            if hit.type == 'gun':
                player.powerup()
                power_sound.play()

        # GAME OVER
        if player.lives == 0 and not death_explosion.alive():
            game_over = True

        # Rendering
        screen.fill(BLACK)
        screen.blit(background, background_rect)
        all_sprites.draw(screen)
        write_text(screen, str(score), 18, WIDTH / 2, 10)
        draw_shield_bar(screen, 5, 5, player.shield)
        draw_lives(screen, WIDTH - 100, 5, player.lives,
                   player_mini_img)
        # Display update
        pygame.display.flip()

    pygame.quit()
