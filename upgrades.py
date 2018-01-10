import pygame
from pygame.sprite import Sprite

class Upgrade(Sprite):
	"""Represents the Upgrade drop that will be shot down."""
	def __init__(self, ai_settings, screen, sb):
		"""Initializes the Upgrade settings."""
		super().__init__()
		self.ai_settings = ai_settings
		self.sb = sb
		self.screen = screen
		self.screen_rect = self.screen.get_rect()
		
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
		self.is_upgrade_timer = False
		
		# Ship Upgrade Modes (Based on Type of Upgrades)
		# 1 - Bullets
		# 2 - Secondary
		# 3 - Missiles
		# 4 - Lasers
		self.upgrade_type = 0
		self.type_set = 0
		
	def update(self):
		"""Updates the position of the Upgrade."""
		# Upgrades will be dropped and move to the left of the screen,
		# towards the ship.
		if self.is_upgrade_timer:
			self.setting_image()
			
			self.image = pygame.transform.scale(self.image, (int(self.rect.width*(0.5)), int(self.rect.height*(0.5))))
			# This image_rect's width is used by UpgradeTimer in timer.py.
			self.image_rect = self.image.get_rect()
			# self.rect was already previously initialized in __init__,
			# not required once more.
			self.rect.left = self.screen_rect.left + self.rect_shift
			self.rect.top = self.sb.top_bracket_height + self.rect_shift
		elif not self.is_upgrade_timer:
			self.setting_image()
			
			self.centerx -= self.ai_settings.upgrades_speed_factor
			# Float values are converted to integers and assigned back to the rect.
			
			self.rect.centerx = self.centerx
			self.rect.centery = self.centery
			
	def setting_image(self):
		"""Changes the image based on the upgrade_type specified."""
		if self.upgrade_type == 1 and not self.type_set:
			self.image = pygame.image.load("images/upgrades/railguns.bmp")
			self.type_set = 1
		elif self.upgrade_type == 2 and not self.type_set:
			self.image = pygame.image.load("images/upgrades/secondary.bmp")
			self.type_set = 1
		elif self.upgrade_type == 3 and not self.type_set:
			self.image = pygame.image.load("images/upgrades/missile.bmp")
			self.type_set = 1
		elif self.upgrade_type == 4 and not self.type_set:
			self.image = pygame.image.load("images/upgrades/laser.bmp")
			self.type_set = 1
		
		
