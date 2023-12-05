import pygame
import math 
import Weapon

def normalize_vector(vector):
    if vector == [0, 0]:
        return [0, 0]    
    pythagoras = math.sqrt(vector[0]*vector[0] + vector[1]*vector[1])
    return (vector[0] / pythagoras, vector[1] / pythagoras)

class Player( pygame.sprite.Sprite):
    projectiles = pygame.sprite.Group()
    def __init__(self, pos: tuple[float, float],  weapon_name: str, screenSize):
        super().__init__()
        self.rect = self.image.get_rect(x=screenSize[0]//2,
                                        y=screenSize[1]//2)
        self.weapon = Weapon.get(weapon_name)
        self.image = pygame.transform.scale(pygame.image.load("FlyWeightProject\Images\player.png"), (100, 100))
        self.pos  = list(pos)
        self.movement_vector = [0, 0]
        self.alive = True
        self.health = 100
        self.speed = 3


    def move(self, screenSize, tDelta):
        self.movementVector = normalize_vector(self.movementVector)
        newPos = (self.pos[0] + self.movementVector[0]*self.movementSpeed*tDelta,
                    self.pos[1] + self.movementVector[1]*self.movementSpeed*tDelta)
        if newPos[0] < 0:
            self.pos[0] = 0
        elif newPos[0] > screenSize[0] - self.rect.width:
            self.pos[0] = screenSize[0] - self.rect.width
        else:
            self.pos[0] = newPos[0]
        
        if newPos[1] < 0:
            self.pos[1] = 0
        elif newPos[1] > screenSize[1]-self.rect.height:
            self.pos[1] = screenSize[1]-self.rect.width
        else:
            self.pos[1] = newPos[1]
            
        self.rect.topleft = self.pos
        self.movementVector = [0, 0]


    def attack(self, target_pos):
        self.weapon.attack(self, target_pos, self.last_shot_time)
        self.last_shot_time = pygame.time.get_ticks()
    
    def collide(self, damage):
        self.health -= damage
        return self.health < 0
        
    def render(self, surface):
        surface.blit(self.image, self.pos)

    def add_to_static_projectiles(self, projectile):
        Player.projectiles.add(projectile)