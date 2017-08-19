import pygame
from pygame.sprite import Sprite

class Helicopter(Sprite):
	"""A class to represent one of the hostile objects, Helicopter."""
	def __init__(self, ai_settings, screen):
		"""Initializes Helicopter settings."""
		super().__init__()
		self.ai_settings = ai_settings
		self.screen = screen
		
		# Loads the image, get image rect, get screen rect.
		self.image = pygame.image.load('images/objects/hostiles/cropped_helicopter.bmp')
		self.rect = self.image.get_rect()
		self.screen_rect = self.screen.get_rect()
		
		# Positions the helicopter to the top right corner of the screen.
		self.rect.x = self.screen_rect.width - self.rect.width
		self.rect.y = self.screen_rect.height - self.rect.height
		
		# Float values to a new variable if not decimals will not be registered.
		self.centerx = float(self.rect.centerx)
		self.centery = float(self.rect.centery)
		
	def update(self):
		"""Updates the position of helicopter."""
		# Helicopters will move from the right side, so just minus x like so.
		self.centerx -= self.ai_settings.helicopter_speed_factor
		
		# Float values are converted to integers and assigned back to the rect.
		self.rect.centerx = self.centerx
		self.rect.centery = self.centery
		
	def blitme(self):
		"""Draws the Helicopter onto the screen."""
		# Only for individual bullets, sprites are prefered to use 
		# self.draw(self.screen) or helis.draw(screen)
		self.screen.blit(self.image, self.rect)

