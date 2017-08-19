import sys
import pygame
import time

from time import process_time

from random import randint

from bullet import ShipBullet
from bullet import HelicopterBullet
from hostile import Helicopter
from hostile import Rocket

from gf_hostiles import *

""" This file is sorted in this pattern:
    1) Objects and ObjectProjectiles Internals
    2) Wave Creation
    3) 
"""

""" 1) Object Internals """

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
	
	
def update_shipbullet_internals(ai_settings, screen, ship, shipbullets, helis, stats):
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
	check_hostile_shipprojectile_collision(ai_settings, shipbullets, helis, stats)
	
	
def check_hostile_shipprojectile_collision(ai_settings, shipbullets, helis, stats):
	"""Removes the shipbullets and the helis that collide with each other.
	Adds the score for destroying the hostile object."""
	# Removes the shipbullet and heli that collides.
	helicopter_shipbullet_collisions = pygame.sprite.groupcollide(shipbullets, helis, True, True)
	# If there is a collision, loop through the collided objects/helis and add
	# based on each individual collision.
	# NOTE: This is optimized to be very exact.
	if helicopter_shipbullet_collisions:
		for helis in helicopter_shipbullet_collisions.values():
			stats.score += ai_settings.helicopter_points
