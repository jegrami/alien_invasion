
import sys
from time import sleep
import pygame
from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    ''' Overall class to manage the assests and behavior of the game'''
    def __init__(self):
        ''' Initalize the game, and create its resources'''
        pygame.init()
        self.settings = Settings()
        
        # game settings
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        # create an instance to store game stats
        self.stats = GameStats(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

    

        
        # background color
        self.bg_color = (230, 230, 230)

    def run_game(self):
        ''' Start the main loop for the game'''
        while True:
            self._check_events()
            
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()

    def _check_events(self):
        ''' responsd to keypresses and mouse events'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                 self._check_keyup_events(event)
    
    def _check_keydown_events(self, event):
        ''' respond to keypresses'''
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT: 
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self.fire_bullet()            
            
    def _check_keyup_events(self, event):
        ''' respond to key releases'''        
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def fire_bullet(self):
        ''' create a new bullet and add it to the bullets group'''
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
    
    def _update_bullets(self):
        ''' update postion of bullets and get rid of old ones'''
        # update bullet postion
        self.bullets.update()

        # get rid of bullets that have diappeared out of the game
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        
        self._check_bullet_alien_collisions()
    
    def _check_bullet_alien_collisions(self):
        '''respond to bullet-alien collision'''
        # remove any aliens and bullets that have collided
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)
        if not self.aliens:
            ''' destroy existing bullets and create new fleet'''
            self.bullets.empty()
            self._create_fleet()

    
    def _update_aliens(self):
        '''check if fleet is at the edge, 
        then update the position of all aliens in the fleet
        '''
        self._check_fleet_edges()
        self.aliens.update()

        # look for alien-ship collsions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        
        # look for aliens hitting the bottom of the screen
        self._check_aliens_bottom()
            

    
    def _create_fleet(self):
        '''Create the fleet of aliens'''
        # create an alien and find the number of aliens in a row
        # spacing between each alien is equal to width of one alien
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # determine the number of rows of aliens that fit the screen
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - 
                             (3 * ship_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)


        # create the full fleet of aliens
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)
            
    def _create_alien(self, alien_number, row_number):
        # create an alien and place it in the row
            alien = Alien(self)
            alien_width, alien_height = alien.rect.size
            alien.x = alien_width + 2 * alien_width * alien_number
            alien.rect.x = alien.x
            alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number

            self.aliens.add(alien)
    
    def _check_fleet_edges(self):
        '''respond appropriately if any alien reaches the edge'''
        for alien in self.aliens.sprites():
            if alien.check_edges:
                self._change_fleet_direction()
                break
    def _change_fleet_direction(self):
        ''' drop the entire fleet and change its direction'''
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
    
    def _ship_hit(self):
        ''' respond to the ship being hit by the alien'''
        if self.stats.ships_left > 0:
            # decrement ship_left
            self.stats.ships_left -= 1

            # get rid of any remaining aliens
            self.aliens.empty()
            self.bullets.empty()

            # create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            # pause
            sleep(0.5)
        else:
            self.stats.game_active = False
    
    def _check_aliens_bottom(self):
        ''' check if any aliens has reached the bottom of the screen'''
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # treat this the same as if the ship got hit
                self._ship_hit()
                break

      
    def _update_screen(self):
    # update images on the screen, and then flip to a new screen
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        
        pygame.display.flip()


if __name__ == '__main__':
    # make a game instance, and run the game
    ai = AlienInvasion()
    ai.run_game()

