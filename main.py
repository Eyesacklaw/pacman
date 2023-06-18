import pygame
import random
from pygame import mixer
from sys import exit

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, velocity):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load('sprites/player.png'), (30, 30)).convert_alpha()
        # images [left, right, up down]
        self.images = [self.image, pygame.transform.rotate(self.image, 180),\
                        pygame.transform.rotate(self.image, 270), \
                        pygame.transform.rotate(self.image, 90), \
                        pygame.transform.scale(pygame.image.load('sprites/closedman.png'), (30, 30)).convert_alpha()]
        self.munch = mixer.Sound("music/Pacman chomp.wav")
        self.eat_ghost_sound = mixer.Sound("music/Pacman eat ghost.wav")
        self.death = mixer.Sound("music/Pacman death.wav")
        self.current_rotation = 0
        self.x = x
        self.y = y
        self.rect = self.image.get_rect(center = (self.x, self.y))
        self.velocity = velocity
        self.mask = pygame.mask.from_surface(self.image)
        self.collide = False
        self.score = 0
        self.ghosts_eaten = 0
        self.dots_eaten = 0
    
    def player_input(self):
        keys = pygame.key.get_pressed()
        # Stops wall hacking (kind of)
        if keys[pygame.K_LEFT] and not self.collide and self.current_rotation != 0: 
            self.x -= self.velocity
            self.current_rotation = 0
        if keys[pygame.K_RIGHT] and not self.collide and self.current_rotation != 1: 
            self.x += self.velocity
            self.current_rotation = 1
        if keys[pygame.K_UP] and not self.collide and self.current_rotation != 2: 
            self.y -= self.velocity
            self.current_rotation = 2
        if keys[pygame.K_DOWN] and not self.collide and self.current_rotation != 3: 
            self.y += self.velocity
            self.current_rotation = 3
        # Keep moving in same direction like regular pacman
        if not self.collide:
            if self.current_rotation == 0:
                self.x -= self.velocity
            if self.current_rotation == 1:
                self.x += self.velocity
            if self.current_rotation == 2:
                self.y -= self.velocity
            if self.current_rotation == 3:
                self.y += self.velocity
        self.collide = False
        # Tunnel thing
        if self.x > 640 and self.y >= 277 and self.y <= 285:
            self.x = -40
        if self.x < -40 and self.y >= 277 and self.y <= 285:
            self.x = 640
    
    def collision(self):
        # Check collision and stop continue moving
        if self.current_rotation == 0:
            self.collide = True
            self.x += self.velocity
        if self.current_rotation == 1:
            self.collide = True
            self.x -= self.velocity
        if self.current_rotation == 2:
            self.collide = True
            self.y += self.velocity
        if self.current_rotation == 3:
            self.collide = True
            self.y -= self.velocity

    def eat_food(self):
        self.image = self.images[4]
        self.munch.play()

    def check_if_dead(self):
        if pygame.Rect.colliderect(self.rect, blinky.sprite.rect) and \
            blinky.sprite.scatter:
            self.score += 2**self.ghosts_eaten * 10 
            self.ghosts_eaten += 1
            blinky.sprite.x = 330
            blinky.sprite.y = 220
            blinky.sprite.scatter = False
            self.eat_ghost_sound.play()
        elif pygame.Rect.colliderect(self.rect, pinky.sprite.rect) and \
            pinky.sprite.scatter:
            self.score += 2**self.ghosts_eaten * 10 
            self.ghosts_eaten += 1
            pinky.sprite.x = 330
            pinky.sprite.y = 220
            pinky.sprite.scatter = False
            self.eat_ghost_sound.play()
        elif pygame.Rect.colliderect(self.rect, inky.sprite.rect) and \
            inky.sprite.scatter:
            self.score += 2**self.ghosts_eaten * 10 
            self.ghosts_eaten += 1
            inky.sprite.x = 330
            inky.sprite.y = 220
            inky.sprite.scatter = False
            self.eat_ghost_sound.play()
        elif pygame.Rect.colliderect(self.rect, clyde.sprite.rect) and \
            clyde.sprite.scatter:
            self.score += 2**self.ghosts_eaten * 10 
            self.ghosts_eaten += 1
            clyde.sprite.x = 330
            clyde.sprite.y = 220
            clyde.sprite.scatter = False
            self.eat_ghost_sound.play()
        else:
            if pygame.Rect.colliderect(self.rect, blinky.sprite.rect) or \
            pygame.Rect.colliderect(self.rect, pinky.sprite.rect) or \
            pygame.Rect.colliderect(self.rect, inky.sprite.rect) or \
            pygame.Rect.colliderect(self.rect, clyde.sprite.rect):
                # Red, Pink, Blue, Orange
                # Kill Pacman
                self.death.play()
                pygame.time.wait(1000)
                run = False
                global score
                score = self.score
                self.kill()
            

    def update(self):
        self.player_input()
        self.check_if_dead()
        self.rect = self.image.get_rect(center = (self.x, self.y))
        #print(self.x, self.y) # For debugging purposes
        self.image = self.images[self.current_rotation]

class Maze(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load('sprites/maze.png'), (600, 600)).convert()
        self.rect = self.image.get_rect(topleft = (0, 0))
        self.mask = pygame.mask.from_surface(self.image)

class Ghost(pygame.sprite.Sprite):
    def __init__(self, x, y, type, rotation, velocity):
        super().__init__()
        self.type = type
        self.image = pygame.transform.scale(pygame.image.load(f'sprites/ghost{self.type}.png'), (30, 30)).convert_alpha()
        # images [type and vulnerable ghost]
        self.images = [ self.image, 
            pygame.transform.scale(pygame.image.load('sprites/ghost5.png'), (30, 30)).convert_alpha()]
        self.x = x
        self.y = y
        self.rect = self.image.get_rect(center = (self.x, self.y))
        self.velocity = velocity
        self.mask = pygame.mask.from_surface(self.image)
        self.collide = False
        self.current_rotation = rotation # 0 - left, 1 - right, 2 - up, 3 - down
        self.vision_lr = pygame.Rect(0, 0, 600, 20)
        self.vision_ud = pygame.Rect(0, 0, 20, 600)
        self.found_pacman = False
        self.invalid_paths = []
        self.scatter = False
    
    def draw_rects(self):
        self.vision_lr = pygame.Rect(0, self.y, 600, 1)
        self.vision_ud = pygame.Rect(self.x, 0, 1, 600)
        # Make rectangles visible (for debugging purposes only)
        #pygame.draw.rect(screen, (0, 255, 0), self.vision_lr)
        #pygame.draw.rect(screen, (0, 0, 255), self.vision_ud)

    def detect_player(self):
        self.draw_rects()
        if self.vision_lr.colliderect(pacman.sprite.rect) and not self.collide\
            and (self.x, self.y) not in self.invalid_paths and not self.scatter:
            self.found_pacman = True
            if self.found_pacman:
                if self.pacmanx < self.x:
                    # If ghost is to the right of pacman
                    # Go left
                    self.current_rotation = 0
                else:
                    # If ghost is to the left of pacman
                    # Go right
                    self.current_rotation = 1
        elif self.vision_lr.colliderect(pacman.sprite.rect) and not self.collide\
            and (self.x, self.y) not in self.invalid_paths and self.scatter: # run away
            if self.found_pacman:
                if self.pacmanx < self.x:
                    # If ghost is to the right of pacman
                    # Go right
                    self.current_rotation = 1
                else:
                    # If ghost is to the left of pacman
                    # Go left
                    self.current_rotation = 2
        if self.vision_ud.colliderect(pacman.sprite.rect) and not self.collide\
            and (self.x, self.y) not in self.invalid_paths and not self.scatter:
            self.found_pacman = True
            if self.found_pacman:
                if self.pacmany < self.y:
                    # If ghost is down
                    # Go up
                    self.current_rotation = 2
                else:
                    # If ghost is up
                    # Go down
                    self.current_rotation = 3
        elif self.vision_ud.colliderect(pacman.sprite.rect) and not self.collide\
            and (self.x, self.y) not in self.invalid_paths and self.scatter: # run away
            if self.found_pacman:
                if self.pacmany < self.y:
                    # If ghost is down
                    # Go down
                    self.current_rotation = 3
                else:
                    # If ghost is up
                    # Go up
                    self.current_rotation = 2

    def ai(self): # Actually both ai(self) and collision(self) are the ai of the ghost
        self.pacmanx = pacman.sprite.x
        self.pacmany = pacman.sprite.y
        # Keep moving in same direction
        if not self.collide:
            if self.current_rotation == 0:
                self.x -= self.velocity
            if self.current_rotation == 1:
                self.x += self.velocity
            if self.current_rotation == 2:
                self.y -= self.velocity
            if self.current_rotation == 3:
                self.y += self.velocity
        self.collide = False
        # Tunnel thing
        if self.x > 640 and self.y >= 277 and self.y <= 285:
            self.x = -40
        if self.x < -40 and self.y >= 277 and self.y <= 285:
            self.x = 640

    def collision(self):
        # Check collision and stop continue moving
        if self.current_rotation == 0:
            self.collide = True
            self.x += self.velocity
        if self.current_rotation == 1:
            self.collide = True
            self.x -= self.velocity
        if self.current_rotation == 2:
            self.collide = True
            self.y += self.velocity
        if self.current_rotation == 3:
            self.collide = True
            self.y -= self.velocity
        if self.collide and self.found_pacman:
            self.found_pacman = False
            self.invalid_paths.append((self.x, self.y))
        # Ai, so chooses between random direction and following either 
        # the x or y coordinates of pacman
        if random.randint(0, 10) == 1:
            self.possible_combinations = [0, 1, 2, 3]
            self.possible_combinations.remove(self.current_rotation)
            self.current_rotation = random.choice(self.possible_combinations)
            self.collide = False
        else:
            # If 0, follow x coords, If 1, follow y coords
            if random.randint(0, 1) == 0:
                if self.pacmanx < self.x:
                    # If ghost is to the right of pacman
                    # Go left
                    self.current_rotation = 0
                else:
                    # If ghost is to the left of pacman
                    # Go right
                    self.current_rotation = 1
            else:
                if self.pacmany < self.y:
                    # If ghost is down
                    # Go up
                    self.current_rotation = 2
                else:
                    # If ghost is up
                    # Go down
                    self.current_rotation = 3
        

    def update(self):
        self.ai()
        self.detect_player()
        self.rect = self.image.get_rect(center = (self.x, self.y))    
        if self.scatter:
            self.image = self.images[-1]
        else:
           self.image = self.images[0]



class Food(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load('sprites/food.png'), (10, 10))
        self.x = x
        self.y = y
        self.rect = self.image.get_rect(center = (x, y))

class BigFood(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load('sprites/bigfood.png'), (20, 20))
        self.x = x
        self.y = y
        self.rect = self.image.get_rect(center = (x, y))

pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption('Pacman')
icon = pygame.image.load('sprites/icon.png').convert_alpha()
pygame.display.set_icon(icon)
clock = pygame.time.Clock()

# play intro music before running
pacman_theme = mixer.Sound("music/Pacman theme.wav")
pacman_theme.play()
pygame.time.wait(4000)
run = True # run
total_dots = 0

maze = pygame.sprite.GroupSingle(Maze())
pacman = pygame.sprite.GroupSingle(Player(300, 340, 2))

# Ghosts
blinky = pygame.sprite.GroupSingle(Ghost(30, 35, 1, 0, 2))
pinky = pygame.sprite.GroupSingle(Ghost(560, 35, 2, 0, 2))
inky = pygame.sprite.GroupSingle(Ghost(30, 560, 3, 0, 2))
clyde = pygame.sprite.GroupSingle(Ghost(575, 560, 4, 0, 2))

food = pygame.sprite.Group()
bigfood = pygame.sprite.Group()

# List comprehension
with open ("food.txt", "r") as f:
    # Take the integer for each coordinate in each line splitted by " ", for every line in 
    # f.read().splitlines()
    location = [[int(coord) for coord in line.split(" ")] for line in f.read().splitlines()]
total_dots += len(location)

# Summon food at that location
for i in range(len(location)):
    food.add(Food(location[i][0], location[i][1]))

# Open Bigfood
with open ("bigfood.txt", "r") as f:
    # Take the integer for each coordinate in each line splitted by " ", for every line in 
    # f.read().splitlines()
    location = [[int(coord) for coord in line.split(" ")] for line in f.read().splitlines()]
total_dots += len(location)

# Summon Bigfood at that location
for i in range(len(location)):
    bigfood.add(BigFood(location[i][0], location[i][1]))

def ghosts_scatter():
    blinky.sprite.scatter = True
    pinky.sprite.scatter = True
    inky.sprite.scatter = True
    clyde.sprite.scatter = True
    return pygame.time.get_ticks()

def ghosts_normal():
    blinky.sprite.scatter = False
    pinky.sprite.scatter = False
    inky.sprite.scatter = False
    clyde.sprite.scatter = False
    ghosts_eaten = 0

start_ticks = 0
while run:
    current_ticks = pygame.time.get_ticks()
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    maze.draw(screen)
    pacman.draw(screen)
    food.draw(screen)
    bigfood.draw(screen)

    # Draw ghosts on screen
    blinky.draw(screen)
    pinky.draw(screen)
    inky.draw(screen)
    clyde.draw(screen)

    # Update ghosts
    blinky.update()
    pinky.update()
    inky.update()
    clyde.update()

    pacman.update()

    if current_ticks > (start_ticks + 10000): # Delay 10 seconds before turning normal
        ghosts_normal()

    # Collision
    try:
        if pygame.sprite.spritecollide(pacman.sprite, food, True):
            pacman.sprite.eat_food()
            pacman.sprite.score += 1
            pacman.sprite.dots_eaten += 1
        if pygame.sprite.spritecollide(pacman.sprite, bigfood, True):
            pacman.sprite.eat_food()
            pacman.sprite.score += 5
            pacman.sprite.dots_eaten += 1
            start_ticks = ghosts_scatter()
        if pygame.sprite.spritecollide(pacman.sprite, maze, False, pygame.sprite.collide_mask):
            pacman.sprite.collision()
            pacman.update()
        
        # If ghosts collide with maze
        if pygame.sprite.spritecollide(blinky.sprite, maze, False, pygame.sprite.collide_mask):
            blinky.sprite.collision()
            blinky.update()
        if pygame.sprite.spritecollide(pinky.sprite, maze, False, pygame.sprite.collide_mask):
            pinky.sprite.collision()
            pinky.update()
        if pygame.sprite.spritecollide(inky.sprite, maze, False, pygame.sprite.collide_mask):
            inky.sprite.collision()
            inky.update()
        if pygame.sprite.spritecollide(clyde.sprite, maze, False, pygame.sprite.collide_mask):
            clyde.sprite.collision()
            clyde.update()
        if pacman.sprite.dots_eaten == total_dots: # If you win all the dots
        # You win
            pygame.quit()
            print('''██    ██  ██████  ██    ██     ██     ██ ██ ███    ██ ██ ██ ██ 
 ██  ██  ██    ██ ██    ██     ██     ██ ██ ████   ██ ██ ██ ██ 
  ████   ██    ██ ██    ██     ██  █  ██ ██ ██ ██  ██ ██ ██ ██ 
   ██    ██    ██ ██    ██     ██ ███ ██ ██ ██  ██ ██          
   ██     ██████   ██████       ███ ███  ██ ██   ████ ██ ██ ██ 
                                                               
                                                               ''')
            # Show score
            print(f"Score: {score}")
            exit()
    except: #If Pacman is dead
        pygame.quit()
        print('''██    ██  ██████  ██    ██     ██████  ██ ███████ ██████  ██ ██ ██ 
 ██  ██  ██    ██ ██    ██     ██   ██ ██ ██      ██   ██ ██ ██ ██ 
  ████   ██    ██ ██    ██     ██   ██ ██ █████   ██   ██ ██ ██ ██ 
   ██    ██    ██ ██    ██     ██   ██ ██ ██      ██   ██          
   ██     ██████   ██████      ██████  ██ ███████ ██████  ██ ██ ██ 
                                                                   
                                                                   ''')
        # Show score
        print(f"Score: {score}")
        exit()

    pygame.display.update()
    clock.tick(30)