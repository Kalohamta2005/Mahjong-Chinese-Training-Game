import pygame
import sys
import random
import math
import os
import json

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

GAME_DATA_DIR = os.path.join(BASE_DIR, "game_data")
SOUNDS_DIR = os.path.join(GAME_DATA_DIR, "sounds")
IMAGES_DIR = os.path.join(GAME_DATA_DIR, "images")

if not os.path.exists(GAME_DATA_DIR):
    os.makedirs(GAME_DATA_DIR, exist_ok=True)
    print(f"Создана папка game_data")

if not os.path.exists(SOUNDS_DIR):
    os.makedirs(SOUNDS_DIR, exist_ok=True)
    print(f"Создана папка game_data/sounds")

if not os.path.exists(IMAGES_DIR):
    os.makedirs(IMAGES_DIR, exist_ok=True)
    print(f"Создана папка game_data/images")


class SoundManager:

    def __init__(self):
        self.music_enabled = True
        self.sfx_enabled = True
        self.current_bgm = None
        self.victory_channel = None
        self.full_victory_channel = None

        self.bgm_paths = {
            'menu': os.path.join(SOUNDS_DIR, "Quiet Mahjong.mp3"),
            'game': os.path.join(SOUNDS_DIR, "Quiet Mahjong (1).mp3")
        }

        self.sfx_paths = {
            'tile_click': os.path.join(SOUNDS_DIR, "knock-on-the-cup (mp3cut.net).mp3"),
            'mismatch': os.path.join(SOUNDS_DIR, "sound-of-small-metal-parts-colliding.mp3"),
            'match': os.path.join(SOUNDS_DIR, "destructive-rock-throw-6.mp3"),
            'victory': os.path.join(SOUNDS_DIR, "勝局銅鑼 (mp3cut.net).mp3"),
            'full_victory': os.path.join(SOUNDS_DIR, "Bronze Gate Triumph (mp3cut.net).mp3"),
            'btn_click': os.path.join(SOUNDS_DIR, "metal-click4.mp3")
        }

        self.sounds = {}
        self.load_sounds()

    def load_sounds(self):
        for name, path in self.sfx_paths.items():
            try:
                sound = pygame.mixer.Sound(path)
                if name == 'tile_click':
                    sound.set_volume(1.0)
                self.sounds[name] = sound
            except Exception as e:
                print(f"Warning: Could not load sound '{name}' from path '{path}': {e}")
                self.sounds[name] = None

    def play_sfx(self, name):
        if not self.sfx_enabled:
            return None
        sound = self.sounds.get(name)
        if sound:
            try:
                return sound.play()
            except Exception as e:
                print(f"Error playing sound '{name}': {e}")
        return None

    def stop_all_bg_audio(self):
        pygame.mixer.music.stop()
        self.current_bgm = None
        if self.victory_channel:
            try:
                self.victory_channel.stop()
            except Exception:
                pass
            self.victory_channel = None
        if self.full_victory_channel:
            try:
                self.full_victory_channel.stop()
            except Exception:
                pass
            self.full_victory_channel = None

    def play_bgm(self, bgm_type, force_restart=False):
        if not force_restart and self.current_bgm == bgm_type and pygame.mixer.music.get_busy():
            return

        self.stop_all_bg_audio()

        if not self.music_enabled:
            return
        if bgm_type not in self.bgm_paths:
            return

        path = self.bgm_paths[bgm_type]
        try:
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(0.82)
            pygame.mixer.music.play(-1)
            self.current_bgm = bgm_type
        except Exception as e:
            print(f"Warning: Could not play music '{bgm_type}' from path '{path}': {e}")

    def stop_bgm(self):
        self.stop_all_bg_audio()

    def play_victory_sound(self):
        self.stop_all_bg_audio()
        if self.sfx_enabled:
            sound = self.sounds.get('victory')
            if sound:
                try:
                    self.victory_channel = sound.play()
                    return self.victory_channel
                except Exception as e:
                    print(f"Error playing victory sound: {e}")
        return None

    def is_victory_sound_playing(self):
        if self.victory_channel:
            return self.victory_channel.get_busy()
        return False

    def play_full_victory_sound(self):
        self.stop_all_bg_audio()
        if self.sfx_enabled:
            sound = self.sounds.get('full_victory')
            if sound:
                try:
                    self.full_victory_channel = sound.play()
                    return self.full_victory_channel
                except Exception as e:
                    print(f"Error playing full victory sound: {e}")
        return None

    def is_full_victory_sound_playing(self):
        if self.full_victory_channel:
            return self.full_victory_channel.get_busy()
        return False


pygame.init()
pygame.mixer.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
DARK_GRAY = (100, 100, 100)
BLUE = (70, 130, 180)
DARK_BLUE = (40, 90, 140)

SOFT_GREEN = (70, 150, 100)
DARK_SOFT_GREEN = (45, 105, 65)
POPUP_GREEN = (81, 151, 109)
GOLD_OUTLINE = (255, 215, 0)

GREEN = (60, 179, 113)
DARK_GREEN = (34, 139, 34)
DEEP_GREEN = (20, 80, 20)
RED = (205, 92, 92)
DARK_RED = (178, 34, 34)
GOLD_WIN = (255, 215, 0)
OVERLAY_COLOR = (0, 0, 0, 180)

BROWN_BASE = (139, 89, 44)
BROWN_HOVER = (119, 69, 24)
MODAL_BG = (71, 111, 70)
TITLE_COLOR = (99, 66, 49)
EXIT_BASE = (180, 180, 180)
EXIT_HOVER = (200, 80, 80)

TILE_LIGHT_BEVEL = (255, 255, 245)
TILE_DARK_BEVEL = (180, 170, 145)
TILE_PATTERN_RED = (200, 30, 30)
TILE_PATTERN_GREEN = (100, 180, 100)
TILE_TEXT_COLOR = (40, 40, 40)
TILE_SELECTED_BORDER = (255, 215, 0)

BROWN_STYLE = {
    'outer': (85, 52, 30),
    'inner': (124, 84, 55),
    'hover': (144, 104, 75)
}

GREY_STYLE = {
    'outer': (105, 107, 105),
    'inner': (159, 161, 160),
    'hover': (159, 161, 160)
}


def get_chinese_font(size):
    fonts = pygame.font.get_fonts()
    for f in ['microsoftyahei', 'simhei', 'simsun', 'msmincho', 'msgothic', 'arialunicodems']:
        if f in fonts:
            return pygame.font.SysFont(f, size, bold=True)
    return pygame.font.SysFont('arial', size, bold=True)


class Button:
    def __init__(self, x, y, width, height, text, font, base_color, hover_color, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.base_color = base_color
        self.hover_color = hover_color
        self.action = action

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        current_color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.base_color

        pygame.draw.rect(surface, current_color, self.rect, border_radius=10)
        pygame.draw.rect(surface, WHITE, self.rect, 2, border_radius=10)

        text_surf = self.font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def handle_event(self, event, sound_mgr=None):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if sound_mgr:
                    sound_mgr.play_sfx('btn_click')
                if self.action:
                    self.action()
                return True
        return False


class OvalButton:
    def __init__(self, x, y, width, height, text, font, base_color, hover_color, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.base_color = base_color
        self.hover_color = hover_color
        self.action = action

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        current_color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.base_color

        radius = self.rect.height // 2
        outer_rect = self.rect.inflate(12, 12)
        pygame.draw.rect(surface, (104, 64, 35), outer_rect, border_radius=radius + 6)
        pygame.draw.rect(surface, current_color, self.rect, border_radius=radius)
        pygame.draw.rect(surface, WHITE, self.rect, 3, border_radius=radius)

        text_surf = self.font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def handle_event(self, event, sound_mgr=None):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if sound_mgr:
                    sound_mgr.play_sfx('btn_click')
                if self.action:
                    self.action()
                return True
        return False


class VerticalButton:
    def __init__(self, x, y, width, height, text, font, style, action=None, active=True):
        self.rect = pygame.Rect(x, y, width, height)
        offset = 8
        self.outer_rect = pygame.Rect(x - offset, y - offset,
                                      width + offset * 2, height + offset * 2)
        self.text = text
        self.font = font
        self.action = action
        self.active = active
        self.set_style(style, active)

    def set_style(self, style, active=True):
        self.outer_color = style['outer']
        self.inner_color = style['inner']
        self.hover_color = style.get('hover', style['inner'])
        self.active = active

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        if self.active and self.rect.collidepoint(mouse_pos):
            current_inner = self.hover_color
        else:
            current_inner = self.inner_color

        pygame.draw.rect(surface, self.outer_color, self.outer_rect, border_radius=16)
        pygame.draw.rect(surface, current_inner, self.rect, border_radius=10)

        char_surfs = [self.font.render(char, True, WHITE) for char in self.text]
        total_height = sum(surf.get_height() for surf in char_surfs)

        start_y = self.rect.y + (self.rect.height - total_height) // 2
        current_y = start_y

        for surf in char_surfs:
            surf_rect = surf.get_rect(midtop=(self.rect.centerx, current_y))
            surface.blit(surf, surf_rect)
            current_y += surf.get_height()

    def handle_event(self, event, sound_mgr=None):
        if not self.active:
            return False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if sound_mgr:
                    sound_mgr.play_sfx('btn_click')
                if self.action:
                    self.action()
                return True
        return False


class Tile:
    def __init__(self, x, y, width, height, font, row, col, layer=0):
        self.logical_rect = pygame.Rect(x, y, width, height)
        self.font = font
        self.char = ""
        self.char_surf = None
        self.ru_value = ""
        self.en_value = ""

        self.row = row
        self.col = col
        self.layer = layer

        self.selected = False
        self.animating = False
        self.anim_start_time = 0
        self.anim_duration = 300

        self.highlighted = False
        self.highlight_start_time = 0

        self.scale = 1.0
        self.scale_target = 1.0
        self.scale_speed = 0.28

        if self.layer == 2:
            self.base_color = (250, 240, 215)
            self.hover_color = (235, 225, 200)
            self.y_offset = -8
        elif self.layer == 1:
            self.base_color = (230, 220, 195)
            self.hover_color = (215, 205, 180)
            self.y_offset = -4
        else:
            self.base_color = (210, 200, 175)
            self.hover_color = (195, 185, 160)
            self.y_offset = 0

        self.light_color = TILE_LIGHT_BEVEL
        self.dark_color = TILE_DARK_BEVEL

    def set_char(self, char, ru_val="", en_val=""):
        self.char = char
        self.ru_value = ru_val
        self.en_value = en_val
        if self.font:
            raw_surf = self.font.render(self.char, True, TILE_TEXT_COLOR)
            bbox = raw_surf.get_bounding_rect()
            if bbox.width > 0 and bbox.height > 0:
                self.char_surf = raw_surf.subsurface(bbox).copy()
            else:
                self.char_surf = raw_surf

    def start_disappear_animation(self):
        self.animating = True
        self.anim_start_time = pygame.time.get_ticks()

    def update(self):
        if abs(self.scale - self.scale_target) > 0.001:
            self.scale += (self.scale_target - self.scale) * self.scale_speed
        else:
            self.scale = self.scale_target

        if not self.animating:
            return False

        elapsed = pygame.time.get_ticks() - self.anim_start_time
        progress = elapsed / self.anim_duration
        return progress >= 1.0

    def get_visual_rect(self):
        cur_w = int(self.logical_rect.width * self.scale)
        cur_h = int(self.logical_rect.height * self.scale)
        draw_rect = pygame.Rect(0, 0, cur_w, cur_h)
        draw_rect.center = self.logical_rect.center
        return draw_rect

    def draw(self, surface):
        draw_rect = self.get_visual_rect()

        if self.animating:
            elapsed = pygame.time.get_ticks() - self.anim_start_time
            progress = elapsed / self.anim_duration
            alpha = max(0, int(255 * (1.0 - progress)))

            w = max(1, int(draw_rect.width * (1.0 - progress)))
            h = max(1, int(draw_rect.height * (1.0 - progress)))
            anim_rect = pygame.Rect(0, 0, w, h)
            anim_rect.center = self.logical_rect.center

            if anim_rect.width > 2 and anim_rect.height > 2:
                surf = pygame.Surface((anim_rect.width, anim_rect.height), pygame.SRCALPHA)
                pattern_col = TILE_PATTERN_GREEN if self.highlighted else TILE_PATTERN_RED
                pygame.draw.rect(surf, (*self.base_color, alpha), (0, 0, anim_rect.width, anim_rect.height))
                pygame.draw.rect(surf, (*pattern_col, alpha), (2, 2, anim_rect.width - 4, anim_rect.height - 4), 2)
                surface.blit(surf, (anim_rect.x, anim_rect.y + int(self.y_offset * self.scale)))
            return

        mouse_pos = pygame.mouse.get_pos()
        current_color = self.hover_color if self.logical_rect.collidepoint(mouse_pos) else self.base_color

        render_rect = draw_rect.copy()
        render_rect.y += int(self.y_offset * self.scale)

        x, y, w, h = render_rect
        t = max(2, int(w * 0.06))

        pygame.draw.rect(surface, current_color, render_rect)

        top_poly = [(x, y), (x + w, y), (x + w - t, y + t), (x + t, y + t)]
        left_poly = [(x, y), (x + t, y + t), (x + t, y + h - t), (x, y + h)]
        pygame.draw.polygon(surface, self.light_color, top_poly)
        pygame.draw.polygon(surface, self.light_color, left_poly)

        bottom_poly = [(x, y + h), (x + w, y + h), (x + w - t, y + h - t), (x + t, y + h - t)]
        right_poly = [(x + w, y), (x + w - t, y + t), (x + w - t, y + h - t), (x + w, y + h)]
        pygame.draw.polygon(surface, self.dark_color, bottom_poly)
        pygame.draw.polygon(surface, self.dark_color, right_poly)

        if self.highlighted:
            elapsed = pygame.time.get_ticks() - self.highlight_start_time
            pulse = (math.sin(elapsed * 0.005) + 1) / 2
            r = int(90 + 15 * pulse)
            g = int(170 + 20 * pulse)
            b = int(95 + 10 * pulse)
            pattern_color = (r, g, b)
            pygame.draw.rect(surface, pattern_color, render_rect.inflate(4, 4), 2, border_radius=4)
        else:
            pattern_color = TILE_PATTERN_RED

        extra_thick = 0
        pw = max(3, w // 6)
        outer_m = t + 2
        inner_m = t + pw - 2

        outer_rect = pygame.Rect(x + outer_m, y + outer_m, w - 2 * outer_m, h - 2 * outer_m)
        pygame.draw.rect(surface, pattern_color, outer_rect, max(1, w // 35) + extra_thick)

        inner_rect = pygame.Rect(x + inner_m, y + inner_m, w - 2 * inner_m, h - 2 * inner_m)
        pygame.draw.rect(surface, pattern_color, inner_rect, max(1, w // 70) + extra_thick)

        line_w = max(1, w // 35) + extra_thick
        pygame.draw.line(surface, pattern_color, (x + outer_m, y + outer_m), (x + inner_m, y + inner_m), line_w)
        pygame.draw.line(surface, pattern_color, (x + w - outer_m, y + outer_m), (x + w - inner_m, y + inner_m), line_w)
        pygame.draw.line(surface, pattern_color, (x + outer_m, y + h - outer_m), (x + inner_m, y + h - inner_m), line_w)
        pygame.draw.line(surface, pattern_color, (x + w - outer_m, y + h - outer_m), (x + w - inner_m, y + h - inner_m), line_w)

        if self.char_surf:
            offset_x = 0
            offset_y = 0
            if self.char in ("牜", "犭", "⻊"):
                offset_x = int(w * 0.05)
            elif self.char in ("⺮", "宀"):
                offset_y = int(h * 0.05)

            char_center = (render_rect.centerx + offset_x, render_rect.centery + offset_y)

            if abs(self.scale - 1.0) > 0.01:
                sw = max(1, int(self.char_surf.get_width() * self.scale))
                sh = max(1, int(self.char_surf.get_height() * self.scale))
                scaled_char = pygame.transform.smoothscale(self.char_surf, (sw, sh))
                char_rect = scaled_char.get_rect(center=char_center)
                surface.blit(scaled_char, char_rect)
            else:
                char_rect = self.char_surf.get_rect(center=char_center)
                surface.blit(self.char_surf, char_rect)

        border_color = TILE_SELECTED_BORDER if self.selected else BLACK
        border_width = 3 if self.selected else 1
        pygame.draw.rect(surface, border_color, render_rect, border_width)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.logical_rect.collidepoint(event.pos) and not self.animating:
                return True
        return False


class ProgressMenu:
    def __init__(self, sw, sh, fonts, close_action, app):
        self.sw = sw
        self.sh = sh
        self.w, self.h = int(sw * 0.8), int(sh * 0.85)
        self.rect = pygame.Rect(0, 0, self.w, self.h)
        self.rect.center = (sw // 2, sh // 2)
        self.fonts = fonts
        self.app = app

        btn_w, btn_h = int(self.w * 0.25), int(self.h * 0.08)
        self.close_btn = Button(self.rect.centerx - btn_w // 2, self.rect.bottom - btn_h - 20,
                                btn_w, btn_h, "", fonts['medium'], RED, DARK_RED, close_action)

        self.scroll_y = 0
        self.list_w = int(self.w * 0.9)
        self.list_h = int(self.h * 0.65)
        self.list_rect = pygame.Rect(self.rect.centerx - self.list_w // 2, self.rect.top + int(self.h * 0.15),
                                     self.list_w, self.list_h)

        self.char_font = get_chinese_font(int(sh * 0.05))
        self.update_language()

    def update_language(self):
        tr = self.app.translations[self.app.language]
        self.close_btn.text = tr["close"]

    def draw(self, surface):
        pygame.draw.rect(surface, MODAL_BG, self.rect, border_radius=15)
        pygame.draw.rect(surface, BLACK, self.rect, 3, border_radius=15)

        tr = self.app.translations[self.app.language]
        title_surf = self.fonts['medium'].render(tr["progress_title"], True, WHITE)
        title_rect = title_surf.get_rect(center=(self.rect.centerx, self.rect.top + int(self.h * 0.08)))
        surface.blit(title_surf, title_rect)

        items = list(self.app.progress.items())
        sorted_prog = sorted(items, key=lambda x: (-x[1], self.app.chars_list.index(x[0])))

        row_h = int(self.sh * 0.08)
        max_scroll = max(0, len(sorted_prog) * row_h - self.list_h)
        self.scroll_y = min(0, max(-max_scroll, self.scroll_y))

        list_surf = pygame.Surface((self.list_w, self.list_h))
        list_surf.fill(MODAL_BG)

        for i, (char, val) in enumerate(sorted_prog):
            y = i * row_h + self.scroll_y
            if y + row_h < 0 or y > self.list_h:
                continue

            char_s = self.char_font.render(char, True, WHITE)
            list_surf.blit(char_s, (40, y + (row_h - char_s.get_height()) // 2))

            bar_w = int(self.list_w * 0.6)
            bar_h = int(row_h * 0.4)
            bar_x = int(self.list_w * 0.2)
            bar_y = y + (row_h - bar_h) // 2

            pygame.draw.rect(list_surf, (85, 52, 30), (bar_x, bar_y, bar_w, bar_h), border_radius=6)

            fill_w = int(bar_w * (val / 50.0))
            if fill_w > 0:
                pygame.draw.rect(list_surf, (245, 245, 220), (bar_x, bar_y, fill_w, bar_h), border_radius=6)

            text_s = self.fonts['medium'].render(f"{val}/50", True, WHITE)
            list_surf.blit(text_s, (bar_x + bar_w + 20, y + (row_h - text_s.get_height()) // 2))

        surface.blit(list_surf, self.list_rect)
        pygame.draw.rect(surface, WHITE, self.list_rect, 2)

        self.close_btn.draw(surface)

    def handle_event(self, event, sound_mgr=None):
        if event.type == pygame.MOUSEWHEEL:
            self.scroll_y += event.y * 30
        self.close_btn.handle_event(event, sound_mgr)


class SettingsMenu:
    def __init__(self, sw, sh, fonts, close_action, sound_mgr, app):
        w, h = int(sw * 0.6), int(sh * 0.7)
        self.rect = pygame.Rect(0, 0, w, h)
        self.rect.center = (sw // 2, sh // 2)
        self.fonts = fonts
        self.sound_mgr = sound_mgr
        self.app = app

        self.confirming_clear = False

        cx = self.rect.centerx
        btn_w = int(w * 0.55)
        btn_h = int(h * 0.1)
        lang_btn_w = int(w * 0.25)

        y_music = self.rect.top + h * 0.2
        y_sfx = self.rect.top + h * 0.35
        y_lang_btns = self.rect.top + h * 0.57
        y_clear = self.rect.top + h * 0.72
        y_close = self.rect.bottom - btn_h - int(h * 0.05)

        self.btn_music = Button(cx - btn_w // 2, y_music, btn_w, btn_h, "", fonts['medium'], BLUE, DARK_BLUE, self.toggle_music)
        self.btn_sfx = Button(cx - btn_w // 2, y_sfx, btn_w, btn_h, "", fonts['medium'], BLUE, DARK_BLUE, self.toggle_sfx)

        self.btn_lang_en = Button(cx - lang_btn_w - 10, y_lang_btns, lang_btn_w, btn_h, "", fonts['medium'], GRAY, DARK_GRAY, lambda: self.set_lang("en"))
        self.btn_lang_ru = Button(cx + 10, y_lang_btns, lang_btn_w, btn_h, "", fonts['medium'], GRAY, DARK_GRAY, lambda: self.set_lang("ru"))

        self.btn_clear = Button(cx - btn_w // 2, y_clear, btn_w, btn_h, "", fonts['medium'], RED, DARK_RED, self.ask_clear)
        self.btn_close = Button(cx - btn_w // 2, y_close, btn_w, btn_h, "", fonts['medium'], BLUE, DARK_BLUE, close_action)

        self.btn_yes = Button(cx - lang_btn_w - 10, self.rect.centery + 20, lang_btn_w, btn_h, "", fonts['medium'], RED, DARK_RED, self.confirm_clear)
        self.btn_no = Button(cx + 10, self.rect.centery + 20, lang_btn_w, btn_h, "", fonts['medium'], GREEN, DARK_GREEN, self.cancel_clear)

        self.update_language()

    def update_language(self):
        tr = self.app.translations[self.app.language]
        self.btn_music.text = tr["music_on"] if self.sound_mgr.music_enabled else tr["music_off"]
        self.btn_sfx.text = tr["sfx_on"] if self.sound_mgr.sfx_enabled else tr["sfx_off"]
        self.btn_lang_en.text = tr["english"]
        self.btn_lang_ru.text = tr["russian"]
        self.btn_clear.text = tr["clear_progress"]
        self.btn_close.text = tr["close"]
        self.btn_yes.text = tr["yes"]
        self.btn_no.text = tr["no"]

    def toggle_music(self):
        self.sound_mgr.music_enabled = not self.sound_mgr.music_enabled
        tr = self.app.translations[self.app.language]
        if self.sound_mgr.music_enabled:
            self.sound_mgr.play_bgm('menu')
            self.btn_music.text = tr["music_on"]
        else:
            self.sound_mgr.stop_bgm()
            self.btn_music.text = tr["music_off"]

    def toggle_sfx(self):
        self.sound_mgr.sfx_enabled = not self.sound_mgr.sfx_enabled
        tr = self.app.translations[self.app.language]
        self.btn_sfx.text = tr["sfx_on"] if self.sound_mgr.sfx_enabled else tr["sfx_off"]

    def set_lang(self, lang):
        self.app.language = lang
        self.app.save_progress()
        self.app.update_language()

    def ask_clear(self):
        self.confirming_clear = True

    def confirm_clear(self):
        self.confirming_clear = False
        if hasattr(self, 'app'):
            for char in self.app.progress:
                self.app.progress[char] = 0
            self.app.save_progress()
            self.app.state = 'MAIN_MENU'

    def cancel_clear(self):
        self.confirming_clear = False

    def draw(self, surface):
        pygame.draw.rect(surface, MODAL_BG, self.rect, border_radius=15)
        pygame.draw.rect(surface, BLACK, self.rect, 3, border_radius=15)

        tr = self.app.translations[self.app.language]

        if not self.confirming_clear:
            title_surf = self.fonts['large'].render(tr["settings"], True, WHITE)
            title_rect = title_surf.get_rect(center=(self.rect.centerx, self.rect.top + self.rect.height * 0.1))
            surface.blit(title_surf, title_rect)

            self.btn_music.draw(surface)
            self.btn_sfx.draw(surface)

            lang_surf = self.fonts['small'].render(tr["language"], True, WHITE)
            lang_rect = lang_surf.get_rect(center=(self.rect.centerx, self.rect.top + self.rect.height * 0.52))
            surface.blit(lang_surf, lang_rect)

            if self.app.language == "en":
                self.btn_lang_en.base_color = DARK_GRAY
                self.btn_lang_ru.base_color = GRAY
            else:
                self.btn_lang_en.base_color = GRAY
                self.btn_lang_ru.base_color = DARK_GRAY

            self.btn_lang_en.draw(surface)
            self.btn_lang_ru.draw(surface)
            self.btn_clear.draw(surface)
            self.btn_close.draw(surface)
        else:
            warn_title = self.fonts['large'].render(tr["clear_confirm"], True, RED)
            warn_rect = warn_title.get_rect(center=(self.rect.centerx, self.rect.top + self.rect.height * 0.3))
            surface.blit(warn_title, warn_rect)

            warn_txt = self.fonts['small'].render(tr["clear_confirm_sub"], True, WHITE)
            txt_rect = warn_txt.get_rect(center=(self.rect.centerx, self.rect.top + self.rect.height * 0.45))
            surface.blit(warn_txt, txt_rect)

            self.btn_yes.draw(surface)
            self.btn_no.draw(surface)

    def handle_event(self, event, sound_mgr=None):
        if not self.confirming_clear:
            self.btn_music.handle_event(event, sound_mgr)
            self.btn_sfx.handle_event(event, sound_mgr)
            self.btn_lang_en.handle_event(event, sound_mgr)
            self.btn_lang_ru.handle_event(event, sound_mgr)
            self.btn_clear.handle_event(event, sound_mgr)
            self.btn_close.handle_event(event, sound_mgr)
        else:
            self.btn_yes.handle_event(event, sound_mgr)
            self.btn_no.handle_event(event, sound_mgr)


def is_tile_available_in_list(tile, tile_list):
    has_left = False
    has_right = False

    for t in tile_list:
        if t == tile:
            continue

        if t.layer == tile.layer and t.row == tile.row:
            if t.col == tile.col - 1:
                has_left = True
            elif t.col == tile.col + 1:
                has_right = True

        if t.layer > tile.layer:
            if t.logical_rect.colliderect(tile.logical_rect):
                return False

    return not (has_left and has_right)


class GameApp:
    def __init__(self):
        infoObject = pygame.display.Info()
        self.sw = infoObject.current_w
        self.sh = infoObject.current_h
        self.screen = pygame.display.set_mode((self.sw, self.sh), pygame.FULLSCREEN)
        pygame.display.set_caption("Mahjong: Chinese Training Game")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'MAIN_MENU'

        self.sound_mgr = SoundManager()
        self.language = "en"

        self.translations = {
            "en": {
                "start": "Start",
                "settings": "Settings",
                "music_on": "Music: ON",
                "music_off": "Music: OFF",
                "sfx_on": "SFX: ON",
                "sfx_off": "SFX: OFF",
                "language": "Language:",
                "russian": "Russian",
                "english": "English",
                "clear_progress": "Clear Progress",
                "clear_confirm": "Are you sure?",
                "clear_confirm_sub": "This will permanently delete your progress.",
                "yes": "Yes",
                "no": "No",
                "close": "Close",
                "my_progress": "My progress",
                "progress_title": "SEMANTIC COMPONENTS OF CHINESE CHARACTERS",
                "back": "Back",
                "hint": "HINT",
                "restart": "RESTART",
                "victory_text": "Congratulations on\nyet another\nsmall victory",
                "continue_training": "Continue training",
                "full_victory_title": "Congratulations!",
                "full_victory_text": "You have mastered all semantic components!",
                "max_progress_message": "Game is already fully completed. You are great!\nTo continue playing, reset progress in Settings."
            },
            "ru": {
                "start": "Начать",
                "settings": "Настройки",
                "music_on": "Музыка: ВКЛ",
                "music_off": "Музыка: ВЫКЛ",
                "sfx_on": "Звуки: ВКЛ",
                "sfx_off": "Звуки: ВЫКЛ",
                "language": "Язык:",
                "russian": "Русский",
                "english": "Английский",
                "clear_progress": "Сбросить прогресс",
                "clear_confirm": "Вы уверены?",
                "clear_confirm_sub": "Это навсегда удалит ваш прогресс.",
                "yes": "Да",
                "no": "Нет",
                "close": "Закрыть",
                "my_progress": "Мой прогресс",
                "progress_title": "СМЫСЛОВЫЕ КОМПОНЕНТЫ КИТАЙСКИХ ИЕРОГЛИФОВ",
                "back": "Назад",
                "hint": "ПОДСКАЗКА",
                "restart": "ПЕРЕЗАПУСК",
                "victory_text": "Поздравляем с\nещё одной\nмаленькой победой",
                "continue_training": "Продолжить тренировку",
                "full_victory_title": "Поздравляем!",
                "full_victory_text": "Вы освоили все смысловые компоненты!",
                "max_progress_message": "Игра уже пройдена. Вы молодец!\nЧтобы продолжить играть, сбросьте прогресс в Настройках."
            }
        }

        self.selected_tile = None
        self.animating_tiles = []
        self.pending_match = None
        self.game_won = False
        self.victory_sound_started = False

        self.full_victory_start_time = 0
        self.full_victory_sound_started = False

        self.max_progress_msg_active = False
        self.max_progress_msg_start_time = 0

        self.display_text = None
        self.display_start_time = 0
        self.display_duration = 1800

        self.char_dict = {
            "口": {"ru": "РОТ", "en": "MOUTH"}, "亻": {"ru": "ЧЕЛОВЕК", "en": "PERSON"}, "木": {"ru": "ДЕРЕВО", "en": "TREE"},
            "氵": {"ru": "ВОДА", "en": "WATER"}, "氺": {"ru": "ВОДА", "en": "WATER"}, "扌": {"ru": "РУКА", "en": "HAND"},
            "忄": {"ru": "СЕРДЦЕ", "en": "HEART"}, "⺗": {"ru": "СЕРДЦЕ", "en": "HEART"}, "灬": {"ru": "ОГОНЬ", "en": "FIRE"},
            "钅": {"ru": "МЕТАЛЛ", "en": "METAL"}, "日": {"ru": "СОЛНЦЕ", "en": "SUN"}, "月": {"ru": "ЛУНА", "en": "MOON"},
            "艹": {"ru": "ТРАВА", "en": "GRASS"}, "纟": {"ru": "ШЁЛК", "en": "SILK"}, "讠": {"ru": "РЕЧЬ", "en": "SPEECH"},
            "辶": {"ru": "ДВИЖЕНИЕ", "en": "MOVEMENT"}, "女": {"ru": "ЖЕНЩИНА", "en": "WOMAN"}, "子": {"ru": "РЕБЁНОК", "en": "CHILD"},
            "大": {"ru": "БОЛЬШОЙ", "en": "BIG"}, "小": {"ru": "МАЛЕНЬКИЙ", "en": "SMALL"}, "山": {"ru": "ГОРА", "en": "MOUNTAIN"},
            "石": {"ru": "КАМЕНЬ", "en": "STONE"}, "目": {"ru": "ГЛАЗ", "en": "EYE"}, "田": {"ru": "ПОЛЕ", "en": "FIELD"},
            "力": {"ru": "СИЛА", "en": "STRENGTH"}, "刀": {"ru": "НОЖ", "en": "KNIFE"}, "广": {"ru": "ШИРОКИЙ", "en": "WIDE"},
            "门": {"ru": "ДВЕРЬ", "en": "DOOR"}, "饣": {"ru": "ЕДА", "en": "FOOD"}, "衤": {"ru": "ОДЕЖДА", "en": "CLOTHING"},
            "车": {"ru": "МАШИНА", "en": "VEHICLE"}, "贝": {"ru": "РАКУШКА", "en": "SHELL"}, "页": {"ru": "СТРАНИЦА", "en": "PAGE"},
            "马": {"ru": "ЛОШАДЬ", "en": "HORSE"}, "鱼": {"ru": "РЫБА", "en": "FISH"}, "鸟": {"ru": "ПТИЦА", "en": "BIRD"},
            "虫": {"ru": "НАСЕКОМОЕ", "en": "INSECT"}, "米": {"ru": "РИС", "en": "RICE"}, "⻗": {"ru": "ДОЖДЬ", "en": "RAIN"},
            "一": {"ru": "ОДИН", "en": "ONE"}, "二": {"ru": "ДВА", "en": "TWO"}, "三": {"ru": "ТРИ", "en": "THREE"},
            "父": {"ru": "ОТЕЦ", "en": "FATHER"}, "母": {"ru": "МАТЬ", "en": "MOTHER"}, "土": {"ru": "ЗЕМЛЯ", "en": "EARTH"},
            "禾": {"ru": "РОСТОК", "en": "GRAIN"}, "⺮": {"ru": "БАМБУК", "en": "BAMBOO"}, "牜": {"ru": "КОРОВА", "en": "COW"},
            "犭": {"ru": "СОБАКА", "en": "DOG"}, "⻊": {"ru": "НОГА", "en": "FOOT"}, "耳": {"ru": "УХО", "en": "EAR"},
            "巾": {"ru": "ТКАНЬ", "en": "CLOTH"}, "户": {"ru": "ДВЕРЬ", "en": "DOOR"}, "宀": {"ru": "КРЫША", "en": "ROOF"},
            "穴": {"ru": "ПЕЩЕРА", "en": "CAVE"}, "走": {"ru": "ИДТИ", "en": "WALK"}, "戈": {"ru": "ОРУЖИЕ", "en": "WEAPON"},
            "风": {"ru": "ВЕТЕР", "en": "WIND"}, "鬼": {"ru": "ПРИЗРАК", "en": "GHOST"}
        }

        self.chars_list = list(self.char_dict.keys())
        self.progress = {char: 0 for char in self.chars_list}

        self.load_progress()

        self.fonts = {
            'title': pygame.font.SysFont('arial', int(self.sw / 25), bold=True),
            'win': pygame.font.SysFont('arial', int(self.sh * 0.06), bold=True),
            'large': pygame.font.SysFont('arial', int(self.sw / 35), bold=True),
            'medium': pygame.font.SysFont('arial', int(self.sw / 50), bold=True),
            'small': pygame.font.SysFont('arial', int(self.sw / 70)),
            'popup': pygame.font.SysFont('arial', int(self.sh / 8), bold=True)
        }

        try:
            bg_path = os.path.join(IMAGES_DIR, "Chinese Art Background (1)_обр.png")
            self.bg_image = pygame.image.load(bg_path).convert()
            self.bg_image = pygame.transform.scale(self.bg_image, (self.sw, self.sh))
        except Exception:
            self.bg_image = None

        try:
            game_bg_path = os.path.join(IMAGES_DIR, "Фон_игра.png")
            self.game_bg_image = pygame.image.load(game_bg_path).convert()
            self.game_bg_image = pygame.transform.scale(self.game_bg_image, (self.sw, self.sh))
        except Exception:
            self.game_bg_image = None

        btn_w = int(self.sw * 0.20)
        btn_h = int(self.sh * 0.08)
        start_w = int(btn_w * 1.5)
        start_h = int(btn_h * 1.5)

        exit_size = int(self.sw * 0.03)
        self.btn_exit = Button(self.sw - exit_size - 20, 20, exit_size, exit_size,
                               "X", self.fonts['medium'], EXIT_BASE, EXIT_HOVER, self.quit_game)

        back_w = int(self.sw * 0.1)
        back_h = int(self.sh * 0.06)
        self.btn_back = Button(20, 20, back_w, back_h, "", self.fonts['medium'], GRAY, DARK_GRAY, self.back_to_main)

        cx = self.sw // 2
        self.btn_start = Button(cx - start_w // 2, int(self.sh * 0.35), start_w, start_h,
                                "", self.fonts['large'], SOFT_GREEN, DARK_SOFT_GREEN, self.start_game)
        self.btn_settings = Button(cx - btn_w // 2, int(self.sh * 0.60), btn_w, btn_h,
                                   "", self.fonts['medium'], BROWN_BASE, BROWN_HOVER, self.open_settings)
        self.btn_progress = Button(cx - btn_w // 2, int(self.sh * 0.72), btn_w, btn_h,
                                   "", self.fonts['medium'], BROWN_BASE, BROWN_HOVER, self.open_progress)

        self.side_btn_w = int(self.sw * 0.08)
        self.side_btn_h = int(self.sh * 0.25)
        hint_x = self.sw - int(self.sw * 0.10) - self.side_btn_w
        restart_x = int(self.sw * 0.10)
        side_btn_y = (self.sh - self.side_btn_h) // 2

        self.fonts['vertical'] = pygame.font.SysFont('arial', 20, bold=True)

        self.btn_hint = VerticalButton(hint_x, side_btn_y, self.side_btn_w, self.side_btn_h, "",
                                       self.fonts['vertical'], BROWN_STYLE, self.hint_action, active=True)
        self.btn_restart = VerticalButton(restart_x, side_btn_y, self.side_btn_w, self.side_btn_h, "",
                                          self.fonts['vertical'], GREY_STYLE, self.restart_action, active=False)

        cont_w = int(self.sw * 0.4)
        cont_h = int(self.sh * 0.25)
        self.btn_continue = OvalButton((self.sw - cont_w) // 2, (self.sh - cont_h) // 2, cont_w, cont_h,
                                       "", self.fonts['large'], (124, 84, 55), (144, 104, 75),
                                       self.continue_training_action)

        self.progress_menu = ProgressMenu(self.sw, self.sh, self.fonts, self.close_modals, self)
        self.settings_menu = SettingsMenu(self.sw, self.sh, self.fonts, self.close_modals, self.sound_mgr, self)

        self.update_language()

        self.overlay = pygame.Surface((self.sw, self.sh), pygame.SRCALPHA)
        self.overlay.fill(OVERLAY_COLOR)

        self.tiles = []

    def update_language(self):
        tr = self.translations[self.language]

        self.btn_back.text = tr["back"]
        self.btn_start.text = tr["start"]
        self.btn_settings.text = tr["settings"]
        self.btn_progress.text = tr["my_progress"]
        self.btn_continue.text = tr["continue_training"]
        self.btn_hint.text = tr["hint"]
        self.btn_restart.text = tr["restart"]

        vert_font_size = int(
            min(self.side_btn_w * 0.6, (self.side_btn_h * 0.9) / max(len(tr["hint"]), len(tr["restart"]))))
        new_vert_font = pygame.font.SysFont('arial', vert_font_size, bold=True)
        self.btn_hint.font = new_vert_font
        self.btn_restart.font = new_vert_font

        if hasattr(self, 'settings_menu'):
            self.settings_menu.update_language()
        if hasattr(self, 'progress_menu'):
            self.progress_menu.update_language()

    def check_all_max_progress(self):
        return all(val >= 50 for val in self.progress.values())

    def trigger_full_victory(self):
        self.state = 'FULL_VICTORY'
        self.full_victory_start_time = pygame.time.get_ticks()
        self.sound_mgr.play_full_victory_sound()
        self.full_victory_sound_started = True

    def load_progress(self):
        save_file = os.path.join(GAME_DATA_DIR, "progress.json")

        if os.path.exists(save_file):
            try:
                with open(save_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.language = data.get("language", "en")
                    for char, val in data.items():
                        if char in self.progress:
                            self.progress[char] = min(50, max(0, int(val)))
            except Exception as e:
                print(f"Failed to load progress: {e}")
        else:
            print("Файл сохранения не найден — создан новый")
            self.save_progress()

    def save_progress(self):
        if not os.path.exists(GAME_DATA_DIR):
            os.makedirs(GAME_DATA_DIR, exist_ok=True)
            print(f"Создана папка {GAME_DATA_DIR}")

        save_file = os.path.join(GAME_DATA_DIR, "progress.json")
        try:
            data_to_save = self.progress.copy()
            data_to_save["language"] = self.language
            with open(save_file, 'w', encoding='utf-8') as f:
                json.dump(data_to_save, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Failed to save progress: {e}")

    def is_tile_available(self, tile):
        return is_tile_available_in_list(tile, self.tiles)

    def is_board_solvable(self, tile_list):
        temp_tiles = []
        for t in tile_list:
            dummy = Tile(t.logical_rect.x, t.logical_rect.y, t.logical_rect.width, t.logical_rect.height, None, t.row,
                         t.col, t.layer)
            dummy.char = t.char
            temp_tiles.append(dummy)

        while len(temp_tiles) > 0:
            free_tiles = [t for t in temp_tiles if is_tile_available_in_list(t, temp_tiles)]

            match_pair = None
            for i in range(len(free_tiles)):
                for j in range(i + 1, len(free_tiles)):
                    if free_tiles[i].char == free_tiles[j].char:
                        match_pair = (free_tiles[i], free_tiles[j])
                        break
                if match_pair:
                    break

            if not match_pair:
                return False

            temp_tiles.remove(match_pair[0])
            temp_tiles.remove(match_pair[1])

        return True

    def create_tiles(self):
        layers_config = [
            (6, 5),
            (6, 4),
            (6, 3)
        ]

        total_tiles = sum(r * c for r, c in layers_config)
        num_pairs = total_tiles // 2
        gap = 2
        max_rows = 6

        available_height = self.sh * 0.82
        tile_h = int((available_height - (max_rows - 1) * gap) / max_rows)
        tile_w = int(tile_h * 11 / 13)

        dice_font_size = int(tile_h * 0.45)
        tile_font = get_chinese_font(dice_font_size)

        while True:
            selected_chars = random.choices(self.chars_list, k=num_pairs)
            game_chars_pool = []
            for char in selected_chars:
                game_chars_pool.extend([char, char])
            random.shuffle(game_chars_pool)

            candidate_tiles = []
            char_idx = 0

            for layer_idx, (rows, cols) in enumerate(layers_config):
                grid_w = cols * tile_w + (cols - 1) * gap
                grid_h = rows * tile_h + (rows - 1) * gap
                start_x = (self.sw - grid_w) // 2
                start_y = (self.sh - grid_h) // 2

                for row in range(rows):
                    for col in range(cols):
                        x = start_x + col * (tile_w + gap)
                        y = start_y + row * (tile_h + gap)
                        new_tile = Tile(x, y, tile_w, tile_h, tile_font, row, col, layer=layer_idx)

                        char = game_chars_pool[char_idx]
                        ru_val = self.char_dict[char]["ru"]
                        en_val = self.char_dict[char]["en"]
                        new_tile.set_char(char, ru_val, en_val)

                        candidate_tiles.append(new_tile)
                        char_idx += 1

            if self.is_board_solvable(candidate_tiles):
                self.tiles = candidate_tiles
                break

    def reset_playing_field(self):
        self.tiles = []
        self.animating_tiles = []
        self.selected_tile = None
        self.pending_match = None
        self.game_won = False
        self.victory_sound_started = False
        self.full_victory_sound_started = False
        self.display_text = None
        self.create_tiles()

        self.btn_hint.set_style(BROWN_STYLE, active=True)
        self.btn_restart.set_style(GREY_STYLE, active=False)

    def find_available_pair(self):
        free_tiles = [t for t in self.tiles if self.is_tile_available(t)]
        for i in range(len(free_tiles)):
            for j in range(i + 1, len(free_tiles)):
                if free_tiles[i].char == free_tiles[j].char:
                    return (free_tiles[i], free_tiles[j])
        return None

    def hint_action(self):
        pair = self.find_available_pair()
        if pair:
            for t in pair:
                t.highlighted = True
                t.highlight_start_time = pygame.time.get_ticks()
        else:
            self.btn_hint.set_style(GREY_STYLE, active=False)
            self.btn_restart.set_style(BROWN_STYLE, active=True)

    def restart_action(self):
        if self.btn_restart.active:
            self.reset_playing_field()

    def continue_training_action(self):
        self.reset_playing_field()
        self.state = 'PLAYING'
        self.sound_mgr.play_bgm('game', force_restart=True)

    def start_game(self):
        if self.check_all_max_progress():
            self.max_progress_msg_active = True
            self.max_progress_msg_start_time = pygame.time.get_ticks()
            return

        self.state = 'PLAYING'
        self.sound_mgr.play_bgm('game', force_restart=True)
        self.reset_playing_field()

    def back_to_main(self):
        self.tiles = []
        self.animating_tiles = []
        self.selected_tile = None
        self.pending_match = None
        self.game_won = False
        self.victory_sound_started = False
        self.full_victory_sound_started = False
        self.display_text = None
        self.state = 'MAIN_MENU'
        self.sound_mgr.play_bgm('menu', force_restart=True)

    def open_settings(self):
        self.state = 'SETTINGS'

    def open_progress(self):
        self.progress_menu.scroll_y = 0
        self.state = 'PROGRESS'

    def close_modals(self):
        self.state = 'MAIN_MENU'

    def quit_game(self):
        self.sound_mgr.play_sfx('tile_click')
        pygame.time.wait(150)
        self.save_progress()
        self.running = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit_game()

            if self.state in ('MAIN_MENU', 'PLAYING', 'VICTORY'):
                if self.btn_exit.handle_event(event, self.sound_mgr):
                    continue

            if self.state == 'MAIN_MENU':
                self.btn_start.handle_event(event, self.sound_mgr)
                self.btn_settings.handle_event(event, self.sound_mgr)
                self.btn_progress.handle_event(event, self.sound_mgr)
            elif self.state == 'SETTINGS':
                self.settings_menu.handle_event(event, self.sound_mgr)
            elif self.state == 'PROGRESS':
                self.progress_menu.handle_event(event, self.sound_mgr)
            elif self.state == 'PLAYING':
                if self.btn_back.handle_event(event, self.sound_mgr):
                    continue
                if self.btn_hint.handle_event(event, self.sound_mgr):
                    continue
                if self.btn_restart.handle_event(event, self.sound_mgr):
                    continue

                if self.pending_match is not None:
                    continue

                if not self.game_won:
                    for tile in reversed(self.tiles):
                        if tile.handle_event(event):
                            if not self.is_tile_available(tile):
                                break

                            if self.selected_tile == tile:
                                self.sound_mgr.play_sfx('mismatch')
                                tile.selected = False
                                tile.scale_target = 1.0
                                self.selected_tile = None
                            elif self.selected_tile is None:
                                self.sound_mgr.play_sfx('tile_click')
                                self.selected_tile = tile
                                tile.selected = True
                                tile.scale_target = 1.15
                            else:
                                self.sound_mgr.play_sfx('tile_click')
                                second_tile = tile
                                if self.selected_tile.char == second_tile.char:
                                    second_tile.selected = True
                                    second_tile.scale_target = 1.15
                                    self.pending_match = (self.selected_tile, second_tile, pygame.time.get_ticks())
                                    self.selected_tile = None
                                else:
                                    self.sound_mgr.play_sfx('mismatch')
                                    self.selected_tile.selected = False
                                    self.selected_tile.scale_target = 1.0
                                    self.selected_tile = None
                            break
            elif self.state == 'VICTORY':
                if self.btn_back.handle_event(event, self.sound_mgr):
                    continue

                elapsed = pygame.time.get_ticks() - self.win_start_time
                if elapsed >= 8500:
                    self.btn_continue.handle_event(event, self.sound_mgr)

    def trigger_victory(self):
        self.game_won = True
        self.win_start_time = pygame.time.get_ticks()
        self.sound_mgr.play_victory_sound()
        self.victory_sound_started = True

    def update(self):
        current_time = pygame.time.get_ticks()

        if self.max_progress_msg_active:
            if current_time - self.max_progress_msg_start_time >= 4000:
                self.max_progress_msg_active = False

        if self.state == 'FULL_VICTORY':
            elapsed = current_time - self.full_victory_start_time
            if self.full_victory_sound_started and elapsed > 500:
                if not self.sound_mgr.is_full_victory_sound_playing():
                    self.back_to_main()
            return

        for tile in self.tiles:
            tile.update()

        if self.state == 'PLAYING':
            if self.display_text:
                if current_time - self.display_start_time >= self.display_duration:
                    self.display_text = None

            if self.pending_match:
                t1, t2, start_t = self.pending_match
                if current_time - start_t >= 300:
                    self.sound_mgr.play_sfx('match')

                    char = t1.char
                    if self.progress[char] < 50:
                        self.progress[char] += 1
                        self.save_progress()

                    if self.check_all_max_progress():
                        self.trigger_full_victory()
                        return

                    if self.language == "ru":
                        self.display_text = t1.ru_value
                    else:
                        self.display_text = t1.en_value

                    self.display_start_time = pygame.time.get_ticks()

                    t1.selected = False
                    t2.selected = False
                    t1.start_disappear_animation()
                    t2.start_disappear_animation()

                    self.animating_tiles.append(t1)
                    self.animating_tiles.append(t2)

                    if t1 in self.tiles:
                        self.tiles.remove(t1)
                    if t2 in self.tiles:
                        self.tiles.remove(t2)

                    self.pending_match = None

            for tile in self.tiles:
                if tile.highlighted:
                    if current_time - tile.highlight_start_time >= 4000:
                        tile.highlighted = False

            finished_animations = []
            for tile in self.animating_tiles:
                if tile.update():
                    finished_animations.append(tile)

            for tile in finished_animations:
                self.animating_tiles.remove(tile)

            if len(self.tiles) == 0 and len(self.animating_tiles) == 0 and not self.game_won and not self.pending_match:
                if self.display_text is None:
                    self.trigger_victory()

            if self.game_won:
                self.state = 'VICTORY'

        elif self.state == 'VICTORY':
            elapsed = current_time - self.win_start_time
            if elapsed >= 8500 and self.victory_sound_started:
                if not self.sound_mgr.is_victory_sound_playing():
                    self.back_to_main()

    def draw(self):
        language = self.translations[self.language]

        if self.state == 'FULL_VICTORY':
            self.screen.fill(BLACK)

            panel_w = int(self.sw * 0.75)
            panel_h = int(self.sh * 0.3)
            panel_rect = pygame.Rect((self.sw - panel_w) // 2, (self.sh - panel_h) // 2, panel_w, panel_h)

            pygame.draw.rect(self.screen, (124, 84, 55), panel_rect, border_radius=20)
            pygame.draw.rect(self.screen, (212, 175, 55), panel_rect, 6, border_radius=20)
            inner_rect = panel_rect.inflate(-30, -30)
            pygame.draw.rect(self.screen, (200, 170, 50), inner_rect, 3, border_radius=15)

            corner_radius = 8
            for dx, dy in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
                cx = panel_rect.centerx + dx * (inner_rect.width // 2)
                cy = panel_rect.centery + dy * (inner_rect.height // 2)
                pygame.draw.circle(self.screen, (212, 175, 55), (cx, cy), corner_radius)
                pygame.draw.circle(self.screen, (124, 84, 55), (cx, cy), corner_radius - 3)

            msg_title = language["full_victory_title"]
            msg_text = language["full_victory_text"]

            surf_title = self.fonts['large'].render(msg_title, True, GOLD_WIN)
            shadow_title = self.fonts['large'].render(msg_title, True, BLACK)
            rect_title = surf_title.get_rect(center=(panel_rect.centerx, panel_rect.centery - 25))

            surf_text = self.fonts['medium'].render(msg_text, True, WHITE)
            shadow_text = self.fonts['medium'].render(msg_text, True, BLACK)
            rect_text = surf_text.get_rect(center=(panel_rect.centerx, panel_rect.centery + 25))

            self.screen.blit(shadow_title, (rect_title.x + 2, rect_title.y + 2))
            self.screen.blit(surf_title, rect_title)

            self.screen.blit(shadow_text, (rect_text.x + 2, rect_text.y + 2))
            self.screen.blit(surf_text, rect_text)

            pygame.display.flip()
            return

        if self.state in ('MAIN_MENU', 'SETTINGS', 'PROGRESS'):
            if self.bg_image:
                self.screen.blit(self.bg_image, (0, 0))
            else:
                self.screen.fill(DEEP_GREEN)

            title_surf = self.fonts['title'].render("Mahjong: Chinese Training Game", True, TITLE_COLOR)
            title_shadow = self.fonts['title'].render("Mahjong: Chinese Training Game", True, WHITE)
            title_rect = title_surf.get_rect(center=(self.sw // 2, int(self.sh * 0.15)))

            self.screen.blit(title_shadow, (title_rect.x + 2, title_rect.y + 2))
            self.screen.blit(title_surf, title_rect)

            self.btn_start.draw(self.screen)
            self.btn_settings.draw(self.screen)
            self.btn_progress.draw(self.screen)
            self.btn_exit.draw(self.screen)

            if self.max_progress_msg_active:
                lines = language["max_progress_message"].split('\n')
                msg_w = int(self.sw * 0.65)
                msg_h = int(self.sh * 0.22)
                msg_rect = pygame.Rect((self.sw - msg_w) // 2, (self.sh - msg_h) // 2, msg_w, msg_h)

                pygame.draw.rect(self.screen, (60, 40, 30), msg_rect, border_radius=15)
                pygame.draw.rect(self.screen, GOLD_WIN, msg_rect, 4, border_radius=15)

                line_h = self.fonts['medium'].get_linesize()
                start_y = msg_rect.centery - (len(lines) * line_h) // 2

                for i, line in enumerate(lines):
                    surf = self.fonts['medium'].render(line, True, WHITE)
                    r = surf.get_rect(center=(self.sw // 2, start_y + i * line_h + line_h // 2))
                    self.screen.blit(surf, r)

            if self.state == 'SETTINGS':
                self.screen.blit(self.overlay, (0, 0))
                self.settings_menu.draw(self.screen)
            elif self.state == 'PROGRESS':
                self.screen.blit(self.overlay, (0, 0))
                self.progress_menu.draw(self.screen)

        elif self.state in ('PLAYING', 'VICTORY'):
            if self.game_bg_image:
                self.screen.blit(self.game_bg_image, (0, 0))
            else:
                self.screen.fill(DARK_RED)

            if self.state == 'PLAYING':
                self.btn_hint.draw(self.screen)
                self.btn_restart.draw(self.screen)

            sorted_tiles = sorted(self.tiles, key=lambda t: (t.layer, t.scale))
            for tile in sorted_tiles:
                tile.draw(self.screen)

            for tile in self.animating_tiles:
                tile.draw(self.screen)

            if self.display_text:
                popup_surf = self.fonts['popup'].render(self.display_text, True, POPUP_GREEN)
                popup_outline = self.fonts['popup'].render(self.display_text, True, GOLD_OUTLINE)

                popup_rect = popup_surf.get_rect(center=(self.sw // 2, int(self.sh * 0.15)))

                outline_offsets = [
                    (-2, -2), (-2, 0), (-2, 2),
                    (0, -2), (0, 2),
                    (2, -2), (2, 0), (2, 2),
                    (3, 3), (3, 4)
                ]

                for dx, dy in outline_offsets:
                    self.screen.blit(popup_outline, (popup_rect.x + dx, popup_rect.y + dy))

                self.screen.blit(popup_surf, popup_rect)

            if self.state == 'VICTORY':
                elapsed = pygame.time.get_ticks() - self.win_start_time
                if elapsed < 8500:
                    panel_w = int(self.sw * 0.75)
                    panel_h = int(self.sh * 0.28)
                    panel_x = (self.sw - panel_w) // 2
                    panel_y = (self.sh - panel_h) // 2
                    panel_rect = pygame.Rect(panel_x, panel_y, panel_w, panel_h)

                    pygame.draw.rect(self.screen, (124, 84, 55), panel_rect, border_radius=20)
                    pygame.draw.rect(self.screen, (212, 175, 55), panel_rect, 6, border_radius=20)
                    inner_rect = panel_rect.inflate(-30, -30)
                    pygame.draw.rect(self.screen, (200, 170, 50), inner_rect, 3, border_radius=15)

                    corner_radius = 8
                    for dx, dy in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
                        cx = panel_rect.centerx + dx * (inner_rect.width // 2)
                        cy = panel_rect.centery + dy * (inner_rect.height // 2)
                        pygame.draw.circle(self.screen, (212, 175, 55), (cx, cy), corner_radius)
                        pygame.draw.circle(self.screen, (124, 84, 55), (cx, cy), corner_radius - 3)

                    lines = language["victory_text"].split('\n')
                    line_height = int(self.fonts['win'].get_linesize() * 0.95)
                    total_h = len(lines) * line_height
                    start_y = panel_rect.centery - total_h // 2

                    for i, line in enumerate(lines):
                        surf = self.fonts['win'].render(line, True, WHITE)
                        shadow = self.fonts['win'].render(line, True, BLACK)
                        cy = start_y + i * line_height + line_height // 2
                        rect = surf.get_rect(center=(self.sw // 2, cy))
                        self.screen.blit(shadow, (rect.x + 2, rect.y + 2))
                        self.screen.blit(surf, rect)
                else:
                    self.btn_continue.draw(self.screen)

            self.btn_back.draw(self.screen)
            self.btn_exit.draw(self.screen)

        pygame.display.flip()

    def run(self):
        self.sound_mgr.play_bgm('menu')
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    app = GameApp()
    app.run()