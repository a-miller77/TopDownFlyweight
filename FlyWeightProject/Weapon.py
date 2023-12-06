import pygame
import math
import random
from Projectile import Projectile, Bomb

class Weapon():
    def __init__(self):
        pass
    
    def attack(self, use, pos, last_shot_time):
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
        self.projectiles_count = 6
        
    def attack(self, user, pos, last_shot_time):
        current_time = pygame.time.get_ticks()
        if current_time - last_shot_time > self.weapon_cooldown:
            direction = (pos[0] - user.pos[0], pos[1] - user.pos[1]) \
                if pos != user.pos else (1, 1)
            last_shot_time = current_time
            arc_difference = self.spread_arc / (self.projectiles_count - 1)
            for proj in range(self.projectiles_count):
                theta = math.radians(arc_difference*proj - self.spread_arc/2)
                proj_dir = super().rotate_vector(direction, theta)
                
                for i in range(6):
                    user.projectiles.add(
                        Projectile(
                            'bullet',
                            user.pos,
                            proj_dir
                        )
                    )
                
                
                
                

class MachineGun(Weapon):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(".\Images\machinegun.png"), (40,40))
        self.weapon_cooldown = 100
        self.spread_arc = 25
        
    def attack(self, user, pos, last_shot_time):
        current_time = pygame.time.get_ticks()
        if current_time - last_shot_time > self.weapon_cooldown:
            direction = (pos[0] - user.pos[0], pos[1] - user.pos[1]) \
                if pos != user.pos else (1, 1)
            last_shot_time = current_time
            # theta = math.radians(random.random()*self.spread_arc - self.spread_arc/2)
            # proj_dir = super().rotate_vector(direction, theta)   

            user.projectiles.add(
                Projectile(
                    'bullet',
                    user.pos,
                    direction)
            )
            
class Rifle(Weapon):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("./Images/rifle.png"), (40,40))
        self.weapon_cooldown = 300
        
    def attack(self, user, pos, last_shot_time):
        current_time = pygame.time.get_ticks()
        if current_time - last_shot_time > self.weapon_cooldown:
            direction = (pos[0] - user.pos[0], pos[1] - user.pos[1]) \
                if pos != user.pos else (1, 1)
            last_shot_time = current_time
            # proj_dir = super().rotate_vector(direction, 0)   
            user.projectiles.add(
                Projectile(
                    'bullet',
                    user.pos,
                    direction
                )
            )
        
                
class Melee(Weapon):
    def __init__(self):
        super().__init__()
        self.weapon_cooldown = 100
        self.melee_range = 10  # Adjust the melee range as needed

    def attack(self, user, pos, last_shot_time):
        current_time = pygame.time.get_ticks()
        if current_time - last_shot_time > self.weapon_cooldown:
            last_shot_time = current_time
            distance_to_player = math.dist(user.pos, pos)
            if distance_to_player <= self.melee_range:
                return 10
        return 0

class MissileLauncher(Weapon):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("./Images/rocketLauncher.png"),(40,40))
        self.weapon_cooldown = 800
        
    def attack(self, user, pos, last_shot_time):
        current_time = pygame.time.get_ticks()
        if current_time - last_shot_time > self.weapon_cooldown:
            direction = (
                pos[0] - user.pos[0], pos[1] - user.pos[1]
            ) if pos != user.pos else (1, 1)
            last_shot_time = current_time
            # proj_dir = super().rotate_vector(direction, 0)
            user.projectiles.add(
                Bomb(
                    'missile',
                    user,
                    direction
                )
            )
            

class LandMine(Weapon):
    def __init__(self):
        super().__init__()
        self.weapon_cooldown = 200
        self.explosion_radius = 50
        
    def attack(self, user, pos, last_shot_time):
        current_time = pygame.time.get_ticks()
        if current_time - last_shot_time > self.weapon_cooldown:
            last_shot_time = current_time
            user.projectiles.add(
                Bomb(
                    'landmine',
                    user,
                    user.pos
                )
            )
            
class WeaponFactory:
    __weapons = {
        'shotgun': Shotgun(),
        'machine_gun': MachineGun(),
        'rifle': Rifle(),
        'melee': Melee(),
        'missilelauncher': MissileLauncher(),
        'landmine': LandMine()
    }
    
    @staticmethod
    def get(name):
        return WeaponFactory.__weapons.get(name)
