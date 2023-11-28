import pygame 
import math
import random
from Projectile import Projectile

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
        self.weapon_cooldown = 100
        self.melee_range = 30  # Adjust the melee range as needed

    def attack(self, user, pos, all_sprites):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot > self.weapon_cooldown:
            direction = (
                pos[0] - user.pos[0], pos[1] - user.pos[1]
            ) if pos != user.pos else (1, 1)
            self.last_shot = current_time
            proj_dir = super().rotate_vector(direction, 0)
            
            # Check for collision with projectiles within melee range
            for sprite in all_sprites:
                if (
                    isinstance(sprite, Projectile)
                    and sprite != user
                    and math.sqrt(
                        (user.pos[0] - sprite.pos[0]) ** 2
                        + (user.pos[1] - sprite.pos[1]) ** 2
                    )
                    <= self.melee_range
                ):
                    # Add code here to apply melee effect to the enemy projectile.
                    # For example, you could remove the projectile or decrease its health.
                    sprite.kill()
            
        
class MissileLauncher(Weapon):
    def __init__(self):
        super().__init__()
        self.weapon_cooldown = 800
        
    def attack(self, user, pos):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot > self.weapon_cooldown:
            direction = (
                pos[0] - user.pos[0], pos[1] - user.pos[1]
            ) if pos != user.pos else (1, 1)
            self.last_shot = current_time
            proj_dir = super().rotate_vector(direction, 0)
            bomb = Bomb(
                user.pos,
                super().normalize_vector(proj_dir),
                speed=4,
                lifetime=3000,
                color=(0, 0, 255)  # Blue color for bombs
            )
            user.projectiles.add(bomb)
            bomb_group = pygame.sprite.Group(bomb)
            bomb.explode(user, bomb_group)
        
class Bomb(Projectile):
    def __init__(self, pos, direction, speed, lifetime, color):
        super().__init__(pos, direction, speed, lifetime, color)
        self.explosion_radius = 30
        
    def explode(self, surface, all_sprites):
        # Add explosion effect code here
        pygame.draw.circle(
            surface, (255, 0, 0), (int(self.pos[0]), int(self.pos[1])), self.explosion_radius
        )
        # You can add additional effects or damage logic based on the surrounding entities
        for sprite in all_sprites:
            if (
                isinstance(sprite, Projectile)
                and sprite != self
                and math.sqrt(
                    (self.pos[0] - sprite.pos[0]) ** 2
                    + (self.pos[1] - sprite.pos[1]) ** 2
                )
                <= self.explosion_radius
            ):
                sprite.kill()