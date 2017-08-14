class Settings():
	
	def __init__(self):
		self.screen_width = 800
		self.screen_height = 600
		self.bg_color = (240, 240, 240)
		
		self.ship_time_immune = 10
		self.ship_time_hit = 0
		
		self.shipbullets_allowed = 100
		self.shipbullet_time_fire_interval = 0.1
		self.shipbullet_time_fire = 0
		
		#self.speedup_scale = 1.1
		self.points_speedup_scale = 1.5
		
		
		self.initialize_dynamic_settings()
		
	def initialize_dynamic_settings(self):
		self.ship_speed_factor = 0.6
		self.ship_bullet_speed_factor = 0.8
		self.ship_limit = 3
		self.ship_max_limit = 10
		
		self.shipbullets_constant_firing = False
		
		
		
		self.helicopter_speed_factor = 0.2
		self.helicopter_bullet_speed_factor = 0.4
		self.helicopter_points = 50
		
		#self.hostile_speed_factor = 0.2
		
		#self.hostile_speed_direction = 1
		#self.hostile_points = 50
		
		
	def increase_points(self):
		self.hostile_points *= self.points_speedup_scale


































		
"""	def increase_speeds(self):
		self.ship_speed_factor *= self.speedup_scale
		self.ship_bullet_speed_factor *= self.speedup_scale
		
		
		
		self.helicopter_speed_factor *= self.speedup_scale
		self.helicopter_bullet_speed_factor *= self.speedup_scale
		self.hostile_speed_factor *= self.speedup_scale
"""	
