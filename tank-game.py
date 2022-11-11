#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 26 15:40:46 2022

@author: hudson
"""

import pygame
import pygame_menu
import math
import time
class Tank:
    def __init__(self, img, crtls, ang, x, y):
        self.img=img
        self.crtls=crtls
        self.ang=ang
        self.x=x
        self.y=y
        self.speed=0.6
        self.lives=3
        self.lastharmtime=0
    def draw(self):
        if time.time()-2 < self.lastharmtime:
            if (time.time()-self.lastharmtime)%0.5>0.25:
                to_blit=pygame.transform.rotate(self.img, self.ang)
                screen.blit(to_blit, (self.x-(to_blit.get_width()/2),self.y-(to_blit.get_height()/2)))
        else:
            to_blit=pygame.transform.rotate(self.img, self.ang)
            screen.blit(to_blit, (self.x-(to_blit.get_width()/2),self.y-(to_blit.get_height()/2)))
        if self.lives==3:
            blitcolor=(0,200,0)
        elif self.lives==2:
            blitcolor=(200,200,0)
        else:
            blitcolor=(200,0,0)
        font=pygame.font.SysFont("TlwgMono", 30, True, True)
        screen.blit(font.render("Lives: "+str(self.lives), True, blitcolor), (10, 10))
    def move(self, keys):
        global width
        global height
        dy=math.cos(math.radians(self.ang))
        dx=math.sin(math.radians(self.ang))
        if keys[self.crtls[0]]:
            self.y-=dy*self.speed
            self.x-=dx*self.speed
        if keys[self.crtls[1]]:
            self.ang+=1*self.speed
        if keys[self.crtls[3]]:
            self.ang-=1*self.speed
        if keys[self.crtls[2]]:
            self.y+=dy*self.speed*0.5
            self.x+=dx*self.speed*0.5
            dx *= -0.5
            dy *= -0.5
        if keys[self.crtls[4]]:
            self.harm()
        print(self.x)
        print(self.y)
        if self.x <= 0:
            self.x += dx*self.speed
        if self.x >= width:
            self.x += dx*self.speed
        if self.y <= 0:
            self.y += dy*self.speed
        if self.y >= height:
            self.y += dy*self.speed
        for wall in walls:
            if pygame.Rect(wall.x-wall.img.get_width()/2, wall.x-wall.img.get_height()/2, wall.img.get_width(), wall.img.get_height()).colliderect(pygame.Rect(self.x-30, self.y-30, 60, 1)):
                self.y+=dy*self.speed
                print("!")
            if pygame.Rect(wall.x-wall.img.get_width()/2, wall.x-wall.img.get_height()/2, wall.img.get_width(), wall.img.get_height()).colliderect(pygame.Rect(self.x-30, self.y+30, 60, 1)):
                self.y+=dy*self.speed
                print("!")
            if pygame.Rect(wall.x-wall.img.get_width()/2, wall.x-wall.img.get_height()/2, wall.img.get_width(), wall.img.get_height()).colliderect(pygame.Rect(self.x+30, self.y+30, 1, -60)):
                self.x+=dx*self.speed
                print("!")
            if pygame.Rect(wall.x-wall.img.get_width()/2, wall.x-wall.img.get_height()/2, wall.img.get_width(), wall.img.get_height()).colliderect(pygame.Rect(self.x-30, self.y+30, 1, -60)):
                self.x+=dx*self.speed
                print("!")
            print(wall)
        
    def harm(self):
        if (time.time()-self.lastharmtime)>2:
            self.lastharmtime=time.time()
            self.lives-=1

class Wall:
    def __init__(self, x, y, vert, img):
        self.x=x
        self.y=y
        self.vert=vert
        self.img=img
    def draw(self):
        #if self.vert:
        #    to_blit=pygame.transform.rotate(self.img, 90)
        #    screen.blit(to_blit, (self.x-to_blit.get_width()/2, self.y-to_blit.get_height()/2))
        #else:
        screen.blit(self.img, (self.x-self.img.get_width()/2, self.y-self.img.get_height()/2))
        pygame.draw.circle(screen, (255,0,0),(self.x, self.y), 5)
        pygame.draw.circle(screen, (255,0,0),(self.x-self.img.get_width()/2, self.y-self.img.get_height()/2), 5)
        pygame.draw.circle(screen, (255,0,0),(self.x+self.img.get_width()/2, self.y+self.img.get_height()/2), 5)

        
num_players = 2
menu_state="startmenu"
def start_game():
    print("Game Started!")
    global menu_state
    menu_state="play"
    menu.disable()
    print(num_players)
def set_num_players(value, num):
    global num_players
    num_players = num

#Display
background_colour = (255,255,0)
(width, height) = (1000, 600)
pygame.init()
flags = pygame.SCALED
screen = pygame.display.set_mode((width, height), flags=flags)
pygame.display.set_caption('Tank Game')

#Menu
menu = pygame_menu.Menu('Welcome', width, height,theme=pygame_menu.themes.THEME_BLUE)
running = True
menu.add.button('Play', start_game)
menu.add.selector('Number of Players: ', [('2', 2), ('3', 3), ('4', 4)], onchange=set_num_players)
menu.add.button('Quit', pygame_menu.events.EXIT)
menu.enable()
background = pygame.image.load("/home/hudson/Pygame-dev/Tank-game/Images/landscape.jpg").convert()

#Tanks
tankB=Tank(pygame.image.load("/home/hudson/Pygame-dev/Tank-game/Images/tankB.png").convert_alpha(), (pygame.K_w,pygame.K_a,pygame.K_s,pygame.K_d,pygame.K_q), 180, 500, 300)

#Walls
walls=[Wall(200, 200, False, pygame.image.load("/home/hudson/Pygame-dev/Tank-game/Images/wall.png").convert()), Wall(800, 200, True, pygame.transform.rotate(pygame.image.load("/home/hudson/Pygame-dev/Tank-game/Images/wall.png").convert(),90))]

#Game loop
while running:
    events=pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
    keys=pygame.key.get_pressed()
    screen.fill(background_colour)
    if menu_state=="startmenu":
        menu.draw(screen)
        menu.update(events)
    elif menu_state=="play":
        screen.blit(background, (0,0))
        for wall in walls:
            wall.draw()
        tankB.draw()
        tankB.move(keys)

    pygame.display.update()
