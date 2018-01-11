class Settings():
	"""A class to represent the settings of the game."""
	def __init__(self):
		"""Initialize all the settings of the game."""
		self.screen_settings()
		self.ship_settings()
		self.hostile_settings()
		self.misc_settings()
		self.game_internal_settings()
		
		
		
	def screen_settings(self):
		# Screen settings.
		self.screen_width = 800
		self.screen_height = 600
		self.bg_color = (240, 240, 240)
		
		
		
	def ship_settings(self):
		# Ship settings.
		self.ship_speed_factor = 0.6
		self.ship_speed_acceleration = 1.1
		self.ship_limit = 3
		self.ship_max_limit = 10
		
		# Ship Immune settings
		self.ship_time_immune = 3
		self.ship_time_hit = 0
		
		# Calls the ship_weapons settings method.
		self.ship_weapons_settings()
		
		
		
	def ship_weapons_settings(self):
		# Ship bullet settings.
		self.shipbullets_allowed = 100
		# Ship missile settings.
		self.shipmissiles_allowed = 100
		
		# Ship Default Firing Mode (Based on Type of Projectiles)
		# 1 - Bullets
		# 2 - Missiles
		# 3 - Lasers
		self.ship_weapon_default = 1
		
		# Ship bullet settings.
		self.shipbullet_time_fire_interval = 0.3
		self.ship_bullet_speed_factor = 0.8
		self.shipbullet_time_fire = 0
		self.shipbullets_constant_firing = False
		self.shipbullet_sound_start_stop = 0
		
		# Ship Railgun settings.
		self.shiprailgun_time_fire = 0
		self.shiprailgun_sound_start_stop = 0
		
		# Ship missile settings.
		self.shipmissile_time_fire_interval = 0.3
		self.ship_missile_speed_factor = 0.85
		self.shipmissile_time_fire = 0
		self.shipmissiles_constant_firing = False  
		self.shipmissile_sound_start_stop = 0
		
		# Calls the ship_upgrade settings method.
		self.ship_upgrade_settings()
		
		
		
	def ship_upgrade_settings(self):
		# Upgrades settings and probability based on Ship's default weapon.
		self.upgrades_speed_factor = 0.1
		
		if self.ship_weapon_default == 1:
			self.upgrades_railgun_p = 0.7		# Default 0.7
			self.upgrades_secondary_p = 0.25	# Default 0.25
			self.upgrades_missile_p = 0.045		# Default 0.045
			self.upgrades_laser_p = 0.005		# Default 0.005
		elif self.ship_weapon_default == 2:
			self.upgrades_railgun_p = 0.045		# Default 0.045
			self.upgrades_secondary_p = 0.25	# Default 0.25
			self.upgrades_missile_p = 0.7		# Default 0.7
			self.upgrades_laser_p = 0.005		# Default 0.005
			
		self.upgrades_total_no = 4
		
		self.upgrades_time_railgun_start = 0
		self.upgrades_time_railgun_duration = 10
		self.upgrades_time_railgun_max = 180
		self.upgrades_time_railgun_end = 0
		
		self.upgrades_time_secondary_start = 0
		self.upgrades_time_secondary_duration = 10
		self.upgrades_time_secondary_max = 180
		self.upgrades_time_secondary_end = 0
		
		self.upgrades_time_missile_start = 0
		self.upgrades_time_missile_duration = 10
		self.upgrades_time_missile_max = 180
		self.upgrades_time_missile_end = 0
		
		self.upgrades_time_laser_start = 0
		self.upgrades_time_laser_duration = 10
		self.upgrades_time_laser_max = 180
		self.upgrades_time_laser_end = 0
		
		self.upgrades_no_of_current_upgrades = 0
		
		self.upgrades_time_start = 0
		self.upgrades_time_duration = 10
		self.upgrades_time_max = 180
		self.upgrades_time_end = 0
		
		
		
	def hostile_settings(self):
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
		
		# Disabling this, disables all hostile spawns.
		# Enabling this, allows the toggling of the different hostile spawns.
		self.wave_hostile_spawn = True
		self.wave_heli_spawn = False
		self.wave_rocket_spawn = False
		self.wave_ad_heli_spawn = True
		
		# Number of Hostiles that will spawn per wave.
		# This is used during the process of wave creation in gf_hostiles.py
		self.helicopter_wave_limit = 10		# Default 10
		self.rocket_wave_limit = 10			# Default 10
		self.ad_heli_wave_limit = 15		# Default 5
		
		
		
	def misc_settings(self):
		# Parachute settings.
		self.parachute_speed_factor = 0.1
		self.parachute_points = 25
		
		# Explosion settings.
		self.explosion_time_disappear = 0.15
		self.explosion_time_create = 0
		
		
		
	def game_internal_settings(self):
		# Mouse start game settings.
		self.mouse_starttime_nowork_interval = 1
		self.mouse_start_time_click = 0
		self.mouse_working = False
		
		# Points increment settings.
		self.points_speedup_scale = 1.5
		
		# Time settings.
		self.time_game = 0
		self.time_game_play = 0
		
		
		
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
