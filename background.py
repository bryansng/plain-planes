import pygame

class Background():
	"""A class used to represent the background of the game."""
	def __init__(self, ai_settings, screen):
		self.ai_settings = ai_settings
		self.screen = screen
		
		self.sky()
		self.grass()
		
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
		self.screen.fill(self.sky_color, self.sky_rect)
		self.screen.fill(self.grass_color, self.grass_rect)
