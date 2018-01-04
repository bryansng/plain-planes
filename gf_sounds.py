import pygame

def update_sounds_internals(ai_settings, ship, shipbullet_sounds, shipmissile_sounds, time_game_play):
	"""
	Upon calling this method, it will update/handle all game sounds that
	will not stop unless a certain condition is met.
	
	1. Shipbullet
		Keeps playing firing mode sound until player stops firing.
		
	2. ShipMissile
		Keeps playing launch sound until player stops firing.
	"""
	# Calls the function shipbullet_sound_firing_internals.
	shipbullet_sound_firing_internals(ai_settings, ship, shipbullet_sounds, time_game_play)
	# Calls the function shipmissile_sound_firing_internals.s
	shipmissile_sound_firing_internals(ai_settings, ship, shipmissile_sounds)




"""_____________________________________________________________________________
   1a) ShipBullet Sound Internals: 
       Start + Firing + End
_____________________________________________________________________________"""
		
def shipbullet_sound_start_internals(ai_settings, ship, shipbullet_sounds):
	"""
	Upon calling this method, it will play the shipbullet firing start sound
	and it will get the stop time for the start sound.
	"""
	if ship.upgrades_allow_bullets: 
		# Starts playing the start sound.
		shipbullet_sounds.start.play()
		
		# Gets the stop time for start sound, so that we know when it should stop.
		#
		# If we hold left mouse button or spacebar, this will just run once.
		# The below is used to update the shipbullet_sound_firing_internals.
		ai_settings.shipbullet_sound_start_stop = ai_settings.shipbullet_time_fire + shipbullet_sounds.start.get_length()
	
def shipbullet_sound_firing_internals(ai_settings, ship, shipbullet_sounds, time_game_play):
	"""
	Requires consistent update, hence placement in update_sounds_internals.
	
	Keeps playing the firing sound after the start sound ended.
	"""
	if ship.upgrades_allow_bullets:
		# If shipbullet firing start sound stopped/ended/finished and player is
		# still firing bullets, then play the shipbullet firing fire sound.
		if time_game_play >= ai_settings.shipbullet_sound_start_stop and ai_settings.shipbullets_constant_firing:
			shipbullet_sounds.firing.play()
	
def shipbullet_sound_end_internals(ai_settings, ship, shipbullet_sounds):
	"""
	Upon calling this method, it will stop the shipbullet firing fire sound
	and it will play the shipbullet firing end sound.
	"""
	if ship.upgrades_allow_bullets: 
		shipbullet_sounds.firing.stop()
		shipbullet_sounds.end.play()




"""_____________________________________________________________________________
   1b) ShipMissile Sound Internals: 
       Start/Firing
_____________________________________________________________________________"""
	
def shipmissile_sound_firing_internals(ai_settings, ship, shipmissile_sounds):
	"""
	Requires consistent update, hence placement in update_sounds_internals.
	
	Keeps playing the missile launch sound.
	"""
	if ship.upgrades_allow_missiles:
		# If player is still firing missiles, then play the shipbullet
		# firing fire sound.
		if ai_settings.shipmissiles_constant_firing:
			shipmissile_sounds.firing.play()




"""_____________________________________________________________________________
   1c) ShipExplode Sound Internals: 
       Start
_____________________________________________________________________________"""
		
def shipexplode_sound_start_internals(ai_settings, shipexplode_sounds):
	"""
	Upon calling this method, it will play the shipexplode sound
	and it will get the stop time for the start sound.
	"""
	# Plays the ShipExplode sound.
	shipexplode_sounds.start.play()
	
	
	
	
	
	
