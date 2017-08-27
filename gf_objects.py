import sys
import pygame
import time

from game_functions import *
from gf_hostiles import *

from time import process_time

from random import randint

from bullet import ShipBullet
from parachute import Parachute
from explosion import Explosion
from bullet import HelicopterBullet
from hostile import Helicopter
from hostile import Rocket
from hostile import AdvancedHelicopter

""" This file is sorted in this pattern:
    1) Objects and ObjectProjectiles Internals
    2) Upgrades
    3) 
"""

""" 1) Objects and ObjectProjectiles Internals
		a) Ship
			i) Ship with HostileObjects
		c) Parachutes
		b) ShipBullet
		
		b) Hostile with ShipProjectile
			i) Helicopter with Shipbullet
			ii) Rocket with ShipBullet
			iii) Advanced Helicopter with 
			
		c) HostileProjectiles with ShipProjectiles
			i) HeliBullet with ShipBullet
"""
"""_____________________________________________________________________________
   a) Ship Internals
_____________________________________________________________________________"""

def update_ship_internals(ai_settings, screen, ship, shipbullets, parachutes, helis, helibullets, rockets, rockets_hits_list, ad_helis, ad_helis_hits_list, explosions, stats, sb):
	"""Updates and handles whatever happens to ship."""
	# Update internals of ship from its class file.
	# Specifically, its movements.
	ship.update()
	# Handles what happens if the hostileobject and ship collides.
	check_hostileobject_ship_collision(ai_settings, screen, ship, helis, rockets, ad_helis, explosions, stats, sb)
	
	
	
"""_____________________________________________________________________________
   ai) Ship Internals: Ship with HostileObjects Internals
_____________________________________________________________________________"""


def check_hostileobject_ship_collision(ai_settings, screen, ship, helis, rockets, ad_helis, explosions, stats, sb):
	"""
	tldr: hostileobject removed, ship removed, immunity counter runs if conditions met.
	
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
			# Runs explosion counter and creates explosion image
			# at death position of object.
			create_explosion_and_time(ai_settings, screen, explosions, heli.rect.centerx, heli.rect.centery)
			
			# Gets the time_hit for immunity counter.
			ai_settings.ship_time_hit = float('{:.1f}'.format((get_process_time())))
			# Runs the method ship_hit for what will happen to the ship.
			ship_hit(ai_settings, screen, ship, explosions, stats, sb)
			# Removes that particular heli in helis.
			helis.remove(heli)
			
	# Get ship rect.
	ship_rect = ship.rect
	for rocket in rockets.sprites():
		# Boolean for collision or overlapping of rect between ship and rocket.
		rocket_overlap_ship = ship_rect.colliderect(rocket)
		# If overlap and immunity false, rocket and ship is removed, immunity 
		# counter starts.
		if rocket_overlap_ship and not ship.immunity:
			# Runs explosion counter and creates explosion image
			# at death position of object.
			create_explosion_and_time(ai_settings, screen, explosions, rocket.rect.centerx, rocket.rect.centery)
			
			# Gets the time_hit for immunity counter.
			ai_settings.ship_time_hit = float('{:.1f}'.format((get_process_time())))
			# Runs the method ship_hit for what will happen to the ship.
			ship_hit(ai_settings, screen, ship, explosions, stats, sb)
			# Removes that particular rocket in rockets.
			rockets.remove(rocket)
			
	# Get ship rect.
	ship_rect = ship.rect
	for ad_heli in ad_helis.sprites():
		# Boolean for collision or overlapping of rect between ship and ad_heli.
		ad_heli_overlap_ship = ship_rect.colliderect(ad_heli)
		# If overlap and immunity false, ad_heli and ship is removed, immunity 
		# counter starts.
		if ad_heli_overlap_ship and not ship.immunity:
			# Runs explosion counter and creates explosion image
			# at death position of object.
			create_explosion_and_time(ai_settings, screen, explosions, ad_heli.rect.centerx, ad_heli.rect.centery)
			
			# Gets the time_hit for immunity counter.
			ai_settings.ship_time_hit = float('{:.1f}'.format((get_process_time())))
			# Runs the method ship_hit for what will happen to the ship.
			ship_hit(ai_settings, screen, ship, explosions, stats, sb)
			# Removes that particular ad_heli in ad_helis.
			ad_helis.remove(ad_heli)
			
def create_explosion_and_time(ai_settings, screen, explosions, death_x, death_y, object='hostile'):
	"""Get object death position and create an explosion on the spot."""
	ai_settings.explosion_time_create = float('{:.1f}'.format(get_process_time()))
	#print("Time create: " + str(ai_settings.explosion_time_create))
	if object == 'hostile':
		create_explosion(ai_settings, screen, explosions, death_x, death_y)
	elif object == 'ship':
		create_explosion(ai_settings, screen, explosions, death_x, death_y, object='ship')





"""_____________________________________________________________________________
   c) Parachutes Internals
_____________________________________________________________________________"""
	
def update_parachutes_internals(ai_settings, screen, parachutes, ad_helis):
	# Updates internals of parachutes in its class file.
	# Specifically, its movements.
	parachutes.update()
	






"""_____________________________________________________________________________
   b) ShipBullet Internals
_____________________________________________________________________________"""

def fire_ship_bullet_internals(ai_settings, screen, ship, shipbullets):
	"""Gets time to fire between shots, creates shipbullet, adds and fire them on that time"""
	# Collects the ship_time_fire and adds the time interval for the 2nd shot.
	shipbullet_time_for_2nd_fire = float('{:.1f}'.format(ai_settings.shipbullet_time_fire + ai_settings.shipbullet_time_fire_interval))
	# Gets the current time in game.
	shipbullet_time_new = float('{:.1f}'.format(get_process_time()))
	# Spacebar or Mousebuttondown, constant_firing is set to True.
	# After that, if the bullet is less than the limit allowed and
	# time_new is greater than time_for_2nd_fire,
	# a bullet is created, added and fired.
	if ai_settings.shipbullets_constant_firing:
		if len(shipbullets) < ai_settings.shipbullets_allowed and shipbullet_time_new >= shipbullet_time_for_2nd_fire:
			ai_settings.shipbullet_time_fire = float('{:.1f}'.format(get_process_time()))
			new_bullet = ShipBullet(ai_settings, screen, ship)
			shipbullets.add(new_bullet)
	
	
def update_shipbullet_internals(ai_settings, screen, ship, shipbullets, parachutes, helis, helibullets, rockets, rockets_hits_list, ad_helis, ad_helis_hits_list, explosions, stats, sb, time_new):
	"""Updates and handles whatever happens to shipbullet."""
	# Create, add, and fires bullet based on specified conditions.
	fire_ship_bullet_internals(ai_settings, screen, ship, shipbullets)
	# Updates internals of shipbullets in its class file.
	# Specifically, its movements.
	shipbullets.update()
	# Get screen rect.
	screen_rect = screen.get_rect()
	
	# Removes the bullets if rect.left passes the screen_rect.right.
	for bullet in shipbullets.copy():
		if bullet.rect.left >= screen_rect.right:
			shipbullets.remove(bullet)
			
	# Handles what happen if hostile and ship projectiles collides.
	check_hostile_shipprojectile_collision(ai_settings, screen, shipbullets, parachutes, helis, rockets, rockets_hits_list, ad_helis, ad_helis_hits_list, explosions, stats, time_new)
	# Handles what happen if hostiles projectiles and ship projectiles collides.
	check_hostileprojectile_shipprojectile_collision(ai_settings, shipbullets, helibullets, stats)
	
	
def check_hostile_shipprojectile_collision(ai_settings, screen, shipbullets, parachutes, helis, rockets, rockets_hits_list, ad_helis, ad_helis_hits_list, explosions, stats, time_new):
	"""Removes the objectprojectiles and the hostiles that collide with each other.
	Adds the score for destroying the hostile object."""
	# Deals with helicopter and objectprojectile.
	check_helicopter_shiprojectile_collision(ai_settings, screen, shipbullets, helis, explosions, stats, time_new)
	# Deals with rocket and objectprojectile.
	check_rocket_shiprojectile_collision(ai_settings, screen, shipbullets, rockets, rockets_hits_list, explosions, stats, time_new)
	# Deals with advanced helicopter and objectprojectile.
	check_ad_heli_shiprojectile_collision(ai_settings, screen, shipbullets, parachutes, ad_helis, ad_helis_hits_list, explosions, stats, time_new)
					
	# Check if it's time for the explosion to disappear. If so, Avada Kedavra.
	check_time_explosion_disappear(ai_settings, explosions, time_new)
	
	






	
	
	
"""_____________________________________________________________________________
   bi) Hostile with ShipProjectile: ShipBullet and Helicopter Internals
_____________________________________________________________________________"""
			
def check_helicopter_shiprojectile_collision(ai_settings, screen, shipbullets, helis, explosions, stats, time_new):
	"""
	Removes the shipbullet and helicopter that collides after 1 hit.
	Adds the score for destroying the helicopter.
	"""
	# Removes the shipbullet and heli that collides.
	helicopter_shipbullet_collisions = pygame.sprite.groupcollide(shipbullets, helis, True, True)
	# If there is a collision, loop through the collided objects/helis and add
	# based on each individual collision.
	# NOTE: This is optimized to be very exact.
	if helicopter_shipbullet_collisions:
		for helis in helicopter_shipbullet_collisions.values():
			stats.score += ai_settings.helicopter_points
			# Loops through the collided helis.
			for heli in helis:
				# Runs explosion counter and creates explosion image
				# at death position of object.
				create_explosion_and_time(ai_settings, screen, explosions, heli.rect.centerx, heli.rect.centery)
	
	






	
	
"""_____________________________________________________________________________
   bii) Hostile with ShipProjectile: ShipBullet and Rocket Internals
_____________________________________________________________________________"""
	
def check_rocket_shiprojectile_collision(ai_settings, screen, shipbullets, rockets, rockets_hits_list, explosions, stats, time_new):
	"""
	Removes the shipbullet and rocket that collides after a specified amount
	of hits.
	Adds the score for destroying the rocket.
	"""
	# NOTE: This whole thing(below) is related to the create_wave_rocket.
	# You can adjust the hits required to remove the rocket by modifying
	# the add_rocket_to_list.
	
	# Removes the shipbullet and rocket that collides.
	rocket_shipbullet_collisions = pygame.sprite.groupcollide(shipbullets, rockets, True, False)
	
	# If there is a collision, loop through the rockets/values that collided
	# with the shipbullets.
	if rocket_shipbullet_collisions:
		for rockets_v in rocket_shipbullet_collisions.values():
			# Loops through the collided rockets and removes that 
			# specific rocket from the list.
			for rocket_v in rockets_v:
				rockets_hits_list.remove(rocket_v)
				
				# Once the number of that specific rocket is removed from the
				# list till 0, the rocket is removed entirely from the screen.
				if rockets_hits_list.count(rocket_v) == 0:
					# Runs explosion counter and creates explosion image
					# at death position of object.
					create_explosion_and_time(ai_settings, screen, explosions, rocket_v.rect.centerx, rocket_v.rect.centery)
					
					rockets.remove(rockets_v)
					stats.score += ai_settings.rocket_points
				
		
	# Ignore for now, it is related to the above rocket_shipbullet_collisions.
	# It is the first version of it.
	# Problem: Can't really append rockets in sprite correctly or accurately
	#          to the dictionary. It can, but once you loop through the list
	#          containing all the dictionaries, the  rocket_id you call might 
	#          not be there.
	""" 
	if rocket_shipbullet_collisions:
		for rockets_v in rocket_shipbullet_collisions.values():
			for rocket_v in rockets_v:
				if not rockets_hits_list:
					print("Empty list: Creating new rocket.")
					create_rocket_hit_dict = {
						'id': rocket_v,
						'hits': 0,
						}
					rockets_hits_list.append(create_rocket_hit_dict)
				
				for rockets_hits_dict in rockets_hits_list:
					print(rockets_hits_list)
					print(rockets_hits_dict.values())
					print(rocket_v)
					print(rocket_v in rockets_hits_dict.values())
					if rocket_v in rockets_hits_dict.values():
						print("Rocket is already in the list, no need to create one.")
					else:
						print("Rocket is not in the list, one should be created.")
						create_rocket_hit_dict = {
							'id': rocket_v,
							'hits': 0,
							}
						rockets_hits_list.append(create_rocket_hit_dict)
						print("Successfully created rocket.\n")
					
				for rockets_hits_dict in rockets_hits_list:
					print("Currently dealing with " + str(len(rockets_hits_list)))
					
					if rockets_hits_dict['id'] == rocket_v:
						print('rockets_hits_dict:', rockets_hits_dict)
						rockets_hits_dict['hits'] = (rockets_hits_dict['hits'] + 1)
						print("Successfully, +1.")
					else:
						continue
						
					if rockets_hits_dict['hits'] == 2:
						rockets.remove(rockets_v)
						rockets_hits_list.remove(rockets_hits_dict)
						print("Successfully removed rocket.")
					
					print("Left to deal with " + str(len(rockets_hits_list)))
					print("-----------------Done for first iteration-----------------\n")
				
				#print("\n")
				#print('rockets_hits_list:', rockets_hits_list)
				
			
	# If there is a collision, loop through the collided objects/rockets and add
	# based on each individual collision.
	# NOTE: This is optimized to be very exact.
	if rocket_shipbullet_collisions:
		for rocket in rocket_shipbullet_collisions.values():
			stats.score += ai_settings.rocket_points

def get_rockets_hits_dict_values(list):
	dicts_v = []
	for dict in list:
		dict_v = dict.values()
		dicts_v.append(dict_v)
		return dicts_v
		"""
	
	






	
	
"""_____________________________________________________________________________
   biii) Hostile with ShipProjectile: ShipBullet and Advanced Helicopter Internals
_____________________________________________________________________________"""

def check_ad_heli_shiprojectile_collision(ai_settings, screen, shipbullets, parachutes, ad_helis, ad_helis_hits_list, explosions, stats, time_new):
	"""
	Removes the shipbullet and ad_heli that collides after a specified amount
	of hits.
	Adds the score for destroying the ad_heli.
	"""
	# NOTE: This whole thing(below) is related to the create_wave_ad_heli.
	# You can adjust the hits required to remove the ad_heli by modifying
	# the add_ad_heli_to_list.
	
	# Removes the shipbullet and ad_heli that collides.
	ad_heli_shipbullet_collisions = pygame.sprite.groupcollide(shipbullets, ad_helis, True, False)
	
	# If there is a collision, loop through the ad_helis/values that collided
	# with the shipbullets.
	if ad_heli_shipbullet_collisions:
		for ad_helis_v in ad_heli_shipbullet_collisions.values():
			# Loops through the collided ad_helis and removes that 
			# specific ad_heli from the list.
			for ad_heli_v in ad_helis_v:
				ad_helis_hits_list.remove(ad_heli_v)
				
				# Once the number of that specific ad_heli is removed from the
				# list till 0, the ad_heli is removed entirely from the screen.
				if ad_helis_hits_list.count(ad_heli_v) == 0:
					# Runs explosion counter and creates explosion image
					# at death position of object.
					create_explosion_and_time(ai_settings, screen, explosions, ad_heli_v.rect.centerx, ad_heli_v.rect.centery)
					
					# Get ad_heli position before removing it.
					ad_heli_death_bottomy = ad_heli_v.rect.bottom
					# Call for parachute upgrades to spawn at the ad_heli's
					# death position.
					create_ad_heli_parachute(ai_settings, screen, parachutes, ad_heli_death_x, ad_heli_death_bottomy)
					
					ad_helis.remove(ad_helis_v)
					stats.score += ai_settings.ad_heli_points
					
					
def create_ad_heli_parachute(ai_settings, screen, parachutes, ad_heli_death_x, ad_heli_death_bottomy):
	"""Creates a new parachute to spawn at the specified position and
	adds it into the list(parachutes)."""
	new_parachute = Parachute(ai_settings, screen)
	new_parachute.centerx = ad_heli_death_x
	new_parachute.centery = ad_heli_death_bottomy
	
	parachutes.add(new_parachute)
	
	
	






	
	
"""_____________________________________________________________________________
   b) Universal
_____________________________________________________________________________"""

def create_explosion(ai_settings, screen, explosions, death_x, death_y, object='hostile'):
	"""Creates a explosion image to spawn at the specified position and
	adds it into the list(explosions)."""
	if object == 'hostile':
		hostile_explosion = Explosion(ai_settings, screen)
		hostile_explosion.centerx = death_x
		hostile_explosion.centery = death_y
		
		explosions.add(hostile_explosion)
	elif object == 'ship':
		ship_explosion = Explosion(ai_settings, screen)
		# Changes the explosion image for ship.
		ship_explosion.image = pygame.image.load('images/explosion/ship_explosion1.bmp')
		ship_explosion.centerx = death_x
		ship_explosion.centery = death_y
		
		explosions.add(ship_explosion)
		
		
def check_time_explosion_disappear(ai_settings, explosions, time_new):
	"""Removes the explosion image after a specified time.
	(Time specified in settings.py)"""
	# Extracts the explosion_time_create and adds the explosion_time_disappear
	# from ai_settings.py to it to get the time_no_immune.
	# Also, gets the process time indefinitely.
	# NOTE: The explosion_time_disappear can be optimized to run just once.
	explosion_time_disappear = float('{:.1f}'.format(ai_settings.explosion_time_create + ai_settings.explosion_time_disappear))
	time_new = float('{:.1f}'.format(get_process_time()))
	#print("Time New: " + str(explosion_time_new))
	#print("Time Disappear: " + str(explosion_time_disappear))
	#print(explosion_time_new == explosion_time_disappear)
	# If time_new equate time_no_immune, remove explosion image.
	for explosion in explosions.copy():
		if time_new == explosion_time_disappear:
			explosions.remove(explosion)
		
	
	







"""_____________________________________________________________________________
   ci) HostileProjectiles with ShipProjectiles: ShipBullet and HeliBullet Internals
_____________________________________________________________________________"""


def check_hostileprojectile_shipprojectile_collision(ai_settings, shipbullets, helibullets, stats):
	"""Removes the shipbullets and the helibullets that collide with each other.
	Adds the score for destroying the hostile projectiles."""
	# Removes the shipbullet and helibullet that collides.
	helibullet_shipbullet_collisions = pygame.sprite.groupcollide(shipbullets, helibullets, True, True)
	# If there is a collision, loop through the collided helibullets and add
	# based on each individual collision.
	# NOTE: This is optimized to be very exact.
	if helibullet_shipbullet_collisions:
		for helibullets in helibullet_shipbullet_collisions.values():
			stats.score += ai_settings.helicopter_bullet_points
			

















""" 12) Upgrades
			a) Rapid Fire
			b) Two Guns
"""

"""_____________________________________________________________________________
   a) Rapid Fire
_____________________________________________________________________________"""



"""_____________________________________________________________________________
   b) Two Guns
_____________________________________________________________________________"""
