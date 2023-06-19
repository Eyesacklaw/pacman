# Pac-man Project
#### Video Demo:  <https://youtu.be/nxOKqrlbKxo>

## Description:

A Pac-man game implemented in python using the pygame library, with object-oriented programming, list comprehensions and file I/O. Navigate the player to eat as many dots as possible, while avoiding the 'ghosts' unless you eat a large dot which makes Pac-man immune to the ghosts for a short period of time.

Project Structure:
- main.py
- food.txt
- bigfood.txt
- sprites
    - bigfood.png
    - closedman.png
    - food.png
    - ghost1.png
    - ghost2.png
    - ghost3.png
    - ghost4.png
    - ghost5.png
    - icon.png
    - maze.png
    - player.png
- music
    - Pacman chomp.wav
    - Pacman death.wav
    - Pacman eat ghost.wav
    - Pacman theme.wav

## Libraries
Uses sys and random from regular python modules (only needed to be imported and not installed).

Uses pygame, a python library which allows the creation of games by displaying images onto a screen.

## Getting Started
You only have to install pygame, which this python program is using version 2.1.3. I am using python 3.8 to code this program. 

To use the application, simply run the main.py file in a Python environment.

How to control the player:
Use arrow keys
- Left arrow moves Pac-man left
- Right arrow moves Pac-man right
- Up arrow moves Pac-man up
- Down arrow moves Pac-man down

## Description of supplementary files
In the folders sprites and music, there are the sprites for this game. These sprites are not owned by me and belong to their respective owners. This project is only intended for educational purposes and allow me to understand Object-oriented programming and pygame better.

The two ```.txt``` files, ```food.txt``` and ```bigfood.txt``` contain the coordinates of the pieces of food Pac-man has to eat, including the regular pieces and large pieces. Python reads the file and creates instances of these food objects in the corresponding locations, through a 2D list comprehension. Thus, it is possible to modify the positions of the food by modifying the coordinates in the ```.txt``` files respectively. These coordinates are found with the help of Raphael Zhang, a co-author of the project.

## Description of main.py
## Classes
### Player
The player class inherits from the ```pygame.sprite.Sprite``` class, as exemplified through the ```super().__init__()``` method. The ```__init__``` method also takes in a few extra arguments, such as the ```x``` and ```y``` coordinates of the player, which will be changed using ```self.x``` and ```self.y```, and the ```velocity``` of the player. Thus, it is also possible to change the velocity of the player to make it go faster or slower, and make the game easier or harder. It has a few images allowing for the smooth rotation of the player, and some sounds such as ```self.munch```. It also keeps a score of the number of dots eaten, as seen through ```self.dots_eaten```.

The ```player_input``` function moves the player based on the keys pressed, and prevents it from colliding with a wall. There is also a tunnel which teleports the player to the other side of the screen to allow an "illusion" of the player passing through the tunnel.

The ```collision``` method checks if it is colliding with a wall and stops moving, if the player collides, ```self.collide``` will be ```True```.

The ```eat_food``` method eats the food, and plays a sound called ```self.munch```.

The ```check_if_dead``` method determines whether or not Pac-man has collided with the other ghosts, and if so then it kills the player and displays the score.

The ```update``` method is the standard method available to all pygame sprites, which checks for player input, checks if the player has died and gets the corresponding rectangle or "hitbox" of the player used for collision, eating and determining if the player has died or not.

### Maze
The maze has an ```__init__``` method which creates a pygame mask, which determines the walls which Pac-man and the ghosts cannot pass through. That's pretty much all it does.

### Ghost
The ghost has an ```__init__``` method similar to Pac-man's, with the different images when the ghost is vulnerable or not, and has two "vision" rectangles, namely ```self.vision_lr``` (a rectangle for the ghost to see "left and right") and ```self.vision_ud``` (a rectangle for the ghost to see "up and down"). These rectangles pass through the walls, and there are boolean variables such as ```self.found_pacman``` and ```self.invalid_paths``` which is an array, and ```self.scatter```.

The ```draw_rects``` function simply draws the vision rectangles based on the position of the ghost.

The ```detect_player``` function determines if Pac-man collides with any of the vision rectangles, if so, the ghost can "see" Pac-man and will try to move towards it. Thus, it is possible for the ghost to see through walls, albeit not able to pass through it. This gives the ghost a huge advantage, and makes the game very difficult to win. However, if ```self.scatter``` is ```True``` the ghost will do the opposite, because Pac-man is "immune" during that phase and can eat the vulnerable ghosts. However, this arises a problem: When the ghost can "see" Pac-man they try to move towards it, but they may collide into walls and still continuously move towards Pac-man, creating a "deadlock". The solution is through ```self.invalid_paths```. When the ghost sees Pac-man and collides with a wall, the ghost's coordinates are appended into ```self.invalid_paths```, and can no longer "see" Pac-man (which can be observed by scrutinizing the conditional statements in the algorithm).

The ```ai``` method and ```collision``` method allow for the movement of the ghost. The ghost will move randomly, trying to take different paths to spot Pac-man. Occasionally, Pac-man's x and y coordinates are revealed and the ghost will try to align with either one of them, hoping to "see" Pac-man. When the ghost sees Pac-man, ```detect_player``` will be initiated and the ghosts will try to catch Pac-man.

The ```update``` method is similar to Pac-man's ```update``` method.

### Food and BigFood
Both have similar attributes, with their ```__init__``` method taking in x, and y coordinates, to "spawn" in the food at certain locations. It can be observed in the list comprehensions below, it spawns in multiple foods and so ```pygame.sprite.GroupSingle``` is not suitable and thus ```pygame.sprite.Group``` is used to store them in variables.

When the game is running, all sprites have their different updates and movements, and when the player wins or loses, a large text is printed in the terminal and their score before the ```exit()``` function is called which terminates the program.

## Author: Law Wai Lok
### Co-author: Raphael Zhang
