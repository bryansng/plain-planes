import pygame
from pygame.sprite import Sprite

class UpgradeRailguns(Sprite):
	def __init__(self, ai_settings, screen, parachutes):
		super().__init__()
		self.ai_settings = ai_settings
		self.screen = screen
		
		self.image = pygame.image.load("images/upgrades/railguns.bmp")
		self.rect = self.image.get_rect()
		
		self.rect.x = 0
		self.rect.y = 0
		
		self.centerx = float(self.rect.centerx)
		self.centery = float(self.rect.centery)
		
	def update(self):
		self.centerx -= self.ai_settings.upgrades_speed_factor
		
		self.rect.centerx = self.centerx
		self.rect.centery = self.centery
		
	def blitme(self):
		self.screen.blit(self.image, self.rect)
	
class UpgradeSecondaryGun(Sprite):
	def __init__(self, ai_settings, screen, parachutes):
		super().__init__()
		self.ai_settings = ai_settings
		self.screen = screen
		
		self.image = pygame.image.load("images/upgrades/secondary.bmp")
		self.rect = self.image.get_rect()
		
		self.rect.x = 0
		self.rect.y = 0
		
		self.centerx = float(self.rect.centerx)
		self.centery = float(self.rect.centery)
		
	def update(self):
		self.centerx -= self.ai_settings.upgrades_speed_factor
		
		self.rect.centerx = self.centerx
		self.rect.centery = self.centery
		
	def blitme(self):
		self.screen.blit(self.image, self.rect)
	
class UpgradeMissiles(Sprite):
	def __init__(self, ai_settings, screen, parachutes):
		super().__init__()
		self.ai_settings = ai_settings
		self.screen = screen
		
		self.image = pygame.image.load("images/upgrades/missile.bmp")
		self.rect = self.image.get_rect()
		
		self.rect.x = 0
		self.rect.y = 0
		
		self.centerx = float(self.rect.centerx)
		self.centery = float(self.rect.centery)
		
	def update(self):
		self.centerx -= self.ai_settings.upgrades_speed_factor
		
		self.rect.centerx = self.centerx
		self.rect.centery = self.centery
		
	def blitme(self):
		self.screen.blit(self.image, self.rect)
	
class UpgradeLaser(Sprite):
	def __init__(self, ai_settings, screen, parachutes):
		super().__init__()
		self.ai_settings = ai_settings
		self.screen = screen
		
		self.image = pygame.image.load("images/upgrades/laser.bmp")
		self.rect = self.image.get_rect()
		
		self.rect.x = 0
		self.rect.y = 0
		
		self.centerx = float(self.rect.centerx)
		self.centery = float(self.rect.centery)
		
	def update(self):
		self.centerx -= self.ai_settings.upgrades_speed_factor
		
		self.rect.centerx = self.centerx
		self.rect.centery = self.centery
		
	def blitme(self):
		self.screen.blit(self.image, self.rect)
		
