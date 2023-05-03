import pygame
from pygame.sprite import Sprite 

class Bullet(Sprite):
    ''' A class to manage bullets fired from the ship'''
    def __init__(self, ai_game):
        ''' create a bullet object at the ship's currect postion'''
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # create a bullet as (0, 0) and then set the correct postion
        self.rect = pygame.Rect(0,0, self.settings.bullet_width, 
                                self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        # store the bullet's postion as a decimal value
        self.y = float(self.rect.y)
    
    def update(self):
        '''to move the bullet up the screen'''
        # first, update the decimal postion of the bullet
        self.y -= self.settings.bullet_speed
        # last, update the bullet rect
        self.rect.y = self.y
    
    def draw_bullet(self):
        ''' draw the bullet to the screen'''
        pygame.draw.rect(self.screen, self.color, self.rect)
