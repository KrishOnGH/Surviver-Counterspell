import pygame
import time
import random

pygame.init()
pygame.mixer.init()

pygame.mixer.music.load("Thick_Of_It__KSI.custom_score.mp3")
pygame.mixer.music.play()

WIDTH, HEIGHT = 800, 600
FPS = 60
WALL_SPEED = 0.025
INITIAL_PROJECTILE_INTERVAL = 500
PROJECTILE_VELOCITY = 5
PLAYER_SPEED = 5
NUM_STARS = random.randint(1, 2)
STAR_SPEED = 1

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

heart_img = pygame.image.load('heart.png')
astronaut_img = pygame.image.load('astronaut.png')
bullet_img = pygame.image.load('bullet.png')

heart_width, heart_height = heart_img.get_size()
astronaut_width, astronaut_height = astronaut_img.get_size()
bullet_width, bullet_height = bullet_img.get_size()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shrinking Box with Moving Projectiles")

box_left = 100
box_top = 100
box_right = WIDTH - 100
box_bottom = HEIGHT - 100

initial_box_width = box_right - box_left
initial_box_height = box_bottom - box_top

player_x = WIDTH // 2
player_y = HEIGHT // 2
player_radius = 20

projectiles = []
last_projectile_time = time.time() * 1000

health = 10

bullets_shot = 0

class Star:
    def __init__(self, x, y, size, speed):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed

    def update(self):
        self.x -= self.speed
        
    def draw(self, screen):
        pygame.draw.circle(screen, WHITE, (self.x, self.y), self.size)

stars = []
last_star_time = time.time() * 1000

running = True
clock = pygame.time.Clock()

def check_collision(projectile, player_x, player_y, player_radius):
    distance = ((projectile['x'] - player_x) ** 2 + (projectile['y'] - player_y) ** 2) ** 0.5
    return distance < (player_radius + projectile['width'] / 2)

def display_text(text, font, color, x, y, max_width=0, max_height=0):
    label = font.render(text, True, color)
    label_width, label_height = label.get_size()
    
    if max_width and label_width > max_width:
        label = pygame.transform.scale(label, (max_width, label_height * max_width // label_width))
        label_width, label_height = label.get_size()
    
    if max_height and label_height > max_height:
        label = pygame.transform.scale(label, (label_width * max_height // label_height, max_height))
        label_width, label_height = label.get_size()

    screen.blit(label, (x - label_width // 2, y - label_height // 2))

def generate_stars():
    current_time = time.time() * 1000
    global last_star_time, NUM_STARS

    if current_time - last_star_time >= 1000:
        NUM_STARS = random.randint(3, 5) 
        for _ in range(NUM_STARS): 
            star_x = WIDTH  
            star_y = random.randint(0, HEIGHT)
            size = 1
            speed = STAR_SPEED 
            stars.append(Star(star_x, star_y, size, speed))
        last_star_time = current_time

def main_menu():
    global running
    menu_running = True
    while menu_running:
        screen.fill(BLACK)
        for star in stars:
            star.draw(screen)
        
        font = pygame.font.SysFont(None, 55)
        
        display_text("Survivor", font, WHITE, WIDTH // 2, HEIGHT // 4)
        
        play_button = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2, 150, 50)
        pygame.draw.rect(screen, WHITE, play_button)
        display_text("Play", font, BLACK, WIDTH // 2, HEIGHT // 2 + 25)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_running = False
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    menu_running = False
        pygame.display.flip()
        clock.tick(FPS)

def end_screen():
    global running, bullets_shot
    end_running = True
    font = pygame.font.SysFont(None, 55)
    
    while end_running:
        screen.fill(BLACK)
        for star in stars:
            star.draw(screen)
        
        display_text(f"Score: {bullets_shot}", font, WHITE, WIDTH // 2, HEIGHT // 4)
        
        play_again_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 50)
        pygame.draw.rect(screen, WHITE, play_again_button)
        display_text("Play Again", font, BLACK, WIDTH // 2, HEIGHT // 2 + 25)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end_running = False
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_again_button.collidepoint(event.pos):
                    end_running = False
                    return True 
        
        pygame.display.flip()
        clock.tick(FPS)

def game_loop():
    global player_x, player_y, health, bullets_shot, projectiles, box_left, box_top, box_right, box_bottom, last_projectile_time
    projectiles = []
    health = 10
    bullets_shot = 0
    box_left = 100
    box_top = 100
    box_right = WIDTH - 100
    box_bottom = HEIGHT - 100
    player_x = WIDTH // 2
    player_y = HEIGHT // 2
    running = True

    while running:
        screen.fill(BLACK)
        generate_stars()
        
        for star in stars:
            star.update()
            star.draw(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            player_y -= PLAYER_SPEED
        if keys[pygame.K_DOWN]:
            player_y += PLAYER_SPEED
        
        player_y = max(box_top + player_radius, min(player_y, box_bottom - player_radius))
        
        current_time = time.time() * 1000

        width_scale = (box_right - box_left) / initial_box_width
        height_scale = (box_bottom - box_top) / initial_box_height
        scale_factor = min(width_scale, height_scale)
        
        scaled_projectile_interval = INITIAL_PROJECTILE_INTERVAL * scale_factor
        
        if current_time - last_projectile_time >= scaled_projectile_interval:
            projectiles.append({
                'x': player_x + player_radius + 5,
                'y': player_y - 5,
                'width': bullet_width,
                'height': bullet_height,
                'velocity': PROJECTILE_VELOCITY
            })
            bullets_shot += 1
            last_projectile_time = current_time
        
        for projectile in projectiles[:]:
            projectile['x'] += projectile['velocity']
            
            if projectile['x'] + projectile['width'] >= box_right:
                projectile['velocity'] = -PROJECTILE_VELOCITY
                
            if projectile['x'] <= box_left:
                projectiles.remove(projectile)
            
            if check_collision(projectile, player_x, player_y, player_radius):
                health -= 1
                projectiles.remove(projectile) 
                
                if health <= 0:
                    running = False
            
            screen.blit(bullet_img, (projectile['x'], projectile['y']))
        
        pygame.draw.rect(screen, (255, 255, 255), (box_left, box_top, box_right - box_left, box_bottom - box_top), 2)
        
        screen.blit(astronaut_img, (player_x - astronaut_width // 2, player_y - astronaut_height // 2))

        for i in range(health):
            screen.blit(heart_img, (10 + i * (heart_width + 5), 10))
        
        box_left += WALL_SPEED
        box_top += WALL_SPEED
        box_right -= WALL_SPEED
        box_bottom -= WALL_SPEED

        if box_left >= box_right or box_top >= box_bottom:
            running = False

        pygame.display.flip()
        clock.tick(FPS)

    return False

while running:
    main_menu() 
    if game_loop() == False:
        if end_screen(): 
            continue
        else:
            running = False

pygame.quit()
