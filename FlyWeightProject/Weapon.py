import pygame 
import math
import random
from Projectile import Projectile

class Weapon():
    def __init__(self):
        self.last_shot = 0
    
    def attack(self, use, pos):
        pass
    
    @staticmethod
    def normalize_vector(vector):
        if vector == [0, 0]:
            return [0, 0]    
        pythagoras = math.sqrt(vector[0]*vector[0] + vector[1]*vector[1])
        return (vector[0] / pythagoras, vector[1] / pythagoras)
    
    @staticmethod
    def rotate_vector(vector, theta):
        resultVector = (vector[0] * math.cos(theta)
                        - vector[1] * math.sin(theta),
                        vector[0] * math.sin(theta)
                        + vector[1] * math.cos(theta))
        return resultVector
    
class Shotgun(Weapon):
    def __init__(self):
        super().__init__()
        self.weapon_cooldown = 550
        self.spread_arc = 60
        self.projectilesCount = 6
        
    def attack(self, user, pos):
        current_time = pygame.time.get_ticks()
        if current_time - self.lastShot > self.weapon_cooldown:
            direction = (pos[0] - user.pos[0], pos[1] - user.pos[1]) \
                if pos != user.pos else (1, 1)
            self.last_shot = current_time
            arc_difference = self.spread_arc / (self.projectiles_count - 1)
            for proj in range(self.projectiles_count):
                theta = math.radians(arc_difference*proj - self.spread_arc/2)
                proj_dir = super().rotate_vector(direction, theta)
                user.projectiles.add(Projectile(user.pos,
                                                super().normalize_vector(proj_dir),
                                                7, 500, (232, 144, 42)))

class MachineGun(Weapon):
    def __init__(self):
        super().__init__()
        self.weapon_cooldown = 100
        self.spread_arc = 25
        
    def attack(self, user, pos):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot > self.weapon_cooldown:
            direction = (pos[0] - user.pos[0], pos[1] - user.pos[1]) \
                if pos != user.pos else (1, 1)
            self.lastShot = current_time
            theta = math.radians(random.random()*self.spread_arc - self.spread_arc/2)
            proj_dir = super().rotate_vector(direction, theta)   
            user.projectiles.add(Projectile(
                user.pos,
                super().normalize_vector(proj_dir),
                speed=6, 
                lifetime=5000,
                color=(194, 54, 16)))
class Rifle(Weapon):
    def __init__(self):
        super().__init__()
        self.weapon_cooldown = 300
        
    def attack(self, user, pos):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot > self.weapon_cooldown:
            direction = (pos[0] - user.pos[0], pos[1] - user.pos[1]) \
                if pos != user.pos else (1, 1)
            self.lastShot = current_time
            proj_dir = super().rotate_vector(direction, 0)   
            user.projectiles.add(
                Projectile(
                    user.pos,
                    super().normalize_vector(proj_dir),
                    speed=6, 
                    lifetime=5000,
                    color=(194, 54, 16)))
        
                
class Melee(Weapon):
    def __init__(self):
        super().__init__()
        self.weapon_cooldwon = 100
        
    def attack(self, user, pos):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot > self.weapon_cooldown:
            direction = (pos[0] - user.pos[0], pos[1] - user.pos[1]) \
                if pos != user.pos else (1, 1)
            self.last_shot = current_time
            proj_dir = super().rotate_vector(direction, 0)
            # Add code here to create the actual mele weapon. 
            
        
class MissileLauncher(Weapon):
    def __init__(self):
        super().__init__()
        self.weapon_cooldown = 1000
        
    def attack(self, user, pos):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot > self.weapon_cooldown:
            direction = (pos[0] - user.pos[0], pos[1] - user.pos[1]) \
                if pos != user.pos else (1, 1)
            self.lastShot = current_time
            proj_dir = super().rotate_vector(direction, 0)   
            user.projectiles.add(Projectile(user.pos,
                                            super().normalize_vector(proj_dir),
                                            speed=6, 
                                            lifetime=5000,
                                            color=(194, 54, 16)))
            # insert code here to add bomb once contact has been made
        
class Bomb(Weapon):
    def __init__(self):
        super().__init__()
        
    def attack(self, user, pos):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot > self.weapon_cooldown:
            direction = (pos[0] - user.pos[0], pos[1] - user.pos[1]) \
                if pos != user.pos else (1, 1)
            self.lastShot = current_time
            proj_dir = super().rotate_vector(direction, 0)   
            # insert code here to create a bomb