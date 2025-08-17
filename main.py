import pygame
import random
import sys
import statistics

# Pygame initialisieren
pygame.init()

# Bildschirmgröße automatisch holen
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Target Game")

# Farben
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLACK = (0, 0, 0)

# Font
font = pygame.font.SysFont("Arial", 40)

# Target Eigenschaften
base_radius = 40  # Grundgröße
def new_target():
    scale = random.uniform(0.7, 1.3)  # ±30%
    radius = int(base_radius * scale)
    x = random.randint(radius, WIDTH - radius)
    y = random.randint(radius, HEIGHT - radius)
    return x, y, radius

def draw_target(surface, x, y, radius, rings=4):
    """ Zeichnet ein Target mit abwechselnden roten/weißen Ringen """
    for i in range(rings, 0, -1):
        color = RED if i % 2 == 0 else WHITE
        pygame.draw.circle(surface, color, (x, y), int(radius * i / rings))

# Spielparameter
clock = pygame.time.Clock()
running = True
hits = 0
misses = 0
offsets = []  # Distanz vom Zentrum
hit_times = []  # Zeitpunkte der Treffer
time_limit = 30  # Sekunden
start_ticks = pygame.time.get_ticks()  # Startzeit

target_x, target_y, target_radius = new_target()
game_over = False

while running:
    screen.fill(WHITE)

    # Zeit berechnen
    seconds = (pygame.time.get_ticks() - start_ticks) // 1000
    remaining_time = max(0, time_limit - seconds)

    if not game_over:
        # Target zeichnen
        draw_target(screen, target_x, target_y, target_radius)

        # Nur Timer anzeigen
        time_text = font.render(f"Time: {remaining_time}", True, BLACK)
        screen.blit(time_text, (20, 20))

        # Spielende prüfen
        if remaining_time <= 0:
            game_over = True

    else:
        # Trefferquote berechnen
        total_shots = hits + misses
        hitrate = (hits / total_shots * 100) if total_shots > 0 else 0
        avg_time_per_target = 0
        avg_offset = 0

        if len(hit_times) > 1:
            diffs = [hit_times[i] - hit_times[i-1] for i in range(1, len(hit_times))]
            avg_time_per_target = statistics.mean(diffs)
        if offsets:
            avg_offset = statistics.mean(offsets)

        # Endscreen
        end_text = font.render("Game Over!", True, BLACK)
        stats1 = font.render(f"Hits: {hits}  Misses: {misses}", True, BLACK)
        stats2 = font.render(f"HitRate: {hitrate:.1f}%", True, BLACK)
        stats3 = font.render(f"Avg Time per Target: {avg_time_per_target:.2f}s", True, BLACK)
        stats4 = font.render(f"Avg Offset from Center: {avg_offset:.1f}px", True, BLACK)
        restart_text = font.render("Press R to Restart or ESC to Quit", True, BLACK)

        screen.blit(end_text, (WIDTH // 2 - end_text.get_width() // 2, HEIGHT // 2 - 140))
        screen.blit(stats1, (WIDTH // 2 - stats1.get_width() // 2, HEIGHT // 2 - 80))
        screen.blit(stats2, (WIDTH // 2 - stats2.get_width() // 2, HEIGHT // 2 - 40))
        screen.blit(stats3, (WIDTH // 2 - stats3.get_width() // 2, HEIGHT // 2))
        screen.blit(stats4, (WIDTH // 2 - stats4.get_width() // 2, HEIGHT // 2 + 40))
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 100))

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if game_over and event.key == pygame.K_r:
                # Reset
                hits = 0
                misses = 0
                offsets.clear()
                hit_times.clear()
                start_ticks = pygame.time.get_ticks()
                target_x, target_y, target_radius = new_target()
                game_over = False

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouse_x, mouse_y = event.pos
            dist = ((mouse_x - target_x) ** 2 + (mouse_y - target_y) ** 2) ** 0.5
            if dist <= target_radius:
                hits += 1
                offsets.append(dist)
                hit_times.append(pygame.time.get_ticks() / 1000)  # Sekunden
                target_x, target_y, target_radius = new_target()
            else:
                misses += 1

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
