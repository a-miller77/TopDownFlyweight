import pygame
from Weapon import WeaponFactory, Weapon
from Enemy import Enemy
from Player import Player
from Coin import Coin
import random

class NoFlyWeightEnemy(pygame.sprite.Sprite):
    projectiles = pygame.sprite.Group()
    def __init__(self, name: str, image: pygame.Surface, weapon_name: str, speed: float, 
                 default_health: int, pos: tuple[float, float]):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("./Images/smallEnemy.png"), (25,25))
        self.dead_image = pygame.transform.rotate(self.image, 90)
        self.rect = self.image.get_rect()
        self.speed = speed
        self.weapon = WeaponFactory.get(weapon_name)

        self.name = name
        self.dead = False
        self.health = default_health
        self.movement_vector = [0, 0]
        self.pos = list(pos)
        self.last_shot_time = pygame.time.get_ticks()
        
    def move(self, enemies: pygame.sprite.Group, player_pos: tuple[float, float], tDelta: float):
        if not self.dead:
            self.movement_vector = (player_pos[0] - self.pos[0],
                                player_pos[1] - self.pos[1])
            self.movement_vector = Weapon.normalize_vector(self.movement_vector)
            self.pos[0] += self.movement_vector[0] * self.speed * tDelta
            self.pos[1] += self.movement_vector[1] * self.speed * tDelta
            
            # Collision test with other enemies
            self.movement_vector = [0, 0]
            for sprite in enemies:
                if sprite is self:
                    continue
                if pygame.sprite.collide_circle(self, sprite):
                    self.movement_vector[0] += self.pos[0] - sprite.pos[0]
                    self.movement_vector[1] += self.pos[1] - sprite.pos[1]

            self.movement_vector = Weapon.normalize_vector(self.movement_vector)
            self.pos[0] += self.movement_vector[0] * 0.5  # The constant is how far the sprite will be
            self.pos[1] += self.movement_vector[1] * 0.5  # dragged from the sprite it collided with
            
            self.rect.topleft = self.pos
        else:
            if pygame.time.get_ticks() - 500 >= self.last_shot_time:
                self.death()

    def collide(self, damage):
        self.health -= damage
        if self.health < 0:
            self.dead = True
            self.image = self.dead_image
            self.last_shot_time = pygame.time.get_ticks()
    
    def death(self):
        #print("Enemy Dead")
        for _ in range(5):
            x = self.pos[0] + random.randrange(-10, 10)
            y = self.pos[1] + random.randrange(-10, 10)
            Player.coins.add(Coin(1, (x, y)))
        self.kill()

    def attack(self, target_pos):
        if not self.dead:
            pass
        # self.weapon.attack(self, target_pos, self.last_shot_time)
        # self.last_shot_time = pygame.time.get_ticks()

    def render(self, surface):
        surface.blit(self.image, self.pos)
    