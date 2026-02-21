import pygame

class Health:
    def __init__(self, max_hp):
        self.max_hp = max_hp
        self.current_hp = max_hp
        
        # ระบบ i-frame (อมตะชั่วขณะหลังโดนตี)
        self.is_invincible = False
        self.invincibility_duration = 500  # 0.5 วินาที
        self.last_hit_time = 0

    def take_damage(self, amount):
        """เรียกใช้เมื่อตัวละครโดนโจมตี"""
        if not self.is_invincible:
            self.current_hp -= amount
            if self.current_hp < 0:
                self.current_hp = 0
            
            # เริ่มสถานะอมตะชั่วคราว
            self.is_invincible = True
            self.last_hit_time = pygame.time.get_ticks()
            return True # บอกว่าโดนดาเมจสำเร็จ
        return False # บอกว่าติดอมตะอยู่ ไม่โดนดาเมจ

    def update(self):
        """ต้องเรียกใน update loop เพื่อจัดการเวลาอมตะ"""
        current_time = pygame.time.get_ticks()
        if self.is_invincible:
            if current_time - self.last_hit_time >= self.invincibility_duration:
                self.is_invincible = False

    @property
    def ratio(self):
        """ส่งค่า 0.0 - 1.0 ให้เพื่อนที่ทำ UI ไปวาดหลอดเลือดได้ทันที"""
        return self.current_hp / self.max_hp

    @property
    def is_dead(self):
        """เช็คว่าตายหรือยัง"""
        return self.current_hp <= 0