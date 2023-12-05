# -*- coding: utf-8 -*-

import pygame
import random
from Player import Player
from Enemy import Enemy
from Enemy import EnemyFactory
from Projectile import Projectile
from Weapon import WeaponFactory

pygame.init()
size    = (800, 600)
BGCOLOR = (255, 255, 255)
screen = pygame.display.set_mode(size)
scoreFont = pygame.font.Font("reference_project/fonts/UpheavalPro.ttf", 30)
healthFont = pygame.font.Font("reference_project/fonts/OmnicSans.ttf", 50)
healthRender = healthFont.render('z', True, pygame.Color('red'))
pygame.display.set_caption("Top Down")

done = False
hero = pygame.sprite.GroupSingle(Player(screen.get_size()))
ranged_enemies = pygame.sprite.Group()
melee_enemies = pygame.sprite.Group()
lastEnemy = 0
score = 0
clock = pygame.time.Clock()

MAX_ENEMIES = 50

def move_entities(hero, melee_enemies, ranged_enemies, timeDelta):
    hero.sprite.move(screen.get_size(), timeDelta)

    for enemy in melee_enemies:
        enemy.move(melee_enemies, player_pos = hero.sprite.rect.topleft, tDelta = timeDelta)
        damage = enemy.attack(hero.sprite.rect.topleft)
        hero.sprite.collide(damage)

    for enemy in ranged_enemies:
        enemy.move(ranged_enemies, player_pos = hero.sprite.rect.topleft, tDelta = timeDelta)
        enemy.attack(hero.sprite.rect.topleft)

    for proj in Enemy.projectiles:
        proj.move(screen.get_size(), timeDelta) #TODO
        if pygame.sprite.spritecollide(proj, hero, False):
            proj.collide()
            hero.collide(proj.damage)

    for proj in Player.projectiles:
        proj.move(screen.get_size(), timeDelta) #TODO
        melee_enemies_hit = pygame.sprite.spritecollide(proj, melee_enemies, False)
        range_enemies_hit = pygame.sprite.spritecollide(proj, ranged_enemies, False)

        for enemy in melee_enemies_hit:
            enemy.collide(proj.damage)
        for enemy in range_enemies_hit:
            enemy.collide(proj.damage)

        if melee_enemies_hit or range_enemies_hit:
            proj.collide()

def render_entities(hero, melee_enemies, ranged_enemies):
    hero.sprite.render(screen)
    for proj in Player.projectiles:
        proj.render(screen)
    for proj in Enemy.projectiles:
        proj.render(screen)
    for enemy in melee_enemies:
        enemy.render(screen)
    for enemy in ranged_enemies:
        enemy.render(screen)
    
def process_keys(keys, hero):
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        hero.sprite.movementVector[1] -= 1
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        hero.sprite.movementVector[0] -= 1
    if keys[pygame.K_s] or keys[pygame.K_RIGHT]:
        hero.sprite.movementVector[1] += 1
    if keys[pygame.K_d] or keys[pygame.K_DOWN]:
        hero.sprite.movementVector[0] += 1
    if keys[pygame.K_1]:
        hero.sprite.equippedWeapon = hero.sprite.availableWeapons[0]
    if keys[pygame.K_2]:
        hero.sprite.equippedWeapon = hero.sprite.availableWeapons[1]
    if keys[pygame.K_3]:
        hero.sprite.equippedWeapon = hero.sprite.availableWeapons[2]
        
def process_mouse(mouse, hero):
    if mouse[0] or keys[pygame.K_SPACE]:
        hero.sprite.shoot(pygame.mouse.get_pos())
 
def game_loop():
    done = False
    # hero = pygame.sprite.GroupSingle(Player(screen.get_size()))
    # enemies = pygame.sprite.Group()
    last_enemy_spawn = pygame.time.get_ticks()
    score = 0
    
    while hero.sprite.alive and not done:
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()
        currentTime = pygame.time.get_ticks()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
        screen.fill(BGCOLOR)
        
        process_keys(keys, hero)
        process_mouse(mouse, hero)
        
        # Enemy spawning process
        num_enemies = len(ranged_enemies) + len(melee_enemies)
        if last_enemy_spawn < currentTime - 200 and num_enemies < MAX_ENEMIES:
            
            enemy_name = EnemyFactory.get_random()

            spawn_side = random.random()
            pos = None
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
        
        move_entities(hero, melee_enemies, ranged_enemies, clock.get_time()/17)
        render_entities(hero, melee_enemies, ranged_enemies)
        
        # Health and score render

        #TODO RENDER HEALTH AND SCORE

        # for hp in range(hero.sprite.health):
        #     screen.blit(healthRender, (15 + hp*35, 0))

        score = hero.sprite.coins
        
        scoreRender = scoreFont.render(str(score), True, pygame.Color('black'))
        scoreRect = scoreRender.get_rect()
        scoreRect.right = size[0] - 20
        scoreRect.top = 20
        screen.blit(scoreRender, scoreRect)
        
        pygame.display.flip()
        clock.tick(120)

done = game_loop()
while not done:
    keys = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pressed()
    currentTime = pygame.time.get_ticks()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    
    if keys[pygame.K_r]:
        done = game_loop()
pygame.quit()
