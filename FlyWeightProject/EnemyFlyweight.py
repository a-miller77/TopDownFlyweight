import pygame
import Weapon

class EnemyFlyweight():
    def __init__(self, name: str, image: pygame.Surface, weapon_name: str, speed: float, 
                 default_health: int):
        self.name = name
        self.image = image
        self.weapon_name = weapon_name
        self.speed = speed
        self.default_health = default_health