import pygame
from pygame import sprite, Surface
from pygame.math import Vector2
from .weapon import Weapon
from ..ui.hp import Health

class Player(sprite.Sprite):
    # [เพิ่ม] รับ groups ที่จะเอาไว้วาดอาวุธเข้ามาใน __init__ ด้วย
    def __init__(self, hp, stamina, pos, weapon_groups): 
        super().__init__() 
        
        self.image = Surface((50, 50))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=pos)
        
        self.pos = Vector2(pos)
        self.direction = Vector2(0,0)
        self.speed = 4
        
        self.gravity = 0.5
        self.ground_y = 250
        
        self.hp = Health(hp)
        self.stamina = stamina

        # [เพิ่ม] เก็บกลุ่มของอาวุธไว้ใช้ตอนสร้าง Weapon
        self.weapon_groups = weapon_groups 

        # [เพิ่ม] ตัวแปรจัดการสถานะการโจมตี (ป้องกันเกม Error ตอนเช็ค Cooldown)
        self.is_attacking = False
        self.attack_cooldown = 400 # ดีเลย์การฟัน (มิลลิวินาที)
        self.attack_time = 0
        
        self.facing = 'right'
        self.current_weapon = None

    def input(self):
        # [เพิ่ม] เช็คก่อนว่า "กำลังฟันอยู่หรือเปล่า" ถ้าฟันอยู่ ห้ามเดินห้ามกดซ้ำ!
        if not self.is_attacking:
            keys = pygame.key.get_pressed()
            mouse = pygame.mouse.get_pressed()
            
            # รับค่าปุ่มเดิน
            if keys[pygame.K_a] or keys[pygame.K_LEFT]: 
                self.direction.x = -1
            elif keys[pygame.K_d] or keys[pygame.K_RIGHT]: 
                self.direction.x = 1
            else: 
                self.direction.x = 0

            # [เพิ่ม] รับค่าปุ่มโจมตี (สมมติใช้ปุ่ม Spacebar)
            if mouse[0]:
                self.is_attacking = True
                self.attack_time = pygame.time.get_ticks() # บันทึกเวลาที่เริ่มฟัน
                self.direction = Vector2(0, 0) # [ทางเลือก] บังคับให้หยุดเดินตอนฟัน
                self.create_weapon()
    
    def create_weapon(self):
        # [แก้ไข] ดึงกลุ่มที่เราเตรียมไว้ใน __init__ มาใช้
        Weapon(self, self.weapon_groups) 

    def move(self):
        # 1. ขยับแกน X (ซ้าย-ขวา)
        self.pos.x += self.direction.x * self.speed
        self.rect.centerx = self.pos.x
        
        # 2. ขยับแกน Y (โดนดึงลงด้วยแรงโน้มถ่วง)
        self.direction.y += self.gravity 
        self.pos.y += self.direction.y
        self.rect.centery = self.pos.y
        
        # 3. ระบบชนพื้น (ไม่งั้นจะร่วงทะลุจอ)
        if self.rect.bottom >= self.ground_y:
            self.rect.bottom = self.ground_y # ดันให้เท้าแตะพื้นพอดี
            self.pos.y = self.rect.centery   # อัปเดต pos ให้ตรงกัน
            self.direction.y = 0             # หยุดความเร็วการร่วง
    
    # ในคลาส Player
    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if self.is_attacking:
            if current_time - self.attack_time > self.attack_cooldown:
                self.is_attacking = False
                # ไม่ต้องสั่ง self.current_weapon.kill() แล้ว ปล่อยให้ Weapon จัดการตัวเอง!

    def update(self):
        self.input()
        self.cooldowns()
        self.move()
        self.hp.update() 
        
        if self.hp.is_dead:
            print("Player is dead!")
            self.kill()