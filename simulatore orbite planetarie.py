# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 17:46:24 2023

@author: matte
"""

import pygame
import math

width, height  =1920,1080
WIN = pygame.display.set_mode((width, height))
pygame.display.set_caption("planet simulator")

black = (0,0,0)
yellow = (255,255,0)
blue  =(100,149,237)
dt = 3600*24

class Planet:
    au = 149.6e9
    G = 6.67428e-11
    scale = 250 / au
    
    def __init__(self,x,y,radius,mass,color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass  = mass
        
        self.sun  = False
        self.distance_to_sun = 0
        
        self.x_vel  = 0
        self.y_vel  = 0
        
        self.a_x = 0
        self.a_y = 0
        
        self.orbit = []
        
        self.theta = 0
        
    def draw(self, win):
        x = self.x*self.scale + width/2
        y = self.y*self.scale + height/2
        
        if len(self.orbit) > 2: 
            updated_point  = []               
            for point in self.orbit:
                x , y = point
                x = x * self.scale + width/2
                y = y * self.scale + height/2
                updated_point.append((x,y))  
                
            pygame.draw.lines(win, self.color, False, updated_point,2)
                
        pygame.draw.circle(win, self.color, (x , y), self.radius)
        
    def attraction(self, win, sun):
        theta = math.atan2(self.y,self.x)
        distance_to_sun = math.sqrt((self.x-sun.x)**2 + (self.y - sun.y)**2)
        if distance_to_sun == 0:
            self.a_x = 0
            self.a_y = 0
        else:            
            self.a_x = -(self.G * (sun.mass/distance_to_sun**2)) * math.cos(theta)
            self.a_y = -(self.G * (sun.mass/distance_to_sun**2)) * math.sin(theta)   
            
            self.x_vel = self.x_vel + self.a_x * dt
            self.y_vel = self.y_vel + self.a_y * dt 
            
            self.x = self.x + self.x_vel * dt + 0.5 * self.a_x **2 * dt
            self.y = self.y + self.y_vel * dt + 0.5 * self.a_y **2 * dt
            
            self.orbit.append((self.x, self.y))
            
            
            
def main():
    run  = True
    clock = pygame.time.Clock()
    
    sun = Planet(1,1,30,1.98892*10**30 , yellow)
    sun.sun = True
    
    mercury = Planet(0.387 * Planet.au ,0 , 8 , 3.3 * 10**23 , (130,130,130))
    mercury.y_vel = -45.4 * 1000
    
    venus = Planet(-0.7 * Planet.au, 0, 8, 48675*10**24, (166,16,34))
    venus.y_vel = 35.02 * 1000
    
    earth = Planet(-1*Planet.au , 0 , 16 , 5.9742*10**24 , blue )
    earth.y_vel = 29.783 * 1000
    
    
    planets  = [sun,mercury,venus,earth]
    
    while run:
        clock.tick(60)
        WIN.fill(black)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        for planet in planets:
            planet.attraction(WIN, sun)
            planet.draw(WIN)
            print(clock.get_fps())
        pygame.display.update()
    pygame.quit()
    
    
main()