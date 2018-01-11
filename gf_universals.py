import sys
import pygame
import time

from time import process_time

from explosion import Explosion

import gf_sounds as gfsounds



""" This file is sorted in this pattern:
    1) Universal
    2) 
    3) 
"""

""" 1) Universal
		a) Time
		b) Explosions
		c) Ship hit
"""

"""_____________________________________________________________________________
   1a) Universal: Time
_____________________________________________________________________________"""

def get_process_time():
	# Returns the process time at the time of request or call of this method.
	process_time = time.process_time()
	return process_time
	
	
	
	
	
	
	
	
	
	
"""_____________________________________________________________________________
   1b) Universal: Explosions
_____________________________________________________________________________"""

def create_explosion_and_time_and_sound(ai_settings, screen, shipexplode_sounds, explosions, death_x, death_y, object_type='hostile'):
	"""Gets object death position and create an explosion on the spot."""
	ai_settings.explosion_time_create = float('{:.1f}'.format(get_process_time()))
	#print("Time create: " + str(ai_settings.explosion_time_create))
	if object_type == 'hostile':
		create_explosion(ai_settings, screen, shipexplode_sounds, explosions, death_x, death_y)
	elif object_type == 'ship':
		create_explosion(ai_settings, screen, shipexplode_sounds, explosions, death_x, death_y, object_type='ship')

def create_explosion(ai_settings, screen, shipexplode_sounds, explosions, death_x, death_y, object_type='hostile'):
	"""Creates an explosion image to spawn at the specified position and
	adds it into the list(explosions)."""
	if object_type == 'hostile':
		hostile_explosion = Explosion(ai_settings, screen)
		hostile_explosion.centerx = death_x
		hostile_explosion.centery = death_y
		explosions.add(hostile_explosion)
	elif object_type == 'ship':
		create_sound_ship(ai_settings, shipexplode_sounds)
		ship_explosion = Explosion(ai_settings, screen)
		# Changes the explosion image for ship.
		ship_explosion.image = pygame.image.load('images/explosion/ship_explosion1.bmp')
		ship_explosion.centerx = death_x
		ship_explosion.centery = death_y
		explosions.add(ship_explosion)
		
def create_sound_ship(ai_settings, shipexplode_sounds):
	# Plays the Ship Explosion Sound.
	gfsounds.shipexplode_sound_start_internals(ai_settings, shipexplode_sounds)
		
		
def check_time_explosion_disappear(ai_settings, explosions):
	"""Removes the explosion image after a specified time.
	(Time specified in settings.py)"""
	# Extracts the explosion_time_create and adds the explosion_time_disappear
	# from ai_settings.py to it to get the time_no_immune.
	# Also, gets the process time indefinitely.
	# NOTE: The explosion_time_disappear can be optimized to run just once.
	explosion_time_disappear = float('{:.1f}'.format(ai_settings.explosion_time_create + ai_settings.explosion_time_disappear))
	#print("Time New: " + str(explosion_time_new))
	#print("Time Disappear: " + str(explosion_time_disappear))
	#print(explosion_time_new == explosion_time_disappear)
	# If time_new equate time_no_immune, remove explosion image.
	for explosion in explosions.copy():
		if ai_settings.time_game >= explosion_time_disappear:
			explosions.remove(explosion)
	
	
	
	
	
	
	
	
	
	
"""_____________________________________________________________________________
   1b) Universal: Ship hit
_____________________________________________________________________________"""
	
		
def ship_hit(ai_settings, screen, ship, shipexplode_sounds, explosions, stats, sb):
	"""Creates explosion image, Continues if there are still ships left,
	Else, end game."""
	# Runs explosion counter and creates explosion image
	# at death position of object.
	create_explosion_and_time_and_sound(ai_settings, screen, shipexplode_sounds, explosions, ship.rect.centerx, ship.rect.centery, object_type='ship')
	
	# If there are still ships left, immunity set to true for immunity counter,
	# ships left decreased by 1, and ship is centered.
	if stats.ship_left > 0:
		ship.immunity = True
		stats.ship_left -= 1
		ship.center_ship()
	# Else, game_active set to False, mouse set to visible again,
	# set_grab set to False
	# High score is dumped to json file so that upon clicking the statistics 
	# button, the statistics will be updated with the new high score that is 
	# newly acquired/achieved.
	else:
		stats.game_active = False
		pygame.mouse.set_visible(True)
		pygame.event.set_grab(False)
		sb.dumps_stats_to_json()
