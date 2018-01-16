import sys
import pygame
import time

import gf_universals as gf_uni
import gf_sounds as gfsounds

from random import randint

from bullet import ShipBulletPrimary
from bullet import ShipBulletSecondary
from bullet import ShipMissilePrimary
from bullet import ShipMissileSecondary
from parachute import Parachute
from explosion import Explosion
from bullet import HelicopterBullet
from hostile import Helicopter
from hostile import Rocket
from hostile import AdvancedHelicopter

""" This file is sorted in this pattern:
    1) Hostiles and HostileProjectiles Internals
    2) Wave Creation
    3) 
"""

""" 1) Hostiles and HostileProjectiles Internals
		a) Helicopter and HeliBullet
		b) Rocket
		c) Advanced Helicopter
"""

"""_____________________________________________________________________________
   1a) Hostiles and HostileProjectiles Internals: 
       Helicopter and HeliBullet Internals
_____________________________________________________________________________"""

def update_heli_internals(ai_settings, screen, ship, shiprailgun_sounds, u_i_rail, u_i_secondary, u_i_missile, u_i_laser, helis, helibullets, explosions, stats, sb):
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
	update_heli_bullet_internals(ai_settings, screen, ship, shiprailgun_sounds, u_i_rail, u_i_secondary, u_i_missile, u_i_laser, helis, helibullets, explosions, stats, sb)
	
	# NOTE: This is temporary
	# Creates a new wave when it detects the number of helis is zero.
	# Also increases the level by 1.
	if (len(helis) == 0) and (ai_settings.wave_heli_spawn == True) and (ai_settings.wave_hostile_spawn == True):
		create_wave_helicopter(ai_settings, screen, helis)
		stats.level += 1
	
	
def update_heli_bullet_internals(ai_settings, screen, ship, shiprailgun_sounds, u_i_rail, u_i_secondary, u_i_missile, u_i_laser, helis, helibullets, explosions, stats, sb):
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
	check_ship_hostileprojectile_collision(ai_settings, screen, ship, shiprailgun_sounds, u_i_rail, u_i_secondary, u_i_missile, u_i_laser, helibullets, explosions, stats, sb)
	
	
def check_ship_hostileprojectile_collision(ai_settings, screen, ship, shiprailgun_sounds, u_i_rail, u_i_secondary, u_i_missile, u_i_laser, helibullets, explosions, stats, sb):
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
			ai_settings.ship_time_hit = ai_settings.time_game_total_play
			# Runs the method ship_hit for what will happen to the ship.
			gf_uni.ship_hit(ai_settings, screen, ship, shiprailgun_sounds, shipexplode_sounds, u_i_rail, u_i_secondary, u_i_missile, u_i_laser, explosions, stats, sb)
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
		ship_hit(ai_settings, screen, ship, shiprailgun_sounds, shipexplode_sounds, explosions, stats, sb)
	"""

	# Possibility 3 (Not suitable as it can't track individual helibullets)
	"""
	if pygame.sprite.spritecollideany(ship, helibullets) and not ship.immunity:
		ai_settings.ship_time_hit = float('{:.1f}'.format((get_process_time())))
		#print("Time Hit: " + str(ai_settings.ship_time_hit))
		ship_hit(ai_settings, screen, ship, shiprailgun_sounds, shipexplode_sounds, explosions, stats, sb)
	"""
		
def check_immunity(ai_settings, ship):
	"""Sets the ship immunity to false once the time of immunity is over."""
	# Extracts the ship_time_hit and adds the time_immune to it to get the
	# time_no_immune.
	# Also, gets the process time indefinitely.
	# NOTE: The time_no_immune can be optimized to run just once.
	ship_time_no_immune = float('{:.1f}'.format((ai_settings.ship_time_hit + ai_settings.ship_time_immune)))
	# If ai_settings.time_game_total_play equate time_no_immune, ship immunity is set to false.
	if ai_settings.time_game_total_play >= ship_time_no_immune:
		ship.immunity = False
		#print("Immunity set to False")
	







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
   1b) Hostiles and HostileProjectiles Internals: 
       Rocket Internals
_____________________________________________________________________________"""

def update_rocket_internals(ai_settings, screen, ship, rockets, rockets_hits_list, stats):
	# Update internals of rocket from its class file.
	# Specifically, its movements.
	rockets.update()
	
	# Removes rocket once they reach the top side of the screen.
	for rocket in rockets.copy():
		if rocket.rect.bottom <= 0:
			# We use rocketss because we don't want any conflicts.
			# This loop removes all of that rocket from the list.
			for rocketss in rockets_hits_list:
				try:
					rockets_hits_list.remove(rocket)
				except ValueError:
					pass
					#print("ValueError at Removal from top side.\n")
					
			rockets.remove(rocket)
			
	# For the first version of rocket_shipbullet_collisions.
	# In charge of removing the rockets once they pass the screen top.
	for rocket in rockets.copy():
		if rocket.rect.bottom <= 0:
			rockets.remove(rocket)
			for rockets_hits_dict in rockets_hits_list:
				if rocket in rockets_hits_dict.values():
					print("rockets_hits_list before removal:", rockets_hits_list)
					rockets_hits_list.remove(rockets_hits_dict)
					print("rockets_hits_list after removal:", rockets_hits_list)
					
	
	# NOTE: This is temporary
	# Creates a new wave when it detects the number of rockets is zero.
	# Also increases the level by 1.
	if (len(rockets) == 0) and (ai_settings.wave_rocket_spawn == True) and (ai_settings.wave_hostile_spawn == True):
		create_wave_rocket(ai_settings, screen, ship, rockets, rockets_hits_list)
		stats.level += 1








"""_____________________________________________________________________________
   1c) Hostiles and HostileProjectiles Internals: 
       Advanced Helicopter Internals
_____________________________________________________________________________"""

def update_ad_heli_internals(ai_settings, screen, ad_helis, ad_helis_hits_list, stats):
	# Update internals of ad_heli from its class file.
	# Specifically, its movements.
	ad_helis.update()
	# Get screen rect.
	screen_rect = screen.get_rect()
	
	# Removes ad_heli once they reach the left side of the screen.
	for ad_heli in ad_helis.copy():
		if ad_heli.rect.right <= screen_rect.left:
			# We use ad_heliss because we don't want any conflicts.
			# This loop removes all of that rocket from the list.
			for ad_heliss in ad_helis_hits_list:
				try:
					ad_helis_hits_list.remove(ad_heli)
				except ValueError:
					pass
					#print("ValueError at Removal from top side.\n")
					
			ad_helis.remove(ad_heli)
	
	# NOTE: This is temporary
	# Creates a new wave when it detects the number of ad_helis is zero.
	# Also increases the level by 1.
	if (len(ad_helis) == 0) and (ai_settings.wave_ad_heli_spawn == True) and (ai_settings.wave_hostile_spawn == True):
		create_wave_ad_heli(ai_settings, screen, ad_helis, ad_helis_hits_list)
		stats.level += 1
	
	
					
	
	
	
	
	




















""" 2) WAVE CREATION
		a) Helicopter
		b) Rocket
		c) Advanced Helicopter
"""


"""_____________________________________________________________________________
   2a) Wave Creation: Helicopter
_____________________________________________________________________________"""

def create_wave_helicopter(ai_settings, screen, helis):
	"""Spawns a new wave of helicopters."""
	# Adds and creates helicopter depending on the wave limit.
	for heli in range(ai_settings.helicopter_wave_limit):
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
	




"""_____________________________________________________________________________
   2b) Wave Creation: Rocket
_____________________________________________________________________________"""

def create_wave_rocket(ai_settings, screen, ship, rockets, rockets_hits_list):
	"""Spawns a new wave of rockets."""
	# Refreshes the list before appending to it.
	for rocket in rockets_hits_list:
		rockets_hits_list.remove(rocket)
	# Adds and creates rocket depending on the wave limit.
	for rocket in range(ai_settings.rocket_wave_limit):
		create_rocket(ai_settings, screen, ship, rockets, rockets_hits_list)
	
def get_rocket_x(ai_settings, ship):
	"""Returns a x coordinate from the specified values."""
	random_x = randint((ship.rect.width + 1), (ai_settings.screen_width - 50))
	return random_x
	
def get_rocket_y(ai_settings):
	"""Returns a y coordinate from the specified values."""
	random_y = randint((ai_settings.screen_height + 100), (ai_settings.screen_height + 2000))
	return random_y

def create_rocket(ai_settings, screen, ship, rockets, rockets_hits_list):
	"""Specify the correct coordinates for the individual rockets to 
	spawn and Adds the new rocket into the list(rockets).
	
	It also adds the new rocket to a list for hits counter."""
	new_rocket = Rocket(ai_settings, screen)
	
	new_rocket.centerx = get_rocket_x(ai_settings, ship)
	new_rocket.centery = get_rocket_y(ai_settings)
	
	# Adds the created new rocket to the rockets_hits_list.
	add_rocket_to_list(new_rocket, rockets_hits_list)
	rockets.add(new_rocket)
	
def add_rocket_to_list(new_rocket, rockets_hits_list):
	"""Adds the created new rocket to the rockets_hits_list."""
	# Specify the hits required for removal.
	# Example: If hits_required_for_removal = 3,
	#          3 shipbullets is required to destory the rocket.
	hits_required_for_removal = 3
	for hits_required in range(hits_required_for_removal):
		rockets_hits_list.append(new_rocket)
	




"""_____________________________________________________________________________
   2c) Wave Creation: Advanced Helicopter
_____________________________________________________________________________"""

def create_wave_ad_heli(ai_settings, screen, ad_helis, ad_helis_hits_list):
	"""Spawns a new wave of advanced helicopters."""
	# Refreshes the list before appending to it.
	for ad_heli in ad_helis_hits_list:
		ad_helis_hits_list.remove(ad_heli)
	# Adds and creates advanced helicopter depending on the wave limit.
	for ad_heli in range(ai_settings.ad_heli_wave_limit):
		create_ad_heli(ai_settings, screen, ad_helis, ad_helis_hits_list)

def get_ad_heli_x(ai_settings):
	"""Returns a x coordinate from the specified values."""
	random_x = randint((ai_settings.screen_width + 100), (ai_settings.screen_width + 2500))
	return random_x
	
def get_ad_heli_y(ai_settings):
	"""Returns a y coordinate from the specified values."""
	# 58 is because of the top bracket.
	# Screen_height - 50 is so that it spawns more naturally.
	random_y = randint(70, (ai_settings.screen_height - 50))
	return random_y
	
def create_ad_heli(ai_settings, screen, ad_helis, ad_helis_hits_list):
	"""Specify the correct coordinates for the individual rockets to 
	spawn and Adds the new rocket into the list(ad_helis)."""
	new_ad_heli = AdvancedHelicopter(ai_settings, screen)
	
	new_ad_heli.centerx = get_ad_heli_x(ai_settings)
	new_ad_heli.centery = get_ad_heli_y(ai_settings)
	
	# Adds the created new rocket to the ad_helis_hits_list.
	add_ad_heli_to_list(new_ad_heli, ad_helis_hits_list)
	ad_helis.add(new_ad_heli)
	
def add_ad_heli_to_list(new_ad_heli, ad_helis_hits_list):
	"""Adds the created new ad_heli to the ad_helis_hits_list."""
	# Specify the hits required for removal.
	# Example: If hits_required_for_removal = 5,
	#          5 shipbullets is required to destory the ad_heli.
	hits_required_for_removal = 5
	for hits_required in range(hits_required_for_removal):
		ad_helis_hits_list.append(new_ad_heli)












