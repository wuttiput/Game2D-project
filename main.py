import pygame, sys


class Button:
    def __init__(self, rect, text, font, bg=(70, 130, 180), fg=(255, 255, 255)):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.bg = bg
        self.fg = fg

    def draw(self, surface):
        pygame.draw.rect(surface, self.bg, self.rect, border_radius=6)
        txt = self.font.render(self.text, True, self.fg)
        txt_r = txt.get_rect(center=self.rect.center)
        surface.blit(txt, txt_r)

    def is_over(self, pos):
        return self.rect.collidepoint(pos)


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Stupid Boat")
        try:
            self.background = pygame.image.load("assets/background.jpg")
            self.background = pygame.transform.scale(self.background, (800, 600))
        except Exception:
            # fallback: solid color surface
            self.background = pygame.Surface((800, 600))
            self.background.fill((20, 20, 40))

        self.running = True
        
        # Groups: หัวใจของการจัดการ Sprite ใน Pygame
        self.all_sprites = pygame.sprite.Group()

        # Menu / settings state
        self.menu_active = True
        self.settings_active = False

        # Fonts
        self.title_font = pygame.font.SysFont(None, 64)
        self.btn_font = pygame.font.SysFont(None, 36)

        # Buttons (centered)
        btn_w, btn_h = 300, 60
        cx, cy = 400, 300
        gap = 80
        self.start_btn = Button((cx - btn_w // 2, cy - gap, btn_w, btn_h), "Start Game", self.btn_font)
        self.settings_btn = Button((cx - btn_w // 2, cy, btn_w, btn_h), "Settings", self.btn_font)
        self.exit_btn = Button((cx - btn_w // 2, cy + gap, btn_w, btn_h), "Exit Game", self.btn_font, bg=(200, 50, 50))

        # Settings back button
        self.back_btn = Button((20, 20, 120, 44), "Back", self.btn_font, bg=(100, 100, 100))

    def start_game(self):
        # Hide menu and start gameplay
        self.menu_active = False
        self.settings_active = False

    def open_settings(self):
        self.settings_active = True
        self.menu_active = False

    def exit_game(self):
        self.running = False

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # toggle menu from gameplay or close settings
                    if self.settings_active:
                        self.settings_active = False
                        self.menu_active = True
                    else:
                        self.menu_active = True

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = event.pos
                if self.menu_active and not self.settings_active:
                    if self.start_btn.is_over(pos):
                        self.start_game()
                    elif self.settings_btn.is_over(pos):
                        self.open_settings()
                    elif self.exit_btn.is_over(pos):
                        self.exit_game()

                elif self.settings_active:
                    if self.back_btn.is_over(pos):
                        self.settings_active = False
                        self.menu_active = True

    def update(self):
        if not self.menu_active and not self.settings_active:
            self.all_sprites.update()

    def draw_menu(self):
        # dim background
        self.screen.blit(self.background, (0, 0))
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        self.screen.blit(overlay, (0, 0))

        # title
        title = self.title_font.render("Stupid Boat", True, (255, 255, 255))
        tr = title.get_rect(center=(400, 150))
        self.screen.blit(title, tr)

        # buttons
        self.start_btn.draw(self.screen)
        self.settings_btn.draw(self.screen)
        self.exit_btn.draw(self.screen)

    def draw_settings(self):
        self.screen.blit(self.background, (0, 0))
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((10, 10, 10, 200))
        self.screen.blit(overlay, (0, 0))

        title = self.title_font.render("Settings", True, (255, 255, 255))
        tr = title.get_rect(center=(400, 120))
        self.screen.blit(title, tr)

        # simple placeholder setting text
        small = pygame.font.SysFont(None, 28)
        txt = small.render("(No settings yet)", True, (220, 220, 220))
        self.screen.blit(txt, (340, 200))

        # back button
        self.back_btn.draw(self.screen)

    def draw(self):
        if self.menu_active:
            if self.settings_active:
                self.draw_settings()
            else:
                self.draw_menu()
        else:
            # gameplay
            self.screen.blit(self.background, (0, 0))
            self.all_sprites.draw(self.screen)

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(60)


if __name__ == "__main__":
    game = Game()
    game.run()

