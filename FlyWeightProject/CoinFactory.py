import pygame
import CoinFlyweight

class CoinFactory:
    coins__ = {
        1 : CoinFlyweight(value = 1, image = (3, pygame.Surface([4, 4])))
        }
    @staticmethod
    def get():
        return CoinFactory.coins__.get(1)