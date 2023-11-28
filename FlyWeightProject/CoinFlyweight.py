from typing import Self
import pygame
import Coin


class CoinFlyweight():
    def __init__(value: int, image: pygame.Surface):
        Self.value = value
        Self.image = image
    #collison