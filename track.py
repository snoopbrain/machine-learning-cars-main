import pygame
import numpy as np



class track(pygame.sprite.Sprite):
    def __init__(self, screen, lenWidth):
        pygame.sprite.Sprite.__init__(self)
        self.length, self.width = lenWidth
        img = pygame.image.load('img/track_edited.png').convert_alpha()
        self.image = pygame.transform.scale(img, (self.length, self.width))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 0, 0
        self.screen = screen

        # Definir color de la calle
        self.streetColor = np.array([163, 171, 160, 255])

        # Crear máscara con rango de color
        self.mask = self.create_mask_with_range(self.image, self.streetColor, (10, 10, 10, 255))

    def create_mask_with_range(self, image, color, tolerance):
        tolerance = np.array(tolerance)
        color_low = np.maximum(color - tolerance, 0)
        color_high = np.minimum(color + tolerance, 255)
        
        # Crear máscara basada en rango de color
        mask = pygame.mask.Mask(image.get_size())
        for x in range(image.get_width()):
            for y in range(image.get_height()):
                pixel = np.array(image.get_at((x, y)))
                if np.all(pixel >= color_low) and np.all(pixel <= color_high):
                    mask.set_at((x, y), 1)
        return mask

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def draw_mask(self):
        mask_surface = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
        mask_surface.fill((0, 0, 0, 0))
        for x in range(self.mask.get_size()[0]):
            for y in range(self.mask.get_size()[1]):
                if self.mask.get_at((x, y)):
                    mask_surface.set_at((x, y), (255, 0, 0, 100))  # Color rojo semitransparente para la máscara
        self.screen.blit(mask_surface, self.rect)
