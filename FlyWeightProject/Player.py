import pygame
class Player( pygame.sprite.Sprite):
    def __init__(self, pos: tuple[float, float],  weapon_name: str):
        super().__init__()
        self.weapon = WeaponFactory.get(weapon_name)
        self.image = pygame.transform.scale(pygame.image.load("FlyWeightProject\Images\player.png"), (100, 100))
        self.pos  = list(pos)
        self.movement_vector = [0, 0]
        self.alive = True
        self.health = 100
        self.speed = 20


    def move(self, surfaceSize, tDelta):
        

    def attack(self, target_pos):
        self.weapon.attack(self, target_pos, self.last_shot_time)
        self.last_shot_time = pygame.time.get_ticks()