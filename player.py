import pygame
from bullet import Bullet

# Carrega as imagens fora da classe para evitar recarregar a cada nova instância
player_img = pygame.image.load("assets/player.png")
player_img = pygame.transform.scale(player_img, (50, 50))
thruster_img = pygame.image.load("assets/flash.png")
thruster_img = pygame.transform.scale(thruster_img, (30, 30))


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.center = (400, 550)
        self.speed = 5
        self.base_speed = 5
        self.thruster_speed = 10  # Velocidade aumentada

        self.thruster_active = False
        self.thruster_start_time = 0
        self.thruster_last_use = 0
        self.thruster_duration = 10000  # 10 segundos em milissegundos
        self.thruster_cooldown = 30000  # 30 segundos em milissegundos

    def update(self):
        keys = pygame.key.get_pressed()
        now = pygame.time.get_ticks()

        # Ativa a propulsão se a tecla CTRL for pressionada e o cooldown tiver terminado
        if keys[pygame.K_LCTRL] and (now - self.thruster_last_use > self.thruster_cooldown) and not self.thruster_active:
            self.thruster_active = True
            self.thruster_start_time = now
            self.thruster_last_use = now

        # Desativa a propulsão se a duração de 10 segundos acabar ou a tecla for solta
        if self.thruster_active:
            if now - self.thruster_start_time > self.thruster_duration or not keys[pygame.K_LCTRL]:
                self.thruster_active = False

        # Define a velocidade atual
        if self.thruster_active:
            self.speed = self.thruster_speed
        else:
            self.speed = self.base_speed

        # Movimento do jogador com a nova velocidade
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < 800:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < 600:
            self.rect.y += self.speed

    def draw_thruster(self, screen):
        """Desenha a imagem da propulsão se estiver ativa."""
        if self.thruster_active:
            thruster_rect = thruster_img.get_rect(centerx=self.rect.centerx, centery=self.rect.bottom + 10)
            screen.blit(thruster_img, thruster_rect)

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        return bullet