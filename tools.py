import pygame

class Tool(pygame.sprite.Sprite):
    def __init__(self, tool_name, image, width, height, player):
        super().__init__()
        self.tool_name = tool_name
        self.image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(center = (0,0))
        self.hidden = True
    def update(self):
        orientation = self.player.orientation
        match orientation:
            case 0:
                self.rect.center = (self.player.rect.width//2 + self.rect.height//2 + self.player.rect.x, self.player.rect.y)
                self.image = pygame.transform.rotate(self.image, orientation)
            case 90:
                self.rect.center = (self.player.rect.x, -self.rect.height//2 + self.player.rect.y)
                self.image = pygame.transform.rotate(self.image, orientation)
            case 180:
                self.rect.center = (self.player.rect.width//2 - self.rect.height//2 - self.player.rect.x, self.player.rect.y)
                self.image = pygame.transform.rotate(self.image, orientation)
            case 270:
                self.rect.center = (self.player.rect.x, self.rect.height//2 + self.player.rect.y)
                self.image = pygame.transform.rotate(self.image, orientation)
                