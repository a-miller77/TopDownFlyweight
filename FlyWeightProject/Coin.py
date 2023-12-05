from math import sqrt
from typing import Self
from FlyWeightProject.CoinFlyweight import CoinFlyweight
import CoinFactory
import pygame

<<<<<<< Updated upstream
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
=======
class CoinFactory:
    coins__ = {
        1 : CoinFlyweight(value = 1, image = (3, pygame.Surface([4, 4])))
        }
    @staticmethod
    def get():
        return CoinFactory.coins__.get(1)
    
    
>>>>>>> Stashed changes
class Coin(pygame.sprite.Sprite):
    def  collide():
        pass 
    def __init__(self, value: int, pos: tuple[float, float]):
        flyweight = CoinFlyweight.get(value)
        self.value = flyweight.rec
        self.image = pygame.image.load('FlyWeightProject\Images\coinImage.png')