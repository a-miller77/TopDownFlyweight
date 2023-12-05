import pygame
import math 
from Weapon import WeaponFactory

def normalize_vector(vector):
    if vector == [0, 0]:
        return [0, 0]    
    pythagoras = math.sqrt(vector[0]*vector[0] + vector[1]*vector[1])
    return (vector[0] / pythagoras, vector[1] / pythagoras)
class Player( pygame.sprite.Sprite):
    projectiles = pygame.sprite.Group()
    coins = pygame.sprite.Group()
    def __init__(self, pos: tuple[float, float], screen_size, weapon_name: str = 'landmine'):
        super().__init__()
        self.weapon = WeaponFactory.get(weapon_name)
        self.image = pygame.transform.scale(pygame.image.load(".\Images\player.png"), (30, 30))
        self.rect = self.image.get_rect()
        self.screen_size = screen_size
        self.pos = list(pos)
        self.movement_vector = [0, 0]
        self.alive = True
        self.health = 100
        self.speed = 1.5
        self.collected_coins = 0
        self.last_shot_time = pygame.time.get_ticks()


    def move(self, tDelta):
        self.movement_vector = normalize_vector(self.movement_vector)
        newPos = (self.pos[0] + self.movement_vector[0]*self.speed*tDelta,
                    self.pos[1] + self.movement_vector[1]*self.speed*tDelta)
        if newPos[0] < 0:
            self.pos[0] = 0
        elif newPos[0] > self.screen_size[0] - self.rect.width:
            self.pos[0] = self.screen_size[0] - self.rect.width
        else:
            self.pos[0] = newPos[0]
        
        if newPos[1] < 0:
            self.pos[1] = 0
        elif newPos[1] > self.screen_size[1]-self.rect.height:
            self.pos[1] = self.screen_size[1]-self.rect.width
        else:
            self.pos[1] = newPos[1]
            
        self.rect.topleft = self.pos
        self.movement_vector = [0, 0]


    def attack(self, target_pos):
        self.weapon.attack(self, target_pos, self.last_shot_time)
        self.last_shot_time = pygame.time.get_ticks()
    
    def collide(self, damage):
        self.health -= damage
        print(f"Player has taken {damage} damage")
        return self.health < 0
        
    def render(self, surface):
        surface.blit(self.image, self.pos)