class Settings:
    ''' A class to handle all settings of the game'''
    def __init__(self):
        ''' initialize the game's settings'''
        # screen settings
        self.screen_width = 1200
        self.screen_height = 600
        self.bg_color = (230, 230, 230)
        self.ship_speed = 1.5

        # bullet settings
        self.bullet_speed = 1.5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 10

        # alien settings
        self.alien_speed = 1.0
        self.fleet_drop_speed = 1.0
        # fleet direction of 1 represents right; -1 represents left
        self.fleet_direction = 1
        
    

    
