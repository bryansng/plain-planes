class Settings():
	
	def __init__(self):
		# Screen settings.
		self.screen_width = 800
		self.screen_height = 600
		self.bg_color = (240, 240, 240)
		
		
		
		# Ship bullet settings.
		self.shipbullets_allowed = 100
		self.shipbullet_time_fire_interval = 0.1
		self.shipbullet_time_fire = 0
		
		# Points increment settings.
		self.points_speedup_scale = 1.5
		
		# Dynamic settings.
		self.initialize_dynamic_settings()
		
	def initialize_dynamic_settings(self):
		# Ship settings.
		self.ship_speed_factor = 0.6
		self.ship_bullet_speed_factor = 0.8
		self.ship_limit = 3
		self.ship_max_limit = 10
		# Ship Immune settings
		self.ship_time_immune = 3
		self.ship_time_hit = 0
		
		# Ship bullet firing settings.
		self.shipbullets_constant_firing = False
		
		# Mouse start game settings.
		self.mouse_starttime_nowork_interval = 1
		self.mouse_start_time_click = 0
		self.mouse_working = False
		
		
		# Helicopter and helicopter bullet settings.
		self.helicopter_speed_factor = 0.2
		self.helicopter_bullet_speed_factor = 0.4
		self.helicopter_points = 50
		
		
	def increase_points(self):
		self.hostile_points *= self.points_speedup_scale


































		
"""	def increase_speeds(self):
		self.ship_speed_factor *= self.speedup_scale
		self.ship_bullet_speed_factor *= self.speedup_scale
		
		
		
		self.helicopter_speed_factor *= self.speedup_scale
		self.helicopter_bullet_speed_factor *= self.speedup_scale
		self.hostile_speed_factor *= self.speedup_scale
"""	
