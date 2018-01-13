import sys
import pygame
import time

import gf_universals as gf_uni
import gf_sounds as gfsounds

from time import process_time

from random import randint
from random import random

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

from timer import UpgradeTimer

from upgrades import Upgrade

""" This file is sorted in this pattern:
    1) Objects and ObjectProjectiles Internals
    2) Upgrades
    3) 
"""

""" 1) Objects and ObjectProjectiles Internals
		a) Ship
			i) Ship with HostileObjects
		c) Parachutes and Drops
		b) Weapons - ShipBullet, ShipMissile
		
		b) Hostile with ShipProjectile
			i) Helicopter with ShipBullet, ShipMissile
			ii) Rocket with ShipBullet, ShipMissile
			iii) Advanced Helicopter with ShipBullet, ShipMissile
			
		c) HostileProjectiles with ShipProjectiles
			i) HeliBullet with ShipBullet, ShipMissile
			
		d) Loots with Ship & ShipProjectiles
			i) Parachute with ShipBullet, ShipMissile
"""
"""_____________________________________________________________________________
   1a) Objects and ObjectProjectiles Internals: Ship
_____________________________________________________________________________"""

def update_ship_internals(ai_settings, screen, ship, shipbullets, shiprailgun_sounds, shipexplode_sounds, parachutes, helis, helibullets, rockets, rockets_hits_list, ad_helis, ad_helis_hits_list, explosions, stats, sb):
	"""Updates and handles whatever happens to ship."""
	# Update internals of ship from its class file.
	# Specifically, its movements.
	ship.update()
	# Handles what happens if the hostileobject and ship collides.
	check_hostileobject_ship_collision(ai_settings, screen, ship, shiprailgun_sounds, shipexplode_sounds, helis, rockets, ad_helis, explosions, stats, sb)
	
	
	
"""_____________________________________________________________________________
   1ai) Objects and ObjectProjectiles Internals: Ship: 
        Ship with HostileObjects
_____________________________________________________________________________"""


def check_hostileobject_ship_collision(ai_settings, screen, ship, shiprailgun_sounds, shipexplode_sounds, helis, rockets, ad_helis, explosions, stats, sb):
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
			gf_uni.create_explosion_and_time_and_sound(ai_settings, screen, shipexplode_sounds, explosions, heli.rect.centerx, heli.rect.centery)
			
			# Gets the time_hit for immunity counter.
			ai_settings.ship_time_hit = ai_settings.time_game_play
			# Runs the method ship_hit for what will happen to the ship.
			gf_uni.ship_hit(ai_settings, screen, ship, shiprailgun_sounds, shipexplode_sounds, explosions, stats, sb)
			# Removes that particular heli in helis.
			helis.remove(heli)
			
	for rocket in rockets.sprites():
		# Boolean for collision or overlapping of rect between ship and rocket.
		rocket_overlap_ship = ship_rect.colliderect(rocket)
		# If overlap and immunity false, rocket and ship is removed, immunity 
		# counter starts.
		if rocket_overlap_ship and not ship.immunity:
			# Runs explosion counter and creates explosion image
			# at death position of object.
			gf_uni.create_explosion_and_time_and_sound(ai_settings, screen, shipexplode_sounds, explosions, rocket.rect.centerx, rocket.rect.centery)
			
			# Gets the time_hit for immunity counter.
			ai_settings.ship_time_hit = ai_settings.time_game_play
			# Runs the method ship_hit for what will happen to the ship.
			gf_uni.ship_hit(ai_settings, screen, ship, shiprailgun_sounds, shipexplode_sounds, explosions, stats, sb)
			# Removes that particular rocket in rockets.
			rockets.remove(rocket)
			
	for ad_heli in ad_helis.sprites():
		# Boolean for collision or overlapping of rect between ship and ad_heli.
		ad_heli_overlap_ship = ship_rect.colliderect(ad_heli)
		# If overlap and immunity false, ad_heli and ship is removed, immunity 
		# counter starts.
		if ad_heli_overlap_ship and not ship.immunity:
			# Runs explosion counter and creates explosion image
			# at death position of object.
			gf_uni.create_explosion_and_time_and_sound(ai_settings, screen, shipexplode_sounds, explosions, ad_heli.rect.centerx, ad_heli.rect.centery)
			
			# Gets the time_hit for immunity counter.
			ai_settings.ship_time_hit = ai_settings.time_game_play
			# Runs the method ship_hit for what will happen to the ship.
			gf_uni.ship_hit(ai_settings, screen, ship, shiprailgun_sounds, shipexplode_sounds, explosions, stats, sb)
			# Removes that particular ad_heli in ad_helis.
			ad_helis.remove(ad_heli)





"""_____________________________________________________________________________
   1c) Objects and ObjectProjectiles Internals: Parachutes and Drops
_____________________________________________________________________________"""
	
def update_parachutes_internals(ai_settings, screen, ship, shipbullets, shipmissiles, parachutes, u_rail, u_secondary, u_missile, u_laser, ad_helis, stats, sb):
	# Updates internals of parachutes in its class file.
	# Specifically, its movements.
	parachutes.update()
	
	# Handles what happen if loots and ship projectiles collides.
	check_loot_shipprojectile_collision(ai_settings, screen, ship, shipbullets, shipmissiles, parachutes, u_rail, u_secondary, u_missile, u_laser, stats, sb)
	
def update_drops_internals(ai_settings, screen, ship, shipbullets, shiprailgun_sounds, shipmissiles, u_rail, u_secondary, u_missile, u_laser, u_i_rail, u_i_secondary, u_i_missile, u_i_laser, sb):
	# Updates internals of all the upgrades in its class file.
	# Specifically, its movements.
	u_rail.update()
	u_secondary.update()
	u_missile.update()
	u_laser.update()
	
	# Get screen rect.
	screen_rect = screen.get_rect()
	# Removes the upgrade_drop if rect.right passes the screen_rect.left.
	for rail in u_rail.copy():
		if rail.rect.right <= screen_rect.left:
			u_rail.remove(rail)
	for secondary in u_secondary.copy():
		if secondary.rect.right <= screen_rect.left:
			u_secondary.remove(secondary)
	for missile in u_missile.copy():
		if missile.rect.right <= screen_rect.left:
			u_missile.remove(missile)
	for laser in u_laser.copy():
		if laser.rect.right <= screen_rect.left:
			u_laser.remove(laser)
	
	# Handles what happens if drops and ship projectiles collides.
	check_drops_shipprojectile_collision(ai_settings, screen, ship, shipbullets, shiprailgun_sounds, shipmissiles, u_rail, u_secondary, u_missile, u_laser, u_i_rail, u_i_secondary, u_i_missile, u_i_laser, sb)
	# If the upgrade time is up, remove the upgrades.
	check_upgrade_cooldown(ai_settings, ship, shiprailgun_sounds, u_i_rail, u_i_secondary, u_i_missile, u_i_laser)
	
def update_upgrade_timers(gameclock, u_i_rail, u_i_secondary, u_i_missile, u_i_laser):
	"""Update and shows the time and upgrade_timer."""
	# Updates the timer with the new time.
	gameclock.update_timer()
	# Updates the time left for the upgrades.
	u_i_rail.update()
	u_i_secondary.update()
	u_i_missile.update()
	u_i_laser.update()





"""_____________________________________________________________________________
   1b) Objects and ObjectProjectiles Internals: Weapons - ShipBullet, ShipMissile
_____________________________________________________________________________"""


def update_shipweapon_internals(ai_settings, screen, ship, shipbullets, shipbullet_sounds, shipmissiles, shipmissile_sounds, shipexplode_sounds, parachutes, helis, helibullets, rockets, rockets_hits_list, ad_helis, ad_helis_hits_list, explosions, stats, sb):
	"""Updates and handles all instances of the ship's weapons."""
	# Deals with ShipBullets.
	update_shipbullet_internals(ai_settings, screen, ship, shipbullets, shipbullet_sounds)
	# Deals with ShipMissiles.
	update_shipmissile_internals(ai_settings, screen, ship, shipmissiles, shipmissile_sounds)
	
	"""print(ship.upgrades_allow_railguns)
	print(ship.upgrades_allow_bullets)
	print(ship.upgrades_allow_bullet_secondary_gun)
	print(ship.upgrades_allow_missiles)
	print(ship.upgrades_allow_missile_secondary_gun)
	print(ship.upgrades_allow_lasers, "\n")"""
			
	# Handles what happen if hostile and ship projectiles collides.
	check_hostile_shipprojectile_collision(ai_settings, screen, shipbullets, shipmissiles, shipexplode_sounds, parachutes, helis, rockets, rockets_hits_list, ad_helis, ad_helis_hits_list, explosions, stats)
	# Handles what happen if hostiles projectiles and ship projectiles collides.
	check_hostileprojectile_shipprojectile_collision(ai_settings, shipbullets, shipmissiles, helibullets, stats)
	
	

def fire_ship_bullet_internals(ai_settings, screen, ship, shipbullets, shipbullet_sounds):
	"""Gets time to fire between shots, creates shipbullet, adds and fire them on that time"""
	# Collects the ship_time_fire and adds the time interval for the 2nd shot.
	shipbullet_time_for_2nd_fire = float('{:.1f}'.format(ai_settings.shipbullet_time_fire + ai_settings.shipbullet_time_fire_interval))
	# Gets the current time in game.
	shipbullet_time_new = ai_settings.time_game_play
	# Spacebar or Mousebuttondown, constant_firing is set to True.
	#
	# After that, if the bullet is less than the limit allowed and
	# ai_settings.time_game_play is greater than time_for_2nd_fire,
	# a bullet is created, added and fired.
	#
	# If Secondary_gun is allowed, we add that to shipbullets too.
	if ai_settings.shipbullets_constant_firing:
		if len(shipbullets) < ai_settings.shipbullets_allowed and shipbullet_time_new >= shipbullet_time_for_2nd_fire:
			# Calls the function shipmissile_sound_firing_internals.
			gfsounds.shipbullet_sound_firing_internals(ai_settings, ship, shipbullet_sounds)
			ai_settings.shipbullet_time_fire = ai_settings.time_game_play
			new_bullet = ShipBulletPrimary(ai_settings, screen, ship)
			shipbullets.add(new_bullet)
			
			# Activates the Railguns.
			upgrade_railguns(ai_settings, ship)
			# Activates the Secondary Gun.
			upgrade_bullet_secondary_gun(ai_settings, screen, ship, shipbullets)
	
def update_shipbullet_internals(ai_settings, screen, ship, shipbullets, shipbullet_sounds):
	"""Updates and handles whatever happens to shipbullet."""
	# Create, add, and fires bullet based on specified conditions.
	fire_ship_bullet_internals(ai_settings, screen, ship, shipbullets, shipbullet_sounds)
	# Updates internals of shipbullets in its class file.
	# Specifically, its movements.
	shipbullets.update()
	# Get screen rect.
	screen_rect = screen.get_rect()
	
	# Removes the bullets if rect.left passes the screen_rect.right.
	for bullet in shipbullets.copy():
		if bullet.rect.left >= screen_rect.right:
			shipbullets.remove(bullet)
		
def upgrade_railguns(ai_settings, ship):
	"""Changes from normal guns to railguns."""
	# Increases the rate of fire.
	if ship.upgrades_allow_railguns:
		ai_settings.shipbullet_time_fire_interval = 0.15
	
def upgrade_bullet_secondary_gun(ai_settings, screen, ship, shipbullets):
	"""Allow secondary guns to fire."""
	# Creates a new bullet that will spawn at the Secondary position.
	if ship.upgrades_allow_bullet_secondary_gun:
		new_bullet = ShipBulletSecondary(ai_settings, screen, ship)
		shipbullets.add(new_bullet)
	
	
	
	
	
	

def fire_ship_missile_internals(ai_settings, screen, ship, shipmissiles, shipmissile_sounds):
	"""Gets time to fire between shots, creates shipmissile, adds and fire them on that time"""
	# Collects the ship_time_fire and adds the time interval for the 2nd shot.
	shipmissile_time_for_2nd_fire = float('{:.1f}'.format(ai_settings.shipmissile_time_fire + ai_settings.shipmissile_time_fire_interval))
	# Gets the current time in game.
	shipmissile_time_new = ai_settings.time_game_play
	# Spacebar or Mousebuttondown, constant_firing is set to True.
	#
	# After that, if the missile is less than the limit allowed and
	# ai_settings.time_game_play is greater than time_for_2nd_fire,
	# a missile is created, added and fired.
	#
	# If Secondary_gun is allowed, we add that to shipmissiles too.
	if ai_settings.shipmissiles_constant_firing:
		if len(shipmissiles) < ai_settings.shipmissiles_allowed and shipmissile_time_new >= shipmissile_time_for_2nd_fire:
			# Calls the function shipmissile_sound_firing_internals.
			gfsounds.shipmissile_sound_firing_internals(ai_settings, ship, shipmissile_sounds)
			ai_settings.shipmissile_time_fire = ai_settings.time_game_play
			new_missile = ShipMissilePrimary(ai_settings, screen, ship)
			shipmissiles.add(new_missile)
			
			# Activates the Secondary Gun.
			upgrade_missile_secondary_gun(ai_settings, screen, ship, shipmissiles, shipmissile_sounds)
		
	
def update_shipmissile_internals(ai_settings, screen, ship, shipmissiles, shipmissile_sounds):
	"""
	Switches main guns to missiles / Allow missiles to be fired.
	
	Updates and handles whatever happens to shipmissile.
	"""
	# Create, add, and fires missile based on specified conditions.
	fire_ship_missile_internals(ai_settings, screen, ship, shipmissiles, shipmissile_sounds)
	# Updates internals of shipmissiles in its class file.
	# Specifically, its movements.
	shipmissiles.update()
	# Get screen rect.
	screen_rect = screen.get_rect()
	
	# Removes the missiles if rect.left passes the screen_rect.right.
	for missile in shipmissiles.copy():
		if missile.rect.left >= screen_rect.right:
			shipmissiles.remove(missile)
	
def upgrade_missile_secondary_gun(ai_settings, screen, ship, shipmissiles, shipmissile_sounds):
	"""Allows secondary guns to fire."""
	# Creates a new missile that will spawn at the Secondary position.
	if ship.upgrades_allow_missile_secondary_gun:
		# Calls the function shipmissile_sound_firing_internals.
		gfsounds.shipmissile_sound_firing_internals(ai_settings, ship, shipmissile_sounds)
		new_missile = ShipMissileSecondary(ai_settings, screen, ship)
		shipmissiles.add(new_missile)
	
	
	
	
	
	


	
def upgrade_laser(ai_settings, screen, ship, shiplasers):
	"""Upgrades/Changes main guns to lasers."""
	#if ship.upgrades_allow_lasers:
	
	
def check_hostile_shipprojectile_collision(ai_settings, screen, shipbullets, shipmissiles, shipexplode_sounds, parachutes, helis, rockets, rockets_hits_list, ad_helis, ad_helis_hits_list, explosions, stats):
	"""Removes the objectprojectiles and the hostiles that collide with each other.
	Adds the score for destroying the hostile object."""
	# Deals with helicopter and objectprojectile.
	check_helicopter_shiprojectile_collision(ai_settings, screen, shipbullets, shipmissiles, shipexplode_sounds, helis, explosions, stats)
	# Deals with rocket and objectprojectile.
	check_rocket_shiprojectile_collision(ai_settings, screen, shipbullets, shipmissiles, shipexplode_sounds, rockets, rockets_hits_list, explosions, stats)
	# Deals with advanced helicopter and objectprojectile.
	check_ad_heli_shiprojectile_collision(ai_settings, screen, shipbullets, shipmissiles, shipexplode_sounds, parachutes, ad_helis, ad_helis_hits_list, explosions, stats)
					
	# Check if it's time for the explosion to disappear. If so, Avada Kedavra.
	gf_uni.check_time_explosion_disappear(ai_settings, explosions)
		
		
	






	
	
	
"""_____________________________________________________________________________
   1bi) Objects and ObjectProjectiles Internals: Hostile with ShipProjectile: 
        ShipBullet, ShipMissile and Helicopter
_____________________________________________________________________________"""

def check_helicopter_shiprojectile_collision(ai_settings, screen, shipbullets, shipmissiles, shipexplode_sounds, helis, explosions, stats):
	"""
	Removes the objectprojectile and helicopter that collides after 1 hit.
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
				gf_uni.create_explosion_and_time_and_sound(ai_settings, screen, shipexplode_sounds, explosions, heli.rect.centerx, heli.rect.centery)
				
	# Removes the shipmissile and heli that collides.
	helicopter_shipmissile_collisions = pygame.sprite.groupcollide(shipmissiles, helis, True, True)
	# If there is a collision, loop through the collided objects/helis and add
	# based on each individual collision.
	# NOTE: This is optimized to be very exact.
	if helicopter_shipmissile_collisions:
		for helis in helicopter_shipmissile_collisions.values():
			stats.score += ai_settings.helicopter_points
			# Loops through the collided helis.
			for heli in helis:
				# Runs explosion counter and creates explosion image
				# at death position of object.
				gf_uni.create_explosion_and_time_and_sound(ai_settings, screen, shipexplode_sounds, explosions, heli.rect.centerx, heli.rect.centery)
	
	






	
	
"""_____________________________________________________________________________
   1bii) Objects and ObjectProjectiles Internals: Hostile with ShipProjectile:
         ShipBullet, ShipMissile and Rocket
_____________________________________________________________________________"""
	
def check_rocket_shiprojectile_collision(ai_settings, screen, shipbullets, shipmissiles, shipexplode_sounds, rockets, rockets_hits_list, explosions, stats):
	"""
	Removes the objectprojectile and rocket that collides after a specified amount
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
					gf_uni.create_explosion_and_time_and_sound(ai_settings, screen, shipexplode_sounds, explosions, rocket_v.rect.centerx, rocket_v.rect.centery)
					
					rockets.remove(rockets_v)
					stats.score += ai_settings.rocket_points
	
	# Removes the shipmissile and rocket that collides.
	rocket_shipmissile_collisions = pygame.sprite.groupcollide(shipmissiles, rockets, True, True)
	# If there is a collision, loop through the collided objects/rockets and add
	# based on each individual collision.
	# NOTE: This is optimized to be very exact.
	if rocket_shipmissile_collisions:
		for rockets_v in rocket_shipmissile_collisions.values():
			stats.score += ai_settings.rocket_points
			# Loops through the collided rockets.
			for rocket_v in rockets_v:
				# Runs explosion counter and creates explosion image
				# at death position of object.
				gf_uni.create_explosion_and_time_and_sound(ai_settings, screen, shipexplode_sounds, explosions, rocket_v.rect.centerx, rocket_v.rect.centery)
	
				
		
	# Ignore for now, it is related to the above rocket_shipbullet_collisions.
	# It is the first version of it.
	# Problem: Can't really append rockets in sprite correctly or accurately
	#          to the dictionary. It can, but once you loop through the list
	#          containing all the dictionaries, the rocket_id you call might 
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
   1biii) Objects and ObjectProjectiles Internals: Hostile with ShipProjectile:
          ShipBullet, ShipMissile and Advanced Helicopter
_____________________________________________________________________________"""

def check_ad_heli_shiprojectile_collision(ai_settings, screen, shipbullets, shipmissiles, shipexplode_sounds, parachutes, ad_helis, ad_helis_hits_list, explosions, stats):
	"""
	Removes the objectprojectile and ad_heli that collides after a specified amount
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
				try:
					ad_helis_hits_list.remove(ad_heli_v)
				except ValueError:
					pass
				
				# Once the number of that specific ad_heli is removed from the
				# list till 0, the ad_heli is removed entirely from the screen.
				if ad_helis_hits_list.count(ad_heli_v) == 0:
					# Runs explosion counter and creates explosion image
					# at death position of object.
					gf_uni.create_explosion_and_time_and_sound(ai_settings, screen, shipexplode_sounds, explosions, ad_heli_v.rect.centerx, ad_heli_v.rect.centery)
					
					# Get ad_heli position before removing it.
					ad_heli_death_bottomy = ad_heli_v.rect.bottom
					ad_heli_death_centerx = ad_heli_v.rect.centerx
					# Call for parachute upgrades to spawn at the ad_heli's
					# death position.
					create_ad_heli_parachute(ai_settings, screen, parachutes, ad_heli_death_centerx, ad_heli_death_bottomy)
					
					ad_helis.remove(ad_helis_v)
					stats.score += ai_settings.ad_heli_points
	
	# Removes the shipmissile and ad_heli that collides.
	ad_heli_shipmissile_collisions = pygame.sprite.groupcollide(shipmissiles, ad_helis, True, False)
	# If there is a collision, loop through the collided objects/ad_helis and add
	# based on each individual collision.
	# NOTE: This is optimized to be very exact.
	if ad_heli_shipmissile_collisions:
		for ad_helis_v in ad_heli_shipmissile_collisions.values():
			stats.score += ai_settings.ad_heli_points
			# Loops through the individually collided ad_helis.
			for ad_heli_v in ad_helis_v:
				# Runs explosion counter and creates explosion image
				# at death position of object.
				gf_uni.create_explosion_and_time_and_sound(ai_settings, screen, shipexplode_sounds, explosions, ad_heli_v.rect.centerx, ad_heli_v.rect.centery)
				
				# Get ad_heli position before removing it.
				ad_heli_death_bottomy = ad_heli_v.rect.bottom
				ad_heli_death_centerx = ad_heli_v.rect.centerx
				# Call for parachute upgrades to spawn at the ad_heli's
				# death position.
				create_ad_heli_parachute(ai_settings, screen, parachutes, ad_heli_death_centerx, ad_heli_death_bottomy)
				
				ad_helis.remove(ad_helis_v)
				stats.score += ai_settings.ad_heli_points
					
					
def create_ad_heli_parachute(ai_settings, screen, parachutes, ad_heli_death_x, ad_heli_death_bottomy):
	"""Creates a new parachute to spawn at the specified position and
	adds it into the list(parachutes)."""
	new_parachute = Parachute(ai_settings, screen)
	new_parachute.centerx = ad_heli_death_x
	new_parachute.centery = ad_heli_death_bottomy - 25
	
	parachutes.add(new_parachute)
		
	
	







"""_____________________________________________________________________________
   1ci) Objects and ObjectProjectiles Internals: HostileProjectiles with ShipProjectiles:
        ShipBullet, ShipMissile and HeliBullet
_____________________________________________________________________________"""

def check_hostileprojectile_shipprojectile_collision(ai_settings, shipbullets, shipmissiles, helibullets, stats):
	"""Removes the objectprojectile and the hostileprojectile that collide with each other.
	Adds the score for destroying the hostile projectiles."""
	
	# Removes the shipbullet and helibullet that collides.
	helibullet_shipbullet_collisions = pygame.sprite.groupcollide(shipbullets, helibullets, True, True)
	# If there is a collision, loop through the collided helibullets and add
	# based on each individual collision.
	# NOTE: This is optimized to be very exact.
	if helibullet_shipbullet_collisions:
		for helibullets in helibullet_shipbullet_collisions.values():
			stats.score += ai_settings.helicopter_bullet_points
	
	# Removes the shipmissile and helibullet that collides.
	helibullet_shipmissile_collisions = pygame.sprite.groupcollide(shipmissiles, helibullets, True, True)
	# If there is a collision, loop through the collided helibullets and add
	# based on each individual collision.
	# NOTE: This is optimized to be very exact.
	if helibullet_shipmissile_collisions:
		for helibullets in helibullet_shipmissile_collisions.values():
			stats.score += ai_settings.helicopter_bullet_points
		
	
	







"""_____________________________________________________________________________
   1di) Objects and ObjectProjectiles Internals: Loots with Ship & ShipProjectiles:
        Parachute with ShipBullet, ShipMissile
_____________________________________________________________________________"""

def check_loot_shipprojectile_collision(ai_settings, screen, ship, shipbullets, shipmissiles, parachutes, u_rail, u_secondary, u_missile, u_laser, stats, sb):
	"""Removes the objectprojectile and the parachute that collide with each other.
	Adds the score for destroying the hostile projectiles."""
	# Removes the shipbullet/shipmissile and parachute that collides.
	parachute_shipbullet_collision = pygame.sprite.groupcollide(shipbullets, parachutes, True, False)
	parachute_shipmissile_collision = pygame.sprite.groupcollide(shipmissiles, parachutes, True, False)
	# If there is a collision, loop through the collided parachutes and create
	# drops/upgrades based on each individual collision at their positions.
	# NOTE: This is optimized to be very exact.
	if parachute_shipbullet_collision:
		for parachutes_v in parachute_shipbullet_collision.values():
			stats.score += ai_settings.parachute_points
			# Loops specifically into the respective parachutes.
			#
			# Creates the drops/upgrades at parachute death positions.
			# Remove the parachute from parachutes when done gathering data.
			for parachute_v in parachutes_v:
				parachute_death_centerx = parachute_v.rect.centerx
				parachute_death_centery = parachute_v.rect.centery
				parachutes.remove(parachute_v)
				
				create_drops(ai_settings, screen, ship, u_rail, u_secondary, u_missile, u_laser, sb, parachute_death_centerx, parachute_death_centery)
			
	if parachute_shipmissile_collision:
		for parachutes_v in parachute_shipmissile_collision.values():
			stats.score += ai_settings.parachute_points
			# Loops specifically into the respective parachutes.
			#
			# Creates the drops/upgrades at parachute death positions.
			# Remove the parachute from parachutes when done gathering data.
			for parachute_v in parachutes_v:
				parachute_death_centerx = parachute_v.rect.centerx
				parachute_death_centery = parachute_v.rect.centery
				parachutes.remove(parachute_v)
				
				create_drops(ai_settings, screen, ship, u_rail, u_secondary, u_missile, u_laser, sb, parachute_death_centerx, parachute_death_centery)
	
def create_drops(ai_settings, screen, ship, u_rail, u_secondary, u_missile, u_laser, sb, parachute_death_centerx, parachute_death_centery):
	"""Spawns the types of upgrades based on probability specified in settings."""
	# chance is the probability.
	#
	# Depending on the Ship's Default Weapon Mode (Specified in settings).
	#
	# Creates the drop at the parachute's death location and adds those to the
	# respective drops/upgrades group.
	chance = random()
	if ai_settings.ship_weapon_default == 1:
		if chance <= ai_settings.upgrades_laser_p:
			print("Laser")
			new_drop = Upgrade(ai_settings, screen, sb)
			new_drop.upgrade_type = 4
			new_drop.centerx = parachute_death_centerx
			new_drop.centery = parachute_death_centery
			u_laser.add(new_drop)
		elif chance <= ai_settings.upgrades_missile_p:
			print("Missile")
			new_drop = Upgrade(ai_settings, screen, sb)
			new_drop.upgrade_type = 3
			new_drop.centerx = parachute_death_centerx
			new_drop.centery = parachute_death_centery
			u_missile.add(new_drop)
		elif chance <= ai_settings.upgrades_secondary_p:
			print("Secondary")
			new_drop = Upgrade(ai_settings, screen, sb)
			new_drop.upgrade_type = 2
			new_drop.centerx = parachute_death_centerx
			new_drop.centery = parachute_death_centery
			u_secondary.add(new_drop)
		elif chance <= ai_settings.upgrades_railgun_p:
			print("Railgun")
			new_drop = Upgrade(ai_settings, screen, sb)
			new_drop.upgrade_type = 1
			new_drop.centerx = parachute_death_centerx
			new_drop.centery = parachute_death_centery
			u_rail.add(new_drop)
			
	elif ai_settings.ship_weapon_default == 2:
		if chance <= ai_settings.upgrades_laser_p:
			print("Laser")
			new_drop = Upgrade(ai_settings, screen, sb)
			new_drop.upgrade_type = 4
			new_drop.centerx = parachute_death_centerx
			new_drop.centery = parachute_death_centery
			u_laser.add(new_drop)
		elif chance <= ai_settings.upgrades_railgun_p:
			print("Railgun")
			new_drop = Upgrade(ai_settings, screen, sb)
			new_drop.upgrade_type = 1
			new_drop.centerx = parachute_death_centerx
			new_drop.centery = parachute_death_centery
			u_rail.add(new_drop)
		elif chance <= ai_settings.upgrades_secondary_p:
			print("Secondary")
			new_drop = Upgrade(ai_settings, screen, sb)
			new_drop.upgrade_type = 2
			new_drop.centerx = parachute_death_centerx
			new_drop.centery = parachute_death_centery
			u_secondary.add(new_drop)
		elif chance <= ai_settings.upgrades_missile_p:
			print("Missile")
			new_drop = Upgrade(ai_settings, screen, sb)
			new_drop.upgrade_type = 3
			new_drop.centerx = parachute_death_centerx
			new_drop.centery = parachute_death_centery
			u_missile.add(new_drop)
			
def check_drops_shipprojectile_collision(ai_settings, screen, ship, shipbullets, shiprailgun_sounds, shipmissiles, u_rail, u_secondary, u_missile, u_laser, u_i_rail, u_i_secondary, u_i_missile, u_i_laser, sb):
	"""Handles the events that will occur based on the different types of
	collision that happens between objectprojectile and the drops/upgrades."""
	# Removes the objectprojectile and the drop that collide with each other.
	u_rail_shipbullet_collision = pygame.sprite.groupcollide(shipbullets, u_rail, True, True)
	u_rail_shipmissile_collision = pygame.sprite.groupcollide(shipmissiles, u_rail, True, True)
	
	u_secondary_shipbullet_collision = pygame.sprite.groupcollide(shipbullets, u_secondary, True, True)
	u_secondary_shipmissile_collision = pygame.sprite.groupcollide(shipmissiles, u_secondary, True, True)
	
	u_missile_shipbullet_collision = pygame.sprite.groupcollide(shipbullets, u_missile, True, True)
	u_missile_shipmissile_collision = pygame.sprite.groupcollide(shipmissiles, u_missile, True, True)
	
	u_laser_shipbullet_collision = pygame.sprite.groupcollide(shipbullets, u_laser, True, True)
	u_laser_shipmissile_collision = pygame.sprite.groupcollide(shipmissiles, u_laser, True, True)
	
	# If that specific upgrade is already True, we extend its duration.
	# Else, sets the Timer, removes all current upgrades and enables the Upgrade.
	if u_rail_shipbullet_collision:
		for u_rail in u_rail_shipbullet_collision.values():
			if ship.upgrades_allow_railguns:
				ai_settings.upgrades_time_railgun_end += ai_settings.upgrades_time_railgun_duration
			else:
				ai_settings.upgrades_no_of_current_upgrades += 1
				ai_settings.upgrades_time_railgun_end = ai_settings.time_game_play + ai_settings.upgrades_time_railgun_duration
				new_upgrade = Upgrade(ai_settings, screen, sb)
				new_upgrade.upgrade_type = 1
				new_upgrade.is_upgrade_timer = True
				new_upgrade.image_placement_no = ai_settings.upgrades_no_of_current_upgrades
				u_i_rail.add(new_upgrade)
				new_time = UpgradeTimer(ai_settings, screen, ship, sb, new_upgrade)
				new_time.upgrade_type = 1
				u_i_rail.add(new_time)
				if ship.upgrades_allow_bullets:
					ship.upgrades_allow_railguns = True
				"""else:
					remove_upgrades_all(ai_settings, ship)
					ship.upgrades_allow_bullets = True
					ship.upgrades_allow_railguns = True"""
	if u_rail_shipmissile_collision:
		for u_rail in u_rail_shipmissile_collision.values():
			if ship.upgrades_allow_railguns:
				ai_settings.upgrades_time_railgun_end += ai_settings.upgrades_time_railgun_duration
			else:
				if ship.upgrades_allow_missiles:
					ship.upgrades_allow_missiles = False
					ai_settings.upgrades_time_missile_end = ai_settings.time_game_play - 1
					ai_settings.upgrades_no_of_current_upgrades -= 1
					u_i_missile.empty()
					ship.upgrades_allow_bullets = True
					ship.upgrades_allow_railguns = True
					if ai_settings.shipmissiles_constant_firing:
						ai_settings.shipmissiles_constant_firing = False
						ai_settings.shipbullets_constant_firing = True
					if ship.upgrades_allow_missile_secondary_gun:
						ship.upgrades_allow_missile_secondary_gun = False
						ai_settings.upgrades_time_secondary_end = ai_settings.time_game - 1
						ai_settings.upgrades_no_of_current_upgrades -= 1
						u_i_secondary.empty()
				ai_settings.upgrades_no_of_current_upgrades += 1
				ai_settings.upgrades_time_railgun_end = ai_settings.time_game_play + ai_settings.upgrades_time_railgun_duration
				new_upgrade = Upgrade(ai_settings, screen, sb)
				new_upgrade.upgrade_type = 1
				new_upgrade.is_upgrade_timer = True
				new_upgrade.image_placement_no = ai_settings.upgrades_no_of_current_upgrades
				u_i_rail.add(new_upgrade)
				new_time = UpgradeTimer(ai_settings, screen, ship, sb, new_upgrade)
				new_time.upgrade_type = 1
				u_i_rail.add(new_time)
				"""else:
					remove_upgrades_all(ai_settings, ship)
					ship.upgrades_allow_railguns = True"""
			
	if u_secondary_shipbullet_collision:
		for u_secondary in u_secondary_shipbullet_collision.values():
			if ship.upgrades_allow_bullet_secondary_gun:
				ai_settings.upgrades_time_secondary_end += ai_settings.upgrades_time_secondary_duration
			else:
				ai_settings.upgrades_no_of_current_upgrades += 1
				ai_settings.upgrades_time_secondary_end = ai_settings.time_game_play + ai_settings.upgrades_time_secondary_duration
				new_upgrade = Upgrade(ai_settings, screen, sb)
				new_upgrade.upgrade_type = 2
				new_upgrade.is_upgrade_timer = True
				new_upgrade.image_placement_no = ai_settings.upgrades_no_of_current_upgrades
				u_i_secondary.add(new_upgrade)
				new_time = UpgradeTimer(ai_settings, screen, ship, sb, new_upgrade)
				new_time.upgrade_type = 2
				u_i_secondary.add(new_time)
				if ship.upgrades_allow_bullets:
					ship.upgrades_allow_bullet_secondary_gun = True
				if ship.upgrades_allow_railguns:
					ship.upgrades_allow_bullet_secondary_gun = True
				"""else:
					remove_upgrades_all(ai_settings, ship)
					ship.upgrades_allow_bullets = True
					ship.upgrades_allow_bullet_secondary_gun = True"""
	if u_secondary_shipmissile_collision:
		for u_secondary in u_secondary_shipmissile_collision.values():
			if ship.upgrades_allow_missile_secondary_gun:
				ai_settings.upgrades_time_secondary_end += ai_settings.upgrades_time_secondary_duration
			else:
				ai_settings.upgrades_no_of_current_upgrades += 1
				ai_settings.upgrades_time_secondary_end = ai_settings.time_game_play + ai_settings.upgrades_time_secondary_duration
				new_upgrade = Upgrade(ai_settings, screen, sb)
				new_upgrade.upgrade_type = 2
				new_upgrade.is_upgrade_timer = True
				new_upgrade.image_placement_no = ai_settings.upgrades_no_of_current_upgrades
				u_i_secondary.add(new_upgrade)
				new_time = UpgradeTimer(ai_settings, screen, ship, sb, new_upgrade)
				new_time.upgrade_type = 2
				u_i_secondary.add(new_time)
				if ship.upgrades_allow_missiles:
					ship.upgrades_allow_missile_secondary_gun = True
				"""else:
					remove_upgrades_all(ai_settings, ship)
					ship.upgrades_allow_missile_secondary_gun = True"""
			
	if u_missile_shipbullet_collision:
		for u_missile in u_missile_shipbullet_collision.values():
			if ship.upgrades_allow_missiles:
				ai_settings.upgrades_time_missile_end += ai_settings.upgrades_time_missile_duration
			else:
				if ship.upgrades_allow_bullets:
					ship.upgrades_allow_bullets = False
					ship.upgrades_allow_missiles = True
					if ai_settings.shipbullets_constant_firing:
						ai_settings.shipbullets_constant_firing = False
						ai_settings.shipmissiles_constant_firing = True
					if ship.upgrades_allow_railguns:
						ship.upgrades_allow_railguns = False
						ai_settings.upgrades_time_railgun_end = ai_settings.time_game_play - 1
						ai_settings.upgrades_no_of_current_upgrades -= 1
						gfsounds.shiprailgun_sound_end_internals(ai_settings, ship, shiprailgun_sounds)
						u_i_rail.empty()
					if ship.upgrades_allow_bullet_secondary_gun:
						ship.upgrades_allow_bullet_secondary_gun = False
						ai_settings.upgrades_time_secondary_end = ai_settings.time_game - 1
						ai_settings.upgrades_no_of_current_upgrades -= 1
						u_i_secondary.empty()
				ai_settings.upgrades_no_of_current_upgrades += 1
				ai_settings.upgrades_time_missile_end = ai_settings.time_game_play + ai_settings.upgrades_time_missile_duration
				new_upgrade = Upgrade(ai_settings, screen, sb)
				new_upgrade.upgrade_type = 3
				new_upgrade.is_upgrade_timer = True
				new_upgrade.image_placement_no = ai_settings.upgrades_no_of_current_upgrades
				u_i_missile.add(new_upgrade)
				new_time = UpgradeTimer(ai_settings, screen, ship, sb, new_upgrade)
				new_time.upgrade_type = 3
				u_i_missile.add(new_time)
				"""else:
					remove_upgrades_all(ai_settings, ship)
					ship.upgrades_allow_missiles = True"""
	if u_missile_shipmissile_collision:
		for u_missile in u_missile_shipmissile_collision.values():
			if ship.upgrades_allow_missiles:
				ai_settings.upgrades_time_missile_end += ai_settings.upgrades_time_missile_duration
			else:
				ai_settings.upgrades_no_of_current_upgrades += 1
				ai_settings.upgrades_time_missile_end = ai_settings.time_game_play + ai_settings.upgrades_time_missile_duration
				new_upgrade = Upgrade(ai_settings, screen, sb)
				new_upgrade.upgrade_type = 3
				new_upgrade.is_upgrade_timer = True
				new_upgrade.image_placement_no = ai_settings.upgrades_no_of_current_upgrades
				u_i_missile.add(new_upgrade)
				new_time = UpgradeTimer(ai_settings, screen, ship, sb, new_upgrade)
				new_time.upgrade_type = 3
				u_i_missile.add(new_time)
				remove_upgrades_all(ai_settings, ship)
				ship.upgrades_allow_missiles = True
			
	if u_laser_shipbullet_collision:
		for u_laser in u_laser_shipbullet_collision.values():
			if ship.upgrades_allow_lasers:
				ai_settings.upgrades_time_laser_end += ai_settings.upgrades_time_laser_duration
			else:
				ai_settings.upgrades_no_of_current_upgrades += 1
				ai_settings.upgrades_time_laser_end = ai_settings.time_game_play + ai_settings.upgrades_time_laser_duration
				new_upgrade = Upgrade(ai_settings, screen, sb)
				new_upgrade.upgrade_type = 4
				new_upgrade.is_upgrade_timer = True
				new_upgrade.image_placement_no = ai_settings.upgrades_no_of_current_upgrades
				u_i_laser.add(new_upgrade)
				new_time = UpgradeTimer(ai_settings, screen, ship, sb, new_upgrade)
				new_time.upgrade_type = 4
				u_i_laser.add(new_time)
				remove_upgrades_all(ai_settings, ship)
				ship.upgrades_allow_lasers = True
	if u_laser_shipmissile_collision:
		for u_laser in u_laser_shipmissile_collision.values():
			if ship.upgrades_allow_lasers:
				ai_settings.upgrades_time_laser_end += ai_settings.upgrades_time_laser_duration
			else:
				ai_settings.upgrades_no_of_current_upgrades += 1
				ai_settings.upgrades_time_laser_end = ai_settings.time_game_play + ai_settings.upgrades_time_laser_duration
				new_upgrade = Upgrade(ai_settings, screen, sb)
				new_upgrade.upgrade_type = 4
				new_upgrade.is_upgrade_timer = True
				new_upgrade.image_placement_no = ai_settings.upgrades_no_of_current_upgrades
				u_i_laser.add(new_upgrade)
				new_time = UpgradeTimer(ai_settings, screen, ship, sb, new_upgrade)
				new_time.upgrade_type = 4
				u_i_laser.add(new_time)
				remove_upgrades_all(ai_settings, ship)
				ship.upgrades_allow_lasers = True
		
def check_upgrade_cooldown(ai_settings, ship, shiprailgun_sounds, u_i_rail, u_i_secondary, u_i_missile, u_i_laser):
	"""Handles the Timing of the upgrades, resets firing mode to the
	default (depends on which firing mode set in settings.py) when
	the time is up."""
	# Depending on the Ship's Default Weapon Mode (Specified in settings).
	#
	# If before time is up, missiles is being fired,
	# stop firing the missiles, and start firing the bullets.
	if ship.upgrades_special and (ai_settings.time_game_play >= ai_settings.upgrades_time_railgun_end or ai_settings.time_game_play >= ai_settings.upgrades_time_secondary_end or ai_settings.time_game_play >= ai_settings.upgrades_time_missile_end or ai_settings.time_game_play >= ai_settings.upgrades_time_laser_end):
		# Removes number of current upgrades (Required to show Upgrade_Timer correctly).
		if ai_settings.ship_weapon_default == 1:
			if ai_settings.time_game_play >= ai_settings.upgrades_time_railgun_end and ship.upgrades_allow_railguns:
				print("Rails Removed.")
				ai_settings.upgrades_no_of_current_upgrades -= 1
				u_i_rail.empty()
				ship.upgrades_allow_railguns = False
				gfsounds.shiprailgun_sound_end_internals(ai_settings, ship, shiprailgun_sounds)
				ai_settings.shipbullet_time_fire_interval = 0.3
			if ai_settings.time_game_play >= ai_settings.upgrades_time_secondary_end and (ship.upgrades_allow_bullet_secondary_gun or ship.upgrades_allow_missile_secondary_gun):
				print("Secondary Removed.")
				ai_settings.upgrades_no_of_current_upgrades -= 1
				u_i_secondary.empty()
				if ship.upgrades_allow_bullets:
					ship.upgrades_allow_bullet_secondary_gun = False
				elif ship.upgrades_allow_missiles:
					ship.upgrades_allow_missile_secondary_gun = False
			if ai_settings.time_game_play >= ai_settings.upgrades_time_missile_end and ship.upgrades_allow_missiles:
				print("Missiles Removed.")
				ai_settings.upgrades_no_of_current_upgrades -= 1
				u_i_missile.empty()
				ship.upgrades_allow_missiles = False
				ship.upgrades_allow_bullets = True
				if ai_settings.shipmissiles_constant_firing:
					ai_settings.shipmissiles_constant_firing = False
					ai_settings.shipbullets_constant_firing = True
			if ai_settings.time_game_play >= ai_settings.upgrades_time_laser_end and ship.upgrades_allow_lasers:
				print("Lasers Removed.")
				ai_settings.upgrades_no_of_current_upgrades -= 1
				u_i_laser.empty()
				ship.upgrades_allow_lasers = False
				
		elif ai_settings.ship_weapon_default == 2:
			if ai_settings.time_game_play >= ai_settings.upgrades_time_railgun_end and ship.upgrades_allow_railguns:
				print("Rails Removed.")
				ai_settings.upgrades_no_of_current_upgrades -= 1
				u_i_rail.empty()
				ship.upgrades_allow_railguns = False
				gfsounds.shiprailgun_sound_end_internals(ai_settings, ship, shiprailgun_sounds)
				ai_settings.shipbullet_time_fire_interval = 0.3
				if ai_settings.shipbullets_constant_firing:
					ai_settings.shipbullets_constant_firing = False
					ai_settings.shipmissiles_constant_firing = True
			if ai_settings.time_game_play >= ai_settings.upgrades_time_secondary_end and (ship.upgrades_allow_bullet_secondary_gun or ship.upgrades_allow_missile_secondary_gun):
				print("Secondary Removed.")
				ai_settings.upgrades_no_of_current_upgrades -= 1
				u_i_secondary.empty()
				if ship.upgrades_allow_bullets:
					ship.upgrades_allow_bullet_secondary_gun = False
				elif ship.upgrades_allow_missiles:
					ship.upgrades_allow_missile_secondary_gun = False
			if ai_settings.time_game_play >= ai_settings.upgrades_time_missile_end and ship.upgrades_allow_missiles:
				print("Missiles Removed.")
				pass
			if ai_settings.time_game_play >= ai_settings.upgrades_time_laser_end and ship.upgrades_allow_lasers:
				print("Lasers Removed.")
				ai_settings.upgrades_no_of_current_upgrades -= 1
				u_i_laser.empty()
				ship.upgrades_allow_lasers = False
		
def remove_upgrades_all(ai_settings, ship):
	"""Removes all the upgrades of ships."""
	ai_settings.upgrades_time_railgun_end = ai_settings.time_game - 1
	ai_settings.upgrades_time_secondary_end = ai_settings.time_game - 1
	ai_settings.upgrades_time_missile_end = ai_settings.time_game - 1
	ai_settings.upgrades_time_laser_end = ai_settings.time_game - 1
	ship.upgrades_allow_railguns = False
	ship.upgrades_allow_bullets = False
	ai_settings.shipbullets_constant_firing = False
	ai_settings.shipbullet_time_fire_interval = 0.3
	ship.upgrades_allow_bullet_secondary_gun = False
	ship.upgrades_allow_missiles = False
	ai_settings.shipmissiles_constant_firing = False
	ship.upgrades_allow_missile_secondary_gun = False
	ship.upgrades_allow_lasers = False
	
	ai_settings.upgrades_no_of_current_upgrades = 0
	
	if ai_settings.ship_weapon_default == 1:
		ship.upgrades_allow_bullets = True
	elif ai_settings.ship_weapon_default == 2:
		ship.upgrades_allow_missiles = True























