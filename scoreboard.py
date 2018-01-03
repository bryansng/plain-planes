import pygame.font
import json

from pygame.sprite import Group

from ship import Ship

class Scoreboard():
	"""A class to represent everything that is required to show the scoreboard."""
	def __init__(self, ai_settings, screen, stats):
		"""Initializes Scoreboard settings."""
		self.ai_settings = ai_settings
		self.stats = stats
		self.screen = screen
		self.screen_rect = self.screen.get_rect()
		
		# Set color and create a font.
		self.text_color = (255, 255, 255)
		self.font = pygame.font.SysFont(None, 48)
		
		# Initializes all the scoreboard required informations.
		self.prep_topbracket()
		self.prep_score()
		self.prep_high_score()
		self.prep_level()
		self.prep_ships()
			
	def prep_topbracket(self):
		"""Preps a rect/bracket at the top of the screen."""
		# Sets its width, height and color.
		self.top_bracket_width, self.top_bracket_height = self.screen_rect.width, 40
		self.topbracket_color = (192, 192, 192)
		
		# Creates the actual rect using the width, height and color.
		self.topbracket_rect = pygame.Rect(0, 0, self.top_bracket_width, self.top_bracket_height)
	
	def prep_score(self):
		"""Preps the score, its font, rect and rect position."""
		# Rounds the score to the nearest 1.
		score = int(round(self.stats.score, 0))
		# Inserts ',' into the score for each 1,000.
		score_str = '{:,}'.format(score)
		self.score_str_image = self.font.render(score_str, True, self.text_color)#, self.ai_settings.bg_color)
		
		self.score_str_rect = self.score_str_image.get_rect()
		self.score_str_rect.right = self.topbracket_rect.width - 5
		self.score_str_rect.top = 5
		
	def prep_high_score(self):
		"""Preps the high score, its font, rect and rect position."""
		# Rounds the score to the nearest 1.
		high_score = int(round(self.stats.high_score, 0))
		# Inserts ',' into the high score for each 1,000.
		high_score_str = '{:,}'.format(high_score)
		self.high_score_str_image = self.font.render(high_score_str, True, self.text_color)#, self.ai_settings.bg_color)
		
		self.high_score_str_rect = self.high_score_str_image.get_rect()
		self.high_score_str_rect.centerx = self.topbracket_rect.centerx
		self.high_score_str_rect.top = 5

	def dumps_stats_to_json(self):
		"""Dumps statistics to a json file."""
		filename = 'stats.json'
		with open(filename, 'w') as highscore:
			json.dump(self.stats.high_score, highscore)
	
	def loads_stats_from_json(self):
		"""Loads statistics from a json file."""
		try:
			filename = 'stats.json'
			with open(filename, 'r') as highscore:
				highscore_fromjson = json.load(highscore)
		# json.decoder.JSONDecodeError is for players that are starting their
		# first new game, they will not have a high score.
		# This is used to prevent json from loading a no value.
		except json.decoder.JSONDecodeError:
			print("Empty High Score, starting first new game.")
			pass
		else:
			self.stats.high_score = int(highscore_fromjson)
		
	def prep_level(self):
		"""Preps the level, its font, rect and rect position."""
		level_str = str(self.stats.level)
		self.level_str_image = self.font.render(level_str, True, self.text_color)#, self.ai_settings.bg_color)
		
		self.level_str_rect = self.level_str_image.get_rect()
		self.level_str_rect.right = self.screen_rect.right - 200
		self.level_str_rect.top = 5
		
	def prep_ships(self):
		"""Preps the ship group, individual resized ship image,
		rect and rect position."""
		self.ships = Group()
		
		# If less than 3, show the remaining ships in their images,
		# else, show the remaining ships in terms of numbers.
		if self.stats.ship_left <= 3:
			for ship_number in range(self.stats.ship_left):
				ship = Ship(self.ai_settings, self.screen, self)
				ship.image = pygame.transform.scale(ship.image, (92, 30))
				ship_rect = ship.image.get_rect()
				ship.rect.x = 5 + ship_rect.width * ship_number
				ship.rect.y = 5
				self.ships.add(ship)
		else:
			# Shows just one ship.
			ship = Ship(self.ai_settings, self.screen, self)
			ship.image = pygame.transform.scale(ship.image, (92, 30))
			ship_rect = ship.image.get_rect()
			ship.rect.x = 5
			ship.rect.y = 5
			self.ships.add(ship)
			
			# Shows the number of the ships left.
			# Create font, get str, renders font image using the str, font and color.
			self.ship_left_font = pygame.font.SysFont(None, 48)
			ship_left_str = "x" + str(self.stats.ship_left)
			self.ship_left_str_image = self.ship_left_font.render(ship_left_str, True, self.text_color)
			self.ship_left_str_rect = self.ship_left_str_image.get_rect()
			self.ship_left_str_rect.x = ship.rect.x + ship_rect.width + 5
			self.ship_left_str_rect.y = ship.rect.y
		
	def show_score(self):
		"""Shows/Draws the topbracket, score, high score, level and ships left."""
		self.screen.fill(self.topbracket_color, self.topbracket_rect)
		self.screen.blit(self.score_str_image, self.score_str_rect)
		self.screen.blit(self.high_score_str_image, self.high_score_str_rect)
		self.screen.blit(self.level_str_image, self.level_str_rect)
		
		# If less than 3, show the remaining ships in their images,
		# else, show the remaining ships in terms of numbers.
		if self.stats.ship_left <= 3:
			self.ships.draw(self.screen)
		else:
			self.ships.draw(self.screen)
			self.screen.blit(self.ship_left_str_image, self.ship_left_str_rect)
			
		
		
