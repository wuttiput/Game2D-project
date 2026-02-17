import pygame
import random
from pygame.math import Vector2

class Boss(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        
        # 1. ขนาดของ Boss (ขนาดใหญ่กว่าผู้เล่น)
        self.image = pygame.Surface((150, 200)) # กว้าง 150 สูง 200
        self.image.fill("purple") # สีม่วงให้ดูน่าเกรงขาม
        self.rect = self.image.get_rect(topleft = pos)
        
        # 2. ระบบฟิสิกส์
        self.pos = Vector2(self.rect.center)
        self.direction = Vector2(0, 0)
        self.speed = 2 # บอสตัวใหญ่จะเดินช้าลงหน่อยเพื่อให้ดูมีน้ำหนัก
        
        # 3. ระบบการเดินสุ่ม (Movement Timer)
        self.move_timer = 0
        self.move_duration = 1000 # จะสุ่มทิศทางใหม่ทุกๆ 1 วินาที (1000 ms)
        self.last_move_time = pygame.time.get_ticks()

    def get_random_direction(self):
        """ สุ่มทิศทาง 8 ทิศ หรือหยุดนิ่ง """
        choices = [(-1, 0), (1, 0), (0, -1), (0, 1),      # บน ล่าง ซ้าย ขวา
                   (-1, -1), (1, 1), (-1, 1), (1, -1),   # แนวทแยง
                   (0, 0)]                               # หยุดนิ่ง
        pick = random.choice(choices)
        self.direction = Vector2(pick)
        
        # ปรับความยาว vector ให้เท่ากับ 1 (ยกเว้นกรณีหยุดนิ่ง)
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

    def update_behavior(self):
        """ จัดการเรื่องเวลาในการเปลี่ยนทิศทาง """
        current_time = pygame.time.get_ticks()
        
        if current_time - self.last_move_time >= self.move_duration:
            self.get_random_direction()
            # สุ่มเวลาเดินครั้งต่อไป (เช่น 0.5 - 2 วินาที) เพื่อไม่ให้เดินเป็นจังหวะเกินไป
            self.move_duration = random.randint(500, 2000)
            self.last_move_time = current_time

    def move(self):
        # เคลื่อนที่ตามทิศทางที่สุ่มได้
        self.pos += self.direction * self.speed
        self.rect.center = self.pos

    def update(self):
        self.update_behavior()
        self.move()