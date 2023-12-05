from math import sqrt
from typing import Self
from FlyWeightProject.CoinFlyweight import CoinFlyweight
import CoinFactory
import pygame

class CoinFlyweight():
    def __init__(self, value: int, image: pygame.Surface):
        self.value = value
        self.image = image
        #collison
class CointFactory():
    __coins__ = {
        'small' : CoinFlyweight(3, pygame.transform.scale(pygame.image.load('FlyWeightProject\Images\coinImage.png'), (10,10))))
        }
    
    @staticmethod
    def get(self, value: int):
        return self.__Coins___.get(value)
class Coin(pygame.sprite.Sprite):
    def  collide():
        pass 
    def __init__(self, value: int, pos: tuple[float, float]):
        flyweight = CoinFlyweight.get(value)
        self.value = flyweight.rec
        self.image = pygame.image.load('FlyWeightProject\Images\coinImage.png')