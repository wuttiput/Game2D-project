import pygame
from pygame import sprite, Surface
from pygame.math import Vector2

class Weapon(sprite.Sprite):
    def __init__(self, player, groups):
        super().__init__(groups)
        self.player = player
        
        self.image = Surface((40, 40)) 
        self.image.fill("yellow") 
        
        # 1. เช็คว่าผู้เล่นหันไปทางไหนตอนสร้างอาวุธ
        if self.player.facing == 'right':
            self.rect = self.image.get_rect(midleft = player.rect.midright)
        else: # ถ้าหันซ้าย
            self.rect = self.image.get_rect(midright = player.rect.midleft)
            
        self.spawn_time = pygame.time.get_ticks() 
        self.duration = 300 

    def update(self):
        # 2. ให้อาวุธตามติดผู้เล่นให้ถูกด้านตลอดเวลาที่ฟัน
        if self.player.facing == 'right':
            self.rect.midleft = self.player.rect.midright
        else:
            self.rect.midright = self.player.rect.midleft
            
        current_time = pygame.time.get_ticks()
        if current_time - self.spawn_time > self.duration:
            self.kill()