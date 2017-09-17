import pygame
		
class ShipBulletSounds():
	"""A class to represent the ShipBullet sounds."""
	def __init__(self):
		"""Initialize the ShipBullet sounds."""
		# Loads the start, firing and end sound for shipbullet.
		self.start = pygame.mixer.Sound('sounds/projectiles/ships/ship_minigun_fire_start.ogg')
		self.firing = pygame.mixer.Sound('sounds/projectiles/ships/ship_minigun_firing.ogg')
		self.end = pygame.mixer.Sound('sounds/projectiles/ships/ship_minigun_fire_end.ogg')
