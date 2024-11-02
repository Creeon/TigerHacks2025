import pygame
import math
import time
import random
#from tiles import Tile, InteractableTile, CropTile, WheatTile
from tiles import *

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
    "wheat" : "images/best_wheat.png"
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

#********INVENTORY CLASS********
class Inventory():
    #initializiation
    def __init__(self):
        self.items=dict()
        self.image=pygame.Surface((50,40))
        self.image.fill((125,125,125))
        self.rect = self.image.get_rect(center=(30,25))
    #Function to add item to inventory
    def add_item(self,item):
        if item in self.items.keys():
            self.items[item]["count"]+=1
        else:
            self.items[item] = dict({
                "image" : pygame.transform.scale(pygame.image.load(item_images[item]).convert_alpha(), (25,25)),
                "count" : 1
            })
            self.image=pygame.Surface((self.image.get_width() + 50, self.image.get_height))
            self.rect = self.image.get_rect(center=(self.image.get_width()//2+5, 25))
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        current_x = 25
        for item in self.items.items():
            screen.blit(item["image"], item["image"].get_rect(center=(current_x, 20)))
            current_x+=50
        
class Player(pygame.sprite.Sprite):
    def __init__(self):
        global screen_width, screen_height
        
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((0, 0, 0))

        self.rect = self.image.get_rect(center=(screen_width // 2, screen_height // 2))
        
    def update(self, movement):
        self.rect = self.rect.move(movement[0], movement[1])
        
        
    def checkXCollision(self, x, movex):
        if movex > 0:
            right = self.rect.right
            if right > x:
                return movex
            if right+movex > x:
                return x-right
            else:
                return movex
        elif movex < 0:
            left = self.rect.left
            if left < x:
                return movex
            if left+movex < x:
                return x-left
            else:
                return movex
        return 0
    
    def checkYCollision(self, y, movey):
        if movey < 0:
            top = self.rect.top
            if top < y:
                return movey
            if top+movey < y:
                return y-top
            else:
                return movey
        elif movey > 0:
            bottom = self.rect.bottom
            if bottom > y:
                return movey
            if bottom+movey > y:
                return y-bottom
            else:
                return movey
        return 0
        
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
        tiles.add(Tile(width=50, height=50, x=x, y=y, image="images/grass.png", collision=False))
        x+=50
    tiles.add(Tile(width=50, height=50, x=x, y=y, color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))))
    y+=50
    x=25
for i in range(50):
    tiles.add(Tile(width=50, height=50, x=x, y=y, color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))))
    x+=50
layers = [tiles, pygame.sprite.Group(), pygame.sprite.Group(), pygame.sprite.Group()]
layers[3].add(player)
layers[2].add(InteractableTile(x=150, y=150, image="images/better_wheat.png"))
layers[2].add(InteractableTile(x=450, y=150, image="images/better_wheat.png"))
layers[2].add(WheatTile(100,500))



last = time.time()
delays = []
while not quit:
    # Process player inputs.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            keys_pressed.append(event.key)
            match event.key:
                case pygame.K_l | pygame.K_e:
                    for layer in layers:
                        for s in layer:
                            if type(s) == WheatTile:
                                if pygame.Vector2(s.rect.center).distance_to(pygame.Vector2(player.rect.center)) <= s.interact_range:
                                    s.interact()
        elif event.type == pygame.KEYUP:
            keys_pressed.remove(event.key)
        

    screen.fill((50,0,0))  # Fill the display with a solid color
    
    player_speed = getSpeed(keys_pressed, 10)
    
    for tile in tiles:
        if tile.collision:
            player_speed = checkCollision(player.rect, tile.rect, player_speed)
    i = 0
    for layer in layers:
        if not i == 3:
            layer.update([-player_speed[0], -player_speed[1]])
        i+=1
    
    #print(player_speed)

    #tiles.draw(screen)
    #screen.blit(player.image,player.rect)
    
    for layer in layers:
        layer.draw(screen)

    pygame.display.flip()  # Refresh on-screen display
    delays.append(time.time() - last)
    #print(1 / (sum(delays) / len(delays)))
    if len(delays) > 60:
        delays.pop(0)
    last = time.time()
    clock.tick(max_frames)