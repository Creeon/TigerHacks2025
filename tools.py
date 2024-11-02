import pygame

class Tool(pygame.sprite.Sprite):
    def __init__(self, tool_name, image, width, height, player, type):
        super().__init__()
        self.tool_name = tool_name
        self.image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.base_image = pygame.image.load(image).convert_alpha()
        self.base_image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(center = (0,0))
        self.hidden = True
        self.player = player
        self.type=type
    def update(self):
        orientation = self.player.orientation
        x,y = self.player.rect.center[0], self.player.rect.center[1]
        self.image = pygame.transform.rotate(self.base_image, orientation)
        self.rect = self.image.get_rect()
        match orientation:
            case 0:
                self.rect.center = (x + self.player.rect.width//2 + self.rect.width//2, y)
            case 90:
                self.rect.center = (x, y - self.rect.height//2 - self.player.rect.height//2)
            case 180:
                self.rect.center = (x - self.player.rect.width//2 - self.rect.width//2, y)
            case 270:
                self.rect.center = (x, y + self.rect.height//2 + self.player.rect.height//2)
            case _:
                print("Uh oh!")
                
class WateringCan(Tool):
    def __init__(self, player):
        super().__init__("Watering Can", "images/watering_can.png", 50,50,player,"watering")     
        
class Tractor(Tool):    
    def __init__(self, player):
        super().__init__("Tractor", "images/tractor.png", 500, 500, player, "tilling")
        
class WaterPlane(Tool):    
    def __init__(self, player):
        super().__init__("Water Plane", "images/water_plane.png", 500, 500, player, "watering")
        
class Shovel(Tool):
    def __init__(self, player):
        super().__init__("Shovel", "images/shovel.png", 100, 50, player, "planting")
        
class Sickle(Tool):
    def __init__(self, player):
        super().__init__("Sickle", "images/sickle.png", 100, 50, player, "harvesting")