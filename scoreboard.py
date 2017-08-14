import pygame.font
import json

from pygame.sprite import Group

from ship import Ship

class Scoreboard():
	
	def __init__(self, ai_settings, screen, stats):
		self.ai_settings = ai_settings
		self.stats = stats
		self.screen = screen
		self.screen_rect = self.screen.get_rect()
		
		self.text_color = (255, 255, 255)
		self.font = pygame.font.SysFont(None, 48)
		
		self.draw_topbracket()
		self.prep_score()
		self.prep_high_score()
		self.prep_level()
		self.prep_ships()
			
	def draw_topbracket(self):
		self.top_bracket_width, self.top_bracket_height = self.screen_rect.width, 40
		self.topbracket_color = (192, 192, 192)
		
		self.topbracket_rect = pygame.Rect(0, 0, self.top_bracket_width, self.top_bracket_height)
	
	def prep_score(self):
		score = int(round(self.stats.score, -1))
		score_str = '{:,}'.format(score)
		self.score_str_image = self.font.render(score_str, True, self.text_color)#, self.ai_settings.bg_color)
		
		self.score_str_rect = self.score_str_image.get_rect()
		self.score_str_rect.right = self.topbracket_rect.width - 5
		self.score_str_rect.top = 5
		
	def prep_high_score(self):
		high_score = int(round(self.stats.high_score, -1))
		high_score_str = '{:,}'.format(high_score)
		self.high_score_str_image = self.font.render(high_score_str, True, self.text_color)#, self.ai_settings.bg_color)
		
		self.high_score_str_rect = self.high_score_str_image.get_rect()
		self.high_score_str_rect.centerx = self.topbracket_rect.centerx
		self.high_score_str_rect.top = 5

	def dumps_highscore_to_json(self):
		filename = 'high_score.json'
		with open(filename, 'w') as highscore:
			json.dump(self.stats.high_score, highscore)
	
	def loads_highscore_from_json(self):
		try:
			filename = 'high_score.json'
			with open(filename, 'r') as highscore:
				highscore_fromjson = json.load(highscore)
		except json.decoder.JSONDecodeError:
			pass
		else:
			self.stats.high_score = int(highscore_fromjson)
		
	def prep_level(self):
		level_str = str(self.stats.level)
		self.level_str_image = self.font.render(level_str, True, self.text_color)#, self.ai_settings.bg_color)
		
		self.level_str_rect = self.level_str_image.get_rect()
		self.level_str_rect.right = self.screen_rect.right - 200
		self.level_str_rect.top = 5
		
	def prep_ships(self):
		self.ships = Group()
		for ship_number in range(self.stats.ship_left):
			ship = Ship(self.ai_settings, self.screen, self)
			ship.image = pygame.transform.scale(ship.image, (92, 30))
			ship_rect = ship.image.get_rect()
			ship.rect.x = 5 + ship_rect.width * ship_number
			ship.rect.y = 5
			self.ships.add(ship)
		
	def show_score(self):
		self.screen.fill(self.topbracket_color, self.topbracket_rect)
		self.screen.blit(self.score_str_image, self.score_str_rect)
		self.screen.blit(self.high_score_str_image, self.high_score_str_rect)
		self.screen.blit(self.level_str_image, self.level_str_rect)
		self.ships.draw(self.screen)
		
		
