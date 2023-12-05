from math import sqrt
from typing import Self
import pygame

class CoinFlyweight():
    def __init__(self, value: int, image: pygame.Surface):
        self.value = value
        self.image = image

class CointFactory():
    __coins__ = {
        1 : CoinFlyweight(1, 
                          pygame.transform.scale(pygame.image.load('FlyWeightProject\Images\coinImage.png'), 
                                                 (10,10)))
        }
    
    @staticmethod
    def get(self, value: int):
        return self.__Coins___.get(value)
    
class Coin(pygame.sprite.Sprite):
    def __init__(self, value: int, pos: tuple[float, float]):
        flyweight = CoinFlyweight.get(value)
        self.value = flyweight.value
        self.image = pygame.image.load('FlyWeightProject\Images\coinImage.png')

    def collide(self):
        self.kill()