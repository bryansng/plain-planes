import pygame.font

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
		self.font = pygame.font.SysFont(None, 48)
		
		# Initializes all the scoreboard required informations.
		self.prep_timer()
		self.prep_timer_upgrades()
		
	def prep_timer(self):
		"""Preps the timer, its font, rect, and rect position."""
		timer_str = str(0)
		self.timer_str_image = self.font.render(timer_str, True, self.text_color)
		
		self.timer_str_rect = self.timer_str_image.get_rect()
		self.timer_str_rect.centerx = self.screen_rect.centerx
		self.timer_str_rect.top = self.ai_settings.screen_height - 50
		
	def prep_timer_upgrades(self):
		"""Preps the timer upgrades, its font, rect, and rect position."""
		timer_upgrades_str = str(self.ai_settings.upgrades_time_end - 0)
		self.timer_upgrades_str_image = self.font.render(timer_upgrades_str, True, self.text_color)
		
		self.timer_upgrades_str_rect = self.timer_upgrades_str_image.get_rect()
		self.timer_upgrades_str_rect.left = 0
		self.timer_upgrades_str_rect.top = 0
		
		
	def update_timer(self, time_new):
		"""Updates the time of timer."""
		timer_str = str(time_new)
		self.timer_str_image = self.font.render(timer_str, True, self.text_color)
		
		self.timer_str_rect = self.timer_str_image.get_rect()
		self.timer_str_rect.centerx = self.screen_rect.centerx
		self.timer_str_rect.top = self.ai_settings.screen_height - 50
		
	def update_timer_upgrades(self, time_new):
		"""Updates the time of upgrades_timer."""
		if self.ship.upgrades_special:
			if self.ship.upgrades_allow_railguns:
				upgrade = UpgradeRailguns(self.ai_settings, self.screen, self.parachutes)
				upgrade.rect.left = self.screen_rect.left + 20
				upgrade.rect.top = self.sb.topbracket_rect.height + 20
			elif self.ship.upgrades_allow_bullet_secondary_gun or self.ship.upgrades_allow_missile_secondary_gun:
				upgrade = UpgradeSecondaryGun(self.ai_settings, self.screen, self.parachutes)
				upgrade.rect.left = self.screen_rect.left + 20
				upgrade.rect.top = self.sb.topbracket_rect.height + 20
			elif self.ship.upgrades_allow_missiles:
				upgrade = UpgradeMissiles(self.ai_settings, self.screen, self.parachutes)
				upgrade.rect.left = self.screen_rect.left + 20
				upgrade.rect.top = self.sb.topbracket_rect.height + 20
			elif self.ship.upgrades_allow_lasers:
				upgrade = UpgradeLaser(self.ai_settings, self.screen, self.parachutes)
				upgrade.rect.left = self.screen_rect.left + 20
				upgrade.rect.top = self.sb.topbracket_rect.height + 20
				
			timer_upgrades_str = str(self.ai_settings.upgrades_time_end - time_new)
			self.timer_upgrades_str_image = self.font.render(timer_upgrades_str, True, self.text_color)
			
			self.timer_upgrades_str_rect = self.timer_upgrades_str_image.get_rect()
			self.timer_upgrades_str_rect.left = self.screen_rect.left + upgrade.rect.left + 5
			self.timer_upgrades_str_rect.top = upgrade.rect.top
			
			upgrade.blitme()
		
		
	def show_timer(self):
		"""Shows/Draws the timer and timer upgrades."""
		self.screen.blit(self.timer_str_image, self.timer_str_rect)
		self.screen.blit(self.timer_upgrades_str_image, self.timer_upgrades_str_rect)
	
	
	
	
	
	
	
	
	
