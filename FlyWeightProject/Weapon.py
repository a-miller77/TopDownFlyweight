import pygame
import math
import random
from Projectile import Projectile, Bomb

class Weapon():
    def __init__(self):
        self.last_shot = 0
    
    def attack(self, use, pos, all_sprites):
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
        self.image = pygame.transform.scale(pygame.image.load(".\Images\shotgun.png"), (40,40))
        self.weapon_cooldown = 550
        self.spread_arc = 60
        self.projectilesCount = 6
        
    def attack(self, user, pos, all_sprites):
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
        self.image = pygame.transform.scale(pygame.image.load(".\Images\machinegun.png"), (40,40))
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

            user.projectiles.add(
                Projectile(
                    'bullet',
                    user.pos,
                    proj_dir)
            )
            
class Rifle(Weapon):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("./Images/rifle.png"), (40,40))
        self.weapon_cooldown = 300
        
    def attack(self, user, pos, all_sprites):
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
        self.weapon_cooldown = 100
        self.melee_range = 10  # Adjust the melee range as needed

    def attack(self, user, pos, last_shot_time):
        current_time = pygame.time.get_ticks()
        if current_time - last_shot_time > self.weapon_cooldown:
            self.last_shot_time = current_time
            distance_to_player = math.dist(user.pos, pos)
            if distance_to_player <= self.melee_range:
                return self.damage
        
        return 0

class MissileLauncher(Weapon):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("./Images/rocketLauncher.png"),(40,40))
        self.weapon_cooldown = 800
        
    def attack(self, user, pos, all_sprites):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot > self.weapon_cooldown:
            direction = (
                pos[0] - user.pos[0], pos[1] - user.pos[1]
            ) if pos != user.pos else (1, 1)
            self.last_shot = current_time
            proj_dir = super().rotate_vector(direction, 0)
            bomb = Bomb(
                'bomb',
                user.pos,
                proj_dir
            )
            user.projectiles.add(bomb)
            bomb_group = pygame.sprite.Group(bomb)
            bomb.explode(user, bomb_group)

class LandMine(Weapon):
    def __init__(self):
        super().__init__()
        self.weapon_cooldown = 200
        self.explosion_radius = 50
        
    def attack(self, user, pos, last_shot_time):
        current_time = pygame.time.get_ticks()
        if current_time - last_shot_time > self.weapon_cooldown:
            user.projectiles.add(
                Bomb(
                    'bomb',
                    user,
                    user.pos
                )
            )
            
class WeaponFactory:
    __weapons = {
        'shotgun': Shotgun(),
        'machinegun': MachineGun(),
        'rifle': Rifle(),
        'melee': Melee(),
        'missilelauncher': MissileLauncher(),
        'landmine': LandMine()
    }
    
    @staticmethod
    def get(name):
        return WeaponFactory.__weapons.get(name)
