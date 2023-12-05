import pygame
import math
import random
#from Projectile import Projectile
from Player import Player
from Coin import Coin
from Weapon import WeaponFactory, Weapon

class EnemyFlyweight:
    def __init__(self, name: str, image: pygame.Surface, weapon_name: str, speed: float, 
                 default_health: int):
        self.name = name
        self.image = image
        self.dead_image = pygame.transform.rotate(self.image, 90)
        self.rect = image.get_rect()
        self.weapon = WeaponFactory.get(weapon_name)
        self.speed = speed
        self.default_health = default_health

class EnemyFactory:
    __enemies = {
        'small': EnemyFlyweight(name='small', 
                                image= pygame.transform.scale(
                                    pygame.image.load('./Images/smallEnemy.png'), 
                                    (25,25)
                                    ), 
                                weapon_name='melee',
                                speed = 0.8, 
                                default_health=2),
        'medium': EnemyFlyweight(name='medium', 
                                image= pygame.transform.scale(
                                    pygame.image.load('./Images/mediumEnemy.png'), 
                                    (30,30)
                                    ), 
                                weapon_name='melee',
                                speed = 0.6, 
                                default_health=10),
        'large': EnemyFlyweight(name='large', 
                                image= pygame.transform.scale(
                                    pygame.image.load('./Images/largeEnemy.png'), 
                                    (40,40)
                                    ), 
                                weapon_name='melee',
                                speed = 0.4, 
                                default_health=45)
    }

    @staticmethod
    def get(name: str):
        return EnemyFactory.__enemies.get(name)
    
    @staticmethod
    def get_random():
        choices = []
        for _ in range(15):
            choices.append('small')
        for _ in range(4):
            choices.append('medium')
        for _ in range(1):
            choices.append('large')
        idx = random.randint(0,len(choices)-1)
        return choices[idx]
    
class Enemy(pygame.sprite.Sprite):
    projectiles = pygame.sprite.Group()
    def __init__(self, name, pos: tuple[float, float]):
        super().__init__()
        flyweight = EnemyFactory.get(name)
        self.image = flyweight.image
        self.dead_image = flyweight.dead_image
        self.rect = self.image.get_rect()
        #self.radius = flyweight.radius
        self.speed = flyweight.speed
        self.weapon = flyweight.weapon

        self.name = name
        self.health = int(flyweight.default_health)
        self.movement_vector = [0, 0]
        self.pos = list(pos)
        self.last_shot_time = pygame.time.get_ticks()
        self.dead = False
        
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

    def attack(self, target_pos):
        if not self.dead:
            pass
            # self.weapon.attack(self, pos=target_pos, last_shot_time = self.last_shot_time)
            # self.last_shot_time = pygame.time.get_ticks()

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

    def render(self, surface):
        surface.blit(self.image, self.pos)