
class GameStats:
    '''Track statistics for alien invasion'''
    def __init__(self, ai_game):
        '''initialize statistics'''
        self.settings = ai_game.settings

        # start Alien Invasion in active state
        self.game_active = False

        self.reset_stats()
    
    def reset_stats(self):
        ''' initialize stats that can change during the game'''
        self.ships_left = self.settings.ship_limit


