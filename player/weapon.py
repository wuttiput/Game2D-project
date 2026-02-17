import pygame
from pygame import sprite, Surface, rect
from pygame.math import Vector2

class Weapon(sprite.Sprite):
    def __init__(self, player, groups):
        super().__init__(groups)
        self.player = player
        
        # กำหนดขนาด Hitbox (เช่น ฟันไปข้างหน้า)
        self.image = Surface((40, 40)) 
        self.image.fill("yellow") # ลองใส่สีเหลืองให้เห็นชัดๆ ก่อน
        
        # วางตำแหน่ง Hitbox ให้อยู่หน้าตัวผู้เล่น
        self.rect = self.image.get_rect(midleft = player.rect.midright)
        
        self.spawn_time = pygame.time.get_ticks() # เวลาที่สร้าง Hitbox ขึ้นมา
        self.duration = 300 # ระยะเวลาที่ Hitbox จะอยู่ (มิลลิวินาที)

    def update(self):
        # ให้ Hitbox ติดตัวผู้เล่นไปตลอดเวลาที่ฟัน
        self.rect.midleft = self.player.rect.midright
        
        current_time = pygame.time.get_ticks()
        if current_time - self.spawn_time > self.duration:
            self.kill() # ลบ Hitbox ออกจากกลุ่มเมื่อหมดเวลา