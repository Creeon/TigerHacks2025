import pygame
import math
import time
import random
#from tiles import Tile, InteractableTile, CropTile, WheatTile


pygame.init()
print(pygame.display.Info())
screen_width, screen_height = 1200, 700
day = 1
screen = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()
quit = False
max_frames = 60
keys_pressed = []

from tiles import *
from tools import *
from misc import *

item_images = dict({
    "Wheat" : "images/best_wheat.png",
    "grass" : "images/grass.png",
    "Pumpkin" : "images/pumpkin.png",
    "Carrot" : "images/Crops/harvested_car.png",
    "Watermelon" : "images/Crops/harvested_watermelon.png",
    "fertilizer" : "images/fertilizer.png"
})

player_walk = dict({
    "forward1" : "images/For_Walk1.png",
    "forward2" : "images/For_Walk2.png",
    "Idle" : "images/Idle.png"
})

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

class Inventory():
    def __init__(self):
        self.items=dict()
        self.image=pygame.Surface((50,90))
        self.image.fill((181,153,128))
        self.rect = self.image.get_rect(center=(30,55))
        self.font = pygame.font.Font(None, 24)
        self.hidden = False
    def add_item(self,item,count=1,custom_image=None):
        if item in self.items.keys():
            self.items[item]["count"]+=count
            self.items[item]["visual_count"] = self.font.render(str(self.items[item]["count"]), True, (255,255,255))
        else:
            self.items[item] = dict({
                "image" : pygame.transform.scale(pygame.image.load(item_images[item if custom_image == None else custom_image]).convert_alpha(), (25,25)),
                "count" : count,
                "visual_count" : self.font.render(str(count), True, (255,255,255))
            })
            self.image=pygame.Surface((self.image.get_width() + 50, self.image.get_height()))
            self.image.fill((181,153,128))
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
        '''self.image = pygame.Surface((50, 50))
        self.image.fill((0, 0, 0))

        self.rect = self.image.get_rect(center=(screen_width // 2, screen_height // 2))'''
        
        
        
        self.animation_change = 20
        self.walking_1 = dict({
            "0" : pygame.transform.scale(pygame.image.load("images/CharacterFrames/right_walk.png").convert_alpha(), (100,100)),
            "90" : pygame.transform.scale(pygame.image.load("images/CharacterFrames/back_walk1.png").convert_alpha(), (100,100)),
            "180" : pygame.transform.scale(pygame.image.load("images/CharacterFrames/left_walk.png").convert_alpha(), (100,100)),
            "270" : pygame.transform.scale(pygame.image.load("images/CharacterFrames/for_walk1.png").convert_alpha(), (100,100))
        })
        self.walking_2 = dict({
            "0" : pygame.transform.scale(pygame.image.load("images/CharacterFrames/face_right.png").convert_alpha(), (100,100)),
            "90" : pygame.transform.scale(pygame.image.load("images/CharacterFrames/back_walk2.png").convert_alpha(), (100,100)),
            "180" : pygame.transform.scale(pygame.image.load("images/CharacterFrames/face_left.png").convert_alpha(), (100,100)),
            "270" : pygame.transform.scale(pygame.image.load("images/CharacterFrames/for_walk2.png").convert_alpha(), (100,100))
        })
        self.idle = dict({
            "0" : pygame.transform.scale(pygame.image.load("images/CharacterFrames/face_right.png").convert_alpha(), (100,100)),
            "90" : pygame.transform.scale(pygame.image.load("images/CharacterFrames/back_idle.png").convert_alpha(), (100,100)),
            "180" : pygame.transform.scale(pygame.image.load("images/CharacterFrames/face_left.png").convert_alpha(), (100,100)),
            "270" : pygame.transform.scale(pygame.image.load("images/CharacterFrames/Idle.png").convert_alpha(), (100,100))
        })
        
        self.image = self.idle["270"]
        self.rect = self.image.get_rect(center=(screen_width // 2, screen_height // 2))
        self.orientation = 270
        self.last_orientation = 270
        
        self.frame_counter=0
        
        self.walking_type = 0
        
        self.current_tool = None
        self.tools = []
        
        self.current_seed = 0

        self.seeds = [
            dict({
                "name" : "Wheat",
                "count" : 100
            }),
            dict({
                "name" : "Pumpkin",
                "count" : 100
            }),
                        dict({
                "name" : "Watermelon",
                "count" : 100
            }),
            dict({
                "name" : "Carrot",
                "count" : 100
            })
        ]
        
    def update(self, movement):
        #self.rect = self.rect.move(movement[0], movement[1])
        if movement[0] == 0:
            if not movement[1] == 0:
                self.orientation = 270 if movement[1] > 0 else 90
        else:
            if not movement[0] == 0:
                self.orientation = 0 if movement[0] > 0 else 180
        if movement[0]==0 and movement[1]==0:
            self.frame_counter=0
            self.walking_type=0
            self.image = self.idle[str(self.orientation)]
        else:
            if self.frame_counter%self.animation_change==0 or not self.last_orientation == self.orientation:
                self.frame_counter=0
                self.walking_type+=1
                if self.walking_type >= 2:
                    self.walking_type = 0
                match self.walking_type:
                    case 0:
                        self.image = self.walking_2[str(self.orientation)]
                    case 1:
                        self.image = self.walking_1[str(self.orientation)]
            self.frame_counter+=1
        print(self.orientation)
        self.last_orientation = self.orientation
        
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

map = [[None for i in range(200)] for i in range(200)]
y=0
for i in range(0,200):
    x=0
    if i == 0 or i == 199:
        for i2 in range(200):
            map[i][i2] = Tile(x=x,y=y,image=images["stone"],image_loaded=True)
            x+=50
    else:
        map[i][0] = Tile(x=x,y=y,image=images["stone"],image_loaded=True)
        x+=50
        for i2 in range(2,199):
            map[i][i2] = GroundTile(x,y)
            x+=50
        map[i][199] = Tile(x=x,y=y,image=images["stone"],image_loaded=True)
    y+=50

last = time.time()
delays = []

inventory = Inventory()
inventory.add_item("seeds", count=player.seeds[player.current_seed]["count"], custom_image=player.seeds[player.current_seed]["name"])
for i in range(100):
    inventory.add_item("grass")
inventory.add_item("fertilizer", count=100)
    
player.tools.append(Tractor(player))
player.tools.append(WateringCan(player))
player.tools.append(WaterPlane(player))
player.tools.append(Shovel(player))
player.tools.append(Sickle(player))
player.tools.append(FertilizingMachine(player))

menu = Menu(background_image="images/angry.jpg")
day_font = pygame.font.Font(None, 48)
day_writing = day_font.render("Day " + str(day), True, (0,0,0))
day_rect = day_writing.get_rect(center=(screen_width-100, 50))

house = House(350,350)

def day_change():
    global player, map, day
    for row in map:
        for tile in row:
            if isinstance(tile, GroundTile):
                if not tile.crop == None:
                    tile.crop.iterate(tile.getRisk())
                tile.iterate()



while not quit:
    # Process player inputs.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            keys_pressed.append(event.key)
            """if(event.key == pygame.K_e):
                for row in map:
                    for tile in row:
                        if isinstance(tile, Gate):
                            if checkRange(player.rect, tile.rect, tile.interact_range):
                                s.interact()"""
            match event.key:
                case pygame.K_k:
                    if not player.current_tool==None:
                        player.current_tool.hidden=False
                case pygame.K_i:
                    inventory.hidden = not inventory.hidden
                case pygame.K_p:
                    menu.hidden = not menu.hidden
                case pygame.K_r:
                    day+=1
                    day_writing = day_font.render("Day " + str(day), True, (0,0,0))
                    day_rect = day_writing.get_rect(center=(screen_width-100, 50))
                    day_change()
                case pygame.K_1:
                    if len(player.tools) >= 1:
                        player.current_tool = player.tools[0]
                case pygame.K_2:
                    if len(player.tools) >= 2:
                        player.current_tool = player.tools[1]
                case pygame.K_3:
                    if len(player.tools) >= 3:
                        player.current_tool = player.tools[2]
                case pygame.K_4:
                    if len(player.tools) >= 4:
                        player.current_tool = player.tools[3]
                case pygame.K_5:
                    if len(player.tools) >= 5:
                        player.current_tool = player.tools[4]
                case pygame.K_6:
                    if len(player.tools) >= 6:
                        player.current_tool = player.tools[5]
                case pygame.K_LEFT:
                    player.current_seed-=1
                    if player.current_seed<0:
                        player.current_seed = len(player.seeds)-1
                    inventory.items["seeds"] = dict({
                        "image" : pygame.transform.scale(pygame.image.load(item_images[player.seeds[player.current_seed]["name"]]).convert_alpha(), (25,25)),
                        "count" : player.seeds[player.current_seed]["count"],
                        "visual_count" : inventory.font.render(str(player.seeds[player.current_seed]["count"]), True, (255,255,255))
                    })
                case pygame.K_RIGHT:
                    player.current_seed+=1
                    if player.current_seed >= len(player.seeds):
                        player.current_seed = 0    
                    inventory.items["seeds"] = dict({
                        "image" : pygame.transform.scale(pygame.image.load(item_images[player.seeds[player.current_seed]["name"]]).convert_alpha(), (25,25)),
                        "count" : player.seeds[player.current_seed]["count"],
                        "visual_count" : inventory.font.render(str(player.seeds[player.current_seed]["count"]), True, (255,255,255))
                    })                
        elif event.type == pygame.KEYUP:
            keys_pressed.remove(event.key)
            match event.key:
                case pygame.K_k:
                    if not player.current_tool == None:
                        player.current_tool.hidden=True

    screen.fill((6,64,43))  # Fill the display with a solid color
    
    player_speed = getSpeed(keys_pressed, 10)
    
    for row in map:
        for tile in row:
            if (not tile == None) and tile.collision:
                player_speed = checkCollision(player.rect, tile.rect, player_speed)
            if (not player.current_tool == None) and not player.current_tool.hidden:
                """if isinstance(tile, CropTile):
                    if tile.rect.colliderect(tool.rect):
                        tile.interact(inventory)"""
                if isinstance(tile, GroundTile):
                    if tile.rect.colliderect(player.current_tool.rect):
                        if player.current_tool.type == "tilling":
                            if not tile.tilled:
                                tile.tilled=True
                        elif player.current_tool.type == "watering":
                            if tile.tilled and not tile.watered:
                                tile.watered=True
                        elif player.current_tool.type == "planting":
                            if tile.tilled and tile.crop==None:
                                if player.seeds[player.current_seed]["count"] > 0:
                                    inventory.items["seeds"]["count"]-=1
                                    player.seeds[player.current_seed]["count"]-=1
                                    inventory.items["seeds"]["visual_count"] = inventory.font.render(str(inventory.items["seeds"]["count"]), True, (255,255,255))
                                    match player.seeds[player.current_seed]["name"]:
                                        case "Pumpkin":
                                            tile.crop=PumpkinTile(tile.rect.center[0], tile.rect.center[1])
                                        case "Wheat":
                                            tile.crop=WheatTile(tile.rect.center[0], tile.rect.center[1])
                                        case "Carrot":
                                            tile.crop=CarrotTile(tile.rect.center[0], tile.rect.center[1])
                        elif player.current_tool.type == "harvesting":
                            if (not tile.crop==None) and (tile.crop.dead or tile.crop.grown):
                                tile.crop = None
                        elif player.current_tool.type == "fertilizing":
                            if tile.fertilized==False:
                                if "fertilizer" in inventory.items.keys():
                                    if inventory.items["fertilizer"]["count"]>0:
                                        inventory.items["fertilizer"]["count"]-=1
                                        inventory.items["fertilizer"]["visual_count"] = inventory.font.render(str(inventory.items["fertilizer"]["count"]), True, (255,255,255))
                                        tile.fertilize()
    player_speed=checkCollision(player.rect,house.rect,player_speed)
    for row in map:
        for tile in row:
            if not tile == None:
                tile.update([-player_speed[0], -player_speed[1]])
        
    house.update([-player_speed[0], -player_speed[1]])        
        
    player.update(player_speed)
    
    #print(player_speed)

    #tiles.draw(screen)
    #screen.blit(player.image,player.rect)
    
    for row in map:
        for tile in row:
            if not tile == None:
                tile.display(screen)
    if not inventory.hidden:
        inventory.draw(screen)
        
    screen.blit(house.image,house.rect)
        
    screen.blit(player.image, player.rect)
    
    if not player.current_tool == None:
        player.current_tool.update()
    
    if (not player.current_tool == None) and not player.current_tool.hidden:
        screen.blit(player.current_tool.image, player.current_tool.rect)
        
    screen.blit(day_writing, day_rect)
        
    if not menu.hidden:
        screen.blit(menu.image, menu.rect)

        

    pygame.display.flip()  # Refresh on-screen display
    delays.append(time.time() - last)
    #print(1 / (sum(delays) / len(delays)))
    if len(delays) > 60:
        delays.pop(0)
    last = time.time()
    clock.tick(max_frames)