import pygame

class Background():
	"""A class used to represent the background of the game."""
	def __init__(self, ai_settings, screen):
		"""Initializes Background settings."""
		self.ai_settings = ai_settings
		self.screen = screen
		
		# Initializes the background, background objects and items.
		#self.background_img()
		self.sky()
		self.grass()
		
	def background_img(self):
		"""."""
		self.bg_img = pygame.image.load('images/display/bohol.png')
		self.bg_img_width, self.bg_img_height = self.ai_settings.screen_width, self.ai_settings.screen_height
		
		self.bg_img = pygame.transform.scale(self.bg_img, (self.bg_img_width, self.bg_img_height))
		
		self.bg_img_rect = self.bg_img.get_rect()
		self.bg_img_rect.x = 0
		self.bg_img_rect.y = 0
		
	def sky(self):
		self.sky_width = 800
		self.sky_height = 500
		self.sky_color = (135, 206, 250)
		
		self.sky_rect = pygame.Rect(0, 0, self.sky_width, self.sky_height)
		
	def grass(self):
		self.grass_width = 800
		self.grass_height = 100
		self.grass_color = (34, 139, 34)
		
		self.grass_rect = pygame.Rect(0, self.sky_height, self.grass_width, self.grass_height)
		
	def draw_background(self):
		#self.screen.blit(self.bg_img, self.bg_img_rect)
		self.screen.fill(self.sky_color, self.sky_rect)
		self.screen.fill(self.grass_color, self.grass_rect)
