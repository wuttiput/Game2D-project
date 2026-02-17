import pygame
from pygame import sprite, Surface, pygame
from pygame.math import Vector2
from .weapon import Weapon
from ..ui.hp import Health


class Player(sprite.Sprite):
    def __init__(self, hp, stamina, pos):
        # 1. เรียกใช้งาน Sprite พื้นฐาน (ต้องมี!)
        super().__init__() 
        
        # 2. ข้อมูลการแสดงผล
        self.image = Surface((50, 50))
        self.image.fill((255, 0, 0)) # สีแดง
        self.rect = self.image.get_rect(center=pos)
        
        # 3. ข้อมูลทางกายภาพ (Vector2 ช่วยให้เดินนุ่ม)
        self.pos = Vector2(pos)
        self.direction = Vector2(0,0)
        self.speed = 5
        
        # 4. ข้อมูลสถานะ (Stats)
        self.hp = Health(hp)
        self.stamina = stamina

    def input(self):
        # รับค่าปุ่มกด
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]: self.direction.y = -1
        elif keys[pygame.K_s]: self.direction.y = 1
        else: self.direction.y = 0

        if keys[pygame.K_a]: self.direction.x = -1
        elif keys[pygame.K_d]: self.direction.x = 1
        else: self.direction.x = 0
    
    def create_weapon(self, groups):
        Weapon(self, groups) # สร้างอาวุธใหม่ที่ตำแหน่งของผู้เล่น

    def move(self):
        # คำนวณตำแหน่งใหม่
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize() # เดินทแยงไม่ให้เร็วเกินไป
        
        self.pos += self.direction * self.speed
        self.rect.center = self.pos # อัปเดตตำแหน่งภาพให้ตรงกับตำแหน่งคำนวณ
    
    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if self.is_attacking:
            if current_time - self.attack_time > self.attack_cooldown:
                self.is_attacking = False

    def update(self):
        # ฟังก์ชันนี้จะถูกเรียกใช้โดยอัตโนมัติจาก self.all_sprites.update() ใน main.py
        self.input()
        self.move()
        self.cooldowns()
        self.hp.update() # อัปเดตสถานะเลือด (เช่น i-frame)
        
        if self.hp.is_dead:
            print("Player is dead!")
            self.kill() # ลบตัวผู้เล่นออกจากกลุ่มเมื่อ HP หมด