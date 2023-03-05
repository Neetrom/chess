import pygame

class Piece(pygame.sprite.Sprite):
    def __init__(self, piece_type, pos):
        super().__init__()
        self.image = pygame.image.load(f"graphics/{piece_type}.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)

        self.color = piece_type[0]
        self.points = 0
        