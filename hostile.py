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
		
		# Positions the helicopter to the bottom right corner of the screen.
		# It can't be seen in the screen.
		self.rect.x = self.screen_rect.width
		self.rect.y = self.screen_rect.height
		
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
		
class Rocket(Sprite):
	"""A class to represent one of the hostile objects, Rocket."""
	def __init__(self, ai_settings, screen):
		"""Initialize Rocket settings."""
		super().__init__()
		self.ai_settings = ai_settings
		self.screen = screen
		
		# Loads the image, get image rect, get screen rect.
		self.image = pygame.image.load('images/objects/hostiles/rocket.bmp')
		self.rect = self.image.get_rect()
		self.screen_rect = self.screen.get_rect()
		
		# Positions the rocket to the bottom right corner of the screen.
		# It can't be seen in the screen.
		self.rect.x = self.screen_rect.width
		self.rect.y = self.screen_rect.height
		
		# Float values to a new variable if not decimals will not be registered.
		self.centerx = float(self.rect.centerx)
		self.centery = float(self.rect.centery)
		
	def update(self):
		"""Updates the position of rocket."""
		# Rockets will move from the bottom to the top, so just minus y like so.
		self.centery -= self.ai_settings.rocket_speed_factor
		
		# Float values are converted to integers and assigned back to the rect.
		self.rect.centerx = self.centerx
		self.rect.centery = self.centery
		
	def blitme(self):
		"""Draws the Rocket onto the screen."""
		# Only for individual bullets, sprites are prefered to use 
		# self.draw(self.screen) or rockets.draw(screen)
		self.screen.blit(self.image, self.rect)
		
class Advanced_Helicopter(Sprite):
	"""A class to represent one of the hostile objects, Advanced Helicopter."""
	def __init__(self, ai_settings, screen):
		"""Initialize Advanced Helicopter settings."""
		super().__init__()
		self.ai_settings = ai_settings
		self.screen = screen
		
		# Loads the image, get image rect, get screen rect.
		self.image = pygame.image.load('images/objects/hostiles/advanced_attack_helicopter.bmp')
		self.rect = self.image.get_rect()
		self.screen_rect = self.screen.get_rect()
		
		# Positions the helicopter to the bottom right corner of the screen.
		# It can't be seen in the screen.
		self.rect.x = self.screen_rect.width
		self.rect.y = self.screen_rect.height
		
		# Float values to a new variable if not decimals will not be registered.
		self.centerx = float(self.rect.centerx)
		self.centery = float(self.rect.centery)
		
	def update(self):
		"""Updates the position of advanced helicopter."""
		# Ad Heli will move from the right to the left, so just minus x like so.
		self.centerx -= self.ai_settings.ad_heli_speed_factor
		
		# Float values are converted to integers and assigned back to the rect.
		self.rect.centerx = self.centerx
		self.rect.centery = self.centery
		
	def blitme(self):
		"""Draws the Advanced Helicopter onto the screen."""
		# Only for individual bullets, sprites are prefered to use 
		# self.draw(self.screen) or adhelis.draw(screen)
		self.screen.blit(self.image, self.rect)

