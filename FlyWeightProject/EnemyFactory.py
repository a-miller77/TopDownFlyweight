import EnemyFlyweight
import pygame

class EnemyFactory:
    __enemies = {
        'small': EnemyFlyweight('small', pygame.Surface([8, 8]), 'melee', 10, 10)
    }

    @staticmethod
    def get(name: str):
        return EnemyFactory.__enemies.get(name)