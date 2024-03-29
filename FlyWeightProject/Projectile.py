import pygame
from typing import Any

class ProjectileFlyweight():
    def __init__(self, name: str, image_path: str, speed: float, lifetime: int, damage: int, pierce: bool , image_size: tuple):
        self.damage = damage
        self.pierce = pierce   
        self.image = pygame.transform.scale(pygame.image.load(f".\Images\{image_path}.png"), image_size)
        self.lifetime = lifetime
        self.name = name
        self.speed = speed
        self.rect = self.image.get_rect()      

class ProjectileFactory:
    __projectiles = {
        'bullet': ProjectileFlyweight(name='bullet', image_path='projectile', speed=0.03, lifetime=1000, damage=3, pierce=False, image_size=(15,15)),
        'slow_bullet': ProjectileFlyweight(name='bullet', image_path='projectile', speed=0.01, lifetime=1000, damage=2, pierce=False, image_size=(15,15)),
        'piercing_bullet': ProjectileFlyweight(name='piercing_bullet', image_path='projectile', speed=0.05, lifetime=5000, damage=10, pierce=True, image_size=(15,15)),
        'explosion': ProjectileFlyweight(name='explosion', image_path='explosion', speed=0, lifetime=100, damage=2, pierce=False, image_size=(200*0.96,200)),
        'landmine': ProjectileFlyweight(name='bomb', image_path='landmine', speed=0, lifetime=700, damage=0, pierce=False, image_size=(20,20)),
        'missile': ProjectileFlyweight(name='bomb', image_path='missile', speed=0.03, lifetime=500, damage=2, pierce=False, image_size=(20,20)),
    }

    @staticmethod
    def get(name):
        return ProjectileFactory.__projectiles.get(name)


class Projectile(pygame.sprite.Sprite):
    def __init__(self, name: str, source: tuple, target: tuple):
        super().__init__()
        self.created_at = pygame.time.get_ticks()
        self.movement_vector = [target[0], target[1]]
        self.pos = [source[0], source[1]]

        flyweight = ProjectileFactory.get(name)
        self.image = flyweight.image
        self.lifetime = flyweight.lifetime
        self.pierce = flyweight.pierce
        self.speed = flyweight.speed       
        self.damage = flyweight.damage
        
        self.rect = self.image.get_rect(topleft=self.pos)
    
    def collide(self):
        if not self.pierce:
            self.kill()
    
    def move(self, surfaceSize, tDelta):
        if pygame.time.get_ticks() > self.created_at + self.lifetime:
            self.kill()
        self.pos[0] += self.movement_vector[0] * self.speed * tDelta
        self.pos[1] += self.movement_vector[1] * self.speed * tDelta
        self.rect.topleft = self.pos
        if self.pos[0] > surfaceSize[0] or self.pos[0] < 0  or \
           self.pos[1] > surfaceSize[1] or self.pos[1] < 0:
               self.collide()
            
    def render(self, surface):
        surface.blit(self.image, self.pos)
        
    


class Bomb(Projectile):
    def __init__(self, name: str, user: object, target: tuple):
        super().__init__(name, user.pos, target)
        self.pos = [user.pos[0], user.pos[1]]
        self.player = user
        
    def collide(self):
        #self.explode()
        pass
        
    def explode(self):
        self.player.add_to_static_projectiles(Explosion("explosion", self.pos, self.pos))
        self.kill()
        
    def move(self, surfaceSize, tDelta):
        if pygame.time.get_ticks() > self.created_at + self.lifetime:
            self.explode()
            
        self.pos[0] += self.movement_vector[0] * self.speed * tDelta
        self.pos[1] += self.movement_vector[1] * self.speed * tDelta
        self.rect.topleft = self.pos
        if self.pos[0] > surfaceSize[0] or self.pos[0] < 0  or \
           self.pos[1] > surfaceSize[1] or self.pos[1] < 0:
               self.explode()
    
    def render(self, surface):
        # TODO: render explosion
        super().render(surface)

class Explosion(Projectile):
    def __init__(self, name, source, target):
        super().__init__(name, source, source)
        self.rect = self.rect.move(-self.rect.height/2, -self.rect.width/2)
    
    def collide(self):
        pass

    def move(self, surfaceSize, tDelta):
        if pygame.time.get_ticks() > self.created_at + self.lifetime:
            self.kill()

    def update(self, *args: Any, **kwargs: Any) -> None:
        return super().update(*args, **kwargs)


