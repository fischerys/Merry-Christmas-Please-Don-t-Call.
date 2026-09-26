import math
import random
import sys
import pygame

# Inisialisasi Pygame & Audio
pygame.init()
pygame.font.init()
pygame.mixer.init()

# Konfigurasi Layar
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Merry Christmas, Please Don't Call - Sync Lyrics")
clock = pygame.time.Clock()

# Warna
BG_COLOR = (12, 6, 14)
CARD_BG = (130, 25, 35)
CARD_BORDER = (220, 70, 80)
TEXT_COLOR = (255, 235, 235)
PARTICLE_COLOR = (200, 50, 60)

try:
    font = pygame.font.SysFont("Georgia", 20, bold=True)
except Exception:
    font = pygame.font.Font(None, 24)

# Data Lirik & Timestamp yang Disesuaikan dengan Detik Video
# Format: ("Teks Lirik", Detik_Muncul, Posisi_Target_X, Posisi_Target_Y)
lyrics_data = [
    ("Just one ticket out of your heavy gaze", 0.2, 380, 180),
    ("I want one ticket off of your carousel", 2.2, 850, 280),
    ("And the toughest part is that we both know", 4.5, 380, 380),
    ("Merry Christmas, please don't call", 8.2, 850, 480),
]

# Jika ada file musik 'song.mp3', aktifkan 2 baris di bawah ini:
# pygame.mixer.music.load("song.mp3")
# pygame.mixer.music.play()


class Particle:

    def __init__(self):
        self.reset()
        self.y = random.randint(0, HEIGHT)

    def reset(self):
        self.x = random.randint(0, WIDTH)
        self.y = HEIGHT + random.randint(10, 50)
        self.size = random.randint(2, 5)
        self.speed = random.uniform(0.6, 2.2)
        self.alpha = random.randint(100, 220)

    def update(self):
        self.y -= self.speed
        if self.y < -10:
            self.reset()

    def draw(self, surface):
        s = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.circle(
            s, (*PARTICLE_COLOR, self.alpha), (self.size, self.size), self.size
        )
        surface.blit(s, (self.x, self.y))


class FloatingCard:

    def __init__(self, text, start_time, target_x, target_y):
        self.text = text
        self.start_time = start_time
        self.target_x = target_x
        self.target_y = target_y
        self.x = target_x + random.randint(-60, 60)
        self.y = HEIGHT + 150
        self.current_y = self.y
        self.is_active = False
        self.angle = random.uniform(-4, 4)
        self.float_offset = random.uniform(0, math.pi * 2)

        self.text_surf = font.render(text, True, TEXT_COLOR)
        self.padding_x = 22
        self.padding_y = 14
        self.width = self.text_surf.get_width() + self.padding_x * 2
        self.height = self.text_surf.get_height() + self.padding_y * 2

    def update(self, current_time):
        if not self.is_active:
            if current_time >= self.start_time:
                self.is_active = True
            else:
                return

        self.x += (self.target_x - self.x) * 0.05
        self.y += (self.target_y - self.y) * 0.05

        self.float_offset += 0.03
        self.current_y = self.y + math.sin(self.float_offset) * 6

    def draw(self, surface):
        if not self.is_active:
            return

        card_surf = pygame.Surface(
            (self.width + 12, self.height + 12), pygame.SRCALPHA
        )

        pygame.draw.rect(
            card_surf,
            (40, 5, 10, 180),
            (5, 7, self.width, self.height),
            border_radius=8,
        )

        pygame.draw.rect(
            card_surf, CARD_BG, (0, 0, self.width, self.height), border_radius=8
        )
        pygame.draw.rect(
            card_surf,
            CARD_BORDER,
            (0, 0, self.width, self.height),
            width=2,
            border_radius=8,
        )

        card_surf.blit(self.text_surf, (self.padding_x, self.padding_y))

        rot_angle = math.sin(self.float_offset * 0.5) * 2 + self.angle
        rotated_surf = pygame.transform.rotate(card_surf, rot_angle)
        new_rect = rotated_surf.get_rect(center=(self.x, self.current_y))

        surface.blit(rotated_surf, new_rect.topleft)


particles = [Particle() for _ in range(70)]
cards = [FloatingCard(text, t, x, y) for text, t, x, y in lyrics_data]
start_ticks = pygame.time.get_ticks()

running = True
while running:
    clock.tick(60)
    screen.fill(BG_COLOR)

    elapsed_seconds = (pygame.time.get_ticks() - start_ticks) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for p in particles:
        p.update()
        p.draw(screen)

    for card in cards:
        card.update(elapsed_seconds)
        card.draw(screen)

    pygame.display.flip()

pygame.quit()
sys.exit()