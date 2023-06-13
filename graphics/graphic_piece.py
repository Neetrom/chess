import pygame
from settings import TILE_SIZE

class Graphic_piece(pygame.sprite.Sprite):
    def __init__(self, piece_type, pos):
        super().__init__()
        self.type = piece_type
        if piece_type != "00":
            self.image = pygame.image.load(f"graphics/graphic_pieces/{piece_type}.png").convert_alpha()
        else:
            self.image = pygame.Surface((0,0))
        self.rect = self.image.get_rect(topleft=(pos[0]*TILE_SIZE, pos[1]*TILE_SIZE))
    
    def update_pos(self,pos):
        self.pos = pos
        self.rect = self.image.get_rect(topleft=(pos[0]*TILE_SIZE, pos[1]*TILE_SIZE))
