import pygame

class Menu(pygame.sprite.Sprite):
    def __init__(self, color = (0,0,0), background_image=None):
        super().__init__()
        if background_image == None:
            self.image = pygame.Surface((1200,700))
            self.image.fill(color)
        else:
            self.image = pygame.image.load(background_image).convert_alpha()
            self.image = pygame.transform.scale(self.image, (1200,700))
        self.rect = self.image.get_rect(center = (1200//2, 700//2))
        self.hidden = True
        
        