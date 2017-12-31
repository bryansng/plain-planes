class Settings():
	"""A class to represent the settings of the game."""
	def __init__(self):
		"""Initialize all the static settings of the game."""
		# Screen settings.
		self.screen_width = 800
		self.screen_height = 600
		self.bg_color = (240, 240, 240)
		
		# Ship bullet settings.
		self.shipbullets_allowed = 100
		self.shipbullet_time_fire_interval = 0.3
		
		# Points increment settings.
		self.points_speedup_scale = 1.5
		
		# Dynamic settings.
		self.initialize_dynamic_settings()
		self.game_internal_settings()
		
	def initialize_dynamic_settings(self):
		"""Initializes all the dynamic settings of the game."""
		# Ship settings.
		self.ship_speed_factor = 0.6
		self.ship_speed_acceleration = 1.1
		self.ship_limit = 3
		self.ship_max_limit = 10
		# Ship Immune settings
		self.ship_time_immune = 3
		self.ship_time_hit = 0
		
		# Ship bullet settings.
		self.ship_bullet_speed_factor = 0.8
		self.shipbullet_time_fire = 0
		self.shipbullets_constant_firing = False
		self.shipbullet_sound_start_stop = 0
		
		# Parachute settings.
		self.parachute_speed_factor = 0.25
		self.parachute_points = 25
		
		# Explosion settings.
		self.explosion_time_disappear = 0.1
		self.explosion_time_create = 0
		
		# Mouse start game settings.
		self.mouse_starttime_nowork_interval = 1
		self.mouse_start_time_click = 0
		self.mouse_working = False
		
		# Helicopter and helicopter bullet settings.
		self.helicopter_speed_factor = 0.2
		self.helicopter_points = 50
		
		# Helicopter bullet settings.
		self.helicopter_bullet_speed_factor = 0.4
		self.helicopter_bullet_points = 2
		
		# Rocket settings
		self.rocket_speed_factor = 0.1
		self.rocket_speed_acceleration = 1.1
		self.rocket_points = 100
		
		# Advanced Helicopter settings
		self.ad_heli_speed_factor = 0.22
		self.ad_heli_points = 150
		
	def game_internal_settings(self):
		self.wave_hostile_spawn = True
		self.wave_heli_spawn = False
		self.wave_rocket_spawn = False
		self.wave_ad_heli_spawn = True
		
	def increase_points(self):
		"""Increases the points of each hostile or hostile projectiles as
		the game progresses to a harder level."""
		self.hostile_points *= self.points_speedup_scale


































		
"""	def increase_speeds(self):
		self.ship_speed_factor *= self.speedup_scale
		self.ship_bullet_speed_factor *= self.speedup_scale
		
		
		
		self.helicopter_speed_factor *= self.speedup_scale
		self.helicopter_bullet_speed_factor *= self.speedup_scale
		self.hostile_speed_factor *= self.speedup_scale
"""	
