import pygame
		
class ShipBulletSounds():
	"""Class Represents the ShipBullet sounds."""
	def __init__(self):
		"""Initialize the ShipBullet sounds."""
		# Loads the start, firing and end sound for shipbullet.
		self.start = pygame.mixer.Sound('sounds/projectiles/ships/ship_minigun_fire_start.ogg')
		self.firing = pygame.mixer.Sound('sounds/projectiles/ships/ship_minigun_firing.ogg')
		self.end = pygame.mixer.Sound('sounds/projectiles/ships/ship_minigun_fire_end.ogg')
		
class ShipMissileSounds():
	"""Class Represents the ShipMissile sounds."""
	def __init__(self):
		"""Initialize the ShipMissile sounds."""
		# Loads the start sound for shipmissile.
		self.firing = pygame.mixer.Sound('sounds/projectiles/ships/ship_missile_fire_start_V2_0.25s.ogg')
		
class ShipExplodeSounds():
	"""Class Represents the Explosion sounds."""
	def __init__(self):
		"""Initialize the Explosion sounds."""
		# Loads the start sound for explosion.
		self.start = pygame.mixer.Sound('sounds/explosion/ship_explode_V2_1s.ogg')
		
