import pygame
import numpy as np
import math
from Projectile import Projectile, Bomb


class ProjectileFlyweight():
    def __init__(self, name: str, image: pygame.Surface, speed: float, lifetime: int, damage: int, pierce: int):
        self.damage = damage
        self.pierce = pierce   
        self.image = image
        self.lifetime = lifetime
        self.name = name
        self.speed = speed
        self.rect = image.get_rect()
        

class ProjectileFactory:
    projectiles = {
        'bullet': ProjectileFlyweight(),
        'PiercingBullet': ProjectileFlyweight(),
        'bomb': Bomb()
    }
    @staticmethod
    def get(name):
        return ProjectileFactory.projectiles.get(name)    

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
        if pygame.time.get_ticks() > self.createdAt + self.lifetime:
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
    def __init__(self, pos, direction, speed, lifetime, color):
        super().__init__(pos, direction, speed, lifetime, color)
        self.explosion_radius = 50

    def explode(self, surface, all_sprites):
        pygame.draw.circle(
            surface, (255, 0, 0), (int(self.pos[0]), int(self.pos[1])), self.explosion_radius
        )
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
