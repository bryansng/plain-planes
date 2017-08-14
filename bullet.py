import pygame
from pygame.sprite import Sprite

class ShipBullet(Sprite):
	
	def __init__(self, ai_settings, screen, ship):
		super().__init__()
		self.ai_settings = ai_settings
		self.screen = screen
		
		self.image = pygame.image.load('images/projectiles/ships/bullet.bmp')
		self.rect = self.image.get_rect()
		
		self.rect.centery = ship.rect.centery + 16
		self.rect.right = ship.rect.right - 50
		
		self.x = float(self.rect.x)
		
	def update(self):
		self.x += self.ai_settings.ship_bullet_speed_factor
		
		self.rect.x = self.x
		
	def draw_bullet(self):
		self.screen.blit(self.image, self.rect)

class HelicopterBullet(Sprite):
	
	def __init__(self, ai_settings, screen, heli):
		super().__init__()
		self.ai_settings = ai_settings
		self.screen = screen
		
		self.image = pygame.image.load('images/projectiles/hostiles/helicopterbullet.bmp')
		self.rect = self.image.get_rect()
		
		#for heli in helis.sprites():
		self.rect.centery = heli.rect.centery + 13
		self.rect.left = heli.rect.left# + 20
		
		#self.fire_bullet_at_x = float(self.rect.x)
		#self.x = float(self.fire_bullet_at_x)
		self.x = float(self.rect.x)
		
	def update(self):
		self.x -= self.ai_settings.helicopter_bullet_speed_factor
		
		self.rect.x = self.x
		
	def draw_bullet(self):
		self.screen.blit(self.image, self.rect)
