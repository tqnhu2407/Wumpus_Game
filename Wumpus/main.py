import pygame
import sys
import os
import numpy as np
import random
import time as mytime
from pygame import *

import logic

pygame.init()
score_show = pygame.font.Font('font1.ttf', 50)
score_font = pygame.font.Font('font1.ttf', 30)
menu_font = pygame.font.Font('font1.ttf', 45)
GO_font = pygame.font.Font('font1.ttf', 70)
mainClock = pygame.time.Clock()

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

#create screen background, logo, title
global screen
screen = pygame.display.set_mode((750, 750))
pygame.display.set_caption("Wumpus")
logo = pygame.image.load('icon1.png')
pygame.display.set_icon(logo)
#Color
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
lemon = (239, 253, 95)
green = (0, 255, 0)
blue = (0, 0, 255)

class main_loop():
    def __init__(self, path):
        self.n, self.map = import_map(path)
        self.new_format_map = []
        for x in range(0, len(self.map)):
            self.new_format_map.append([])
            for _ in range(0, len(self.map[0])):
                self.new_format_map[x].append([])
        self.x = 0
        self.y = 0
        for i in range(0, len(self.map)):
            for j in range(0, len(self.map[0])):
                if self.map[i][j] == 'A':
                    self.new_format_map[i][j] = [1, 4, 0]
                    self.x = j * 75
                    self.y = i * 75
                if self.map[i][j] == '-':
                    self.new_format_map[i][j] = [0, 0, 0]
                if self.map[i][j] == 'G':
                    self.new_format_map[i][j] = [0, 1, 0]
                if self.map[i][j] == 'BG':
                    self.new_format_map[i][j] = [0, 1, 1]
                if self.map[i][j] == 'SG':
                    self.new_format_map[i][j] = [0, 1, 2]
                if self.map[i][j] == 'BSG':
                    self.new_format_map[i][j] = [0, 1, 3]
                if self.map[i][j] == 'W':
                    self.new_format_map[i][j] = [0, 3, 0]
                if self.map[i][j] == 'P':
                    self.new_format_map[i][j] = [0, 2, 0]
                if self.map[i][j] == 'B':
                    self.new_format_map[i][j] = [0, 0, 1]
                if self.map[i][j] == 'S':
                    self.new_format_map[i][j] = [0, 0, 2]
                if self.map[i][j] == 'BS':
                    self.new_format_map[i][j] = [0, 0, 3]
        self.dir = 'UP'

        #Load object
        self.player_img = pygame.image.load('right1.png')
        self.player_img_left = pygame.image.load('left1.png')
        self.player_img_right = pygame.image.load('right1.png')
        self.player_img_up = pygame.image.load('up1.png')
        self.player_img_down = pygame.image.load('down1.png')

        self.wumpus_img = pygame.image.load('wumpus1.png')

        self.gold_img = pygame.image.load('gold1.png')

        self.floor_img = pygame.image.load('floor1.jpg')

        self.breeze_img = pygame.image.load('breeze1.png')
        self.stench_img = pygame.image.load('stench1.png')

        self.door_img = pygame.image.load('door1.png')
        self.pit_img = pygame.image.load('pit1.png')
        self.fog_img = pygame.image.load('fog1.jpg')

        self.score = 0

        self.screen = pygame.display.set_mode((750, 750))
    #create object on screen
    def generate_object(self, obj_img, x, y):
        self.screen.blit(obj_img, (x, y))
    #move by keyboard
    def move_by_keyboard(self, keys1):
        if keys1[pygame.K_LEFT]:
            if self.player_img != self.player_img_left:
                self.player_img = self.player_img_left
            else:
                self.x -= 75
                if self.x < 0:
                    self.x += 75
                    return
                if self.new_format_map[self.y // 75][self.x // 75][1] == 2 or self.new_format_map[self.y // 75][self.x // 75][1] == 3:
                    self.score -= 1000
                    game_over(self.score)
                self.score -= 10
                self.player_img = self.player_img_left
                self.new_format_map[self.y // 75][self.x // 75][0] = 1
        if keys1[pygame.K_RIGHT]:
            if self.player_img != self.player_img_right:
                self.player_img = self.player_img_right
            else:
                self.x += 75
                if self.x > 675:
                    self.x -= 75
                    return
                if self.new_format_map[self.y // 75][self.x // 75][1] == 2 or self.new_format_map[self.y // 75][self.x // 75][1] == 3:
                    self.score -= 1000
                    game_over(self.score)
                self.score -= 10
                self.new_format_map[self.y // 75][self.x // 75][0] = 1
        if keys1[pygame.K_UP]:
            if self.player_img != self.player_img_up:
                self.player_img = self.player_img_up
            else:
                self.y -= 75
                if self.y < 0:
                    self.y += 75
                    return
                if self.new_format_map[self.y // 75][self.x // 75][1] == 2 or self.new_format_map[self.y // 75][self.x // 75][1] == 3:
                    self.score -= 1000
                    game_over(self.score)
                self.score -= 10
                self.player_img = self.player_img_up
                self.new_format_map[self.y // 75][self.x // 75][0] = 1
        if keys1[pygame.K_DOWN]:
            if self.player_img != self.player_img_down:
                self.player_img = self.player_img_down
            else:
                self.y += 75
                if self.y > 675:
                    self.y -= 75
                    return
                if self.new_format_map[self.y // 75][self.x // 75][1] == 2 or self.new_format_map[self.y // 75][self.x // 75][1] == 3:
                    self.score -= 1000
                    game_over(self.score)
                self.score -= 10
                self.player_img = self.player_img_down
                self.new_format_map[self.y // 75][self.x // 75][0] = 1

    def move_by_command(self, command):
        if command == 'LEFT':
            if self.player_img != self.player_img_left:
                self.player_img = self.player_img_left
            else:
                self.x -= 75
                if self.x < 0:
                    self.x += 75
                    return
                if self.new_format_map[self.y // 75][self.x // 75][1] == 2 or self.new_format_map[self.y // 75][self.x // 75][1] == 3:
                    self.score -= 1000
                    game_over(self.score, 'Game over!')
                elif self.new_format_map[self.y // 75][self.x // 75][1] == 4:
                    self.score += 100
                    game_over(self.score, '  Win!!!  ')
                self.score -= 10
                self.player_img = self.player_img_left
                self.new_format_map[self.y // 75][self.x // 75][0] = 1
            x_room = int(self.y // 75)
            y_room = int(self.x // 75)
            self.dir = logic.update_dir(self.new_format_map, x_room, y_room)
            
        if command == 'RIGHT':
            if self.player_img != self.player_img_right:
                self.player_img = self.player_img_right
            else:
                self.x += 75
                if self.x > 675:
                    self.x -= 75
                    return
                if self.new_format_map[self.y // 75][self.x // 75][1] == 2 or self.new_format_map[self.y // 75][self.x // 75][1] == 3:
                    self.score -= 1000
                    game_over(self.score, 'Game over!')
                elif self.new_format_map[self.y // 75][self.x // 75][1] == 4:
                    self.score += 100
                    game_over(self.score, '  Win!!!  ')
                self.score -= 10
                self.new_format_map[self.y // 75][self.x // 75][0] = 1
            x_room = int(self.y // 75)
            y_room = int(self.x // 75)
            self.dir = logic.update_dir(self.new_format_map, x_room, y_room)
            
        if command == 'UP':
            if self.player_img != self.player_img_up:
                self.player_img = self.player_img_up
            else:
                self.y -= 75
                if self.y < 0:
                    self.y += 75
                    return
                if self.new_format_map[self.y // 75][self.x // 75][1] == 2 or self.new_format_map[self.y // 75][self.x // 75][1] == 3:
                    self.score -= 1000
                    game_over(self.score, 'Game over!')
                elif self.new_format_map[self.y // 75][self.x // 75][1] == 4:
                    self.score += 100
                    game_over(self.score, '  Win!!!  ')
                self.score -= 10
                self.player_img = self.player_img_up
                self.new_format_map[self.y // 75][self.x // 75][0] = 1
            x_room = int(self.y // 75)
            y_room = int(self.x // 75)
            self.dir = logic.update_dir(self.new_format_map, x_room, y_room)
            
        if command == 'DOWN':
            if self.player_img != self.player_img_down:
                self.player_img = self.player_img_down
            else:
                self.y += 75
                if self.y > 675:
                    self.y -= 75
                    return
                if self.new_format_map[self.y // 75][self.x // 75][1] == 2 or self.new_format_map[self.y // 75][self.x // 75][1] == 3:
                    self.score -= 1000
                    game_over(self.score, 'Game over!')
                elif self.new_format_map[self.y // 75][self.x // 75][1] == 4:
                    self.score += 100
                    game_over(self.score, '  Win!!!  ')
                self.score -= 10
                self.player_img = self.player_img_down
                self.new_format_map[self.y // 75][self.x // 75][0] = 1
            x_room = int(self.y // 75)
            y_room = int(self.x // 75)
            self.dir = logic.update_dir(self.new_format_map, x_room, y_room)

    def take_gold(self, keys1):
        if (keys1[pygame.K_RETURN]) and self.new_format_map[self.y // 75][self.x // 75][1] == 1:
            self.new_format_map[self.y // 75][self.x // 75][1] = 0
            self.score += 100
    
    def stench_disappear(self, wx, wy):
        if self.new_format_map[wx - 1][wy][2] == 3:
            self.new_format_map[wx - 1][wy][2] = 1
        else:
            self.new_format_map[wx - 1][wy][2] = 0
        if self.new_format_map[wx + 1][wy][2] == 3:
            self.new_format_map[wx + 1][wy][2] = 1
        else:
            self.new_format_map[wx + 1][wy][2] = 0
        if self.new_format_map[wx][wy - 1][2] == 3:
            self.new_format_map[wx][wy - 1][2] = 1
        else:
            self.new_format_map[wx][wy - 1][2] = 0
        if self.new_format_map[wx][wy + 1][2] == 3:
            self.new_format_map[wx][wy + 1][2] = 1
        else:
            self.new_format_map[wx][wy + 1][2] = 0
    
    def shoot_arrow(self, keys1):
        if (keys1[pygame.K_SPACE]) and self.new_format_map[self.y // 75 - 1][self.x // 75][1] == 3 and self.player_img == self.player_img_up:
            self.new_format_map[self.y // 75 - 1][self.x // 75][1] = 0
            self.new_format_map[self.y // 75 - 1][self.x // 75][0] = 1
            self.stench_disappear(self.y // 75 - 1, self.x // 75)
            self.score -= 100
        if (keys1[pygame.K_SPACE]) and self.new_format_map[self.y // 75 + 1][self.x // 75][1] == 3 and self.player_img == self.player_img_down:
            self.new_format_map[self.y // 75 + 1][self.x // 75][1] = 0
            self.new_format_map[self.y // 75 + 1][self.x // 75][0] = 1
            self.stench_disappear(self.y // 75 + 1, self.x // 75)
            self.score -= 100
        if (keys1[pygame.K_SPACE]) and self.new_format_map[self.y // 75][self.x // 75 - 1][1] == 3 and self.player_img == self.player_img_left:
            self.new_format_map[self.y // 75][self.x // 75 - 1][1] = 0
            self.new_format_map[self.y // 75][self.x // 75 - 1][0] = 1
            self.stench_disappear(self.y // 75, self.x // 75 - 1)
            self.score -= 100
        if (keys1[pygame.K_SPACE]) and self.new_format_map[self.y // 75][self.x // 75 + 1][1] == 3 and self.player_img == self.player_img_right:
            self.new_format_map[self.y // 75][self.x // 75 + 1][1] = 0
            self.new_format_map[self.y // 75][self.x // 75 + 1][0] = 1
            self.stench_disappear(self.y // 75, self.x // 75 + 1)
            self.score -= 100
    
    def climb_out(self, keys1):
        if (keys1[pygame.K_RETURN]) and self.new_format_map[self.y // 75][self.x // 75] == [1, 4, 0]:
            self.score += 10
            game_over(self.score)
    
    def game_run(self):
        running = True
        while running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                #keys1 = pygame.key.get_pressed()
                #self.move_by_keyboard(keys1)
                #self.take_gold(keys1)
                #self.shoot_arrow(keys1)
                #self.climb_out(keys1)


            for i in range(0, len(self.new_format_map)):
                for j in range(0, len(self.new_format_map[0])):
                    self.generate_object(self.floor_img, j * 75, i * 75)

            for i in range(0, len(self.new_format_map)):
                for j in range(0, len(self.new_format_map[0])):
                    if self.new_format_map[i][j][1] == 1:
                        self.generate_object(self.gold_img, j * 75, i * 75)

            for i in range(0, len(self.new_format_map)):
                for j in range(0, len(self.new_format_map[0])):
                    if self.new_format_map[i][j][1] == 2:
                        self.generate_object(self.pit_img, j * 75, i * 75)

            for i in range(0, len(self.new_format_map)):
                for j in range(0, len(self.new_format_map[0])):
                    if self.new_format_map[i][j][1] == 3:
                        self.generate_object(self.wumpus_img, j * 75, i * 75)

            for i in range(0, len(self.new_format_map)):
                for j in range(0, len(self.new_format_map[0])):
                    if self.new_format_map[i][j] == [1, 4, 0]:
                        self.generate_object(self.door_img, j * 75, i * 75)

            for i in range(0, len(self.new_format_map)):
                for j in range(0, len(self.new_format_map[0])):
                    if self.new_format_map[i][j][2] == 1:
                        self.generate_object(self.breeze_img, j * 75, i * 75)

            for i in range(0, len(self.new_format_map)):
                for j in range(0, len(self.new_format_map[0])):
                    if self.new_format_map[i][j][2] == 2:
                        self.generate_object(self.stench_img, j * 75, i * 75)

            for i in range(0, len(self.new_format_map)):
                for j in range(0, len(self.new_format_map[0])):
                    if self.new_format_map[i][j][2] == 3:
                        self.generate_object(self.stench_img, j * 75, i * 75)
                        self.generate_object(self.breeze_img, j * 75, i * 75)

            for i in range(0, len(self.new_format_map)):
                for j in range(0, len(self.new_format_map[0])):
                    if self.new_format_map[i][j][0] == 0:
                        self.generate_object(self.fog_img, j * 75, i * 75)

            self. generate_object(self.player_img, self.x, self.y)
            pygame.display.update()
            
            mytime.sleep(0.1)
            self.move_by_command(self.dir)

def menu_config():
    # change title and logo
    pygame.display.set_caption("Wumpus")
    logo = pygame.image.load('icon1.png')
    pygame.display.set_icon(logo)
    menu_img = pygame.image.load('wumpus.png')
    screen.blit(menu_img, (0, 0))

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def map_selection_menu():
    map_run = True
    global state
    screen = pygame.display.set_mode((750, 750), 0)
    while map_run:
        screen.fill(white)
        menu_config()

        map_1 = pygame.Rect(290, 330, 170, 45)
        map_2 = pygame.Rect(290, 390, 170, 45)
        map_3 = pygame.Rect(290, 450, 170, 45)
        map_4 = pygame.Rect(290, 510, 170, 45)
        map_5 = pygame.Rect(290, 570, 170, 45)
        exit_button = pygame.Rect(290, 630, 170, 45)

        pygame.draw.rect(screen, white, map_1)
        pygame.draw.rect(screen, white, map_2)
        pygame.draw.rect(screen, white, map_3)
        pygame.draw.rect(screen, white, map_4)
        pygame.draw.rect(screen, white, map_5)
        pygame.draw.rect(screen, white, exit_button)

        draw_text("Map 1", menu_font, red, screen, 305, 325)
        draw_text("Map 2", menu_font, red, screen, 305, 385)
        draw_text("Map 3", menu_font, red, screen, 305, 445)
        draw_text("Map 4", menu_font, red, screen, 305, 505)
        draw_text("Map 5", menu_font, red, screen, 305, 565)
        draw_text("Back", menu_font, red, screen, 317, 625)

        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        mx, my = pygame.mouse.get_pos()
        if map_1.collidepoint((mx, my)):
            if click:
                path = 'maps\\map1.txt'
                game = main_loop(path)
                game.game_run()

        if map_2.collidepoint((mx, my)):
            if click:
                path = 'maps\\map2.txt'
                game = main_loop(path)
                game.game_run()


        if map_3.collidepoint((mx, my)):
            if click:
                path = 'maps\\map3.txt'
                game = main_loop(path)
                game.game_run()


        if map_4.collidepoint((mx, my)):
            if click:
                path = 'maps\\map4.txt'
                game = main_loop(path)
                game.game_run()

        if map_5.collidepoint((mx, my)):
            if click:
                path = 'maps\\map5.txt'
                game = main_loop(path)
                game.game_run()

        if exit_button.collidepoint((mx, my)):
            if click:
                map_run = False


        pygame.display.update()
        mainClock.tick(60)

def main_menu():
    while True:
        screen = pygame.display.set_mode((750, 750))
        screen.fill(white)
        menu_config()
        play_button = pygame.Rect(290, 405, 170, 55)
        exit_button = pygame.Rect(290, 515, 170, 55)

        pygame.draw.rect(screen, white, play_button)
        pygame.draw.rect(screen, white, exit_button)

        draw_text("Play", menu_font, red, screen, 317, 400)
        draw_text("Quit", menu_font, red, screen, 320, 510)

        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        mx, my = pygame.mouse.get_pos()
        if play_button.collidepoint((mx, my)):
            if click:
                map_selection_menu()
        if exit_button.collidepoint((mx, my)):
            if click:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        mainClock.tick(60)

def game_over(score, noti):
    waiting = True
    screen = pygame.display.set_mode((750, 750), 0)

    while waiting:
        screen.fill(white)
        play_again = pygame.Rect(200, 405, 350, 55)
        quit = pygame.Rect(300, 515, 150, 55)
        pygame.draw.rect(screen, white, play_again)
        pygame.draw.rect(screen, white, quit)

        draw_text(noti, GO_font, blue, screen, 143, 75)
        draw_text("Score: " + str(score), score_show, black, screen, 195, 250)
        draw_text("Play again", menu_font, red, screen, 230, 400)
        draw_text("Exit", menu_font, red, screen, 323, 510)

        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        mx, my = pygame.mouse.get_pos()
        if play_again.collidepoint((mx, my)):
            if click:
                main_menu()
                waiting = False
        if quit.collidepoint((mx, my)):
            if click:
                waiting = False
                sys.exit()
        pygame.display.update()
        mainClock.tick(60)



main_menu()