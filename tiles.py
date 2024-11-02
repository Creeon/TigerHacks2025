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
        interact_range = 50
    ):
        super().__init__(width=width, height=height, x=x, y=y, color=color, collision=collision, image=image)
        self.interact_range = interact_range        
class CropTile(InteractableTile):
    def __init__(
        self,
        crop_name: str,
        grow_time: int,
        harvest_time: int,
        width = 50,
        height = 50,
        x = 0,
        y = 0,
        color = (255,255,255),
        collision = True,
        image = None,
        interact_range = 50
    ):
        super().__init__(width=width, height=height, x=x, y=y, color=color, collision=collision, image=image, interact_range=interact_range)
        self.crop_name = crop_name
        self.grow_time = grow_time
        self.harvest_time = harvest_time
        
class WheatTile(CropTile):
    def __init__(
        self,
        x = 0,
        y = 0,
    ):
        super().__init__("Wheat", 10, 10, width=50, height=50, x=x, y=y, collision=False, image="images/best_wheat.png", interact_range=100)
    
    def interact(self):
        self.image = pygame.transform.scale(self.image, (1000,1000))
        