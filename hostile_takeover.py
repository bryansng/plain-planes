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
from scoreboard import Scoreboard

def run_game():
	# Initialize pygame
	pygame.init()
	
	# Initializing all the game classes.
	ai_settings = Settings()
	stats = GameStats(ai_settings)
	screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
	pygame.display.set_caption("Hostile Takeover")
	
	sb = Scoreboard(ai_settings, screen, stats)
	ship = Ship(ai_settings, screen, sb)
	helis = Group()
	shipbullets = Group()
	helibullets = Group()
	
	play_button = Button(ai_settings, screen, 'Play')
	
	print(pygame.display.Info())
	
	# Creates a wave of helicopters
	gf.create_wave_helicopter(ai_settings, screen, helis)
	
	# Ensures that the events, internals and screen is always running.
	while True:
		# In charge of checking all game events prior to screen updates.
		gf.check_events(ai_settings, screen, ship, shipbullets, helis, helibullets, stats, play_button, sb)
		
		# Updates all game internal functions prior to screen updates and only when game is active.
		if stats.game_active:
			gf.update_internals(ai_settings, screen, ship, shipbullets, helis, helibullets, stats, sb)
		
		# Updates the screen with all the objects and projectiles.
		gf.update_screen(ai_settings, screen, ship, shipbullets, helis, helibullets, stats, play_button, sb)
		


run_game()
