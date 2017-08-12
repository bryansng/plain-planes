import pygame
from pygame.sprite import Sprite

class Helicopter(Sprite):
	
	def __init__(self, ai_settings, screen):
		super().__init__()
		self.ai_settings = ai_settings
		self.screen = screen
		
		self.image = pygame.image.load('images/objects/hostiles/cropped_helicopter.bmp')
		self.rect = self.image.get_rect()
		self.screen_rect = self.screen.get_rect()
		self.rect.x = self.screen_rect.width - self.rect.width
		self.rect.y = self.screen_rect.height - self.rect.height
		
		self.centerx = float(self.rect.centerx)
		self.centery = float(self.rect.centery)
		
	def update(self):
		self.centerx -= self.ai_settings.helicopter_speed_factor
		
		self.rect.centerx = self.centerx
		self.rect.centery = self.centery
		
	def blitme(self):
		self.screen.blit(self.image, self.rect)

