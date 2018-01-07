import pygame

from pygame.sprite import Group
from pygame.sprite import GroupSingle

import game_functions as gf
from settings import Settings
from ship import Ship
from parachute import Parachute
from hostile import Helicopter
from hostile import Rocket
from hostile import AdvancedHelicopter
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from timer import Timer
from background import Background
from sounds import ShipBulletSounds, ShipRailgunSounds, ShipMissileSounds, ShipExplodeSounds

from gf_universals import get_process_time

def run_game():
	# Initialize pygame
	pygame.init()
	# Initialize pygame mixer
	pygame.mixer.init()
	
	# Initializing all the game classes.
	ai_settings = Settings()
	stats = GameStats(ai_settings)
	screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
	pygame.display.set_caption("Hostile Takeover")
	
	bg = Background(ai_settings, screen)
	sb = Scoreboard(ai_settings, screen, stats)
	ship = Ship(ai_settings, screen, sb)
	timer = Timer(ai_settings, screen, ship, sb)
	
	# Initializes all the sound classes.
	shipbullet_sounds = ShipBulletSounds()
	shiprailgun_sounds = ShipRailgunSounds()
	shipmissile_sounds = ShipMissileSounds()
	shipexplode_sounds = ShipExplodeSounds()
	# Sets the volume to 0.1, (range is from 0.0 to 1.0).
	low_volume = 0.05
	mid_volume = 0.3
	high_volume = 0.7
	shipbullet_sounds.firing.set_volume(high_volume)
	shiprailgun_sounds.start.set_volume(low_volume)
	shiprailgun_sounds.firing.set_volume(low_volume)
	shiprailgun_sounds.end.set_volume(low_volume)
	shipmissile_sounds.firing.set_volume(low_volume)
	shipexplode_sounds.start.set_volume(high_volume)
	
	# Actually, there is no need to import their classes into this file.
	parachutes = Group()
	u_rails = Group()
	u_secondary = Group()
	u_missile = Group()
	u_laser = Group()
	
	# Actually, there is no need to import their classes into this file.
	explosions = Group()
	
	# Actually, there is no need to import their classes into this file.
	helis = Group()
	rockets = Group()
	ad_helis = Group()
	shipbullets = Group()
	shipmissiles = Group()
	helibullets = Group()
	
	# Create buttons to be pressed.
	play_button_mm = Button(screen, 'Play')
	stats_button_mm = Button(screen, 'Statistics')
	quit_button_mm = Button(screen, 'Quit Game')
	
	resume_button_esc = Button(screen, 'Resume')
	restart_button_esc = Button(screen, 'Restart Game')
	stats_button_esc = Button(screen, 'Statistics')
	exit_button_esc = Button(screen, 'Exit to Main Menu')
	#settings_button = Button(screen, 'Settings')
	
	# Reposition Main menu buttons based on the button above it.
	space_btw_buttons = 8
	stats_button_mm.rect.y += space_btw_buttons + play_button_mm.rect.height
	stats_button_mm.msg_image_rect.centery = stats_button_mm.rect.centery
	quit_button_mm.rect.y = space_btw_buttons + stats_button_mm.rect.y + stats_button_mm.rect.height
	quit_button_mm.msg_image_rect.centery = quit_button_mm.rect.centery
	
	# Reposition Esc menu buttons based on the button above it.
	restart_button_esc.rect.y += space_btw_buttons + resume_button_esc.rect.height
	restart_button_esc.msg_image_rect.centery = restart_button_esc.rect.centery
	stats_button_esc.rect.y = space_btw_buttons + restart_button_esc.rect.y + restart_button_esc.rect.height
	stats_button_esc.msg_image_rect.centery = stats_button_esc.rect.centery
	exit_button_esc.rect.y = space_btw_buttons + stats_button_esc.rect.y + stats_button_esc.rect.height
	exit_button_esc.msg_image_rect.centery = exit_button_esc.rect.centery
	
	#settings_button.rect.y = space_btw_buttons + 
	#settings_button.msg_image_rect.centery = settings_button.rect.centery
	
	#print(pygame.display.Info())
	
	# Creating list for rocket and ad_helis.
	rockets_hits_list = []
	ad_helis_hits_list = []
	
	# Ensures that the events, internals and screen is always running.
	while True:
		time_game = float('{:.1f}'.format(get_process_time()))
		
		# In charge of checking all game events prior to screen updates.
		gf.check_events(ai_settings, screen, ship, shipbullets, shipbullet_sounds, shiprailgun_sounds, shipmissiles, shipmissile_sounds, shipexplode_sounds, helis, helibullets, rockets, rockets_hits_list, ad_helis, ad_helis_hits_list, explosions, stats, play_button_mm, stats_button_mm, quit_button_mm, resume_button_esc, restart_button_esc, stats_button_esc, exit_button_esc, sb, timer, time_game)
		
		# Updates all game internal functions prior to screen updates and only when game is active.
		if stats.game_active:
			time_game_play = float('{:.1f}'.format(get_process_time()))
			
			gf.update_internals(ai_settings, screen, ship, shipbullets, shipbullet_sounds, shiprailgun_sounds, shipmissiles, shipmissile_sounds, shipexplode_sounds, parachutes, u_rails, u_secondary, u_missile, u_laser, helis, helibullets, rockets, rockets_hits_list, ad_helis, ad_helis_hits_list, explosions, stats, sb, timer, time_game_play)
		
		# Updates the screen with all the objects and projectiles.
		gf.update_screen(ai_settings, screen, ship, shipbullets, shipmissiles, parachutes, u_rails, u_secondary, u_missile, u_laser, helis, helibullets, rockets, ad_helis, explosions, stats, play_button_mm, stats_button_mm, quit_button_mm, resume_button_esc, restart_button_esc, stats_button_esc, exit_button_esc, sb, timer, bg)
		


run_game()
