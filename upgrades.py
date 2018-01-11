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
		
		# Loads image and gets the image rect (Default image is railguns).
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
		
		# Upgrades are used for spawning and appearing as upgrade_timer,
		# if it is an upgrade_timer, then the update() will update it
		# as a upgrade_timer, else, as a upgrade drop for the ship to
		# shot down.
		self.is_upgrade_timer = False
		
		# Image placement number is used to identify where should the upgrade
		# image's position be at. If it is 1, then it should be the first.
		# If it is 2, then it should be to the right of the first upgrade image.
		self.image_placement_no = 0
		
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
			self.initialise_image()
			
			self.image = pygame.transform.scale(self.image, (int(self.rect.width*(0.5)), int(self.rect.height*(0.5))))
			# This image_rect's width is used by UpgradeTimer in timer.py.
			self.image_rect = self.image.get_rect()
			
			self.rect.left = self.screen_rect.left + self.rect_shift
			self.rect.left += (self.rect.right + self.rect_shift) * (self.image_placement_no - 1)
			self.rect.top = self.sb.top_bracket_height + self.rect_shift
		elif not self.is_upgrade_timer:
			self.initialise_image()
			
			self.centerx -= self.ai_settings.upgrades_speed_factor
			# Float values are converted to integers and assigned back to the rect.
			
			self.rect.centerx = self.centerx
			self.rect.centery = self.centery
			
	def initialise_image(self):
		"""Changes the image based on the upgrade_type specified."""
		# self.type_set stops the game from updating self.image all the time.
		# With self.type_set, it will update just once.
		if not self.type_set and self.upgrade_type == 1:
			self.image = pygame.image.load("images/upgrades/railguns.bmp")
			self.type_set = 1
		elif not self.type_set and self.upgrade_type == 2:
			self.image = pygame.image.load("images/upgrades/secondary.bmp")
			self.type_set = 1
		elif not self.type_set and self.upgrade_type == 3:
			self.image = pygame.image.load("images/upgrades/missile.bmp")
			self.type_set = 1
		elif not self.type_set and self.upgrade_type == 4:
			self.image = pygame.image.load("images/upgrades/laser.bmp")
			self.type_set = 1
		
		
