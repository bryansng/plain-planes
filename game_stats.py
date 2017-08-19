class GameStats():
	"""A class to represent the statistics of a game."""
	def __init__(self, ai_settings):
		"""Initializes game stats settings."""
		self.ai_settings = ai_settings
		self.reset_stats()
		
		self.game_active = False
		
		self.high_score = 0
		
	def reset_stats(self):
		"""Resets statistics."""
		self.ship_left = self.ai_settings.ship_limit
		self.score = 0
		self.level = 1
	
		


