import pygame
import math
import time
import random
#from tiles import Tile, InteractableTile, CropTile, WheatTile
from tiles import *
from tools import *
from misc import *

#********INITIALIZE SCREEN/BOARD********
pygame.init()
print(pygame.display.Info())
screen_width, screen_height = 1200, 700 #Initialize screen dimensions
screen = pygame.display.set_mode((screen_width,screen_height)) #Initialize screen to size
clock = pygame.time.Clock() #For use with screen updating and timed events
quit = False #Game loop quit boolean
max_frames = 60 #Frame rate
keys_pressed = [] #Stores key currently being pressed (for harvest time tracking)

#Dictionary of item images
item_images = dict({
    "Wheat" : "images/best_wheat.png",
    "grass" : "images/grass.png",
    "Pumpkin" : "images/pumpkin.png"
})

#Function to check if player and screen-edge tile are touching
def checkCollision(moving_rect: pygame.rect.Rect, static_rect: pygame.rect.Rect, movement):
    if moving_rect.colliderect(static_rect):
        return movement
    new_movement = [movement[0], movement[1]]
    moving_rect.x += movement[0]
    if moving_rect.colliderect(static_rect):
        new_movement[0] = movement[0] + ((static_rect.right - moving_rect.left) if (movement[0] < 0) else (-moving_rect.right + static_rect.left))
    moving_rect.x -= movement[0]
    moving_rect.y += movement[1]
    if moving_rect.colliderect(static_rect):
        new_movement[1] = movement[1] + ((-moving_rect.bottom + static_rect.top) if (movement[1] > 0) else (static_rect.bottom - moving_rect.top))
    moving_rect.y -= movement[1]
    
    return new_movement

def checkRange(rect_1: pygame.rect.Rect, rect_2:pygame.rect.Rect, distance):
    rect_1.inflate_ip(distance*2,distance*2)
    would_collide = rect_1.colliderect(rect_2)
    rect_1.inflate_ip(-distance*2,-distance*2)
    return would_collide

#********INVENTORY CLASS********
class Inventory():
    #initializiation
    def __init__(self):
        self.items=dict()
        self.image=pygame.Surface((50,90))
        self.image.fill((125,125,125))
        self.rect = self.image.get_rect(center=(30,55))
        self.font = pygame.font.Font(None, 24)
    def add_item(self,item):
        if item in self.items.keys():
            self.items[item]["count"]+=1
            self.items[item]["visual_count"] = self.font.render(str(self.items[item]["count"]), True, (255,255,255))
        else:
            self.items[item] = dict({
                "image" : pygame.transform.scale(pygame.image.load(item_images[item]).convert_alpha(), (25,25)),
                "count" : 1,
                "visual_count" : self.font.render(str(1), True, (255,255,255))
            })
            self.image=pygame.Surface((self.image.get_width() + 50, self.image.get_height()))
            self.rect = self.image.get_rect(center=(self.image.get_width()//2+5, 30))
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        current_x = 25
        for item in self.items.items():
            screen.blit(item[1]["image"], item[1]["image"].get_rect(center=(current_x, 25)))
            screen.blit(item[1]["visual_count"], item[1]["visual_count"].get_rect(center=(current_x, 50)))
            current_x+=50
        
class Player(pygame.sprite.Sprite):
    def __init__(self):
        global screen_width, screen_height
        
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((0, 0, 0))

        self.rect = self.image.get_rect(center=(screen_width // 2, screen_height // 2))
        self.orientation = 270
        
        self.animation_change = 30
        self.idle = pygame.Surface((50, 50))
        self.idle.fill((0, 0, 0))
        self.walking = pygame.Surface((50, 50))
        self.walking.fill((0,0,200))
        
        self.frame_counter=0
        
    def update(self, movement):
        #self.rect = self.rect.move(movement[0], movement[1])
        if movement[0]==0 and movement[1]==0:
            self.frame_counter=0
            self.image=self.idle
        else:
            if self.frame_counter%30==0:
                if self.image==self.idle:
                    self.image=self.walking
                else:
                    self.image=self.idle
            self.frame_counter+=1
        if movement[0] == 0:
            if not movement[1] == 0:
                self.orientation = 270 if movement[1] > 0 else 90
        else:
            if not movement[0] == 0:
                self.orientation = 0 if movement[0] > 0 else 180
        print(self.orientation)
        
def getSpeed(keys, speed):
    target_speed = [0,0,0,0] #+x -x +y -y
    for key in keys:
        match key:
            case pygame.K_w:
                target_speed[2] = 1
            case pygame.K_a:
                target_speed[0] = 1
            case pygame.K_s:
                target_speed[3] = 1
            case pygame.K_d:
                target_speed[1] = 1
    target_speed = [-target_speed[0]+target_speed[1],-target_speed[2]+target_speed[3]]
    if (not target_speed[0] == 0) and (not target_speed[1] == 0):
        target_speed[0] = target_speed[0] * speed * math.sqrt(2) / 2
        target_speed[1] = target_speed[1] * speed * math.sqrt(2) / 2
    else:
        target_speed[0] = target_speed[0] * speed
        target_speed[1] = target_speed[1] * speed
    return target_speed

player = Player()

#tile = Tile(width=100, height=100, x = 100, y=100)
#tile2 = Tile(width=100, height=100, x = 220, y=200, color=(0,255,0))
keys_pressed = []

tiles = pygame.sprite.Group()
layers = [tiles, pygame.sprite.Group(), pygame.sprite.Group(), pygame.sprite.Group()]

x=25
y=25
for i in range(50):
    tiles.add(Tile(width=50, height=50, x=x, y=y, color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))))
    x+=50
x=25
y+=50
for i in range(48):
    tiles
    tiles.add(Tile(width=50, height=50, x=x, y=y, color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))))
    x+=50
    for i in range(48):
        if random.randint(0,1) == 1:
            tiles.add(Tile(width=50, height=50, x=x, y=y, image="images/grass.png", collision=False))
            layers[1].add(WheatTile(x,y))
        else:
            tiles.add(Tile(width=50, height=50, x=x, y=y, image="images/grass.png", collision=False))
            layers[1].add(PumpkinTile(x,y))
        x+=50
    tiles.add(Tile(width=50, height=50, x=x, y=y, color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))))
    y+=50
    x=25
for i in range(50):
    tiles.add(Tile(width=50, height=50, x=x, y=y, color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))))
    x+=50
layers[3].add(player)
layers[2].add(Gate(400,400, 90))
#layers[2].add(InteractableTile(x=150, y=150, image="images/better_wheat.png"))
#layers[2].add(InteractableTile(x=450, y=150, image="images/better_wheat.png"))
#layers[2].add(WheatTile(100,500))



last = time.time()
delays = []

inventory = Inventory()
for i in range(100):
    inventory.add_item("grass")
    
tool = Tool("test", "images/temp_tool.png", 35, 650, player)
menu = Menu(background_image="images/angry.jpg")

while not quit:
    # Process player inputs.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            keys_pressed.append(event.key)
            if(event.key == pygame.K_e):
                for layer in layers:
                    for s in layer:
                        if isinstance(s, Gate):
                            if checkRange(player.rect, s.rect, s.interact_range):
                                s.interact()
            elif(event.key == pygame.K_k):
                tool.hidden=False
            elif(event.key == pygame.K_i):
                inventory.hidden = not inventory.hidden
            elif(event.key == pygame.K_p):
                menu.hidden = not menu.hidden
        elif event.type == pygame.KEYUP:
            keys_pressed.remove(event.key)
            if event.key == pygame.K_k:
                tool.hidden=True

    screen.fill((50,0,0))  # Fill the display with a solid color
    
    player_speed = getSpeed(keys_pressed, 10)
    
    for layer in layers:
        for tile in layer:
            if (not type(tile) == Player) and tile.collision:
                player_speed = checkCollision(player.rect, tile.rect, player_speed)
            if not tool.hidden:
                if isinstance(tile, CropTile):
                    if tile.rect.colliderect(tool.rect):
                        tile.interact(inventory)
    i = 0
    for layer in layers:
        if not i == 3:
            layer.update([-player_speed[0], -player_speed[1]])
        i+=1
        
    player.update(player_speed)
    
    #print(player_speed)

    #tiles.draw(screen)
    #screen.blit(player.image,player.rect)
    
    for layer in layers:
        layer.draw(screen)
    if not inventory.hidden:
        inventory.draw(screen)
    tool.update()
    if not tool.hidden:
        screen.blit(tool.image, tool.rect)
    if not menu.hidden:
        screen.blit(menu.image, menu.rect)

    pygame.display.flip()  # Refresh on-screen display
    delays.append(time.time() - last)
    #print(1 / (sum(delays) / len(delays)))
    if len(delays) > 60:
        delays.pop(0)
    last = time.time()
    clock.tick(max_frames)