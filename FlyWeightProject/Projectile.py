import pygame
import numpy as np
import math
from Projectile import Projectile, Bomb
from Player import Player



class ProjectileFlyweight():
    def __init__(self, name: str, path: str, speed: float, lifetime: int, damage: int, pierce: int , image_size: tuple):
        self.damage = damage
        self.pierce = pierce   
        self.image = pygame.transform.scale(pygame.image.load(f"FlyWeightProject\Images\{path}.png"), image_size)
        self.lifetime = lifetime
        self.name = name
        self.speed = speed
        self.rect = self.image.get_rect()      

class ProjectileFactory:
    __projectiles = {
        'bullet': ProjectileFlyweight(name='bullet', path='projectile', speed=1, lifetime=1000, damage=1, pierce=0, image_size=(5,5)),
        'PiercingBullet': ProjectileFlyweight(name='PiercingBullet', path='projectile', speed=1, lifetime=1000, damage=1, pierce=1, image_size=(5,5)),
        'explosion': ProjectileFlyweight(name='explosion', path='explosion', speed=0, lifetime=100, damage=1, pierce=0, image_size=(50,50)),
        'bomb': ProjectileFlyweight(name='bomb', path='bomb', speed=0, lifetime=1000, damage=1, pierce=0, image_size=(5,5))
    }
    image = pygame.transform.scale(pygame.image.load("FlyWeightProject\Images\projectile.png"), (5,5))

    @staticmethod
    def get(name):
        return ProjectileFactory.__projectiles.get(name)

class Projectile(pygame.sprite.Sprite):
    def __init__(self, name: str, source: tuple, target: tuple):
        super().__init__()
        self.created_at = pygame.time.get_ticks()
        self.movementVector = [target[0], target[1]]
        self.pos = [source[0], source[1]]

        flyweight = ProjectileFactory.get(name)
        self.image = flyweight.image
        self.lifetime = flyweight.lifetime
        self.pierce = flyweight.pierce
        self.rect = flyweight.rect
        self.speed = flyweight.speed        
        
    def move(self, surfaceSize, tDelta):
        if pygame.time.get_ticks() > self.created_at + self.lifetime:
            self.kill()
        self.pos[0] += self.movementVector[0] * self.speed * tDelta
        self.pos[1] += self.movementVector[1] * self.speed * tDelta
        self.rect.topleft = self.pos
        if self.pos[0] > surfaceSize[0] or self.pos[0] < 0  or \
           self.pos[1] > surfaceSize[1] or self.pos[1] < 0:
            self.kill()
    def render(self, surface):
        surface.blit(self.image, self.pos)
        
    


class Bomb(Projectile):
    def __init__(self, name: str, source: tuple, target: tuple):
        super().__init__("bomb", source, target)
        
        
    def explode(self):
        Player.projectiles.add(Projectile('explosion', self.pos, (0, 0)))
        self.kill()
        
    def move(self, surfaceSize, tDelta):
        pass
    
    def render(self, surface):
        # TODO: render explosion
        super().render(surface)
    


