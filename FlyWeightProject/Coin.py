from math import sqrt
from typing import Self
from FlyWeightProject.CoinFlyweight import CoinFlyweight
import CoinFactory
import pygame

class Coin(pygame.sprite.Sprite):
    def __init__(value: int, pos: tuple[float, float]):
            flyweight = CoinFactory.get()
            Self.pos = pos
            Self.vaule = value

    def collide():
        pass