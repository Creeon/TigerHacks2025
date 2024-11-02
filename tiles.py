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
    
    def interact(self):
        pass
    
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

    def interact(self, inv):
        inv.add_item(self.crop_name)
        self.kill()
        
class WheatTile(CropTile):
    def __init__(
        self,
        x = 0,
        y = 0,
    ):
        super().__init__("Wheat", 10, 10, width=50, height=50, x=x, y=y, collision=False, image="images/best_wheat.png", interact_range=100)
        
class PumpkinTile(CropTile):
    def __init__(
        self,
        x = 0,
        y = 0,
    ):
        super().__init__("Pumpkin", 10, 10, width=50, height=50, x=x, y=y, collision=False, image="images/pumpkin.png", interact_range=100)
        
class Carrot(CropTile):
    def __init__(
        self,
        x = 0,
        y = 0,
    ):
        super().__init__("Wheat", 10, 10, width=50, height=50, x=x, y=y, collision=False, image="images/best_wheat.png", interact_range=100)

        
class Gate(InteractableTile):
    def __init__(self,x:int,y:int,rot:int):
        super().__init__(width=200, height=10, x=x, y=y, color=(0,0,0), collision=True, interact_range=50)
        self.image = pygame.transform.rotate(self.image,rot)
        self.rect = self.image.get_rect(center=self.rect.center)
    def interact(self):
        self.collision = not self.collision
        if self.collision:
            self.image.fill((0,0,0))
        else:
            self.image.fill((0,125,0))
        