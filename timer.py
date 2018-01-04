import pygame.font

from pygame.sprite import Group

from upgrades import UpgradeRailguns, UpgradeSecondaryGun, UpgradeMissiles, UpgradeLaser

class Timer():
	"""A class to represent everything that is required to show as Time."""
	def __init__(self, ai_settings, screen, ship, parachutes, sb):
		"""Initializes Timer settings."""
		self.ai_settings = ai_settings
		self.ship = ship
		self.parachutes = parachutes
		self.sb = sb
		self.screen = screen
		self.screen_rect = self.screen.get_rect()
		
		# Set color and creates a font for timer and font for timer_upgrades.
		self.text_color = (255, 255, 255)
		self.timer_font = pygame.font.SysFont(None, 48)
		self.time_upgrade_font = pygame.font.SysFont(None, 36)
		
		# Initializes all the scoreboard required informations.
		# Basically just prepares the rects and images of the timers.
		self.prep_timer()
		self.prep_timer_upgrades()
		
	def prep_timer(self):
		"""Preps the timer, its font, rect, and rect position."""
		# Sets the time to 0 first,
		# it is updated in game in update_internals via update_timer().
		timer_str = str(0)
		self.timer_str_image = self.timer_font.render(timer_str, True, self.text_color)
		
		self.timer_str_rect = self.timer_str_image.get_rect()
		self.timer_str_rect.centerx = self.screen_rect.centerx
		self.timer_str_rect.top = self.ai_settings.screen_height - 50
		
	def prep_timer_upgrades(self):
		"""Preps the timer upgrades, its font, rect, and rect position."""
		# Sets the time to 0 first.
		# It will be updated in game in update_internals.
		timer_upgrades_str = str(self.ai_settings.upgrades_time_end - 0)
		self.timer_upgrades_str_image = self.time_upgrade_font.render(timer_upgrades_str, True, self.text_color)
		
		# The rect position is set to be anywhere first,
		# it is updated in game in update_internals via update_timer_upgrades().
		self.timer_upgrades_str_rect = self.timer_upgrades_str_image.get_rect()
		self.timer_upgrades_str_rect.left = 0
		self.timer_upgrades_str_rect.top = 0
		
		
	def update_timer(self, time_game_play):
		"""Updates the time of timer."""
		timer_str = str('{:.0f}'.format(time_game_play))
		self.timer_str_image = self.timer_font.render(timer_str, True, self.text_color)
		
		self.timer_str_rect = self.timer_str_image.get_rect()
		self.timer_str_rect.centerx = self.screen_rect.centerx
		self.timer_str_rect.top = self.ai_settings.screen_height - 50
		
	def update_timer_upgrades(self, time_game_play):
		"""Updates the time of upgrades_timer."""
		# Changing upgrade_rect_shift changes the position of the
		# upgrades offset.
		upgrade_rect_shift = 10
		self.upgrades = Group()
		
		# If there is any special upgrades activated, then go into this chunk.
		#
		# It then specializes into the respective types of upgrades to print
		# its upgrade image, also updating/making them appear onto the screen
		# in the process.
		if self.ship.upgrades_special:
			if self.ship.upgrades_allow_railguns:
				upgrade = UpgradeRailguns(self.ai_settings, self.screen, self.parachutes)
				upgrade.image = pygame.transform.scale(upgrade.image, (int(upgrade.rect.width*(0.5)), int(upgrade.rect.height*(0.5))))
				upgrade.rect = upgrade.image.get_rect()
				upgrade.rect.left = self.screen_rect.left + upgrade_rect_shift
				upgrade.rect.top = self.sb.topbracket_rect.height + upgrade_rect_shift
				self.upgrades.add(upgrade)
				self.update_timer_upgrade_rect(time_game_play, upgrade)
			elif self.ship.upgrades_allow_bullet_secondary_gun or self.ship.upgrades_allow_missile_secondary_gun:
				upgrade = UpgradeSecondaryGun(self.ai_settings, self.screen, self.parachutes)
				upgrade.image = pygame.transform.scale(upgrade.image, (int(upgrade.rect.width*(0.5)), int(upgrade.rect.height*(0.5))))
				upgrade.rect = upgrade.image.get_rect()
				upgrade.rect.left = self.screen_rect.left + upgrade_rect_shift
				upgrade.rect.top = self.sb.topbracket_rect.height + upgrade_rect_shift
				self.upgrades.add(upgrade)
				self.update_timer_upgrade_rect(time_game_play, upgrade)
			elif self.ship.upgrades_allow_missiles:
				upgrade = UpgradeMissiles(self.ai_settings, self.screen, self.parachutes)
				upgrade.image = pygame.transform.scale(upgrade.image, (int(upgrade.rect.width*(0.5)), int(upgrade.rect.height*(0.5))))
				upgrade.rect = upgrade.image.get_rect()
				upgrade.rect.left = self.screen_rect.left + upgrade_rect_shift
				upgrade.rect.top = self.sb.topbracket_rect.height + upgrade_rect_shift
				self.upgrades.add(upgrade)
				self.update_timer_upgrade_rect(time_game_play, upgrade)
			elif self.ship.upgrades_allow_lasers:
				upgrade = UpgradeLaser(self.ai_settings, self.screen, self.parachutes)
				upgrade.image = pygame.transform.scale(upgrade.image, (int(upgrade.rect.width*(0.5)), int(upgrade.rect.height*(0.5))))
				upgrade.rect = upgrade.image.get_rect()
				upgrade.rect.left = self.screen_rect.left + upgrade_rect_shift
				upgrade.rect.top = self.sb.topbracket_rect.height + upgrade_rect_shift
				self.upgrades.add(upgrade)
				self.update_timer_upgrade_rect(time_game_play, upgrade)
				
	def update_timer_upgrade_rect(self, time_game_play, upgrade):
		"""Updates the timer and the rect position based on the upgrades in
		function update_timer_upgrades()."""
		timer_upgrades_str = str('{:.0f}'.format(self.ai_settings.upgrades_time_end - time_game_play))
		self.timer_upgrades_str_image = self.time_upgrade_font.render(timer_upgrades_str, True, self.text_color)
		
		self.timer_upgrades_str_rect = self.timer_upgrades_str_image.get_rect()
		self.timer_upgrades_str_rect.left = self.screen_rect.left + upgrade.rect.right + 6
		self.timer_upgrades_str_rect.top = upgrade.rect.top
		
		
		
	def show_timer(self):
		"""Shows/Draws the timer and timer upgrades."""
		self.screen.blit(self.timer_str_image, self.timer_str_rect)
		
		# If any upgrades are activated, then print the time duration
		# and draw the upgrade type.
		if self.ship.upgrades_special:
			self.screen.blit(self.timer_upgrades_str_image, self.timer_upgrades_str_rect)
			self.upgrades.draw(self.screen)
	
	
	
	
	
	
	
	
