import time
import pygame.font

from pygame.sprite import Sprite
from pygame.sprite import Group

from upgrades import Upgrade

class GameClock():
	"""A class to represent everything that is required to show as Time."""
	def __init__(self, ai_settings, screen):
		"""Initializes Clock settings."""
		self.ai_settings = ai_settings
		self.screen = screen
		self.screen_rect = self.screen.get_rect()
		
		# Set color and creates a font for clock.
		self.text_color = (255, 255, 255)
		self.font = pygame.font.SysFont(None, 36)
		
		# Initializes all the scoreboard required informations.
		# Basically just prepares the rects and images of the clock.
		self.prep_clock()
		
	def prep_clock(self):
		"""Preps the clock time, its font, rect, and rect position."""
		# Sets the time to 0 first,
		# it is updated in game in update_internals via update_clock().
		clock = str(0)
		self.clock_image = self.font.render(clock, True, self.text_color)
		
		self.clock_rect = self.clock_image.get_rect()
		self.clock_rect.centerx = self.screen_rect.centerx
		self.clock_rect.top = self.ai_settings.screen_height - 50
		
	def update_clock(self):
		"""Updates the time of clock."""
		clock = int(self.ai_settings.time_game_play)
		clock = time.strftime("%H:%M:%S", time.gmtime(clock))
		self.clock_image = self.font.render(clock, True, self.text_color)
		
		self.clock_rect = self.clock_image.get_rect()
		self.clock_rect.centerx = self.screen_rect.centerx
		self.clock_rect.top = self.ai_settings.screen_height - 50
		
	def show_game_clock(self):
		"""Shows/Draws the clock."""
		self.screen.blit(self.clock_image, self.clock_rect)
		
		
		
		
		
		
class UpgradeTimer(Sprite):
	"""Represents all the separate timing groups."""
	def __init__(self, ai_settings, screen, ship, sb, upgrade):
		"""Initialize all UpgradeTimer settings."""
		super().__init__()
		self.ai_settings = ai_settings
		self.ship = ship
		self.sb = sb
		self.upgrade = upgrade
		self.screen = screen
		self.screen_rect = self.screen.get_rect()
		
		# Set color and creates a font for timer and font for timer_upgrades.
		self.text_color = (255, 255, 255)
		self.font = pygame.font.SysFont(None, 36)
		
		# Preps the timer upgrades, its font, rect, and rect position.#
		#
		# Sets the time to 0 first.
		# It will be updated in game in update_internals.
		self.time = str(0)
		self.image = self.font.render(self.time, True, self.text_color)
		
		# The rect position is set to be anywhere first,
		# it is updated in game in update_internals via update_timer_upgrades().
		self.rect = self.image.get_rect()
		self.rect.left = 0
		self.rect.top = 0
		
		# Changing rect_shift changes the position of the
		# upgrades offset.
		self.rect_shift = 5
		
		# Ship Upgrade Modes (Based on Type of Upgrades)
		# 1 - Bullets
		# 2 - Secondary
		# 3 - Missiles
		# 4 - Lasers
		self.upgrade_type = 0
		
	def update(self):
		"""Updates the time of upgrade timer."""
		if self.upgrade_type == 1:
			self.time = str('{:.0f}'.format(self.ai_settings.upgrades_time_railgun_end - self.ai_settings.time_game_play))
			self.image = self.font.render(self.time, True, self.text_color)
		elif self.upgrade_type == 2:
			self.time = str('{:.0f}'.format(self.ai_settings.upgrades_time_secondary_end - self.ai_settings.time_game_play))
			self.image = self.font.render(self.time, True, self.text_color)
		elif self.upgrade_type == 3:
			self.time = str('{:.0f}'.format(self.ai_settings.upgrades_time_missile_end - self.ai_settings.time_game_play))
			self.image = self.font.render(self.time, True, self.text_color)
		elif self.upgrade_type == 4:
			self.time = str('{:.0f}'.format(self.ai_settings.upgrades_time_laser_end - self.ai_settings.time_game_play))
			self.image = self.font.render(self.time, True, self.text_color)
		
		# Relative Distance between Upgrade Image and Upgrade Timer.
		self.rect.left = (self.upgrade.rect.right - (self.upgrade.rect.right - self.upgrade.image_rect.right) + self.upgrade.rect.left) + self.rect_shift
		self.rect.top = self.upgrade.rect.top
		
		
		
		
		
		
