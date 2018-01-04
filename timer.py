import pygame.font

from pygame.sprite import Group

from upgrades import UpgradeRailguns, UpgradeSecondaryGun, UpgradeMissiles, UpgradeLaser

class Timer():
	"""A class to represent everything that is required to show as Time."""
	def __init__(self, ai_settings, screen, ship, parachutes, sb):
		self.ai_settings = ai_settings
		self.ship = ship
		self.parachutes = parachutes
		self.sb = sb
		self.screen = screen
		self.screen_rect = self.screen.get_rect()
		
		# Set color and create a font.
		self.text_color = (255, 255, 255)
		self.timer_font = pygame.font.SysFont(None, 48)
		self.time_upgrade_font = pygame.font.SysFont(None, 36)
		
		# Initializes all the scoreboard required informations.
		self.prep_timer()
		self.prep_timer_upgrades()
		
	def prep_timer(self):
		"""Preps the timer, its font, rect, and rect position."""
		timer_str = str(0)
		self.timer_str_image = self.timer_font.render(timer_str, True, self.text_color)
		
		self.timer_str_rect = self.timer_str_image.get_rect()
		self.timer_str_rect.centerx = self.screen_rect.centerx
		self.timer_str_rect.top = self.ai_settings.screen_height - 50
		
	def prep_timer_upgrades(self):
		"""Preps the timer upgrades, its font, rect, and rect position."""
		timer_upgrades_str = str(self.ai_settings.upgrades_time_end - 0)
		self.timer_upgrades_str_image = self.time_upgrade_font.render(timer_upgrades_str, True, self.text_color)
		
		self.timer_upgrades_str_rect = self.timer_upgrades_str_image.get_rect()
		self.timer_upgrades_str_rect.left = 0
		self.timer_upgrades_str_rect.top = 0
		
		
	def update_timer(self, time_new):
		"""Updates the time of timer."""
		timer_str = str('{:.0f}'.format(time_new))
		self.timer_str_image = self.timer_font.render(timer_str, True, self.text_color)
		
		self.timer_str_rect = self.timer_str_image.get_rect()
		self.timer_str_rect.centerx = self.screen_rect.centerx
		self.timer_str_rect.top = self.ai_settings.screen_height - 50
		
	def update_timer_upgrades(self, time_new):
		"""Updates the time of upgrades_timer."""
		upgrade_rect_shift = 10
		self.upgrades = Group()
		
		if self.ship.upgrades_special:
			if self.ship.upgrades_allow_railguns:
				upgrade = UpgradeRailguns(self.ai_settings, self.screen, self.parachutes)
				upgrade.image = pygame.transform.scale(upgrade.image, (int(upgrade.rect.width*(0.5)), int(upgrade.rect.height*(0.5))))
				upgrade.rect = upgrade.image.get_rect()
				upgrade.rect.left = self.screen_rect.left + upgrade_rect_shift
				upgrade.rect.top = self.sb.topbracket_rect.height + upgrade_rect_shift
				self.upgrades.add(upgrade)
				self.update_timer_upgrades_rect(time_new, upgrade)
			elif self.ship.upgrades_allow_bullet_secondary_gun or self.ship.upgrades_allow_missile_secondary_gun:
				upgrade = UpgradeSecondaryGun(self.ai_settings, self.screen, self.parachutes)
				upgrade.image = pygame.transform.scale(upgrade.image, (int(upgrade.rect.width*(0.5)), int(upgrade.rect.height*(0.5))))
				upgrade.rect = upgrade.image.get_rect()
				upgrade.rect.left = self.screen_rect.left + upgrade_rect_shift
				upgrade.rect.top = self.sb.topbracket_rect.height + upgrade_rect_shift
				self.upgrades.add(upgrade)
				self.update_timer_upgrades_rect(time_new, upgrade)
			elif self.ship.upgrades_allow_missiles:
				upgrade = UpgradeMissiles(self.ai_settings, self.screen, self.parachutes)
				upgrade.image = pygame.transform.scale(upgrade.image, (int(upgrade.rect.width*(0.5)), int(upgrade.rect.height*(0.5))))
				upgrade.rect = upgrade.image.get_rect()
				upgrade.rect.left = self.screen_rect.left + upgrade_rect_shift
				upgrade.rect.top = self.sb.topbracket_rect.height + upgrade_rect_shift
				self.upgrades.add(upgrade)
				self.update_timer_upgrades_rect(time_new, upgrade)
			elif self.ship.upgrades_allow_lasers:
				upgrade = UpgradeLaser(self.ai_settings, self.screen, self.parachutes)
				upgrade.image = pygame.transform.scale(upgrade.image, (int(upgrade.rect.width*(0.5)), int(upgrade.rect.height*(0.5))))
				upgrade.rect = upgrade.image.get_rect()
				upgrade.rect.left = self.screen_rect.left + upgrade_rect_shift
				upgrade.rect.top = self.sb.topbracket_rect.height + upgrade_rect_shift
				self.upgrades.add(upgrade)
				self.update_timer_upgrades_rect(time_new, upgrade)
				
	def update_timer_upgrades_rect(self, time_new, upgrade):
		timer_upgrades_str = str('{:.0f}'.format(self.ai_settings.upgrades_time_end - time_new))
		self.timer_upgrades_str_image = self.time_upgrade_font.render(timer_upgrades_str, True, self.text_color)
		
		self.timer_upgrades_str_rect = self.timer_upgrades_str_image.get_rect()
		self.timer_upgrades_str_rect.left = self.screen_rect.left + upgrade.rect.right + 6
		self.timer_upgrades_str_rect.top = upgrade.rect.top
		
		
		
	def show_timer(self):
		"""Shows/Draws the timer and timer upgrades."""
		self.screen.blit(self.timer_str_image, self.timer_str_rect)
		
		if self.ship.upgrades_special:
			self.screen.blit(self.timer_upgrades_str_image, self.timer_upgrades_str_rect)
			self.upgrades.draw(self.screen)
	
	
	
	
	
	
	
	
