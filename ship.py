import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
	
	def __init__(self, ai_settings, screen):
		super().__init__()
		self.ai_settings = ai_settings
		self.screen = screen
		
		self.image = pygame.image.load('images/objects/ships/ship.bmp')
		self.rect = self.image.get_rect()
		self.screen_rect = self.screen.get_rect()
		
		self.rect.centery = self.screen_rect.centery
		self.rect.left = self.screen_rect.left
		
		self.centery = float(self.rect.centery)
		self.centerx = float(self.rect.centerx)
		
		self.moving_up = False
		self.moving_left = False
		self.moving_down = False
		self.moving_right = False
		
		self.immunity = False
		
	def center_ship(self):
		self.centery = self.screen_rect.centery
		self.centerx = (self.screen_rect.left + (self.rect.width / 2))
		
	def update(self):
		if self.moving_up and self.rect.top > 0:
			self.centery -= self.ai_settings.ship_speed_factor
		if self.moving_left and self.rect.left > 0:
			self.centerx -= self.ai_settings.ship_speed_factor
		if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
			self.centery += self.ai_settings.ship_speed_factor
		if self.moving_right and self.rect.right < self.screen_rect.right:
			self.centerx += self.ai_settings.ship_speed_factor
		
		self.rect.centery = self.centery
		self.rect.centerx = self.centerx
		
	def blitme(self):
		self.screen.blit(self.image, self.rect)
