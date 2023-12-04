import pygame 
import math
import random
from Projectile import Projectile, Bomb
from Weapon import Shotgun, MachineGun, Rifle, Melee, MissileLauncher, Landmine


class WeaponFactory:
    __weapons = {
        'shotgun': Shotgun(),
        'machinegun': MachineGun(),
        'rifle': Rifle(),
        'melee': Melee(),
        'missilelauncher': MissileLauncher(),
        'landmine': Landmine()
    }
    
    @staticmethod
    def get(name):
        return WeaponFactory.__weapons.get(name)

class Weapon():
    def __init__(self):
        pass
        
    def attack(self, user, pos, last_shot):
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
        self.weapon_cooldown = 550
        self.spread_arc = 60
        self.projectilesCount = 6
        
    def attack(self, user, pos, last_shot):
        current_time = pygame.time.get_ticks()
        if current_time - last_shot > self.weapon_cooldown:
            direction = (pos[0] - user.pos[0], pos[1] - user.pos[1]) \
                if pos != user.pos else (1, 1)
            last_shot = current_time
            arc_difference = self.spread_arc / (self.projectiles_count - 1)
            for proj in range(self.projectiles_count):
                theta = math.radians(arc_difference*proj - self.spread_arc/2)
                proj_dir = super().rotate_vector(direction, theta)
                user.projectiles.add(Projectile(user.pos,
                                                super().normalize_vector(proj_dir),
                                                7, 500, (232, 144, 42)))

class MachineGun(Weapon):
    def __init__(self):
        self.weapon_cooldown = 100
        self.spread_arc = 25
        
    def attack(self, user, pos, last_shot):
        current_time = pygame.time.get_ticks()
        if current_time - last_shot > self.weapon_cooldown:
            direction = (pos[0] - user.pos[0], pos[1] - user.pos[1]) \
                if pos != user.pos else (1, 1)
            last_shot = current_time
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
        
    def attack(self, user, pos, last_shot):
        current_time = pygame.time.get_ticks()
        if current_time - last_shot > self.weapon_cooldown:
            direction = (pos[0] - user.pos[0], pos[1] - user.pos[1]) \
                if pos != user.pos else (1, 1)
            last_shot = current_time
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

    def attack(self, user, pos, last_shot, player):
        current_time = pygame.time.get_ticks()
        if current_time - last_shot > self.weapon_cooldown:
            self.last_shot = current_time
            if (
                isinstance(player, Projectile)
                and player != user
                and math.sqrt(
                    (user.pos[0] - player.get_pos()) ** 2
                    + (user.pos[1] - player.get_pos()) ** 2
                )
                <= self.melee_range
            ):
                player.take_damage()
            
class MissileLauncher(Weapon):
    def __init__(self):
        super().__init__()
        self.weapon_cooldown = 800
        
    def attack(self, user, pos, last_shot):
        current_time = pygame.time.get_ticks()
        if current_time - last_shot > self.weapon_cooldown:
            direction = (
                pos[0] - user.pos[0], pos[1] - user.pos[1]
            ) if pos != user.pos else (1, 1)
            last_shot = current_time
            proj_dir = super().rotate_vector(direction, 0)
            bomb = Bomb(
                user.pos,
                super().normalize_vector(proj_dir),
                speed=4,
                lifetime=3000,
                color=(255, 0, 0)  # Red color for bombs
            )
            user.projectiles.add(bomb)
            bomb_group = pygame.sprite.Group(bomb)
            bomb.explode(user, bomb_group)

class Landmine(Weapon):
    def __init__(self):
        super().__init__()
        self.weapon_cooldown = 2000
        self.explosion_radius = 50  # Adjust the explosion radius as needed

    def attack(self, user, pos, last_shot):
        current_time = pygame.time.get_ticks()
        if current_time - last_shot > self.weapon_cooldown:
            last_shot = current_time
            bomb = Bomb(
                user.pos,
                None,
                speed=0,
                lifetime=3000,
                color=(255, 0, 0)  # Red color for bombs
            )
            user.projectiles.add(bomb)
            bomb_group = pygame.sprite.Group(bomb)
            bomb.explode(user, bomb_group)

