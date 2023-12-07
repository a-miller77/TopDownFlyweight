from math import sqrt
from typing import Any
import pygame

class CoinFlyweight():
    def __init__(self, value: int, image: pygame.Surface):
        self.value = value
        self.image = image

class CoinFactory():
    __coins = {
        1 : CoinFlyweight(1, 
                          pygame.transform.scale(pygame.image.load('./Images/coinImage.png'), 
                                                 (7,7)))
        }
    
    @staticmethod
    def get(value: int):
        return CoinFactory.__coins.get(value)
    
class Coin(pygame.sprite.Sprite):
    def __init__(self, value: int, pos: tuple[float, float]):
        super().__init__()
        flyweight = CoinFactory.get(value)
        self.value = flyweight.value
        self.image = flyweight.image
        self.rect = self.image.get_rect(topleft=pos)
        self.pos = pos

    def update(self, *args: Any, **kwargs: Any) -> None:
        return super().update(*args, **kwargs)

    def render(self, surface):
        surface.blit(self.image, self.pos)

    def collide(self):
        self.kill()