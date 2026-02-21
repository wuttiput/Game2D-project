import pygame, sys, json, os


SETTINGS_FILE = "settings.json"


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


class Slider:
    """แถบเลื่อนสำหรับปรับค่า 0.0 – 1.0"""
    def __init__(self, x, y, w, h, label, font, value=1.0):
        self.rect = pygame.Rect(x, y, w, h)
        self.label = label
        self.font = font
        self.value = value          # 0.0 – 1.0
        self.dragging = False
        self.knob_radius = h // 2 + 4
        self.track_color = (80, 80, 100)
        self.fill_color = (100, 200, 255)
        self.knob_color = (255, 255, 255)
        self.label_color = (220, 220, 220)

    @property
    def knob_x(self):
        return int(self.rect.x + self.value * self.rect.w)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            kx = self.knob_x
            ky = self.rect.centery
            # click on knob or on track
            if self.rect.inflate(0, 20).collidepoint(event.pos):
                self.dragging = True
                self._update_value(event.pos[0])
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self._update_value(event.pos[0])

    def _update_value(self, mx):
        self.value = max(0.0, min(1.0, (mx - self.rect.x) / self.rect.w))

    def draw(self, surface):
        # Label + percentage
        lbl = self.font.render(f"{self.label}: {int(self.value * 100)}%", True, self.label_color)
        surface.blit(lbl, (self.rect.x, self.rect.y - 28))

        # Track background
        pygame.draw.rect(surface, self.track_color, self.rect, border_radius=6)
        # Filled part
        fill_rect = pygame.Rect(self.rect.x, self.rect.y, int(self.value * self.rect.w), self.rect.h)
        pygame.draw.rect(surface, self.fill_color, fill_rect, border_radius=6)
        # Knob
        pygame.draw.circle(surface, self.knob_color, (self.knob_x, self.rect.centery), self.knob_radius)
        pygame.draw.circle(surface, self.fill_color, (self.knob_x, self.rect.centery), self.knob_radius - 3)


class FPSOption:
    """ปุ่มเลือก FPS แบบ radio"""
    def __init__(self, x, y, w, h, label, fps_value, font):
        self.rect = pygame.Rect(x, y, w, h)
        self.label = label
        self.fps_value = fps_value   # 0 = Unlimited
        self.font = font
        self.selected = False
        self.hover = False

    def draw(self, surface):
        if self.selected:
            bg = (100, 200, 255)
            fg = (10, 10, 30)
        elif self.hover:
            bg = (60, 70, 90)
            fg = (255, 255, 255)
        else:
            bg = (40, 45, 60)
            fg = (200, 200, 200)
        pygame.draw.rect(surface, bg, self.rect, border_radius=8)
        pygame.draw.rect(surface, (100, 200, 255) if self.selected else (80, 80, 100),
                         self.rect, 2, border_radius=8)
        txt = self.font.render(self.label, True, fg)
        surface.blit(txt, txt.get_rect(center=self.rect.center))

    def is_over(self, pos):
        return self.rect.collidepoint(pos)


class SettingsManager:
    """จัดการค่า settings ทั้งหมด + save/load JSON"""
    def __init__(self):
        self.master_volume = 1.0
        self.bgm_volume = 0.7
        self.sfx_volume = 0.8
        self.target_fps = 60
        self.load()

    def load(self):
        if os.path.exists(SETTINGS_FILE):
            try:
                with open(SETTINGS_FILE, "r") as f:
                    data = json.load(f)
                self.master_volume = data.get("master_volume", self.master_volume)
                self.bgm_volume = data.get("bgm_volume", self.bgm_volume)
                self.sfx_volume = data.get("sfx_volume", self.sfx_volume)
                self.target_fps = data.get("target_fps", self.target_fps)
            except Exception:
                pass

    def save(self):
        data = {
            "master_volume": round(self.master_volume, 2),
            "bgm_volume": round(self.bgm_volume, 2),
            "sfx_volume": round(self.sfx_volume, 2),
            "target_fps": self.target_fps,
        }
        with open(SETTINGS_FILE, "w") as f:
            json.dump(data, f, indent=2)

    def effective_bgm(self):
        return self.master_volume * self.bgm_volume

    def effective_sfx(self):
        return self.master_volume * self.sfx_volume


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()  # เริ่มต้นระบบเสียง
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

        # Settings manager (load/save JSON)
        self.settings = SettingsManager()

        # Fonts
        self.title_font = pygame.font.SysFont(None, 64)
        self.btn_font = pygame.font.SysFont(None, 36)
        self.small_font = pygame.font.SysFont(None, 28)
        self.section_font = pygame.font.SysFont(None, 40)

        # ── Menu buttons ──
        btn_w, btn_h = 300, 60
        cx, cy = 400, 300
        gap = 80
        self.start_btn = Button((cx - btn_w // 2, cy - gap, btn_w, btn_h), "Start Game", self.btn_font)
        self.settings_btn = Button((cx - btn_w // 2, cy, btn_w, btn_h), "Settings", self.btn_font)
        self.exit_btn = Button((cx - btn_w // 2, cy + gap, btn_w, btn_h), "Exit Game", self.btn_font, bg=(200, 50, 50))

        # ── Settings UI elements ──
        self.back_btn = Button((20, 20, 120, 44), "< Back", self.btn_font, bg=(80, 80, 100))

        slider_x, slider_w, slider_h = 250, 300, 12
        self.master_slider = Slider(slider_x, 210, slider_w, slider_h, "Master Volume",
                                    self.small_font, self.settings.master_volume)
        self.bgm_slider = Slider(slider_x, 280, slider_w, slider_h, "BGM Volume",
                                 self.small_font, self.settings.bgm_volume)
        self.sfx_slider = Slider(slider_x, 350, slider_w, slider_h, "SFX Volume",
                                 self.small_font, self.settings.sfx_volume)
        self.volume_sliders = [self.master_slider, self.bgm_slider, self.sfx_slider]

        # FPS options
        fps_choices = [("30 FPS", 30), ("60 FPS", 60), ("120 FPS", 120), ("Unlimited", 0)]
        opt_w, opt_h, opt_gap = 130, 44, 15
        total_w = len(fps_choices) * opt_w + (len(fps_choices) - 1) * opt_gap
        start_x = 400 - total_w // 2
        fy = 460
        self.fps_options = []
        for i, (label, val) in enumerate(fps_choices):
            opt = FPSOption(start_x + i * (opt_w + opt_gap), fy, opt_w, opt_h, label, val, self.small_font)
            if val == self.settings.target_fps:
                opt.selected = True
            self.fps_options.append(opt)

        # Apply loaded volume to mixer
        self._apply_volume()

    def start_game(self):
        # Hide menu and start gameplay
        self.menu_active = False
        self.settings_active = False

    def open_settings(self):
        self.settings_active = True
        self.menu_active = False

    def _apply_volume(self):
        """ปรับ volume ของ mixer ตามค่า settings ปัจจุบัน"""
        try:
            pygame.mixer.music.set_volume(self.settings.effective_bgm())
        except Exception:
            pass

    def _sync_settings_from_sliders(self):
        """อ่านค่า slider -> SettingsManager แล้ว apply"""
        self.settings.master_volume = self.master_slider.value
        self.settings.bgm_volume = self.bgm_slider.value
        self.settings.sfx_volume = self.sfx_slider.value
        self._apply_volume()

    def exit_game(self):
        self.running = False

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.settings_active:
                        # save & go back
                        self.settings.save()
                        self.settings_active = False
                        self.menu_active = True
                    else:
                        self.menu_active = True

            # ── Settings ต้องรับ event ก่อน (slider drag) ──
            if self.settings_active:
                for s in self.volume_sliders:
                    s.handle_event(event)
                self._sync_settings_from_sliders()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
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
                        self.settings.save()
                        self.settings_active = False
                        self.menu_active = True

                    # FPS option click
                    for opt in self.fps_options:
                        if opt.is_over(pos):
                            for o in self.fps_options:
                                o.selected = False
                            opt.selected = True
                            self.settings.target_fps = opt.fps_value

            # Hover effect for FPS options
            if event.type == pygame.MOUSEMOTION and self.settings_active:
                for opt in self.fps_options:
                    opt.hover = opt.is_over(event.pos)

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
        overlay.fill((10, 10, 10, 210))
        self.screen.blit(overlay, (0, 0))

        # ── Title ──
        title = self.title_font.render("Settings", True, (255, 255, 255))
        self.screen.blit(title, title.get_rect(center=(400, 80)))

        # ── Divider line ──
        pygame.draw.line(self.screen, (80, 80, 120), (100, 130), (700, 130), 2)

        # ── Section: Volume ──
        sec = self.section_font.render("Volume", True, (100, 200, 255))
        self.screen.blit(sec, (100, 150))
        for s in self.volume_sliders:
            s.draw(self.screen)

        # ── Divider ──
        pygame.draw.line(self.screen, (80, 80, 120), (100, 400), (700, 400), 2)

        # ── Section: FPS ──
        sec2 = self.section_font.render("Frame Rate (FPS)", True, (100, 200, 255))
        self.screen.blit(sec2, (100, 415))
        for opt in self.fps_options:
            opt.draw(self.screen)

        # ── Current FPS display ──
        actual_fps = self.clock.get_fps()
        fps_txt = self.small_font.render(f"Current: {actual_fps:.0f} FPS", True, (180, 255, 180))
        self.screen.blit(fps_txt, (350, 520))

        # ── Back button ──
        self.back_btn.draw(self.screen)

    def draw(self):
        if self.settings_active:
            self.draw_settings()
        elif self.menu_active:
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
            fps = self.settings.target_fps if self.settings.target_fps > 0 else 0
            self.clock.tick(fps)


if __name__ == "__main__":
    game = Game()
    game.run()

