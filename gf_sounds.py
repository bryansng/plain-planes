import pygame

def update_sounds_internals(ai_settings, ship, shiprailgun_sounds):
	"""
	Upon calling this method, it will update/handle all game sounds that
	will not stop unless a certain condition is met.
	
	1. Shipbullet
		Keeps playing firing mode sound until player stops firing.
		
	2. ShipMissile
		Keeps playing launch sound until player stops firing.
	"""
	# Calls the function shiprailgun_sound_firing_internals.
	shiprailgun_sound_firing_internals(ai_settings, ship, shiprailgun_sounds)




"""_____________________________________________________________________________
   1a) ShipBullet Sound Internals:
       Start/Firing
_____________________________________________________________________________"""
	
def shipbullet_sound_firing_internals(ai_settings, ship, shipbullet_sounds):
	"""
	Upon calling this method, plays the shipmissile launch sound once.
	
	Added into the methods to where new_missiles are created (gf_objects.py).
	"""
	if ship.upgrades_allow_bullets:
		# If player is still firing missiles, then play the shipmissile
		# firing fire sound.
		if ai_settings.shipbullets_constant_firing:
			shipbullet_sounds.firing.play()




"""_____________________________________________________________________________
   1b) ShipRailgun Sound Internals: 
       Start + Firing + End
_____________________________________________________________________________"""
		
def shiprailgun_sound_start_internals(ai_settings, ship, shiprailgun_sounds):
	"""
	Upon calling this method, it will play the Railgun firing start sound
	and it will get the stop time for the start sound.
	"""
	if ship.upgrades_allow_railguns: 
		# Starts playing the start sound.
		shiprailgun_sounds.start.play()
		
		# Gets the stop time for start sound, so that we know when it should stop.
		#
		# If we hold left mouse button or spacebar, this will just run once.
		# The below is used to update the shiprailgun_sound_firing_internals.
		ai_settings.shiprailgun_sound_start_stop = ai_settings.shiprailgun_time_fire + shiprailgun_sounds.start.get_length()
	
def shiprailgun_sound_firing_internals(ai_settings, ship, shiprailgun_sounds):
	"""
	Requires consistent update, hence placement in update_sounds_internals.
	
	Keeps playing the firing sound after the start sound ended.
	
	Deals with the case where the activation button is pressed but not let go,
	thus it will not stop the firing sound on the spot.
	"""
	if ship.upgrades_allow_railguns:
		# If Railgun firing start sound stopped/ended/finished and player is
		# still firing bullets, then play the Railgun firing fire sound.
		if ai_settings.time_game_play >= ai_settings.shiprailgun_sound_start_stop and ai_settings.shipbullets_constant_firing:
			shiprailgun_sounds.firing.play()
	
def shiprailgun_sound_end_internals(ai_settings, ship, shiprailgun_sounds):
	"""
	Upon calling this method, it will stop the shipbullet firing fire sound
	and it will play the shipbullet firing end sound.
	"""
	shiprailgun_sounds.firing.stop()
	shiprailgun_sounds.end.play()




"""_____________________________________________________________________________
   1c) ShipMissile Sound Internals: 
       Start/Firing
_____________________________________________________________________________"""
	
def shipmissile_sound_firing_internals(ai_settings, ship, shipmissile_sounds):
	"""
	Upon calling this method, plays the shipmissile launch sound once.
	
	Added into the methods to where new_missiles are created (gf_objects.py).
	"""
	if ship.upgrades_allow_missiles:
		# If player is still firing missiles, then play the shipmissile
		# firing fire sound.
		if ai_settings.shipmissiles_constant_firing:
			shipmissile_sounds.firing.play()




"""_____________________________________________________________________________
   1d) ShipExplode Sound Internals: 
       Start
_____________________________________________________________________________"""
		
def shipexplode_sound_start_internals(ai_settings, shipexplode_sounds):
	"""
	Upon calling this method, it will play the shipexplode sound.
	
	Added into the methods where explosions are created.
	"""
	# Plays the ShipExplode sound.
	shipexplode_sounds.start.play()
	
	
	
	
	
	
