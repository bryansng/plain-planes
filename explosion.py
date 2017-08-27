import pygame
from pygame.sprite import Sprite

class Explosion(Sprite):
	"""A class to represent explosions after destroying any objects."""
	def __init__(self, ai_settings, screen):
		"""Initializes explosion settings."""
		super().__init__()
		self.ai_settings = ai_settings
		self.screen = screen
		
		# Loads image, get image rect, get screen rect.
		self.image = pygame.image.load('images/explosion/hostile_explosion1.bmp')
		self.rect = self.image.get_rect()
		self.screen_rect = self.screen.get_rect()
		
		# Position the explosion/image to the top left corner of the screen.
		self.rect.x = 0
		self.rect.y = 0
		
		# Float values to a new variable if not decimals will not be registered.
		self.centerx = float(self.rect.centerx)
		self.centery = float(self.rect.centery)
		
	def update(self):
		"""Updates the position of the Explosion."""
		# Float values are converted to integers and assigned back to the rect.
		self.rect.centerx = self.centerx
		self.rect.centery = self.centery
		
	def blitme(self):
		"""Draws the Explosion onto the screen."""
		# Only for individual bullets, sprites are prefered to use 
		# self.draw(self.screen) or explosions.draw(screen)
		self.screen.blit(self.image, self.rect)
