from math import sqrt
from typing import Self
from FlyWeightProject.CoinFlyweight import CoinFlyweight
import CoinFlyweight
import pygame
class Coin(pygame.sprite.Sprite):
    def  collide():
        pass 
    def __init__(value: int, pos: tuple[float, float]):
        flyweight = CoinFlyweight.get(value)
        Self.pos = pos
        Self.vaule = value