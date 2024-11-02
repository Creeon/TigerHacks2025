import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, width=50, height=50, x=0, y=0, color=(255,255,255), collision = True, image=None):
        super().__init__()
        if image == None:
            self.image = pygame.Surface((width, height))
            self.image.fill(color)
        else:
            self.image = pygame.image.load(image).convert_alpha()
            self.image = pygame.transform.scale(self.image, (width,height))
        self.rect = self.image.get_rect(center=(x,y))
        self.collision = collision
        
    def update(self, movement):
        self.rect = self.rect.move(movement[0], movement[1])
        
class InteractableTile(Tile):
    def __init__(
        self,
        width = 50,
        height = 50,
        x = 0,
        y = 0,
        color = (255,255,255),
        collision = True,
        image = None,
        interact_range = 50,
        interact_function = None
    ):
        super().__init__(width=width, height=height, x=x, y=y, color=color, collision=collision, image=image)
        self.interact_range = interact_range
        self.interact_function = interact_function