import pygame
from bullet import Bullet

# Carrega as imagens fora da classe para evitar recarregar a cada nova instância
player_img = pygame.image.load("assets/player.png")
player_img = pygame.transform.scale(player_img, (50, 50))


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.center = (400, 550)
        self.speed = 5
        self.base_speed = 5

        # Variáveis para o bônus de 3 tiros
        self.bonus_3_shots_active = False
        self.bonus_3_shots_start_time = 0
        self.bonus_3_shots_duration = 5000  # 10 segundos em milissegundos

        # Variáveis para o bônus de velocidade
        self.speed_bonus_active = False
        self.speed_bonus_start_time = 0
        self.speed_bonus_duration = 5000  # 5 segundos em milissegundos

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < 800:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < 600:
            self.rect.y += self.speed

        now = pygame.time.get_ticks()

        # Verifica se o tempo do bônus de 3 tiros acabou
        if self.bonus_3_shots_active and now - self.bonus_3_shots_start_time > self.bonus_3_shots_duration:
            self.bonus_3_shots_active = False
            print("Bônus de 3 tiros expirado.")

        # Verifica se o tempo do bônus de velocidade acabou
        if self.speed > self.base_speed and now - self.speed_bonus_start_time > self.speed_bonus_duration:
            self.speed = self.base_speed
            print("Bônus de velocidade expirado.")

    def grant_3_shots_bonus(self):
        """Disponibiliza o bônus de 3 tiros."""
        self.bonus_3_shots_active = True
        self.bonus_3_shots_start_time = pygame.time.get_ticks()

    def grant_speed_bonus(self):
        """Disponibiliza o bônus de velocidade."""
        self.speed_bonus_active = True

    def activate_speed_bonus(self):
        """Ativa o bônus de velocidade."""
        if self.speed_bonus_active:
            self.speed_bonus_active = False
            self.speed = self.base_speed * 2
            self.speed_bonus_start_time = pygame.time.get_ticks()

    def shoot(self):
        """Dispara um tiro normal."""
        bullet = Bullet(self.rect.centerx, self.rect.top)
        return bullet

    def shoot_bonus(self, all_sprites, bullets):
        """Dispara 3 tiros e desativa o bônus."""
        if self.bonus_3_shots_active:
            bullet1 = Bullet(self.rect.centerx, self.rect.top)
            bullet2 = Bullet(self.rect.centerx - 15, self.rect.top)
            bullet3 = Bullet(self.rect.centerx + 15, self.rect.top)

            all_sprites.add(bullet1, bullet2, bullet3)
            bullets.add(bullet1, bullet2, bullet3)