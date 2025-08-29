import pygame


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.images = []
        # Carrega 5 imagens da explosão: explosion1.png até explosion5.png
        for i in range(1, 6):
            img = pygame.image.load(f"assets/explosion{i}.png").convert_alpha()
            self.images.append(pygame.transform.scale(img, (75, 75)))  # Ajuste o tamanho

        self.frame = 0
        self.image = self.images[self.frame]
        self.rect = self.image.get_rect(center=center)
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50  # Velocidade da animação (em milissegundos por frame)

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.images):
                self.kill()  # Remove a explosão quando a animação termina
            else:
                center = self.rect.center
                self.image = self.images[self.frame]
                self.rect = self.image.get_rect(center=center)