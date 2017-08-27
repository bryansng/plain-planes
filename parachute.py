import pygame
from pygame.sprite import Sprite

class Parachute(Sprite):
	"""A class to represent the upgrades carrier of ship."""
	def __init__(self, ai_settings, screen):
		"""Initializes parachute settings."""
		super().__init__()
		self.ai_settings = ai_settings
		self.screen = screen
		
		# Loads image, get image rect, get screen rect.
		self.image = pygame.image.load('images/upgrades/parachute.bmp')
		self.rect = self.image.get_rect()
		self.screen_rect = self.screen.get_rect()
		
		# Position the parachute/image to specified spot.
		self.rect.x = 0
		self.rect.y = 0
		
		# Float values to a new variable if not decimals will not be registered.
		self.centerx = float(self.rect.centerx)
		self.centery = float(self.rect.centery)
		
	def update(self):
		"""Updates the parachute's movements."""
		# Down
		self.centery += self.ai_settings.parachute_speed_factor
		
		# Float values are converted to integers and assigned back to the rect.
		self.rect.centerx = self.centerx
		self.rect.centery = self.centery
		
	def blitme(self):
		"""Draws the ship onto the screen."""
		# Only for individual bullets, sprites are prefered to use 
		# self.draw(self.screen) or parachutes.draw(screen)
		self.screen.blit(self.image, self.rect)







