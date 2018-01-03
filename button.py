import pygame
import pygame.font

class Button():
	"""A class to represent a simple button."""
	def __init__(self, screen, msg):
		"""Initialize Button settings."""
		self.screen = screen
		
		# Sets the width, height, button color, text color and font.
		self.width, self.height = 300, 36
		self.button_color = (0, 255, 0)
		self.text_color = (255, 255, 255)
		self.font = pygame.font.SysFont(None, 40, bold=True)
		
		# Creates a rect for the button, gets screen rect and positions 
		# the button/rect at the center of the screen.
		self.rect = pygame.Rect(0, 0, self.width, self.height)
		self.screen_rect = self.screen.get_rect()
		self.rect.center = self.screen_rect.center
		
		# Merge sides to the rect.
		#self.prep_rect()
		
		# Initializes prep_msg from a method.
		self.prep_msg(msg)
		
	def prep_rect(self):
		"""Preps the sides for the rect."""
		self.sides_color = (192, 192, 192)
		
		# Positions the sides_rect to fit into the rect.
		self.sides_rect = pygame.Rect(0, 0, (self.width + 8), (self.height + 8))
		self.sides_rect.x = (self.rect.x - 4)
		self.sides_rect.y = (self.rect.y - 4)
		
	def prep_msg(self, msg):
		"""Renders the msg using the font created prior,
		get rect and center the rect based on button rect."""
		self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
		self.msg_image_rect = self.msg_image.get_rect()
		self.msg_image_rect.center = self.rect.center
		
	def draw_button(self):
		"""Draws the button and msg_image onto the screen."""
		#self.screen.fill(self.sides_color, self.sides_rect)
		self.screen.fill(self.button_color, self.rect)
		self.screen.blit(self.msg_image, self.msg_image_rect)
