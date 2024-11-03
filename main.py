import pygame
import sys
from button import Button
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
    "Pumpkin" : "images/pumpkin.png"
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
            "90" : pygame.transform.scale(pygame.image.load("images/CharacterFrames/back_idle.png").convert_alpha(), (100,100)),
            "180" : pygame.transform.scale(pygame.image.load("images/CharacterFrames/left_walk.png").convert_alpha(), (100,100)),
            "270" : pygame.transform.scale(pygame.image.load("images/CharacterFrames/for_walk1.png").convert_alpha(), (100,100))
        })
        self.walking_2 = dict({
            "0" : pygame.transform.scale(pygame.image.load("images/CharacterFrames/face_right.png").convert_alpha(), (100,100)),
            "90" : pygame.transform.scale(pygame.image.load("images/CharacterFrames/back_idle.png").convert_alpha(), (100,100)),
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

    coins = 50
        
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
    
tool = Tool("test", "images/tractor.png", 500, 500, player)
menu = Menu(background_image="images/angry.jpg")
day_font = pygame.font.Font(None, 48)
day_writing = day_font.render("Day " + str(day), True, (0,0,0))
day_rect = day_writing.get_rect(center=(screen_width-100, 50))

#************SHOP MENU************
#Font size function from Baraltech's tutorial. Found on his gitHub as part of his menu tutorial here: https://github.com/baraltech/Menu-System-PyGame/blob/main/main.py
def get_font(size):
    return pygame.font.Font(None, size)

#Functions to buy seeds
def buyWheat():
    player.coins -= 10
    #TODO: Add 10 wheat seeds to inventory
    print("COINS: ")
    print(player.coins)
def buyGMOWheat():
    player.coins -= 7
    #TODO: Add 10 seeds inventory
    print("COINS: ")
    print(player.coins)
def buyPumpkin():
    player.coins -= 15
    #TODO: Add 10 seeds to inventory
    print("COINS: ")
    print(player.coins)
def buyGMOPumpkin():
    player.coins -= 11
    #TODO: Add 10 seeds to inventory
    print("COINS: ")
    print(player.coins)

#Class to store static variable so shop menu can open and close
class shopMenu:
    menu_quit = True
    screen = pygame.display.set_mode((screen_width,screen_height))
    menu_mouse_pos = pygame.mouse.get_pos() #Get mouse position
    seed_button = Button(image = None, pos = (0,0), text_input = None, font = get_font(100), base_color = (255, 255, 255), hovering_color = (0, 0, 0))
    tools_button = Button(image = None, pos = (0,0), text_input = None, font = get_font(100), base_color = (255, 255, 255), hovering_color = (0, 0, 0))

#Function to open and close main shop menu, initialize, etc
def shopMenuShow():
    background = pygame.transform.scale(pygame.image.load("images/MenuSprites/menu1.png").convert_alpha(), (400, 400))
    shopMenu.screen.blit(background, background.get_rect(center=(screen_width//2, screen_height//2)))

    shopMenu.menu_quit = not shopMenu.menu_quit
    #While quit is false
    print("Shop menu open!")
    while (shopMenu.menu_quit == False):
        #Credit for the majority of this menu structure AND Button class to Baraltech in this tutorial (https://www.youtube.com/watch?v=GMBqjxcKogA)
        menu_mouse_pos = pygame.mouse.get_pos() #Get mouse position
        shop_text_header = get_font(48).render("SHOP", True, (255, 255, 255))
        shop_menu_rect = shop_text_header.get_rect(center = (screen_width // 2,(screen_height - 300)// 2))

        shopMenu.seed_button = Button(image = pygame.transform.scale(pygame.image.load("images/MenuSprites/button1.png"), (180, 120)), pos = (screen_width // 2,(screen_height - 120)// 2),
                             text_input = "SEEDS", font = get_font(48), base_color = (0,255,0), hovering_color = (0, 0, 0))
        shopMenu.tools_button = Button(image = pygame.transform.scale(pygame.image.load("images/MenuSprites/button1.png"), (180, 120)), pos = (screen_width // 2,(screen_height + 200)// 2),
                              text_input = "TOOLS", font = get_font(48), base_color = (0, 0, 255), hovering_color = (0, 0, 0))
        
        shopMenu.screen.blit(shop_text_header, shop_menu_rect)

        for button in [shopMenu.seed_button, shopMenu.tools_button]:
            button.changeColor(menu_mouse_pos)
            button.update(shopMenu.screen)
    
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                keys_pressed.append(event.key)
                if event.key == pygame.K_x:
                    shopMenu.menu_quit=True
            if event.type == pygame.KEYUP:
                keys_pressed.remove(event.key)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if shopMenu.seed_button.checkForInput(pygame.mouse.get_pos()):
                    print("SEEDS!")
                    seedShop()
                if shopMenu.tools_button.checkForInput(pygame.mouse.get_pos()):
                    print("TOOLS!")
                    toolsShop()
                

        pygame.display.update()

#Function to open seed window in shop
def seedShop():
    print("Seed shop!")
    
    while (shopMenu.menu_quit == False):
        seed_mouse_pos = pygame.mouse.get_pos()

        background = pygame.transform.scale(pygame.image.load("images/MenuSprites/menu1.png").convert_alpha(), (400, 400))
        shopMenu.screen.blit(background, background.get_rect(center=(screen_width//2, screen_height//2)))

        seed_text = get_font(48).render("SEED SHOP", True, (0, 30, 0))
        seed_rect = seed_text.get_rect(center = (screen_width // 2, (screen_height // 2) - 140))
        shopMenu.screen.blit(seed_text, seed_rect)

        #initialize buttons
        seed_back = Button(image = pygame.transform.scale(pygame.image.load("images/MenuSprites/button1.png"), (100, 70)), pos = (screen_width // 2, (screen_height // 2) + 100),
                           text_input = "BACK", font = get_font(20), base_color = (255, 255, 255), hovering_color = (100,200))
        wheat_button = Button(image = pygame.transform.scale(pygame.image.load("images/MenuSprites/button2.png"), (100, 70)), pos = ((screen_width // 2) - 50, (screen_height // 2) - 50),
                           text_input = "WHEAT", font = get_font(20), base_color = (255, 255, 255), hovering_color = (0, 0, 0))
        gmo_wheat_button = Button(image = pygame.transform.scale(pygame.image.load("images/MenuSprites/button2.png"), (100, 70)), pos = ((screen_width // 2) + 50, (screen_height // 2) - 50),
                           text_input = "GMO WHEAT", font = get_font(20), base_color = (255, 255, 255), hovering_color = (0, 0, 0))
        pumpkin_button = Button(image =pygame.transform.scale(pygame.image.load("images/MenuSprites/button2.png"), (100, 70)), pos = ((screen_width // 2) - 50, (screen_height // 2) + 50),
                           text_input = "PUMPKIN", font = get_font(20), base_color = (255, 255, 255), hovering_color = (0, 0, 0))
        gmo_pumpkin_button = Button(image = pygame.transform.scale(pygame.image.load("images/MenuSprites/button2.png"), (100, 70)), pos = ((screen_width // 2) + 50, (screen_height // 2) + 50),
                           text_input = "GMO PUMPKIN", font = get_font(20), base_color = (255, 255, 255), hovering_color = (0, 0, 0))

        #Display Buttons
        seed_back.changeColor(seed_mouse_pos)
        seed_back.update(shopMenu.screen)
        wheat_button.changeColor(seed_mouse_pos)
        wheat_button.update(shopMenu.screen)
        gmo_wheat_button.changeColor(seed_mouse_pos)
        gmo_wheat_button.update(shopMenu.screen)
        pumpkin_button.changeColor(seed_mouse_pos)
        pumpkin_button.update(shopMenu.screen)
        gmo_pumpkin_button.changeColor(seed_mouse_pos)
        gmo_pumpkin_button.update(shopMenu.screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                keys_pressed.append(event.key)
                if event.key == pygame.K_x:
                    shopMenu.menu_quit=True
            elif event.type == pygame.KEYUP:
                keys_pressed.remove(event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if seed_back.checkForInput(pygame.mouse.get_pos()):
                    print("BACK SEEDS!")
                    shopMenu.menu_quit = not shopMenu.menu_quit
                    shopMenuShow()
                if wheat_button.checkForInput(pygame.mouse.get_pos()):
                    print("WHEAT!")
                    buyWheat()
                if gmo_wheat_button.checkForInput(pygame.mouse.get_pos()):
                    print("GMO WHEAT!")
                    buyGMOWheat()
                if pumpkin_button.checkForInput(pygame.mouse.get_pos()):
                    print("PUMPKIN!")
                    buyPumpkin()
                if gmo_pumpkin_button.checkForInput(pygame.mouse.get_pos()):
                    print("GMO PUMPKIN!")
                    buyGMOPumpkin()


    

        pygame.display.update()


#Function to open tool window in shop
def toolsShop():
    print("Tool shop!")

    while (shopMenu.menu_quit == False):
        tools_mouse_pos = pygame.mouse.get_pos()

        background = pygame.transform.scale(pygame.image.load("images/MenuSprites/menu1.png").convert_alpha(), (400, 400))
        shopMenu.screen.blit(background, background.get_rect(center=(screen_width//2, screen_height//2)))

        tools_text = get_font(48).render("TOOLS SCREEN", True, (0, 0, 30))
        tools_rect = tools_text.get_rect(center = (screen_width // 2, (screen_height - 200)// 2))
        shopMenu.screen.blit(tools_text, tools_rect)

        tools_back = Button(image = None, pos = (screen_width // 2, (screen_height - 100)// 2),
                           text_input = "BACK", font = get_font(48), base_color = (255, 255, 255), hovering_color = (0, 0, 0))
        
        tools_back.changeColor(tools_mouse_pos)
        tools_back.update(shopMenu.screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                keys_pressed.append(event.key)
                if event.key == pygame.K_x:
                    shopMenu.menu_quit=True
            elif event.type == pygame.KEYUP:
                keys_pressed.remove(event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if tools_back.checkForInput(pygame.mouse.get_pos()):
                    print("BACK SEEDS!")
                    shopMenu.menu_quit = not shopMenu.menu_quit
                    shopMenuShow()

        pygame.display.update()


def day_change():
    global player, layers, day
    for layer in layers:
        for tile in layer:
            if isinstance(tile, CropTile):
                tile.iterate()

shopping = False

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
            elif(event.key == pygame.K_x):
                print("MENU!")
                shopMenuShow()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if shopMenu.seed_button.checkForInput(shopMenu.menu_mouse_pos):
                        seedShop()
                    if shopMenu.tools_button.checkForInput(shopMenu.menu_mouse_pos):
                        toolsShop()  
            elif(event.key == pygame.K_r):
                day+=1
                day_writing = day_font.render("Day " + str(day), True, (0,0,0))
                day_rect = day_writing.get_rect(center=(screen_width-100, 50))
                day_change()
        elif event.type == pygame.KEYUP:
            keys_pressed.remove(event.key)
            if event.key == pygame.K_k:
                tool.hidden=True
    if not shopping:
        screen.fill((6,64,43))  # Fill the display with a solid color
        
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