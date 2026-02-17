import pygame,sys

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.running = True
        
        
        # Groups: หัวใจของการจัดการ Sprite ใน Pygame
        self.all_sprites = pygame.sprite.Group()

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        self.all_sprites.update() # Polymorphism: เรียก update ของทุกตัว

    def draw(self):
        self.screen.fill((30, 30, 30))
        self.all_sprites.draw(self.screen)
        pygame.display.flip()

    def run(self):
        while self.running :
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(60)


if __name__ == "__main__":
    game = Game()
    game.run()

