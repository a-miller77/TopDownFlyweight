import EnemyFlyweight
import pygame

class EnemyFactory():
    self.__enemies__ = {
        'small': EnemyFlyweight('small', pygame.Surface([8, 8]), 'melee', 10, 10)
    }
    @staticmethod
    def get(self, name: str):
        return self.__enemies__.get(name)