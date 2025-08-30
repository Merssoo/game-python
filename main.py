import pygame
import sys
from player import Player
from enemy import Enemy
from explosion import Explosion

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Meu Jogo Demo")

pygame.mixer.music.load('assets/musica_fundo.wav')
pygame.mixer.music.play(-1)
som_tiro = pygame.mixer.Sound('assets/tiro.wav')
som_explosao = pygame.mixer.Sound('assets/explosao.wav')
som_hit = pygame.mixer.Sound('assets/hit.wav')

player_img = pygame.image.load("assets/player.png")
player_img = pygame.transform.scale(player_img, (50, 50))
enemy_img = pygame.image.load("assets/enemy.png")
enemy_img = pygame.transform.scale(enemy_img, (50, 50))
background_img = pygame.image.load("assets/background.png")
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
bullet_img = pygame.image.load("assets/bullet.png")
bullet_img = pygame.transform.scale(bullet_img, (10, 20))

font = pygame.font.Font(None, 50)
score_font = pygame.font.Font(None, 36)

score = 0
lives = 3
start_time = 0
enemy_spawn_rate = 60
max_enemies = 5

game_state = "MENU"

bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
player = None

# Nova variável global para controlar o disparo
last_shot_time = pygame.time.get_ticks()
shot_delay = 200  # 200 milissegundos entre tiros


def reset_game():
    global player, enemies, all_sprites, bullets, score, lives, start_time, max_enemies

    score = 0
    lives = 3
    start_time = pygame.time.get_ticks()
    max_enemies = 5

    player = Player()
    enemies.empty()
    bullets.empty()
    all_sprites.empty()

    all_sprites.add(player, *enemies, bullets)


def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)


def main_menu():
    global game_state

    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)

    while game_state == "MENU":
        screen.blit(background_img, (0, 0))

        title_text = font.render("Meu Jogo Demo", 1, WHITE)
        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
        screen.blit(title_text, title_rect)

        start_text = font.render("Clique para Iniciar", 1, WHITE)
        start_rect = start_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

        controls_text = font.render("Controles", 1, WHITE)
        controls_rect = controls_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))

        mouse_pos = pygame.mouse.get_pos()

        if start_rect.collidepoint(mouse_pos):
            start_text = font.render("Clique para Iniciar", 1, GREEN)
        if controls_rect.collidepoint(mouse_pos):
            controls_text = font.render("Controles", 1, GREEN)

        screen.blit(start_text, start_rect)
        screen.blit(controls_text, controls_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_rect.collidepoint(mouse_pos):
                    reset_game()
                    game_state = "PLAYING"
                if controls_rect.collidepoint(mouse_pos):
                    game_state = "CONTROLS"

        pygame.display.flip()


def controls_screen():
    global game_state

    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)

    while game_state == "CONTROLS":
        screen.blit(background_img, (0, 0))

        draw_text("Controles", font, WHITE, screen, WIDTH // 2, HEIGHT // 3)
        draw_text("SETAS: Mover", score_font, WHITE, screen, WIDTH // 2, HEIGHT // 2 - 30)
        draw_text("ESPAÇO: Atirar", score_font, WHITE, screen, WIDTH // 2, HEIGHT // 2)
        draw_text("CTRL: Bônus de 3 tiros", score_font, WHITE, screen, WIDTH // 2, HEIGHT // 2 + 30)
        draw_text("ALT: Bônus de velocidade", score_font, WHITE, screen, WIDTH // 2, HEIGHT // 2 + 60)

        back_text = font.render("Voltar ao Menu", 1, WHITE)
        back_rect = back_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 150))

        mouse_pos = pygame.mouse.get_pos()
        if back_rect.collidepoint(mouse_pos):
            back_text = font.render("Voltar ao Menu", 1, GREEN)

        screen.blit(back_text, back_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(mouse_pos):
                    game_state = "MENU"

        pygame.display.flip()


def game_loop():
    global game_state, score, lives, max_enemies, player, last_shot_time

    player_exploding = False
    player_explosion_sprite = None

    running = True
    clock = pygame.time.Clock()

    spawn_enemy_event = pygame.USEREVENT + 1
    pygame.time.set_timer(spawn_enemy_event, 1000)

    difficulty_event = pygame.USEREVENT + 2
    pygame.time.set_timer(difficulty_event, 30000)
    while running and game_state == "PLAYING":
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL:
                    if player and player.bonus_3_shots_active:
                        som_tiro.play()
                        player.shoot_bonus(all_sprites, bullets)
                if event.key == pygame.K_LALT:
                    if player and player.speed_bonus_active:
                        player.activate_speed_bonus()
                        print("Bônus de velocidade ativado!")

            if event.type == spawn_enemy_event:
                if len(enemies) < max_enemies:
                    new_enemy = Enemy()
                    enemies.add(new_enemy)
                    all_sprites.add(new_enemy)

            if event.type == difficulty_event:
                if max_enemies < 15:
                    max_enemies += 1

        # Lógica para tiro contínuo ao segurar a tecla de espaço
        keys = pygame.key.get_pressed()
        now = pygame.time.get_ticks()
        if keys[pygame.K_SPACE] and now - last_shot_time > shot_delay:
            som_tiro.play()
            if player:
                bullet = player.shoot()
                all_sprites.add(bullet)
                bullets.add(bullet)
            last_shot_time = now

        all_sprites.update()

        if player and not player_exploding:
            player_hits = pygame.sprite.spritecollide(player, enemies, True, pygame.sprite.collide_circle)
            for hit in player_hits:
                lives -= 1
                if lives > 0:
                    som_hit.play()
                if lives <= 0:
                    som_explosao.play()
                    player_exploding = True
                    player_explosion_sprite = Explosion(player.rect.center)
                    all_sprites.add(player_explosion_sprite)
                    player.kill()

                new_enemy = Enemy()
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)

        bullet_hits = pygame.sprite.groupcollide(bullets, enemies, True, True)
        for hit in bullet_hits:
            som_explosao.play()
            score += 1
            if score % 50 == 0:
                player.grant_3_shots_bonus()
                print("Bônus de 3 tiros disponível!")

            if score % 20 == 0:
                player.grant_speed_bonus()
                print("Bônus de velocidade disponível!")

            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

        if player_exploding and player_explosion_sprite and not player_explosion_sprite.alive():
            game_state = "GAME_OVER"

        screen.blit(background_img, (0, 0))
        all_sprites.draw(screen)

        time_elapsed = (pygame.time.get_ticks() - start_time) // 1000
        draw_text(f"Tempo: {time_elapsed}", score_font, (255, 255, 255), screen, 100, 20)
        draw_text(f"Pontos: {score}", score_font, (255, 255, 255), screen, WIDTH // 2, 20)
        draw_text(f"Vidas: {lives}", score_font, (255, 255, 255), screen, WIDTH - 100, 20)

        if player and (player.bonus_3_shots_active or player.speed_bonus_active):
            draw_text("BÔNUS DISPONÍVEL", score_font, (0, 255, 0), screen, WIDTH // 2, 50)
        if player and player.speed > player.base_speed:
            draw_text("VELOCIDADE ATIVA", score_font, (0, 255, 0), screen, WIDTH // 2, 80)

        pygame.display.flip()


def game_over_screen():
    global game_state

    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)

    while game_state == "GAME_OVER":
        screen.blit(background_img, (0, 0))

        draw_text("Game Over!", font, WHITE, screen, WIDTH // 2, HEIGHT // 3)

        final_score_text = f"Sua Pontuação Final: {score}"
        draw_text(final_score_text, score_font, WHITE, screen, WIDTH // 2, HEIGHT // 3 + 60)

        restart_text = font.render("Recomeçar", 1, WHITE)
        restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

        menu_text = font.render("Voltar ao Menu", 1, WHITE)
        menu_rect = menu_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))

        mouse_pos = pygame.mouse.get_pos()

        if restart_rect.collidepoint(mouse_pos):
            restart_text = font.render("Recomeçar", 1, GREEN)

        if menu_rect.collidepoint(mouse_pos):
            menu_text = font.render("Voltar ao Menu", 1, GREEN)

        screen.blit(restart_text, restart_rect)
        screen.blit(menu_text, menu_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_rect.collidepoint(mouse_pos):
                    reset_game()
                    game_state = "PLAYING"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                game_state = "MENU"

        pygame.display.flip()


while True:
    if game_state == "MENU":
        main_menu()
    elif game_state == "PLAYING":
        game_loop()
    elif game_state == "GAME_OVER":
        game_over_screen()
    elif game_state == "CONTROLS":
        controls_screen()