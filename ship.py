import pygame
from pygame.sprite import Sprite

import time
from time import process_time

class Ship(Sprite):
	"""A class to represent the player controlled ship."""
	def __init__(self, ai_settings, screen, sb):
		"""Initializes ship settings."""
		super().__init__()
		self.ai_settings = ai_settings
		self.screen = screen
		self.sb = sb
		
		# Loads image, get image rect, get screen rect.
		self.image = pygame.image.load('images/objects/ships/ship.bmp')
		self.rect = self.image.get_rect()
		self.screen_rect = self.screen.get_rect()
		
		# Position the ship/image to specified spot.
		self.rect.centery = self.screen_rect.centery
		self.rect.left = self.screen_rect.left
		
		# Float values to a new variable if not decimals will not be registered.
		self.centery = float(self.rect.centery)
		self.centerx = float(self.rect.centerx)
		
		# Flag for movements.
		self.moving_up = False
		self.moving_left = False
		self.moving_down = False
		self.moving_right = False
		
		# For immunity counter.
		self.immunity = False
		
	def center_ship(self):
		"""Centers the ship to the left center of the screen."""
		self.centery = self.screen_rect.centery
		# (self.rect.width / 2) is added, if not the half the ship is out of place.
		self.centerx = (self.screen_rect.left + (self.rect.width / 2))
		
	def update(self):
		"""Updates the ship's movements."""
		# Up
		if self.moving_up and self.rect.top > self.sb.topbracket_rect.bottom:
			self.centery -= self.ai_settings.ship_speed_factor
		# Left
		if self.moving_left and self.rect.left > 0:
			self.centerx -= self.ai_settings.ship_speed_factor
		# Bottom
		if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
			self.centery += self.ai_settings.ship_speed_factor
		# Right
		if self.moving_right and self.rect.right < self.screen_rect.right:
			self.centerx += self.ai_settings.ship_speed_factor
		
		# Float values are converted to integers and assigned back to the rect.
		self.rect.centery = self.centery
		self.rect.centerx = self.centerx
		
	def blitme(self):
		"""Draws the ship onto the screen."""
		# Only for individual ship, sprites are prefered to use 
		# self.draw(self.screen) or ships.draw(screen)
		self.screen.blit(self.image, self.rect)
