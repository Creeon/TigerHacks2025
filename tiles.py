import pygame
import random

images = dict({
    "baby_pumpkin" : pygame.transform.scale(pygame.image.load("images/Crops/pum1.png").convert_alpha(), (50,50)),
    "grown_pumpkin" : pygame.transform.scale(pygame.image.load("images/Crops/pum2.png").convert_alpha(), (50,50)),
    "dead_pumpkin" : pygame.transform.scale(pygame.image.load("images/Crops/pum3.png").convert_alpha(), (50,50)),
    "baby_wheat" : pygame.transform.scale(pygame.image.load("images/Crops/wheat1.png").convert_alpha(), (50,50)),
    "grown_wheat" : pygame.transform.scale(pygame.image.load("images/Crops/wheat2.png").convert_alpha(), (50,50)),
    "dead_wheat" : pygame.transform.scale(pygame.image.load("images/Crops/wheat3.png").convert_alpha(), (50,50)),
    "baby_carrot" : pygame.transform.scale(pygame.image.load("images/Crops/car1.png").convert_alpha(), (50,50)),
    "grown_carrot" : pygame.transform.scale(pygame.image.load("images/Crops/car2.png").convert_alpha(), (50,50)),
    "dead_carrot" : pygame.transform.scale(pygame.image.load("images/Crops/car3.png").convert_alpha(), (50,50)),
    "baby_watermelon" : pygame.transform.scale(pygame.image.load("images/Crops/watermelon1.png").convert_alpha(), (50,50)),
    "grown_watermelon" : pygame.transform.scale(pygame.image.load("images/Crops/watermelon2.png").convert_alpha(), (50,50)),
    "dead_watermelon" : pygame.transform.scale(pygame.image.load("images/Crops/watermelon3.png").convert_alpha(), (50,50)),
    "baby_corn" : pygame.transform.scale(pygame.image.load("images/Crops/corn1.png").convert_alpha(), (50,50)),
    "grown_corn" : pygame.transform.scale(pygame.image.load("images/Crops/corn2.png").convert_alpha(), (50,50)),
    "dead_corn" : pygame.transform.scale(pygame.image.load("images/Crops/corn3.png").convert_alpha(), (50,50)),
    "baby_lettuce" : pygame.transform.scale(pygame.image.load("images/Crops/lettuce1.png").convert_alpha(), (50,50)),
    "grown_lettuce" : pygame.transform.scale(pygame.image.load("images/Crops/lettuce2.png").convert_alpha(), (50,50)),
    "dead_lettuce" : pygame.transform.scale(pygame.image.load("images/Crops/dead_bush.png").convert_alpha(), (50,50)),
    "grass" : pygame.transform.scale(pygame.image.load("images/grass.png").convert_alpha(), (50,50)),
    "dirt" : pygame.transform.scale(pygame.image.load("images/dirt.png").convert_alpha(), (50,50)),
    "wet_dirt" : pygame.transform.scale(pygame.image.load("images/wet_dirt.png").convert_alpha(), (50,50)),
    "stone" : pygame.transform.scale(pygame.image.load("images/stone.png").convert_alpha(), (50,50)),
    "tree" : pygame.transform.scale(pygame.image.load("images/tree.png").convert_alpha(), (200,325))
})

class Tile(pygame.sprite.Sprite):
    def __init__(self, width=50, height=50, x=0, y=0, color=(255,255,255), collision = True, image=None, image_loaded = False):
        super().__init__()
        if not image_loaded:
            if image == None:
                self.image = pygame.Surface((width, height))
                self.image.fill(color)
            else:
                self.image = pygame.image.load(image).convert_alpha()
                self.image = pygame.transform.scale(self.image, (width,height))
        else:
            self.image = image
        self.rect = self.image.get_rect(center=(x,y))
        self.collision = collision
        
    def update(self, movement):
        self.rect = self.rect.move(movement[0], movement[1])
        
    def change_image(self, image, width, height):
        self.image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width,height))
        
    def display(self, screen):
        screen.blit(self.image, self.rect)
        
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
        image_loaded=False
    ):
        super().__init__(width=width, height=height, x=x, y=y, color=color, collision=collision, image=image, image_loaded=image_loaded)
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
        dead_image = None,
        grown_image = None,
        interact_range = 50,
        risk = 0,
        cost=10,
        quality=1,
        season="Spring"
    ):
        super().__init__(width=width, height=height, x=x, y=y, color=color, collision=collision, image=image, interact_range=interact_range, image_loaded=True)
        self.crop_name = crop_name
        self.grow_time = grow_time
        self.harvest_time = harvest_time
        self.dead_image = dead_image
        self.grown_image = grown_image
        self.risk = risk
        self.grown = False
        self.dead = False
        self.age = 0
        self.cost=cost
        self.quality=quality
        self.season=season

    def interact(self, money):
        if self.grown:
            money.money+=int(self.cost*self.quality)

        if self.grown or self.dead:
            self.kill()
        
    def iterate(self, risk, season):
        self.age+=1
        if random.randint(0,100) < self.risk+risk+(0 if season==self.season else 50):
            self.die()
        elif self.age == self.grow_time and not self.dead:
            self.grow()
    def die(self):
        self.dead=True
        self.image = self.dead_image
        
    def grow(self):
        self.grown=True
        self.image=self.grown_image
        
        
class WheatTile(CropTile):
    def __init__(
        self,
        x = 0,
        y = 0,
    ):
        super().__init__("Wheat", 10, 10, width=50, height=50, x=x, y=y, collision=False, image=images["baby_wheat"], dead_image=images["dead_wheat"], grown_image=images["grown_wheat"], interact_range=100, risk=3, season="Fall", cost=5)
        
class PumpkinTile(CropTile):
    def __init__(
        self,
        x = 0,
        y = 0,
    ):
        super().__init__("Pumpkin", 10, 10, width=50, height=50, x=x, y=y, collision=False, image=images["baby_pumpkin"], dead_image=images["dead_pumpkin"], grown_image=images["grown_pumpkin"], interact_range=100, risk=3, season="Fall", cost=7)

class CarrotTile(CropTile):
    def __init__(
        self,
        x = 0,
        y = 0,
    ):
        super().__init__("Carrot", 10, 10, width=50, height=50, x=x, y=y, collision=False, image=images["baby_carrot"], dead_image=images["dead_carrot"], grown_image=images["grown_carrot"], interact_range=100, risk=3, season="Spring", cost=5)
        
class WatermelonTile(CropTile):
    def __init__(
        self,
        x = 0,
        y = 0,
    ):
        super().__init__("Watermelon", 10, 10, width=50, height=50, x=x, y=y, collision=False, image=images["baby_watermelon"], dead_image=images["dead_watermelon"], grown_image=images["grown_watermelon"], interact_range=100, risk=3, season="Summer", cost=7)

class CornTile(CropTile):
    def __init__(
        self,
        x = 0,
        y = 0,
    ):
        super().__init__("Corn", 10, 10, width=50, height=50, x=x, y=y, collision=False, image=images["baby_corn"], dead_image=images["dead_corn"], grown_image=images["grown_corn"], interact_range=100, risk=3, season="Summer", cost=5)
        
class LettuceTile(CropTile):
    def __init__(
        self,
        x = 0,
        y = 0,
    ):
        super().__init__("Lettuce", 10, 10, width=50, height=50, x=x, y=y, collision=False, image=images["baby_lettuce"], dead_image=images["dead_lettuce"], grown_image=images["grown_lettuce"], interact_range=100, risk=3, season="Spring", cost=7)
        
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
            
class GroundTile(Tile):
    def __init__(self,x:int,y:int,default_image="grass",tilled_image="dirt",watered_image="wet_dirt",collision=False):
        self.default_image = images[default_image]
        self.tilled_image = images[tilled_image]
        self.watered_image = images[watered_image]
        super().__init__(width=50,height=50,x=x,y=y,collision=collision,image=self.default_image,image_loaded=True)
        self.crop = None
        self.soil_quality=10
        self.fertilized = False
        self.watered = False
        self.tilled = False
        self.shader = pygame.Surface((50,50))
        self.shader.fill((0,125,0))
        self.shader.set_alpha(0)
        self.last_crop=None
        self.tree=None
    def getRisk(self):
        return 30 - self.soil_quality - (5 if self.fertilized else 0) - (15 if self.watered else 0)
    def update(self, movement):
        if not self.tilled:
            self.image = self.default_image
        else:
            if self.watered:
                self.image = self.watered_image
            else:
                self.image = self.tilled_image
        self.rect = self.rect.move(movement[0], movement[1])
        if not self.crop == None:
            self.crop.rect = self.crop.rect.move(movement[0], movement[1])
    def iterate(self):
        if self.watered and (random.randint(1,100) < 21):
            self.watered=False
        if self.crop == None and self.tilled:
            if random.randint(1,100) < 15:
                self.tilled=False
        if self.fertilized:
            if random.randint(1,100) <=5:
                self.fertilized=False
    def fertilize(self):
        self.fertilized = True
        self.shader.set_alpha(35)
    def display(self, screen):
        screen.blit(self.image, self.rect)
        if not self.crop == None:
            screen.blit(self.crop.image, self.crop.rect)
        if self.fertilized:
            screen.blit(self.shader, self.shader.get_rect(center=self.rect.center))
            
class House(InteractableTile):
    def __init__(self,x,y):
        super().__init__(500,500,x,y,image="images/house.png")
    def interact(self):
        pass
    
class ChristmasTiger(InteractableTile):
    def __init__(self,x,y):
        super().__init__(300,600,x,y,image="images/Crops/santa_tiger.png", collision=False)
    def interact(self, money):
        money.money+=1

class Tree(Tile):
    def __init__(self, x=0, y=0):
        # Use the predefined tree image from images dictionary
        image = images["tree"]
        
        # Initialize the full tree image using Tile
        super().__init__(width=image.get_width(), height=image.get_height(), x=x-7, y=y-325//2+17, image=image, image_loaded=True)
        
        # Set `self.rect` to represent only the base (50x50) for collision
        # Position it at the bottom center of the tree image
        self.collision_rect = pygame.rect.Rect(0,0,10,10)
        self.collision_rect.center = (self.rect.x+7,self.rect.y+self.rect.height//2-13)

    def update(self, movement):
        # Update the position of the image's main rect
        super().update(movement)
        self.collision_rect.center = (self.rect.center[0]+7,self.rect.center[1]+self.rect.height//2-25)

