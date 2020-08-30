import pygame
import sys
import os
import numpy as np
import random
import time
pygame.init()

import logic

# Import a maze from file name
# Return (n, m, 2D_array_maze, pacman_i, pacman_j)
def import_map(filename):
    if (not os.path.exists(filename)):
        return (0, 0, None)

    file = open(filename, 'r')

    data = file.readline().strip().split('.')
    n = int(data[0])
    map = []

    for i in range(n):
        data = file.readline().strip().split('.')
        map.append([x for x in data])

    file.close()

    return (n, map)

(n, map) = import_map('maps\\map1.txt')

new_format_map = []
for x in range(0, len(map)):
    new_format_map.append([])
    for _ in range(0, len(map[0])):
        new_format_map[x].append([])
x = 0
y = 0
for i in range(0, len(map)):
    for j in range(0, len(map[0])):
        if map[i][j] == 'A':
            new_format_map[i][j] = [1, 4, 0]
            x = j * 75
            y = i * 75
        if map[i][j] == '-':
            new_format_map[i][j] = [0, 0, 0]
        if map[i][j] == 'G':
            new_format_map[i][j] = [0, 1, 0]
        if map[i][j] == 'BG':
            new_format_map[i][j] = [0, 1, 1]
        if map[i][j] == 'SG':
            new_format_map[i][j] = [0, 1, 2]
        if map[i][j] == 'BSG':
            new_format_map[i][j] = [0, 1, 3]
        if map[i][j] == 'W':
            new_format_map[i][j] = [0, 3, 0]
        if map[i][j] == 'P':
            new_format_map[i][j] = [0, 2, 0]
        if map[i][j] == 'B':
            new_format_map[i][j] = [0, 0, 1]
        if map[i][j] == 'S':
            new_format_map[i][j] = [0, 0, 2]
        if map[i][j] == 'BS':
            new_format_map[i][j] = [0, 0, 3]

screen = pygame.display.set_mode((len(map) * 75, len(map) * 75))

# change title and logo

pygame.display.set_caption("Wumpus")
logo = pygame.image.load('icon1.png')
pygame.display.set_icon(logo)

#Load object
player_img = pygame.image.load('right1.png')
player_img_left = pygame.image.load('left1.png')
player_img_right = pygame.image.load('right1.png')
player_img_up = pygame.image.load('up1.png')
player_img_down = pygame.image.load('down1.png')

wumpus_img = pygame.image.load('wumpus1.png')

gold_img = pygame.image.load('gold1.png')

floor_img = pygame.image.load('floor1.jpg')

breeze_img = pygame.image.load('breeze1.png')
stench_img = pygame.image.load('stench1.png')

door_img = pygame.image.load('door1.png')
pit_img = pygame.image.load('pit1.png')
fog_img = pygame.image.load('fog1.jpg')
#create object on screen
def generate_object(obj_img, x, y):
    screen.blit(obj_img, (x, y))
#move by keyboard

def move_by_keyboard():
    global x, y, player_img, running
    if keys1[pygame.K_LEFT]:
        if player_img != player_img_left:
            player_img = player_img_left
        else:
            x -= 75
            if x < 0:
                x += 75
                return
            if new_format_map[y // 75][x // 75][1] == 2 or new_format_map[y // 75][x // 75][1] == 3:
                print('game over')
                running = False
            player_img = player_img_left
            new_format_map[y // 75][x // 75][0] = 1
    if keys1[pygame.K_RIGHT]:
        if player_img != player_img_right:
            player_img = player_img_right
        else:
            x += 75
            if x > 675:
                x -= 75
                return
            if new_format_map[y // 75][x // 75][1] == 2 or new_format_map[y // 75][x // 75][1] == 3:
                print('game over')
                running = False
            player_img = player_img_right
            new_format_map[y // 75][x // 75][0] = 1
    if keys1[pygame.K_UP]:
        if player_img != player_img_up:
            player_img = player_img_up
        else:
            y -= 75
            if y < 0:
                y += 75
                return
            if new_format_map[y // 75][x // 75][1] == 2 or new_format_map[y // 75][x // 75][1] == 3:
                print('game over')
                running = False
            player_img = player_img_up
            new_format_map[y // 75][x // 75][0] = 1
    if keys1[pygame.K_DOWN]:
        if player_img != player_img_down:
            player_img = player_img_down
        else:
            y += 75
            if y > 675:
                y -= 75
                return
            if new_format_map[y // 75][x // 75][1] == 2 or new_format_map[y // 75][x // 75][1] == 3:
                print('game over')
                running = False
            player_img = player_img_down
            new_format_map[y // 75][x // 75][0] = 1

dir = ['UP']

def move_by_command(command):
    global x, y, player_img, running
    if command == 'LEFT':
        if player_img != player_img_left:
            player_img = player_img_left
        else:
            x -= 75
            if x < 0:
                x += 75
                return
            if new_format_map[y // 75][x // 75][1] == 2 or new_format_map[y // 75][x // 75][1] == 3:
                print('game over')
                running = False
            player_img = player_img_left
            new_format_map[y // 75][x // 75][0] = 1
        x_room = int(y // 75)
        y_room = int(x // 75)
        dir.append(logic.update_dir(new_format_map, x_room, y_room))
        
    if command == 'RIGHT':
        if player_img != player_img_right:
            player_img = player_img_right
        else:
            x += 75
            if x > 675:
                x -= 75
                return
            if new_format_map[y // 75][x // 75][1] == 2 or new_format_map[y // 75][x // 75][1] == 3:
                print('game over')
                running = False
            player_img = player_img_right
            new_format_map[y // 75][x // 75][0] = 1
        x_room = int(y // 75)
        y_room = int(x // 75)
        dir.append(logic.update_dir(new_format_map, x_room, y_room))
        
    if command == 'UP':
        if player_img != player_img_up:
            player_img = player_img_up # Rotate the agent
        else:
            y -= 75
            if y < 0:
                y += 75
                return
            if new_format_map[y // 75][x // 75][1] == 2 or new_format_map[y // 75][x // 75][1] == 3:
                print('game over')
                running = False
            player_img = player_img_up
            new_format_map[y // 75][x // 75][0] = 1
        x_room = int(y // 75)
        y_room = int(x // 75)
        dir.append(logic.update_dir(new_format_map, x_room, y_room))
        
    if command == 'DOWN':
        if player_img != player_img_down:
            player_img = player_img_down
        else:
            y += 75
            if y > 675:
                y -= 75
                return
            if new_format_map[y // 75][x // 75][1] == 2 or new_format_map[y // 75][x // 75][1] == 3:
                print('game over')
                running = False
            player_img = player_img_down
            new_format_map[y // 75][x // 75][0] = 1
        x_room = int(y // 75)
        y_room = int(x // 75)
        dir.append(logic.update_dir(new_format_map, x_room, y_room))

def take_gold():
    if (keys1[pygame.K_RETURN]) and new_format_map[y // 75][x // 75][1] == 1:
        new_format_map[y // 75][x // 75][1] = 0
def stench_disappear(wx, wy):
    if new_format_map[wx - 1][wy][2] == 3:
        new_format_map[wx - 1][wy][2] = 1
    else:
        new_format_map[wx - 1][wy][2] = 0
    if new_format_map[wx + 1][wy][2] == 3:
        new_format_map[wx + 1][wy][2] = 1
    else:
        new_format_map[wx + 1][wy][2] = 0
    if new_format_map[wx][wy - 1][2] == 3:
        new_format_map[wx][wy - 1][2] = 1
    else:
        new_format_map[wx][wy - 1][2] = 0
    if new_format_map[wx][wy + 1][2] == 3:
        new_format_map[wx][wy + 1][2] = 1
    else:
        new_format_map[wx][wy + 1][2] = 0
def shoot_arrow():
    global player_img
    if (keys1[pygame.K_SPACE]) and new_format_map[y // 75 - 1][x // 75][1] == 3 and player_img == player_img_up:
        new_format_map[y // 75 - 1][x // 75][1] = 0
        new_format_map[y // 75 - 1][x // 75][0] = 1
        stench_disappear(y // 75 - 1, x // 75)
    if (keys1[pygame.K_SPACE]) and new_format_map[y // 75 + 1][x // 75][1] == 3 and player_img == player_img_down:
        new_format_map[y // 75 + 1][x // 75][1] = 0
        new_format_map[y // 75 + 1][x // 75][0] = 1
        stench_disappear(y // 75 + 1, x // 75)
    if (keys1[pygame.K_SPACE]) and new_format_map[y // 75][x // 75 - 1][1] == 3 and player_img == player_img_left:
        new_format_map[y // 75][x // 75 - 1][1] = 0
        new_format_map[y // 75][x // 75 - 1][0] = 1
        stench_disappear(y // 75, x // 75 - 1)
    if (keys1[pygame.K_SPACE]) and new_format_map[y // 75][x // 75 + 1][1] == 3 and player_img == player_img_right:
        new_format_map[y // 75][x // 75 + 1][1] = 0
        new_format_map[y // 75][x // 75 + 1][0] = 1
        stench_disappear(y // 75, x // 75 + 1)

running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # keys1 = pygame.key.get_pressed()
        # move_by_keyboard()
        # take_gold()
        # shoot_arrow()
    

    for i in range(0, len(new_format_map)):
        for j in range(0, len(new_format_map[0])):
            generate_object(floor_img, j * 75, i * 75)

    for i in range(0, len(new_format_map)):
        for j in range(0, len(new_format_map[0])):
            if new_format_map[i][j] == [1, 1, 0]:
                generate_object(gold_img, j * 75, i * 75)

    for i in range(0, len(new_format_map)):
        for j in range(0, len(new_format_map[0])):
            if new_format_map[i][j] == [1, 2, 0]:
                generate_object(pit_img, j * 75, i * 75)

    for i in range(0, len(new_format_map)):
        for j in range(0, len(new_format_map[0])):
            if new_format_map[i][j] == [1, 3, 0]:
                generate_object(wumpus_img, j * 75, i * 75)

    for i in range(0, len(new_format_map)):
        for j in range(0, len(new_format_map[0])):
            if new_format_map[i][j] == [1, 4, 0]:
                generate_object(door_img, j * 75, i * 75)

    for i in range(0, len(new_format_map)):
        for j in range(0, len(new_format_map[0])):
            if new_format_map[i][j] == [1, 0, 1]:
                generate_object(breeze_img, j * 75, i * 75)

    for i in range(0, len(new_format_map)):
        for j in range(0, len(new_format_map[0])):
            if new_format_map[i][j] == [1, 0, 2]:
                generate_object(stench_img, j * 75, i * 75)

    for i in range(0, len(new_format_map)):
        for j in range(0, len(new_format_map[0])):
            if new_format_map[i][j] == [1, 0, 3]:
                generate_object(stench_img, j * 75, i * 75)
                generate_object(breeze_img, j * 75, i * 75)

    for i in range(0, len(new_format_map)):
        for j in range(0, len(new_format_map[0])):
            if new_format_map[i][j][0] == 0:
                generate_object(fog_img, j * 75, i * 75)

    generate_object(player_img, x, y)

    pygame.display.update()
    
    time.sleep(0.1)
    move_by_command(dir.pop(0))
