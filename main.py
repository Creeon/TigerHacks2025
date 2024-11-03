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
from button import *

item_images = dict({
    "Wheat" : "images/Crops/wheat2.png",
    "Pumpkin" : "images/Crops/pum2.png",
    "Carrot" : "images/Crops/car2.png",
    "Watermelon" : "images/Crops/watermelon2.png",
    "Corn" : "images/Crops/corn2.png",
    "GMO_Wheat" : "images/Crops/wheat2.png",
    "grass" : "images/grass.png",
    "GMO_Pumpkin" : "images/Crops/pum2.png",
    "GMO_Carrot" : "images/Crops/car2.png",
    "GMO_Watermelon" : "images/Crops/watermelon2.png",
    "GMO_Corn" : "images/Crops/corn2.png",
    "Lettuce" : "images/Crops/watermelon2.png",
    "GMO_Lettuce" : "images/Crops/watermelon2.png",
    "fertilizer" : "images/fertilizer.png",
    "grass" : "images/grass.png"
})

grass_images = dict({
    "Spring" : pygame.transform.scale(pygame.image.load("images/HomeGrown/grass_tile_spring.png").convert_alpha(), (50,50)),
    "Summer" : pygame.transform.scale(pygame.image.load("images/HomeGrown/grass_tile_summer.png").convert_alpha(), (50,50)),
    "Fall" : pygame.transform.scale(pygame.image.load("images/HomeGrown/grass_tile_fall.png").convert_alpha(), (50,50)),
    "Winter" : pygame.transform.scale(pygame.image.load("images/HomeGrown/grass_tile_winter.png").convert_alpha(), (50,50))
})


def get_font(size):
    return pygame.font.Font(None, size)

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
            self.image.fill((110,110,110))
            self.rect = self.image.get_rect(center=(self.image.get_width()//2+5, 30))
    def update_inventory(self):
        for seed in player.seeds:
            difference = seed["count"] - self.items[seed["name"]]["count"]
            if not difference == 0:
                self.add_item(seed["name"], count=difference)
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        current_x = 25
        for item in self.items.items():
            screen.blit(item[1]["image"], item[1]["image"].get_rect(center=(current_x, 25)))
            screen.blit(item[1]["visual_count"], item[1]["visual_count"].get_rect(center=(current_x, 50)))
            current_x+=50
            
class Money():
    def __init__(self):
        self.icon_image = pygame.transform.scale(pygame.image.load("images/coin.png").convert_alpha(), (25,25))
        self.icon_rect = self.icon_image.get_rect(center=(0,0))
        self.font = pygame.font.Font(None, 48)
        self.money = 100
    def draw(self,screen):
        text = self.font.render(str(self.money),True,(255,255,255))
        screen.blit(text,text.get_rect(center=(screen_width-100, 100)))
        screen.blit(self.icon_image, self.icon_image.get_rect(center=(screen_width-100+text.get_width()//2 + 25//2, 100)))
        
        
class Calendar():
    def __init__(self):
        self.font = pygame.font.Font(None, 48)
        self.writing = day_font.render("Day " + str(day), True, (0,0,0))
        self.rect = day_writing.get_rect(center=(screen_width-100, 50))
        self.months = ["Spring", "Summer", "Fall", "Winter"]
        self.current_month = self.months[0]
        self.current_index = 0
        self.current_day = 1
        self.writing = self.font.render(self.current_month + " " + str(self.current_day), True, (0,0,0))
        self.rect = self.writing.get_rect(center=(screen_width-100, 50))
        
    def iterate(self):
        global map
        self.current_day+=1
        if self.current_day%31==0 or self.current_month=="Winter":
            self.current_day=1
            self.current_index+=1
            if self.current_index>=len(self.months):
                self.current_index=0
            self.current_month=self.months[self.current_index]
            for row in map:
                for tile in row:
                    if isinstance(tile, GroundTile):
                        tile.default_image = grass_images[self.current_month]
        self.writing = self.font.render(self.current_month + " " + str(self.current_day), True, (0,0,0))
        self.rect = self.writing.get_rect(center=(screen_width-100, 50))
        for row in map:
            for tile in row:
                if isinstance(tile, GroundTile):
                    if not tile.crop == None:
                        tile.crop.iterate(tile.getRisk(), self.current_month)
                    tile.iterate()
    
    def display(self, screen):
        screen.blit(self.writing,self.rect)
        
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
                "name" : "Carrot",
                "count" : 10
            }),
            dict({
                "name" : "Lettuce",
                "count" : 10
            }),
            dict({
                "name" : "Corn",
                "count" : 10
            }),
            dict({
                "name" : "Watermelon",
                "count" : 10
            }),
            dict({
                "name" : "Wheat",
                "count" : 10
            }),
            dict({
                "name" : "Pumpkin",
                "count" : 10
            }),
            dict({
                "name" : "GMO_Carrot",
                "count" : 0
            }),
            dict({
                "name" : "GMO_Lettuce",
                "count" : 0
            }),
            dict({
                "name" : "GMO_Corn",
                "count" : 0
            }),
            dict({
                "name" : "GMO_Watermelon",
                "count" : 0
            }),
            dict({
                "name" : "GMO_Wheat",
                "count" : 0
            }),
            dict({
                "name" : "GMO_Pumpkin",
                "count" : 0
            })
        ]
        
    def increase_seeds(self, seed, count):
        for s in self.seeds:
            if s["name"]==seed:
                s["count"]+=count
                break
        
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

#*****************SHOP!!!!*****************
#Functions to buy seeds

def buyWheat():
    money.money -= 10
    player.increase_seeds("Wheat", 10)
def buyGMOWheat():
    money.money -= 15
    player.increase_seeds("GMO_Wheat", 10)
def buyPumpkin():
    money.money -= 20
    player.increase_seeds("Pumpkin", 10)
def buyGMOPumpkin():
    money.money -= 25
    player.increase_seeds("GMO_Pumpkin", 10)
def buyCarrot():
    money.money -= 10
    player.increase_seeds("Carrot", 10)
def buyGMOCarrot():
    money.money -= 15
    player.increase_seeds("GMO_Carrot", 10)
def buyLettuce():
    money.money -= 20
    player.increase_seeds("Lettuce", 10)
def buyGMOLettuce():
    money.money -= 25
    player.increase_seeds("GMO_Lettuce", 10)
def buyCorn():
    money.money -= 10
    player.increase_seeds("Corn", 10)
def buyGMOCorn():
    money.money -= 15
    player.increase_seeds("GMO_Corn", 10)
def buyWatermelon():
    money.money -= 20
    player.increase_seeds("Watermelon", 10)
def buyGMOWatermelon():
    money.money -= 25
    player.increase_seeds("GMO_Watermelon", 10)

#Functions to buy tools
def buyTilling2():
    if money.money >= 250:
        money.money -= 250
        player.tools[0]=GardenFork(player)
    #TODO: Add 10 wheat seeds to inventory
def buyTilling3():
    if money.money >= 500:
        money.money -= 500
        player.tools[0]=Tractor(player)
    #TODO: Add 10 wheat seeds to inventory
def buyHarvesting2():
    if money.money >= 250:
        money.money -= 250
        player.tools[4]=Scythe(player)
    #TODO: Add 10 wheat seeds to inventory
def buyHarvesting3():
    if money.money >= 500:
        money.money -= 500
        player.tools[4]=Combine(player)
    #TODO: Add 10 wheat seeds to inventory
def buyWatering2():
    if money.money >= 250:
        money.money -= 250
        player.tools[1]=Hose(player)
    #TODO: Add 10 wheat seeds to inventory
def buyWatering3():
    if money.money >= 500:
        money.money -= 500
        player.tools[1]=WaterPlane(player)
    #TODO: Add 10 wheat seeds to inventory
def buyFertlization2():
    if money.money >= 250:
        money.money -= 250
        player.tools[3]=Sprayer(player)
    #TODO: Add 10 wheat seeds to inventory
def buyFertlization3():
    if money.money >= 500:
        money.money -= 500
        player.tools[3]=FertilizingMachine(player)
    #TODO: Add 10 wheat seeds to inventory
def buyPlanting2():
    if money.money >= 250:
        money.money -= 250
        player.tools[2]=Plow(player)
    #TODO: Add 10 wheat seeds to inventory
def buyPlanting3():
    if money.money >= 500:
        money.money -= 500
        player.tools[2]=Ox(player)
    #TODO: Add 10 wheat seeds to inventory

    
class shopMenu:
    menu_quit = True
    screen = pygame.display.set_mode((screen_width,screen_height))
    menu_mouse_pos = pygame.mouse.get_pos() #Get mouse position
    seed_button = Button(image = None, pos = (0,0), text_input = None, font = get_font(100), base_color = (255, 255, 255), hovering_color = (0, 0, 0))
    tools_button = Button(image = None, pos = (0,0), text_input = None, font = get_font(100), base_color = (255, 255, 255), hovering_color = (0, 0, 0))

#Function to open and close main shop menu, initialize, etc

def shopMenuShow():
    for row in map:
        for tile in row:
            if not tile == None:
                tile.display(screen)
    inventory.update_inventory()
    if not inventory.hidden:
        inventory.draw(screen)
    money.draw(screen)
    background = pygame.transform.scale(pygame.image.load("images/MenuSprites/menu1.png").convert_alpha(), (650, 700))
    shopMenu.screen.blit(background, background.get_rect(center=(screen_width//2, screen_height//2)))

    shopMenu.menu_quit = not shopMenu.menu_quit
    #While quit is false
    print("Shop menu open!")
    while (shopMenu.menu_quit == False):
        #Credit for the majority of this menu structure AND Button class to Baraltech in this tutorial (https://www.youtube.com/watch?v=GMBqjxcKogA)
        menu_mouse_pos = pygame.mouse.get_pos() #Get mouse position
        shop_text_header = get_font(85).render("SHOP", True, (255, 255, 255))
        shop_menu_rect = shop_text_header.get_rect(center = (screen_width // 2,(screen_height - 480)// 2))

        shopMenu.seed_button = Button(image = pygame.transform.scale(pygame.image.load("images/MenuSprites/button1.png"), (250, 180)), pos = (screen_width // 2,(screen_height - 250)// 2),
                             text_input = "SEEDS", font = get_font(75), base_color = (0,255,0), hovering_color = (0, 0, 0))
        shopMenu.tools_button = Button(image = pygame.transform.scale(pygame.image.load("images/MenuSprites/button1.png"), (250, 180)), pos = (screen_width // 2,(screen_height + 250)// 2),
                              text_input = "TOOLS", font = get_font(75), base_color = (0, 0, 255), hovering_color = (0, 0, 0))
        
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
        for row in map:
            for tile in row:
                if not tile == None:
                    tile.display(screen)
        inventory.update_inventory()
        if not inventory.hidden:
            inventory.draw(screen)
        money.draw(screen)

        background = pygame.transform.scale(pygame.image.load("images/MenuSprites/menu1.png").convert_alpha(), (650, 700))
        shopMenu.screen.blit(background, background.get_rect(center=(screen_width//2, screen_height//2)))

        seed_text = get_font(48).render("SEED SHOP", True, (0, 0, 0))
        seed_rect = seed_text.get_rect(center = (screen_width // 2,(screen_height - 580)// 2))
        shopMenu.screen.blit(seed_text, seed_rect)

        #initialize buttons
        seed_back = Button(image = pygame.transform.scale(pygame.image.load("images/MenuSprites/button1.png"), (140, 80)), pos = (screen_width // 2, (screen_height // 2) + 270),
                           text_input = "BACK", font = get_font(20), base_color = (255, 255, 255), hovering_color = (0, 0, 0))
        #SPRING 
        carrot_button = Button(image = pygame.transform.scale(pygame.image.load("images/MenuSprites/button2.png"), (190, 100)), pos = ((screen_width // 2) - 120, (screen_height // 2) - 230),
                           text_input = "CARROT (10)", font = get_font(20), base_color = (0, 0, 0), hovering_color = (0, 255, 0))
        gmo_carrot_button = Button(image = pygame.transform.scale(pygame.image.load("images/MenuSprites/button2.png"), (190, 100)), pos = ((screen_width // 2) + 120, (screen_height // 2) - 230),
                           text_input = "GMO CARROT (15)", font = get_font(20), base_color = (0, 0, 0), hovering_color = (0, 255, 0))
        lettuce_button = Button(image =pygame.transform.scale(pygame.image.load("images/MenuSprites/button2.png"), (190, 100)), pos = ((screen_width // 2) - 120, (screen_height // 2) - 140),
                           text_input = "LETTUCE (20)", font = get_font(20), base_color = (0, 0, 0), hovering_color = (0, 255, 0))
        gmo_lettuce_button = Button(image = pygame.transform.scale(pygame.image.load("images/MenuSprites/button2.png"), (170, 100)), pos = ((screen_width // 2) + 120, (screen_height // 2) - 140),
                           text_input = "GMO LETTUCE (25)", font = get_font(20), base_color = (0, 0, 0), hovering_color = (0, 255, 0))
        #SUMMER
        corn_button = Button(image = pygame.transform.scale(pygame.image.load("images/MenuSprites/button2.png"), (190, 100)), pos = ((screen_width // 2) - 120, (screen_height // 2) - 50),
                           text_input = "CORN (10)", font = get_font(20), base_color = (0, 0, 0), hovering_color = (0, 255, 0))
        gmo_corn_button = Button(image = pygame.transform.scale(pygame.image.load("images/MenuSprites/button2.png"), (190, 100)), pos = ((screen_width // 2) + 120, (screen_height // 2) - 50),
                           text_input = "GMO CORN (15)", font = get_font(20), base_color = (0, 0, 0), hovering_color = (0, 255, 0))
        watermelon_button = Button(image =pygame.transform.scale(pygame.image.load("images/MenuSprites/button2.png"), (190, 100)), pos = ((screen_width // 2) - 120, (screen_height // 2) + 40),
                           text_input = "WATERMELON (20)", font = get_font(20), base_color = (0, 0, 0), hovering_color = (0, 255, 0))
        gmo_watermelon_button = Button(image = pygame.transform.scale(pygame.image.load("images/MenuSprites/button2.png"), (190, 100)), pos = ((screen_width // 2) + 120, (screen_height // 2) + 40),
                           text_input = "GMO WATERMELON (25)", font = get_font(20), base_color = (0, 0, 0), hovering_color = (0, 255, 0))
        #FALL
        wheat_button = Button(image = pygame.transform.scale(pygame.image.load("images/MenuSprites/button2.png"), (190, 100)), pos = ((screen_width // 2) - 120, (screen_height // 2) + 130),
                           text_input = "WHEAT (10)", font = get_font(20), base_color = (0, 0, 0), hovering_color = (0, 255, 0))
        gmo_wheat_button = Button(image = pygame.transform.scale(pygame.image.load("images/MenuSprites/button2.png"), (190, 100)), pos = ((screen_width // 2) + 120, (screen_height // 2) + 130),
                           text_input = "GMO WHEAT (15)", font = get_font(20), base_color = (0, 0, 0), hovering_color = (0, 255, 0))
        pumpkin_button = Button(image =pygame.transform.scale(pygame.image.load("images/MenuSprites/button2.png"), (190, 100)), pos = ((screen_width // 2) - 120, (screen_height // 2) + 220),
                           text_input = "PUMPKIN (20)", font = get_font(20), base_color = (0, 0, 0), hovering_color = (0, 255, 0))
        gmo_pumpkin_button = Button(image = pygame.transform.scale(pygame.image.load("images/MenuSprites/button2.png"), (190, 100)), pos = ((screen_width // 2) + 120, (screen_height // 2) + 220),
                           text_input = "GMO PUMPKIN (25)", font = get_font(20), base_color = (0, 0, 0), hovering_color = (0, 255, 0))

        #Display Buttons
        carrot_button.changeColor(seed_mouse_pos)
        carrot_button.update(shopMenu.screen)
        gmo_carrot_button.changeColor(seed_mouse_pos)
        gmo_carrot_button.update(shopMenu.screen)
        lettuce_button.changeColor(seed_mouse_pos)
        lettuce_button.update(shopMenu.screen)
        gmo_lettuce_button.changeColor(seed_mouse_pos)
        gmo_lettuce_button.update(shopMenu.screen)
        corn_button.changeColor(seed_mouse_pos)
        corn_button.update(shopMenu.screen)
        gmo_corn_button.changeColor(seed_mouse_pos)
        gmo_corn_button.update(shopMenu.screen)
        watermelon_button.changeColor(seed_mouse_pos)
        watermelon_button.update(shopMenu.screen)
        gmo_watermelon_button.changeColor(seed_mouse_pos)
        gmo_watermelon_button.update(shopMenu.screen)
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

        #TODO: MAKE SURE MONEY CANNOT GO NEGATIVE!
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
                    if (money.money >= 10):
                        buyWheat()
                if gmo_wheat_button.checkForInput(pygame.mouse.get_pos()):
                    print("GMO WHEAT!")
                    if (money.money>= 15):
                        buyGMOWheat()
                if pumpkin_button.checkForInput(pygame.mouse.get_pos()):
                    print("PUMPKIN!")
                    if (money.money >= 20):
                        buyPumpkin()
                if gmo_pumpkin_button.checkForInput(pygame.mouse.get_pos()):
                    print("GMO PUMPKIN!")
                    if (money.money >= 25):
                        buyGMOPumpkin()
                if carrot_button.checkForInput(pygame.mouse.get_pos()):
                    print("CARROT!")
                    if (money.money >= 10):
                        buyCarrot()
                if gmo_carrot_button.checkForInput(pygame.mouse.get_pos()):
                    print("GMO CARROT!")
                    if (money.money >= 15):
                        buyGMOCarrot()
                if lettuce_button.checkForInput(pygame.mouse.get_pos()):
                    print("LETTUCE!")
                    if (money.money >= 20):
                        buyLettuce()
                if gmo_lettuce_button.checkForInput(pygame.mouse.get_pos()):
                    print("GMO LETTUCE!")
                    if (money.money >= 25):
                        buyGMOLettuce()
                if corn_button.checkForInput(pygame.mouse.get_pos()):
                    print("CORN!")
                    if (money.money >= 10):
                        buyCorn()
                if gmo_corn_button.checkForInput(pygame.mouse.get_pos()):
                    print("GMO CORN!")
                    if (money.money >= 15):
                        buyGMOCorn()
                if watermelon_button.checkForInput(pygame.mouse.get_pos()):
                    print("WATERMELON!")
                    if (money.money >= 20):
                        buyWatermelon()
                if gmo_watermelon_button.checkForInput(pygame.mouse.get_pos()):
                    print("GMO WATERMELON!")
                    if (money.money >= 25):
                        buyGMOWatermelon()
        pygame.display.update()


#Function to open tool window in shop
def toolsShop():
    print("Tool shop!")

    while (shopMenu.menu_quit == False):
        for row in map:
            for tile in row:
                if not tile == None:
                    tile.display(screen)
        inventory.update_inventory()
        if not inventory.hidden:
            inventory.draw(screen)
        money.draw(screen)
        tools_mouse_pos = pygame.mouse.get_pos()

        background = pygame.transform.scale(pygame.image.load("images/MenuSprites/menu1.png").convert_alpha(), (650, 700))
        shopMenu.screen.blit(background, background.get_rect(center=(screen_width//2, screen_height//2)))

        tools_text = get_font(48).render("TOOL SHOP", True, (0, 0, 0))
        tools_rect = tools_text.get_rect(center = (screen_width // 2,(screen_height - 580)// 2))
        shopMenu.screen.blit(tools_text, tools_rect)

        tools_back = Button(image = pygame.transform.scale(pygame.image.load("images/MenuSprites/button1.png"), (140, 80)), pos = (screen_width // 2, (screen_height // 2) + 270),
                           text_input = "BACK", font = get_font(20), base_color = (255, 255, 255), hovering_color = (0, 0, 0))
        
        tilling2_button = Button(image = pygame.transform.scale(pygame.image.load("images/MenuSprites/button2.png"), (190, 100)), pos = ((screen_width // 2) - 120, (screen_height // 2) - 200),
                           text_input = "HOE (250)", font = get_font(20), base_color = (255, 255, 255), hovering_color = (0, 0, 0))
        tilling3_button = Button(image = pygame.transform.scale(pygame.image.load("images/MenuSprites/button2.png"), (190, 100)), pos = ((screen_width // 2) + 120, (screen_height // 2) - 200),
                           text_input = "TRACTOR (500)", font = get_font(20), base_color = (255, 255, 255), hovering_color = (0, 0, 0))
        
        watering2_button = Button(image =pygame.transform.scale(pygame.image.load("images/MenuSprites/button2.png"), (190, 100)), pos = ((screen_width // 2) - 120, (screen_height // 2) - 100),
                           text_input = "HOSE (250)", font = get_font(20), base_color = (255, 255, 255), hovering_color = (0, 0, 0))
        watering3_button = Button(image = pygame.transform.scale(pygame.image.load("images/MenuSprites/button2.png"), (190, 100)), pos = ((screen_width // 2) + 120, (screen_height // 2) - 100),
                           text_input = "WATER PLANE (500)", font = get_font(20), base_color = (255, 255, 255), hovering_color = (0, 0, 0))
        
        planting2_button = Button(image = pygame.transform.scale(pygame.image.load("images/MenuSprites/button2.png"), (190, 100)), pos = ((screen_width // 2) - 120, (screen_height // 2) - 0),
                           text_input = "PLOW (250)", font = get_font(20), base_color = (255, 255, 255), hovering_color = (0, 0, 0))
        planting3_button = Button(image = pygame.transform.scale(pygame.image.load("images/MenuSprites/button2.png"), (190, 100)), pos = ((screen_width // 2) + 120, (screen_height // 2) - 0),
                           text_input = "OX (500)", font = get_font(20), base_color = (255, 255, 255), hovering_color = (0, 0, 0))
        
        fertilization2_button = Button(image = pygame.transform.scale(pygame.image.load("images/MenuSprites/button2.png"), (190, 100)), pos = ((screen_width // 2) - 120, (screen_height // 2) + 100),
                           text_input = "SPRAYER (250)", font = get_font(20), base_color = (255, 255, 255), hovering_color = (0, 0, 0))
        fertilization3_button = Button(image = pygame.transform.scale(pygame.image.load("images/MenuSprites/button2.png"), (190, 100)), pos = ((screen_width // 2) + 120, (screen_height // 2) + 100),
                           text_input = "MACHINE (500)", font = get_font(20), base_color = (255, 255, 255), hovering_color = (0, 0, 0))
        
        harvesting2_button = Button(image = pygame.transform.scale(pygame.image.load("images/MenuSprites/button2.png"), (190, 100)), pos = ((screen_width // 2) - 120, (screen_height // 2) + 200),
                           text_input = "FORK (250)", font = get_font(20), base_color = (255, 255, 255), hovering_color = (0, 0, 0))
        harvesting3_button = Button(image = pygame.transform.scale(pygame.image.load("images/MenuSprites/button2.png"), (190, 100)), pos = ((screen_width // 2) + 120, (screen_height // 2) + 200),
                           text_input = "COMBINE (500)", font = get_font(20), base_color = (255, 255, 255), hovering_color = (0, 0, 0))
        
        
        tools_back.changeColor(tools_mouse_pos)
        tools_back.update(shopMenu.screen)
        tilling2_button.changeColor(tools_mouse_pos)
        tilling2_button.update(shopMenu.screen)
        tilling3_button.changeColor(tools_mouse_pos)
        tilling3_button.update(shopMenu.screen)
        harvesting2_button.changeColor(tools_mouse_pos)
        harvesting2_button.update(shopMenu.screen)
        harvesting3_button.changeColor(tools_mouse_pos)
        harvesting3_button.update(shopMenu.screen)
        watering2_button.changeColor(tools_mouse_pos)
        watering2_button.update(shopMenu.screen)
        watering3_button.changeColor(tools_mouse_pos)
        watering3_button.update(shopMenu.screen)
        fertilization2_button.changeColor(tools_mouse_pos)
        fertilization2_button.update(shopMenu.screen)
        fertilization3_button.changeColor(tools_mouse_pos)
        fertilization3_button.update(shopMenu.screen)
        planting2_button.changeColor(tools_mouse_pos)
        planting2_button.update(shopMenu.screen)
        planting3_button.changeColor(tools_mouse_pos)
        planting3_button.update(shopMenu.screen)

        #TODO: MAKE SURE MONEY CANNOT GO NEGATIVE!
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
                    print("BACK TOOLS!")
                    shopMenu.menu_quit = not shopMenu.menu_quit
                    shopMenuShow()
                if  tilling2_button.checkForInput(pygame.mouse.get_pos()): #tilling, harvesting, watering, fertilization, planting
                    #TODO: If player does not already have:
                    print("TOOL1!")
                    buyTilling2()
                if tilling3_button.checkForInput(pygame.mouse.get_pos()):
                    #TODO: If player does not already have:
                    print("TOOL2!")
                    buyTilling3()
                if harvesting2_button.checkForInput(pygame.mouse.get_pos()):
                    #TODO: If player does not already have:
                    print("TOOL3!")
                    buyHarvesting2()
                if harvesting3_button.checkForInput(pygame.mouse.get_pos()):
                    #TODO: If player does not already have:
                    print("TOOL4!")
                    buyHarvesting3()
                if watering2_button.checkForInput(pygame.mouse.get_pos()):
                    #TODO: If player does not already have:
                    print("TOOL4!")
                    buyWatering2()
                if watering3_button.checkForInput(pygame.mouse.get_pos()):
                    #TODO: If player does not already have:
                    print("TOOL4!")
                    buyWatering3()
                if fertilization2_button.checkForInput(pygame.mouse.get_pos()):
                    #TODO: If player does not already have:
                    print("TOOL4!")
                    buyFertlization2()
                if fertilization3_button.checkForInput(pygame.mouse.get_pos()):
                    #TODO: If player does not already have:
                    print("TOOL4!")
                    buyFertlization3()
                if planting2_button.checkForInput(pygame.mouse.get_pos()):
                    #TODO: If player does not already have:
                    print("TOOL4!")
                    buyPlanting2()
                if planting3_button.checkForInput(pygame.mouse.get_pos()):
                    #TODO: If player does not already have:
                    print("TOOL4!")
                    buyPlanting3()
        pygame.display.update()
        
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
player.tools.append(Hoe(player))
player.tools.append(WateringCan(player))
player.tools.append(Shovel(player))
player.tools.append(FertilizationSpray(player))
player.tools.append(Sickle(player))



menu = Menu(background_image="images/angry.jpg")
day_font = pygame.font.Font(None, 48)
day_writing = day_font.render("Day " + str(day), True, (0,0,0))
day_rect = day_writing.get_rect(center=(screen_width-100, 50))

house = House(250,200)

money = Money()
money.money=100
calendar = Calendar()

christmas_tiger = ChristmasTiger(800,400)

for seed in player.seeds:
    inventory.add_item(seed["name"], count=seed["count"])

def day_change():
    global player, map, calendar
    calendar.iterate()



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
                case pygame.K_e:
                    if(checkRange(player.rect,house.rect,house.interact_range)):
                        day_change()
                    elif(calendar.current_month=="Winter" and checkRange(player.rect,christmas_tiger.rect,christmas_tiger.interact_range)):
                        christmas_tiger.interact(money)
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
                case pygame.K_7:
                    if len(player.tools) >= 7:
                        player.current_tool = player.tools[6]
                case pygame.K_8:
                    if len(player.tools) >= 8:
                        player.current_tool = player.tools[7]
                case pygame.K_9:
                    if len(player.tools) >= 9:
                        player.current_tool = player.tools[8]
                case pygame.K_0:
                    if len(player.tools) >= 10:
                        player.current_tool = player.tools[9]
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
                case pygame.K_x:
                    shopMenuShow()
        elif event.type == pygame.KEYUP:
            keys_pressed.remove(event.key)
            match event.key:
                case pygame.K_k:
                    if not player.current_tool == None:
                        player.current_tool.hidden=True

    screen.fill((6,64,43))  # Fill the display with a solid color
    speed_mod = 1   
    if not player.current_tool == None and not player.current_tool.hidden:
        speed_mod = player.current_tool.speed_mod
    player_speed = getSpeed(keys_pressed, 10)
    player_speed = [int(player_speed[0] * speed_mod), int(player_speed[1] * speed_mod)]
    
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
                                        case "Watermelon":
                                            tile.crop=WatermelonTile(tile.rect.center[0], tile.rect.center[1])
                                        case "Corn":
                                            tile.crop=CornTile(tile.rect.center[0], tile.rect.center[1])
                                        case "Lettuce":
                                            tile.crop=LettuceTile(tile.rect.center[0], tile.rect.center[1])
                                        case "GMO_Pumpkin":
                                            tile.crop=PumpkinTile(tile.rect.center[0], tile.rect.center[1])
                                            tile.crop.risk-=5
                                            tile.crop.quality-=0.25
                                        case "GMO_Wheat":
                                            tile.crop=WheatTile(tile.rect.center[0], tile.rect.center[1])
                                            tile.crop.risk-=5
                                            tile.crop.quality-=0.25
                                        case "GMO_Carrot":
                                            tile.crop=CarrotTile(tile.rect.center[0], tile.rect.center[1])
                                            tile.crop.risk-=5
                                            tile.crop.quality-=0.25
                                        case "GMO_Watermelon":
                                            tile.crop=WatermelonTile(tile.rect.center[0], tile.rect.center[1])
                                            tile.crop.risk-=5
                                            tile.crop.quality-=0.25
                                        case "GMO_Corn":
                                            tile.crop=CornTile(tile.rect.center[0], tile.rect.center[1])
                                            tile.crop.risk-=5
                                            tile.crop.quality-=0.25
                                        case "GMO_Lettuce":
                                            tile.crop=LettuceTile(tile.rect.center[0], tile.rect.center[1])
                                            tile.crop.risk-=5
                                            tile.crop.quality-=0.25
                                    tile.crop.quality-=0.05*(5-tile.soil_quality)
                                    if tile.soil_quality==10:
                                        tile.crop.risk-=5
                                    if(tile.fertilized):
                                        tile.crop.quality-=0.25
                                        tile.crop.risk-=10
                                    if(tile.last_crop == player.seeds[player.current_seed]["name"]):
                                        tile.soil_quality -= 3
                                        if tile.soil_quality < 0:
                                            tile.soil_quality = 0
                                        else:
                                            tile.soil_quality+=2
                                            if tile.soil_quality > 10:
                                                tile.soil_quality = 10
                                    tile.last_crop = player.seeds[player.current_seed]["name"]
                                        
                        elif player.current_tool.type == "harvesting":
                            if (not tile.crop==None) and (tile.crop.dead or tile.crop.grown):
                                tile.crop.interact(money)
                                tile.crop=None
                        elif player.current_tool.type == "fertilizing":
                            if tile.fertilized==False:
                                """if "fertilizer" in inventory.items.keys():
                                    if inventory.items["fertilizer"]["count"]>0:
                                        inventory.items["fertilizer"]["count"]-=1
                                        inventory.items["fertilizer"]["visual_count"] = inventory.font.render(str(inventory.items["fertilizer"]["count"]), True, (255,255,255))
                                        tile.fertilize()"""
                                if money.money > 0:
                                    tile.fertilize()
                                    money.money-=1
    player_speed=checkCollision(player.rect,house.rect,player_speed)
    for row in map:
        for tile in row:
            if not tile == None:
                tile.update([-player_speed[0], -player_speed[1]])
        
    house.update([-player_speed[0], -player_speed[1]])   
    christmas_tiger.update([-player_speed[0], -player_speed[1]])    
        
    player.update(player_speed)
    
    inventory.update_inventory()

    
    #print(player_speed)

    #tiles.draw(screen)
    #screen.blit(player.image,player.rect)
    
    for row in map:
        for tile in row:
            if not tile == None:
                tile.display(screen)
    
        
    screen.blit(house.image,house.rect)
        
    screen.blit(player.image, player.rect)
    
    if not player.current_tool == None:
        player.current_tool.update()
        
    if calendar.current_month=="Winter":
        screen.blit(christmas_tiger.image, christmas_tiger.rect)
    
    if (not player.current_tool == None) and not player.current_tool.hidden:
        screen.blit(player.current_tool.image, player.current_tool.rect)
        
    calendar.display(screen)
        
    if not menu.hidden:
        screen.blit(menu.image, menu.rect)

    money.draw(screen)
    
    if not inventory.hidden:
        inventory.draw(screen)
        
        

    pygame.display.flip()  # Refresh on-screen display
    delays.append(time.time() - last)
    #print(1 / (sum(delays) / len(delays)))
    if len(delays) > 60:
        delays.pop(0)
    last = time.time()
    clock.tick(max_frames)