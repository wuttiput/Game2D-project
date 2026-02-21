import pygame
from pygame.math import Vector2

class Boss(pygame.sprite.Sprite):
    # [เพิ่ม] รับตัวแปร player เข้ามา เพื่อให้บอสรู้ว่าต้องเดินไปทางไหน
    def __init__(self, pos, groups, player):
        super().__init__(groups)
        
        self.image = pygame.Surface((150, 200)) 
        self.image.fill("purple") 
        self.rect = self.image.get_rect(topleft = pos)
        
        self.player = player # เก็บข้อมูลผู้เล่นไว้ใช้อ้างอิง
        
        # ระบบฟิสิกส์ 2D (เหมือนของผู้เล่น)
        self.pos = Vector2(self.rect.center)
        self.direction = Vector2(0, 0)
        self.speed = 2 
        self.gravity = 0.5 
        self.ground_y = 250 # ระดับพื้น ต้องเท่ากับของผู้เล่น
        
        # ระบบการหันหน้าและโจมตี
        self.facing = 'left'
        self.attack_range = 150 # ระยะโจมตี (กว้างมาก เพราะบอสตัวใหญ่)
        self.is_attacking = False
        self.attack_cooldown = 2000 # ดีเลย์การโจมตี (2 วินาที)
        self.last_attack_time = 0

    def update_behavior(self):
        """ AI ของบอส: เดินตามและโจมตี """
        # ถ้ากำลังโจมตีอยู่ ให้ยืนนิ่งๆ
        if self.is_attacking:
            self.direction.x = 0
            return

        # คำนวณระยะห่างระหว่างบอสกับผู้เล่น (แกน X)
        distance_x = self.player.rect.centerx - self.rect.centerx
        
        # เช็คว่าผู้เล่นอยู่ในระยะโจมตีหรือไม่ (ใช้ abs เพื่อแปลงค่าติดลบเป็นบวก)
        if abs(distance_x) <= self.attack_range:
            self.attack() # เข้าใกล้แล้ว สั่งโจมตี!
        else:
            # ถ้ายังไม่ถึง ให้เดินตาม
            if distance_x > 0: # ผู้เล่นอยู่ทางขวา
                self.direction.x = 1
                self.facing = 'right'
            else:              # ผู้เล่นอยู่ทางซ้าย
                self.direction.x = -1
                self.facing = 'left'

    def attack(self):
        """ ฟังก์ชันสั่งโจมตี """
        current_time = pygame.time.get_ticks()
        # เช็ค Cooldown ว่าพร้อมฟันรอบต่อไปหรือยัง
        if current_time - self.last_attack_time >= self.attack_cooldown:
            self.is_attacking = True
            self.last_attack_time = current_time
            
            # [ตรงนี้คือจุดที่จะลดเลือดผู้เล่น]
            print("Boss โจมตีผู้เล่น! ตู้มมมม!")
            # สมมติว่าผู้เล่นมีฟังก์ชันรับดาเมจ: self.player.hp.take_damage(20)

    def cooldowns(self):
        """ ปลดล็อกสถานะการโจมตี """
        if self.is_attacking:
            current_time = pygame.time.get_ticks()
            # ให้บอสยืนนิ่งฟันค้างไว้ 0.5 วินาที (500 ms) แล้วค่อยเดินต่อ
            if current_time - self.last_attack_time >= 500:
                self.is_attacking = False

    def move(self):
        """ ระบบการเคลื่อนที่และแรงโน้มถ่วง """
        # แกน X (เดินซ้าย-ขวา)
        self.pos.x += self.direction.x * self.speed
        self.rect.centerx = self.pos.x
        
        # แกน Y (แรงโน้มถ่วง ดึงลงพื้น)
        self.direction.y += self.gravity 
        self.pos.y += self.direction.y
        self.rect.centery = self.pos.y
        
        # ชนพื้น (ตกพื้น)
        if self.rect.bottom >= self.ground_y:
            self.rect.bottom = self.ground_y
            self.pos.y = self.rect.centery
            self.direction.y = 0

    def update(self):
        self.update_behavior()
        self.cooldowns()
        self.move()