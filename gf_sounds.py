import pygame

from gf_universals import get_process_time

def update_sounds(ai_settings, shipbullet_sounds, time_new):
	shipbullet_sound_firing_internals(ai_settings, shipbullet_sounds, time_new)
		
def shipbullet_sound_start_internals(ai_settings, shipbullet_sounds):
	shipbullet_sounds.start.set_volume(0.1)
	shipbullet_sounds.start.play()
	
	ai_settings.shipbullet_sound_start_stop = ai_settings.shipbullet_time_fire + shipbullet_sounds.start.get_length()
	
def shipbullet_sound_firing_internals(ai_settings, shipbullet_sounds, time_new):
	if time_new >= ai_settings.shipbullet_sound_start_stop and ai_settings.shipbullets_constant_firing:
		print("time_new", time_new)
		print("shipbullet_sound_start_stop", ai_settings.shipbullet_sound_start_stop)
		shipbullet_sounds.firing.play()
	
def shipbullet_sound_end_internals(ai_settings, shipbullet_sounds):
	shipbullet_sounds.firing.set_volume(0.1)
	shipbullet_sounds.firing.stop()
	shipbullet_sounds.end.set_volume(0.1)
	shipbullet_sounds.end.play()
	
