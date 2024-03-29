import pygame
import math
import random
#from Projectile import Projectile
from Player import Player
from Coin import Coin
from Weapon import WeaponFactory, Weapon

class EnemyFlyweight:
    def __init__(self, name: str, image: pygame.Surface, weapon_name: str, speed: float, 
                 default_health: int, value: int):
        self.name = name
        self.image = image
        self.dead_image = pygame.transform.rotate(self.image, 90)
        self.inverted_image = pygame.transform.flip(self.image, True, False)
        self.rect = image.get_rect()
        self.weapon = WeaponFactory.get(weapon_name)
        self.speed = speed
        self.value = value
        self.default_health = default_health

class EnemyFactory:
    __enemies = {
        'small': EnemyFlyweight(name='small', 
                                image= pygame.transform.scale(
                                    pygame.image.load('./Images/smallEnemy.png'), 
                                    (40,40)
                                    ), 
                                weapon_name='melee',
                                speed = 1, 
                                default_health=2,
                                value=1),
        'medium': EnemyFlyweight(name='medium', 
                                image= pygame.transform.scale(
                                    pygame.image.load('./Images/mediumEnemy.png'), 
                                    (40,40*1.92)
                                    ), 
                                weapon_name='melee',
                                speed = 0.7, 
                                default_health=10,
                                value=3),
        'large': EnemyFlyweight(name='large', 
                                image= pygame.transform.scale(
                                    pygame.image.load('./Images/largeEnemy.png'), 
                                    (100,100)
                                    ), 
                                weapon_name='melee',
                                speed = 0.4, 
                                default_health=45,
                                value=10),
        'small_shooter': EnemyFlyweight(name='small_shooter', 
                                image= pygame.transform.scale(
                                    pygame.image.load('./Images/smallShootingEnemy.png'), 
                                    (40,40)
                                    ), 
                                weapon_name='pistol',
                                speed = 1, 
                                default_health=2,
                                value=2),
    }

    @staticmethod
    def get(name: str):
        return EnemyFactory.__enemies.get(name)
    
    @staticmethod
    def get_random():
        choices = []
        for _ in range(12):
            choices.append('small')
        for _ in range(3):
            choices.append('small_shooter')
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
        self.regular_image = flyweight.image
        self.dead_image = flyweight.dead_image
        
        self.rect = self.image.get_rect()
        self.inverted_image = flyweight.inverted_image
        #self.radius = flyweight.radius
        self.speed = flyweight.speed
        self.weapon = flyweight.weapon

        self.name = name
        self.health = int(flyweight.default_health)
        self.value = flyweight.value
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
            
            # add code to check what direction the player is in and flip the image accordingly
            if self.movement_vector[0] > 0:
                self.image = self.inverted_image
            else:
                self.image = self.regular_image
                            
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
            if pygame.time.get_ticks() - 300 >= self.last_shot_time:
                self.death()

    def attack(self, target_pos):
        if not self.dead:
            damage = self.weapon.attack(self, pos=target_pos, last_shot_time = self.last_shot_time)
            if not damage == 0:
                self.last_shot_time = pygame.time.get_ticks()
            return damage

    def collide(self, damage):
        self.health -= damage
        if self.health < 0 and not self.dead:
            self.dead = True
            self.image = self.dead_image
            self.last_shot_time = pygame.time.get_ticks()
    
    def death(self):
        #print("Enemy Dead")
        coin_sizes = Coin.get_coin_sizes()
        coin_sizes.sort(reverse=True)

        for coin_value in coin_sizes:
            while self.value >= coin_value:
                self.value -= coin_value
                self.create_coin(coin_value) 
        self.kill()

    def create_coin(self, value):
        x = self.pos[0] + random.randrange(-10, 10)
        y = self.pos[1] + random.randrange(-10, 10)
        Player.coins.add(Coin(value, (x, y)))

    def render(self, surface):
        surface.blit(self.image, self.pos)