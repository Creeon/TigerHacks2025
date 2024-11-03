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
        self.speed_mod = 1
    def update(self):
        orientation = self.player.orientation
        x,y = self.player.rect.center[0], self.player.rect.center[1]
        self.image = pygame.transform.rotate(self.base_image, orientation)
        if(orientation==180):
            self.image = pygame.transform.flip(self.image, False, True)
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
        
class Hose(Tool):
    def __init__(self, player):
        super().__init__("Hose", "images/hose.png", 150,150, player,"watering") 
        self.speed_mod=1.5
    
class WaterPlane(Tool):    
    def __init__(self, player):
        super().__init__("Water Plane", "images/water_plane.png", 400, 400, player, "watering")
        self.speed_mod = 3
        
class Tractor(Tool):    
    def __init__(self, player):
        super().__init__("Tractor", "images/tractor.png", 400, 400, player, "tilling")
        self.speed_mod=3
        
class Hoe(Tool):
    def __init__(self, player):
        super().__init__("Hoe", "images/hoe.png", 100, 50, player, "tilling")
        
class GardenFork(Tool):
    def __init__(self, player):
        super().__init__("Garden Fork", "images/garden_fork.png", 175,100, player, "tilling")
        self.speed_mod=1.5
        
class Shovel(Tool):
    def __init__(self, player):
        super().__init__("Shovel", "images/shovel.png", 75, 40, player, "planting")
        
class Plow(Tool):
    def __init__(self, player):
        super().__init__("Plow", "images/plow.png", 150, 80, player, "planting")
        
class Ox(Tool):
    def __init__(self, player):
        super().__init__("Ox", "images/Ox.png", 300, 150, player, "planting")
        self.speed_mod=2.5
        
class Sickle(Tool):
    def __init__(self, player):
        super().__init__("Sickle", "images/sickle.png", 100, 50, player, "harvesting")
        
class Scythe(Tool):
    def __init__(self, player):
        super().__init__("Scythe", "images/scythe.png", 200, 100, player, "harvesting")
        
class Combine(Tool):
    def __init__(self, player):
        super().__init__("Combine", "images/Combine.png", 400, 400, player, "harvesting")
        self.speed_mod=3
        
class FertilizingMachine(Tool):
    def __init__(self,player):
        super().__init__("Machine", "images/machine.png", 400,400,player,"fertilizing")
        
class Sprayer(Tool):
    def __init__(self, player):
        super().__init__("Sprayer", "images/sprayer.png", 50,50, player, "fertilizing")
        
class FertilizationSpray(Tool):
    def __init__(self, player):
        super().__init__("Spray", "images/spray_bottle.png", 50,50, player, "fertilizing")
        