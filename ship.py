import pygame 

class Ship: 
    '''A class to manage the ship'''
    def __init__(self, ai_game):
        ''' initialize the ship and set its starting postion'''
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        # load the ship's image and get rect
        self.image = pygame.image.load("C:\\Users\\USER\.vscode\\py_crash_course\\alien_invasion\\images\\ship.bmp")
        self.rect = self.image.get_rect()

        # start each new ship at the bottom center of the screen
        self.rect.midbottom = self.screen_rect.midbottom

        # store a decimal value for the ship's position
        self.x = float(self.rect.x)

        #movement flag
        self.moving_right = False
        self.moving_left = False
    
    def update(self):
        ''' update the ship's position based on the movement flag'''
        # update the ships x value, not the rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        # update the rect object from self.x position
        self.rect.x = self.x
    
    def blitme(self):
        ''' draw the ship at the curent location'''
        self.screen.blit(self.image, self.rect)
