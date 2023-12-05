import pygame
import math
from Projectile import Projectile
from Weapon import normalize_vector
import WeaponFactory

class EnemyFlyweight:
    def __init__(self, name: str, image: pygame.Surface, weapon_name: str, speed: float, 
                 default_health: int):
        self.name = name
        self.image = image
        self.weapon = WeaponFactory.get(weapon_name)
        self.speed = speed
        self.default_health = default_health

class EnemyFactory:
    __enemies = {
        'small': EnemyFlyweight('small', pygame.Surface([8, 8]), 'melee', 10, 10),
        'medium': None,
        'large': None
    }

    @staticmethod
    def get(name: str):
        return EnemyFactory.__enemies.get(name)

class Enemy(pygame.sprite.Sprite):
    projectiles = pygame.sprite.Group()
    def __init__(self, name, pos: tuple[float, float]):
        super().__init__()
        flyweight = EnemyFactory.get(name)
        self.image = flyweight.image
        self.rect = flyweight.rect
        self.radius = flyweight.radius
        self.speed = flyweight.speed
        self.weapon = flyweight.weapon

        self.name = name
        self.health = flyweight.default_health
        self.movement_vector = [0, 0]
        self.pos = list(pos)
        self.last_shot_time = pygame.time.get_ticks()
        
    def move(self, enemies: pygame.sprite.Group, player_pos: tuple[float, float], tDelta: float):
        self.movement_vector = (player_pos[0] - self.pos[0],
                               player_pos[1] - self.pos[1])
        self.movement_vector = normalize_vector(self.movementVector)
        self.pos[0] += self.movement_vector[0] * self.speed * tDelta
        self.pos[1] += self.movement_vector[1] * self.speed * tDelta
        
        # Collision test with other enemies
        self.movementVector = [0, 0]
        for sprite in enemies:
            if sprite is self:
                continue
            if pygame.sprite.collide_circle(self, sprite):
                self.movement_vector[0] += self.pos[0] - sprite.pos[0]
                self.movement_vector[1] += self.pos[1] - sprite.pos[1]

        self.movement_vector = normalize_vector(self.movement_vector)
        self.pos[0] += self.movement_vector[0] * 0.5  # The constant is how far the sprite will be
        self.pos[1] += self.movement_vector[1] * 0.5  # dragged from the sprite it collided with
        
        self.rect.topleft = self.pos

    def attack(self, target_pos):
        self.weapon.attack(self, user=self, target_pos=target_pos, last_shot_time = self.last_shot_time)
        self.last_shot_time = pygame.time.get_ticks()

    def collide(self, damage):
        self.health -= damage
        if self.health < 0:
            self.kill()

    def render(self, surface):
        surface.blit(self.image, self.pos)