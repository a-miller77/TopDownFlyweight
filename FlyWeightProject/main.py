# -*- coding: utf-8 -*-

import pygame
import random
from Player import Player
from Enemy import Enemy
from Enemy import EnemyFactory
from Projectile import Projectile
from Weapon import WeaponFactory
import cProfile

pygame.init()
pygame.display.set_caption("Pew Pew Game MF")
size = (1280, 800)
screen = pygame.display.set_mode(size)

# set an image for the background
background = pygame.image.load("./Images/background.png")
background = pygame.transform.scale(background, size)
background = background.convert()

try:
    font = pygame.font.Font("Roboto-Regular.ttf", 25)
except OSError:
    # If the font file is not available, the default will be used.
    font = pygame.font.Font(pygame.font.get_default_font(), 25)

# display the hero health on the top left of the screen with white text
hero_health_text = font.render("Hero Health: ", True, (225, 225, 225))
# display the hero score on the top right of the screen with white text
hero_score_text = font.render("Score: ", True, (225, 225, 225))

done = False
hero = pygame.sprite.GroupSingle(Player((screen.get_size()[0]/2, screen.get_size()[1]/2), screen.get_size()))
ranged_enemies = pygame.sprite.Group()
melee_enemies = pygame.sprite.Group()
lastEnemy = 0
score = 0
clock = pygame.time.Clock()

MAX_ENEMIES = 50

def move_entities(hero, melee_enemies, ranged_enemies, timeDelta):
    hero.sprite.move(timeDelta)

    for enemy in melee_enemies:
        enemy.move(melee_enemies, player_pos = hero.sprite.rect.topleft, tDelta = timeDelta)
        damage = enemy.attack(hero.sprite.rect.topleft)
        if damage != None:
            hero.sprite.collide(damage)

    for enemy in ranged_enemies:
        enemy.move(ranged_enemies, player_pos = hero.sprite.rect.topleft, tDelta = timeDelta)
        enemy.attack(hero.sprite.rect.topleft)

    for proj in Enemy.projectiles:
        proj.move(screen.get_size(), timeDelta) #TODO
        if pygame.sprite.spritecollide(proj, hero, False):
            proj.collide()
            hero.sprite.collide(proj.damage)

    for proj in Player.projectiles:
        proj.move(screen.get_size(), timeDelta) #TODO
        melee_enemies_hit = pygame.sprite.spritecollide(proj, melee_enemies, False)
        ranged_enemies_hit = pygame.sprite.spritecollide(proj, ranged_enemies, False)

        for enemy in melee_enemies_hit:
            enemy.collide(proj.damage)

        for enemy in ranged_enemies_hit:
            enemy.collide(proj.damage)

        if melee_enemies_hit or ranged_enemies_hit:
            proj.collide()
               
    collected = None
    collected = pygame.sprite.spritecollide(hero.sprite, Player.coins, True)
    hero.sprite.collected_coins += len(collected)

def render_entities(hero, melee_enemies, ranged_enemies):
    hero.draw(screen)
    Player.projectiles.draw(screen)
    # for coin in Player.coins:
    #     coin.render(screen)
    Player.coins.draw(screen)
    Enemy.projectiles.draw(screen)
    melee_enemies.draw(screen)
    ranged_enemies.draw(screen)
def draw_centered_surface(screen, surface, y):
    screen.blit(surface, (screen.get_width()/2 - surface.get_width()/2, y))
    

    
def process_keys(keys, hero):
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        hero.sprite.movement_vector[1] -= 1
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        hero.sprite.movement_vector[0] -= 1
    if keys[pygame.K_s] or keys[pygame.K_RIGHT]:
        hero.sprite.movement_vector[1] += 1
    if keys[pygame.K_d] or keys[pygame.K_DOWN]:
        hero.sprite.movement_vector[0] += 1
    
    if keys[pygame.K_1]:
        hero.sprite.weapon = WeaponFactory.get('shotgun')
    if keys[pygame.K_2]:
        hero.sprite.weapon = WeaponFactory.get('machine_gun')
    if keys[pygame.K_3]:
        hero.sprite.weapon = WeaponFactory.get('rifle')
    if keys[pygame.K_4]:
        hero.sprite.weapon = WeaponFactory.get('missilelauncher')
    if keys[pygame.K_5]:
        hero.sprite.weapon = WeaponFactory.get('landmine')
        
def process_mouse(mouse, hero):
    if mouse[0]:
        hero.sprite.attack(pygame.mouse.get_pos())
 
def game_loop():
    # reset the hero's health and score
    hero.sprite.alive = True
    hero.sprite.health = 100
    hero.sprite.collected_coins = 0
    
    # clear any existing enemies if there are any
    melee_enemies.empty()
    ranged_enemies.empty()
    Enemy.projectiles.empty()
    Player.projectiles.empty()
    Player.coins.empty()
    
    done = False
    # hero = pygame.sprite.GroupSingle(Player(screen.get_size()))
    # enemies = pygame.sprite.Group()
    # pygame.key.set_repeat(10)
    last_enemy_spawn = pygame.time.get_ticks()
    
    while hero.sprite.alive and not done:
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()
        currentTime = pygame.time.get_ticks()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
        # check to see if the hero is dead
        if hero.sprite.health <= 0:
            hero.sprite.alive = False
            
        
        process_keys(keys, hero)
        process_mouse(mouse, hero)
        
        # Enemy spawning process
        num_enemies = len(ranged_enemies) + len(melee_enemies)
        if last_enemy_spawn < currentTime - 150 and num_enemies < MAX_ENEMIES:
            
            enemy_name = EnemyFactory.get_random()

            spawn_side = random.random()
            
            if spawn_side < 0.25:
                pos = (0, random.randint(0, size[1]))
            elif spawn_side < 0.5:
                pos = (size[0], random.randint(0, size[1]))
            elif spawn_side < 0.75:
                pos = (random.randint(0, size[0]), 0)
            else:
                pos = (random.randint(0, size[0]), size[1])

            enemy = Enemy(enemy_name, pos)

            if(enemy.weapon == WeaponFactory.get('melee')):
                melee_enemies.add(enemy)
            else:
                ranged_enemies.add(enemy)

            last_enemy_spawn = currentTime
        # Draw the background
        screen.blit(background, (0, 0))
        
        move_entities(hero, melee_enemies, ranged_enemies, clock.get_time()/10)
        render_entities(hero, melee_enemies, ranged_enemies)
        
        hero_health_text = font.render(f"Hero Health: {hero.sprite.health}", True, (225, 225, 225))
        hero_score_text = font.render(f"Score: {hero.sprite.collected_coins}", True, (225, 225, 225))
        # display the hero health on the bottom of the screen
        draw_centered_surface(screen, hero_health_text, screen.get_height() - hero_health_text.get_height())
        draw_centered_surface(screen, hero_score_text, 0)
        
        pygame.display.flip()
        clock.tick(30)

#cProfile.run('game_loop()')
game_loop()
while not done:
    keys = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pressed()
    currentTime = pygame.time.get_ticks()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    
    if keys[pygame.K_r]:
        game_loop()
pygame.quit()
