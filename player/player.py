from pygame import sprite, Surface
from pygame.math import Vector2


class Player(sprite.Sprite):
    def __init__(self, hp,stamina,pos):
        
        self.hp = hp
        self.stamina = stamina
        
        self.image = Surface((50, 50))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=pos)
    
    def move(self):
        
