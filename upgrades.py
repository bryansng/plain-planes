import pygame
from pygame.sprite import Sprite

class Upgrade(Sprite):
	"""Represents the Upgrade drop that will be shot down."""
	def __init__(self, ai_settings, screen):
		"""Initializes the Upgrade settings."""
		super().__init__()
		self.ai_settings = ai_settings
		self.screen = screen
		
		# Loads image and get image rect (Default image is railguns).
		self.image = pygame.image.load("images/upgrades/railguns.bmp")
		#self.image = pygame.image.load("images/upgrades/secondary.bmp")
		#self.image = pygame.image.load("images/upgrades/missile.bmp")
		#self.image = pygame.image.load("images/upgrades/laser.bmp")
		self.rect = self.image.get_rect()
		
		# Positions the upgrade image anywhere first.
		self.rect.x = 0
		self.rect.y = 0
		
		# Float values to a new variable if not decimals will not be registered.
		self.centerx = float(self.rect.centerx)
		self.centery = float(self.rect.centery)
		
		# Changing rect_shift changes the position of the
		# upgrades offset.
		self.rect_shift = 10
		self.upgrade_timer = False
		
	def update(self):
		"""Updates the position of the Upgrade."""
		# Upgrades will be dropped and move to the left of the screen,
		# towards the ship.
		if not self.upgrade_timer:
			self.centerx -= self.ai_settings.upgrades_speed_factor
		
		# Float values are converted to integers and assigned back to the rect.
		self.rect.centerx = self.centerx
		self.rect.centery = self.centery
		
	def blitme(self):
		"""Draws the Upgrade onto the screen."""
		# Only for individual upgrades, sprites are preferred to use
		# self.draw(self.screen) or u_upgrades.draw(screen)
		self.screen.blit(self.image, self.rect)

class UpgradeRailguns(Sprite):
	"""Represents the UpgradeRailguns drop that can be shot down."""
	def __init__(self, ai_settings, screen):
		"""Initializes the UpgradeRailguns settings."""
		super().__init__()
		self.ai_settings = ai_settings
		self.screen = screen
		
		# Load image and get image rect.
		self.image = pygame.image.load("images/upgrades/railguns.bmp")
		self.rect = self.image.get_rect()
		
		# Position the upgrade image anywhere first.
		self.rect.x = 0
		self.rect.y = 0
		
		# Float values to a new variable if not decimals will not be registered.
		self.centerx = float(self.rect.centerx)
		self.centery = float(self.rect.centery)
		
		# Changing rect_shift changes the position of the
		# upgrades offset.
		self.rect_shift = 10
		self.upgrade_timer = False
		
	def update(self):
		"""Updates the position of the Upgrade."""
		# UpgradeRailguns will be dropped and move to the left of the screen,
		# towards the ship.
		if not self.upgrade_timer:
			self.centerx -= self.ai_settings.upgrades_speed_factor
		
		# Float values are converted to integers and assigned back to the rect.
		self.rect.centerx = self.centerx
		self.rect.centery = self.centery
		
	def blitme(self):
		"""Draws the Upgrade onto the screen."""
		# Only for individual upgrades, sprites are preferred to use
		# self.draw(self.screen) or u_rails.draw(screen)
		self.screen.blit(self.image, self.rect)
	
class UpgradeSecondaryGun(Sprite):
	"""Represents the UpgradeSecondaryGun drop that can be shot down."""
	def __init__(self, ai_settings, screen):
		"""Initializes the UpgradeSecondaryGun settings."""
		super().__init__()
		self.ai_settings = ai_settings
		self.screen = screen
		
		# Load image and get image rect.
		self.image = pygame.image.load("images/upgrades/secondary.bmp")
		self.rect = self.image.get_rect()
		
		# Position the upgrade image anywhere first.
		self.rect.x = 0
		self.rect.y = 0
		
		# Float values to a new variable if not decimals will not be registered.
		self.centerx = float(self.rect.centerx)
		self.centery = float(self.rect.centery)
		
	def update(self):
		"""Updates the position of the Upgrade."""
		# UpgradeSecondaryGun will be dropped and move to the left of the screen,
		# towards the ship.
		self.centerx -= self.ai_settings.upgrades_speed_factor
		
		# Float values are converted to integers and assigned back to the rect.
		self.rect.centerx = self.centerx
		self.rect.centery = self.centery
		
	def blitme(self):
		"""Draws the Upgrade onto the screen."""
		# Only for individual upgrades, sprites are preferred to use
		# self.draw(self.screen) or u_secondary.draw(screen)
		self.screen.blit(self.image, self.rect)
	
class UpgradeMissiles(Sprite):
	"""Represents the UpgradeMissiles drop that can be shot down."""
	def __init__(self, ai_settings, screen):
		"""Initializes the UpgradeMissiles settings."""
		super().__init__()
		self.ai_settings = ai_settings
		self.screen = screen
		
		# Load image and get image rect.
		self.image = pygame.image.load("images/upgrades/missile.bmp")
		self.rect = self.image.get_rect()
		
		# Position the upgrade image anywhere first.
		self.rect.x = 0
		self.rect.y = 0
		
		# Float values to a new variable if not decimals will not be registered.
		self.centerx = float(self.rect.centerx)
		self.centery = float(self.rect.centery)
		
	def update(self):
		"""Updates the position of the Upgrade."""
		# UpgradeMissiles will be dropped and move to the left of the screen,
		# towards the ship.
		self.centerx -= self.ai_settings.upgrades_speed_factor
		
		# Float values are converted to integers and assigned back to the rect.
		self.rect.centerx = self.centerx
		self.rect.centery = self.centery
		
	def blitme(self):
		"""Draws the Upgrade onto the screen."""
		# Only for individual upgrades, sprites are preferred to use
		# self.draw(self.screen) or u_missile.draw(screen)
		self.screen.blit(self.image, self.rect)
	
class UpgradeLaser(Sprite):
	"""Represents the UpgradeLaser drop that can be shot down."""
	def __init__(self, ai_settings, screen):
		"""Initializes the UpgradeLaser settings."""
		super().__init__()
		self.ai_settings = ai_settings
		self.screen = screen
		
		# Load image and get image rect.
		self.image = pygame.image.load("images/upgrades/laser.bmp")
		self.rect = self.image.get_rect()
		
		# Position the upgrade image anywhere first.
		self.rect.x = 0
		self.rect.y = 0
		
		# Float values to a new variable if not decimals will not be registered.
		self.centerx = float(self.rect.centerx)
		self.centery = float(self.rect.centery)
		
	def update(self):
		"""Updates the position of the Upgrade."""
		# UpgradeLaser will be dropped and move to the left of the screen,
		# towards the ship.
		self.centerx -= self.ai_settings.upgrades_speed_factor
		
		# Float values are converted to integers and assigned back to the rect.
		self.rect.centerx = self.centerx
		self.rect.centery = self.centery
		
	def blitme(self):
		"""Draws the Upgrade onto the screen."""
		# Only for individual upgrades, sprites are preferred to use
		# self.draw(self.screen) or u_laser.draw(screen)
		self.screen.blit(self.image, self.rect)
		
