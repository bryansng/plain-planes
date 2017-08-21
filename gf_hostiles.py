import sys
import pygame
import time

from time import process_time

from random import randint

from bullet import ShipBullet
from bullet import HelicopterBullet
from hostile import Helicopter
from hostile import Rocket

from gf_objects import *

""" This file is sorted in this pattern:
    1) Hostiles and HostileProjectiles Internals
    2) Wave Creation
    3) 
"""

""" 1) Hostiles and HostileProjectiles Internals

	a) Helicopter and HeliBullet
	b) Rocket
"""

"""_____________________________________________________________________________
   Helicopter and HeliBullet Internals
_____________________________________________________________________________"""

def update_heli_internals(ai_settings, screen, ship, helis, helibullets, stats, sb):
	"""Updates and handles whatever that happens to heli and helibullet."""
	# Update internals of heli from its class file.
	# Specifically, its movements.
	helis.update()
	# Get screen rect.
	screen_rect = screen.get_rect()
	
	# Removes heli once they reach the left side of the screen.
	for heli in helis.copy():
		if heli.rect.right <= screen_rect.left:
			helis.remove(heli)
	
	# Updates internals of helibullets.
	update_heli_bullet_internals(ai_settings, screen, ship, helis, helibullets, stats, sb)
	
	# NOTE: This is temporary
	# Creates a new wave when it detects the number of helis is zero.
	# Also increases the level by 1.
	"""if len(helis) == 0:
		create_wave_helicopter(ai_settings, screen, helis)
		stats.level += 1"""
	
	# Handles what happens if the hostileobject and ship collides.
	check_ship_hostileobject_collision(ai_settings, ship, helis, stats, sb)
	
	
def check_ship_hostileobject_collision(ai_settings, ship, helis, stats, sb):
	"""
	tldr: heli removed, ship removed, immunity counter runs if conditions met.
	
	Sets condition for how ship collide with heli, based on colliderect.
	If they overlap and immunity is false, heli that collided is removed, ship is removed and time_hit for immunity is set.
	"""
	# Get ship rect.
	ship_rect = ship.rect
	for heli in helis.sprites():
		# Boolean for collision or overlapping of rect between ship and heli.
		heli_overlap_ship = ship_rect.colliderect(heli)
		# If overlap and immunity false, heli and ship is removed, immunity 
		# counter starts.
		if heli_overlap_ship and not ship.immunity:
			# Gets the time_hit for immunity counter.
			ai_settings.ship_time_hit = float('{:.1f}'.format((get_process_time())))
			# Runs the method ship_hit for what will happen to the ship.
			ship_hit(ai_settings, ship, stats, sb)
			# Removes that particular heli in helis.
			helis.remove(heli)
	
	
def update_heli_bullet_internals(ai_settings, screen, ship, helis, helibullets, stats, sb):
	"""Updates and handles whatever that happens to helibullet."""
	# Update internals of helibullet from its class file.
	# Specifically, its movements.
	helibullets.update()
	
	# Creates, assign, add and fire a new heli bullet upon meeting the 
	# conditions of fire.
	fire_heli_bullets(ai_settings, screen, ship, helis, helibullets)
	
	# Get screen rect.
	screen_rect = screen.get_rect()
	# Removes the helibullets that leaves the left side of the screen.
	for bullet in helibullets.copy():
		if bullet.rect.right <= screen_rect.left:
			helibullets.remove(bullet)
			
	# Handles what happens if the hostileprojectile and ship collides.
	check_ship_hostileprojectile_collision(ai_settings, ship, helibullets, stats, sb)
	
	
def check_ship_hostileprojectile_collision(ai_settings, ship, helibullets, stats, sb):
	"""
	Based on Possibility 2,
	tldr: helibullet removed, ship removed, immunity counter runs if conditions 
	met.
	
	For each individual projectile in the sprite, if ship_rect contains that
	projectile, objectprojectile_inside_ship is set to True.
	
	If that is true and ship immunity is false,
	time_hit for immunity counter is set, ship_hit runs, helibullet is removed.
	"""
	
	# Possibility 1 (Works best because you can remove helibullets individually)
	
	# Get ship rect.
	ship_rect = ship.rect
	for helibullet in helibullets.sprites():
		# True if ship_rect contains the specific helibullet in the sprite.
		helicopterbullet_inside_ship = ship_rect.contains(helibullet)
		# If True and ship_immunity false, helibullet and ship is removed, immunity counter starts.
		if helicopterbullet_inside_ship and not ship.immunity:
			# Gets the time_hit for immunity counter.
			ai_settings.ship_time_hit = float('{:.1f}'.format((get_process_time())))
			# Runs the method ship_hit for what will happen to the ship.
			ship_hit(ai_settings, ship, stats, sb)
			# Removes that particular heli in helis.
			helibullets.remove(helibullet)
			
	# Check and handles the immunity and immunity counter.
	check_immunity(ai_settings, ship)
	
	# Possibility 2 (Doesn't work, because ship is not a sprite group)
	"""
	if not ship.immunity:
		ship_helicopterbullet_collisions = pygame.sprite.groupcollide(helibullets, ship, True, True)
		
	if ship_helicopterbullet_collisions:
		#time_hit = int(get_process_time())
		ship_hit(ai_settings, ship, stats)
	"""

	# Possibility 3 (Not suitable as it can't track individual helibullets)
	"""
	if pygame.sprite.spritecollideany(ship, helibullets) and not ship.immunity:
		ai_settings.ship_time_hit = float('{:.1f}'.format((get_process_time())))
		#print("Time Hit: " + str(ai_settings.ship_time_hit))
		ship_hit(ai_settings, ship, stats, sb)
	"""
	
		
def ship_hit(ai_settings, ship, stats, sb):
	"""Continues if there are still ships left, else, end game."""
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
		sb.dumps_highscore_to_json()
		
		
def check_immunity(ai_settings, ship):
	"""Sets the ship immunity to false once the time of immunity is over."""
	# Extracts the ship_time_hit and adds the time_immune to it to get the
	# time_no_immune.
	# Also, gets the process time indefinitely.
	# NOTE: The time_no_immune can be optimized to run just once.
	ship_time_no_immune = float('{:.1f}'.format((ai_settings.ship_time_hit + ai_settings.ship_time_immune)))
	ship_time_new = float('{:.1f}'.format(get_process_time()))
	# If time_new equate time_no_immune, ship immunity is set to false.
	if ship_time_new == ship_time_no_immune:
		ship.immunity = False
		#print("Immunity set to False")
	
	
def get_process_time():
	# Returns the process time at the time of request or call of this method.
	process_time = time.process_time()
	return process_time
	







# NOTE: The x coordinate for which the bullets start firing out from is buggy
# and not working as expected, might have to change to using a counter.
def fire_heli_bullets(ai_settings, screen, ship, helis, helibullets):
	"""Creates, assign, add and fire a new heli bullet upon meeting the 
	conditions of fire."""
	# Get screen_rect and ship_rect for later.
	screen_rect = screen.get_rect()
	ship_rect = ship.rect
	for heli in helis.sprites():
		# Boolean return if screen_rect contains heli.
		heli_inside_screen = screen_rect.contains(heli)
		# Boolean return if the points ship_rect.centerx and heli.rect_centery
		# are in the ship_rect.
		# ship_rect.centerx will always be true since it follows the ship.
		# heli_rect.centery will be true if the ship moves into the heli's y,
		# since the y of the heli is always fixed, the condition for it to be
		# true would be if the ship moved into heli's y.
		heli_centery_in_ship = ship_rect.collidepoint(ship_rect.centerx , heli.rect.centery)
		# Get the x coordinate for which the bullet will start firing.
		heli_bullet_x_1 = get_heli_bullet_x_1(ai_settings)
		# If heli inside screen, followed after by if the heli.rect.x reach
		# the x for firing and if the ship is within heli's line of sight,
		# helibullets are created, added and fired.
		if heli_inside_screen:
			if heli.rect.x == heli_bullet_x_1 and heli_centery_in_ship:
				create_heli_bullet(ai_settings, screen, heli, helibullets, heli_bullet_x_1)
	
	
def create_heli_bullet(ai_settings, screen, heli, helibullets, heli_bullet_x_1):
	"""Creates a new bullet, assign it the x coordinate for which it will
	start firing at and adds it to the list(helibullets)."""
	new_heli_bullet = HelicopterBullet(ai_settings, screen, heli)
	# Extracts the x coordinate from get_heli_bullet_x_1 and assigns it to
	# each individual new heli bullet.
	new_heli_bullet.x = heli_bullet_x_1
	new_heli_bullet.rect.x = new_heli_bullet.x
	helibullets.add(new_heli_bullet)
	
	
def get_heli_bullet_x_1(ai_settings):
	"""Returns a x coordinate for the helibullet to start fire at."""
	random_x = randint(0, ai_settings.screen_width)
	return random_x








"""_____________________________________________________________________________
   Rocket
_____________________________________________________________________________"""

def update_rocket_internals(rockets, rockets_hits_list):
	# Update internals of heli from its class file.
	# Specifically, its movements.
	rockets.update()
	
	
	for rocket in rockets.copy():
		if rocket.rect.bottom <= 0:
			rockets.remove(rocket)
			for rocketss in rockets_hits_list:
				try:
					rockets_hits_list.remove(rocket)
				except ValueError:
					print("Rocket: ValueError from top removal")
					pass
	
	"""
	for rocket in rockets.copy():
		if rocket.rect.bottom <= 0:
			rockets.remove(rocket)
			for rockets_hits_dict in rockets_hits_list:
				if rocket in rockets_hits_dict.values():
					print("rockets_hits_list before removal:", rockets_hits_list)
					rockets_hits_list.remove(rockets_hits_dict)
					print("rockets_hits_list after removal:", rockets_hits_list)
					"""
					
	
	
	
	
	




















""" 2) WAVE CREATION """

def create_wave_helicopter(ai_settings, screen, helis):
	"""Spawns a new wave of helicopters."""
	# Sets helicopter limit to 10.
	helicopter_wave_limit = 10
	# Adds and creates helicopter depending on the wave limit.
	for heli in range(helicopter_wave_limit):
		create_helicopter(ai_settings, screen, helis)
	
def get_helicopter_x(ai_settings):
	"""Returns a x coordinate from the specified values."""
	random_x = randint((ai_settings.screen_width + 100), (ai_settings.screen_width + 2000))
	return random_x
	
def get_helicopter_y(ai_settings):
	"""Returns a y coordinate from the specified values."""
	# 58 is because of the top bracket.
	# Screen_height - 50 is so that it spawns more naturally.
	random_y = randint(58, (ai_settings.screen_height - 50))
	return random_y
	
def create_helicopter(ai_settings, screen, helis):
	"""Specify the correct coordinates for the individual helicopters to 
	spawn and Adds the new helicopter into the list(helis)."""
	new_heli = Helicopter(ai_settings, screen)
	
	new_heli.centerx = get_helicopter_x(ai_settings)
	new_heli.centery = get_helicopter_y(ai_settings)
	
	helis.add(new_heli)
	
	# These methods of assigning does not work.
	# Because these values are not updated in helis.update()
	# We will need to use the float values made in hostile146 to do it.
	# Unless we assign the variables below to hostile146 for updates.
	# The above is just a theory.
	
	#heli_x = get_helicopter_x(ai_settings)
	#heli_y = get_helicopter_y(ai_settings)
	
	#new_heli.rect.x = heli_x
	#new_heli.rect.y = heli_y
	




def create_wave_rocket(ai_settings, screen, ship, rockets):
	rocket_wave_limit = 10
	for rocket in range(rocket_wave_limit):
		create_rocket(ai_settings, screen, ship, rockets)
	
def get_rocket_x(ai_settings, ship):
	random_x = randint((ship.rect.width - 1), (ai_settings.screen_width - 50))
	return random_x
	
def get_rocket_y(ai_settings):
	random_y = randint((ai_settings.screen_height + 100), (ai_settings.screen_height + 2000))
	return random_y

def create_rocket(ai_settings, screen, ship, rockets):
	new_rocket = Rocket(ai_settings, screen)
	
	new_rocket.centerx = get_rocket_x(ai_settings, ship)
	new_rocket.centery = get_rocket_y(ai_settings)
	
	rockets.add(new_rocket)
