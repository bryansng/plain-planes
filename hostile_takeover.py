import pygame

from pygame.sprite import Group
from pygame.sprite import GroupSingle

import game_functions as gf
from settings import Settings
from ship import Ship
from bullet import ShipBullet
from hostile import Helicopter
from game_stats import GameStats
from button import Button
#from scoreboard import Scoreboard

def run_game():
	pygame.init()
	
	ai_settings = Settings()
	stats = GameStats(ai_settings)
	screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
	pygame.display.set_caption("Hostile Takeover")
	
	ship = Ship(ai_settings, screen)
	helis = Group()
	shipbullets = Group()
	helibullets = Group()
	
	play_button = Button(ai_settings, screen, 'Play')
	#sb = Scoreboard()
	
	gf.create_wave_helicopter(ai_settings, screen, helis)
	
	while True:
		gf.check_events(ai_settings, screen, ship, shipbullets, stats, play_button)
		
		if stats.game_active:
			gf.update_internals(ai_settings, screen, ship, shipbullets, helis, helibullets, stats)
		
		
		
		gf.update_screen(ai_settings, screen, ship, shipbullets, helis, helibullets, stats, play_button)
		



run_game()
