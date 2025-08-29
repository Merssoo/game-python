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

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        return bullet