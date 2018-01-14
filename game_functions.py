import sys
import pygame
import time

from time import process_time

from random import randint

from bullet import ShipBulletPrimary
from bullet import ShipBulletSecondary
from bullet import ShipMissilePrimary
from bullet import ShipMissileSecondary
from bullet import HelicopterBullet
from hostile import Helicopter
from hostile import Rocket

import gf_objects as gfobjects
import gf_hostiles as gfhostiles
import gf_sounds as gfsounds
import gf_universals as gf_uni

#def fire_ship_bullet(ai_settings, screen, ship, shipbullets):
#	if ai_settings.shipbullets_constant_firing:
#		if len(shipbullets) < ai_settings.shipbullets_allowed:
#			new_bullet = ShipBullet(ai_settings, screen, ship)
#			shipbullets.add(new_bullet)

def check_keydown_events(event, ai_settings, screen, ship, shipbullets, shiprailgun_sounds, shipmissiles, parachutes, u_rail, u_secondary, u_missile, u_laser, u_i_rail, u_i_secondary, u_i_missile, u_i_laser, helis, helibullets, rockets, rockets_hits_list, ad_helis, ad_helis_hits_list, explosions, stats, sb):
	"""Deals with all keydown events."""
	if event.key == pygame.K_r:
		ai_settings.upgrades_time_railgun_end = ai_settings.time_game - 1
		ai_settings.upgrades_time_secondary_end = ai_settings.time_game - 1
		ai_settings.upgrades_time_missile_end = ai_settings.time_game - 1
		ai_settings.upgrades_time_laser_end = ai_settings.time_game - 1
	# Dumps highscore to json and exit game.
	if event.key == pygame.K_q:
		sb.dumps_stats_to_json()
		pygame.quit()
		sys.exit()
	# Pauses the Game, opens the ESC menu.
	if event.key == pygame.K_ESCAPE:
		if stats.game_active and not stats.game_pause:
			stats.game_active = False
			stats.game_pause = True
			# Set mouse visibility to true and grab to false.
			pygame.mouse.set_visible(True)
			pygame.event.set_grab(False)
		elif not stats.game_active and stats.game_pause:
			stats.game_pause = False
			stats.game_active = True
			# Set mouse visibility to false and grab to true.
			pygame.mouse.set_visible(False)
			pygame.event.set_grab(True)
	# Starts the game upon pressing p during game_active = false.
	if not stats.game_pause and not stats.game_active and event.key == pygame.K_p:
		start_game(ai_settings, screen, ship, shipbullets, shipmissiles, parachutes, u_rail, u_secondary, u_missile, u_laser, u_i_rail, u_i_secondary, u_i_missile, u_i_laser, helis, helibullets, rockets, rockets_hits_list, ad_helis, ad_helis_hits_list, explosions, stats, sb)
	# Events for WASD, controls the motion of the ships.
	# Up
	if event.key == pygame.K_w or event.key == pygame.K_UP:
		ship.moving_up = True
	# Left
	if event.key == pygame.K_a or event.key == pygame.K_LEFT:
		ship.moving_left = True
	# Down
	if event.key == pygame.K_s or event.key == pygame.K_DOWN:
		ship.moving_down = True
	# Right
	if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
		ship.moving_right = True
	# Creates and fires bullets upon holding down spacebar.
	# Time of fire is required for rate of bullet firing.
	if event.key == pygame.K_SPACE:
		if ship.upgrades_allow_bullets:
			ai_settings.shipbullet_time_fire = ai_settings.time_game
			ai_settings.shipbullets_constant_firing = True
		elif ship.upgrades_allow_missiles:
			ai_settings.shipmissile_time_fire = ai_settings.time_game
			ai_settings.shipmissiles_constant_firing = True
		# Plays the Minigun/Railgun sound when the upgrade is active (in the file function).
		gfsounds.shiprailgun_sound_start_internals(ai_settings, ship, shiprailgun_sounds)
			
		#elif ship.upgrades_allow_missiles:
			#gfsounds.shipmissile_sound_start_internals(ai_settings, shipmissile_sounds)
		#fire_ship_bullet(ai_settings, screen, ship, shipbullets)
	# Creates and fires special weapons upon holding down either the Left or Right ALT.
	#if event.key == pygame.K_LALT or event.key == pygame.K_RALT:
	#	upgrade_missiles(ai_settings, screen, ship, shipmissiles)
		
	
def check_keyup_events(event, ai_settings, ship, shipbullets, shiprailgun_sounds, shipmissiles):
	"""Deals with all keyup events."""
	# Event for WASD, controls the motion of the ships.
	# Up
	if event.key == pygame.K_w or event.key == pygame.K_UP:
		ship.moving_up = False
	# Left
	if event.key == pygame.K_a or event.key == pygame.K_LEFT:
		ship.moving_left = False
	# Down
	if event.key == pygame.K_s or event.key == pygame.K_DOWN:
		ship.moving_down = False
	# Right
	if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
		ship.moving_right = False
	# No bullets are created/fired upon letting go spacebar.
	# Also starts playing end sound of firing, and stops playing firing sound.
	if event.key == pygame.K_SPACE:
		if ship.upgrades_allow_bullets:
			ai_settings.shipbullets_constant_firing = False
		elif ship.upgrades_allow_missiles:
			ai_settings.shipmissiles_constant_firing = False
		if ship.upgrades_allow_railguns:
			gfsounds.shiprailgun_sound_end_internals(ai_settings, ship, shiprailgun_sounds)
		
		
def check_events(ai_settings, screen, ship, shipbullets, shipbullet_sounds, shiprailgun_sounds, shipmissiles, shipmissile_sounds, shipexplode_sounds, parachutes, u_rail, u_secondary, u_missile, u_laser, u_i_rail, u_i_secondary, u_i_missile, u_i_laser, helis, helibullets, rockets, rockets_hits_list, ad_helis, ad_helis_hits_list, explosions, stats, play_button_mm, stats_button_mm, quit_button_mm, resume_button_esc, restart_button_esc, stats_button_esc, exit_button_esc, sb, gameclock):
	"""Deals with all the events."""
	for event in pygame.event.get():
		# Dumps highscore to json and exit game upon clicking the 'x'.
		if event.type == pygame.QUIT:
			sb.dumps_stats_to_json()
			pygame.quit()
			sys.exit()
		# Checks all key down events for the keyboard.
		if event.type == pygame.KEYDOWN:
			check_keydown_events(event, ai_settings, screen, ship, shipbullets, shiprailgun_sounds, shipmissiles, parachutes, u_rail, u_secondary, u_missile, u_laser, u_i_rail, u_i_secondary, u_i_missile, u_i_laser, helis, helibullets, rockets, rockets_hits_list, ad_helis, ad_helis_hits_list, explosions, stats, sb)
		# Checks all key up events for the keyboard.
		if event.type == pygame.KEYUP:
			check_keyup_events(event, ai_settings, ship, shipbullets, shiprailgun_sounds, shipmissiles)
		
		# Checking all mouse events in a separate method.
		check_mouse_events(event, ai_settings, screen, ship, shipbullets, shiprailgun_sounds, shipmissiles, parachutes, u_rail, u_secondary, u_missile, u_laser, u_i_rail, u_i_secondary, u_i_missile, u_i_laser, helis, helibullets, rockets, rockets_hits_list, ad_helis, ad_helis_hits_list, explosions, stats, play_button_mm, stats_button_mm, quit_button_mm, resume_button_esc, restart_button_esc, stats_button_esc, exit_button_esc, sb)


def check_mouse_events(event, ai_settings, screen, ship, shipbullets, shiprailgun_sounds, shipmissiles, parachutes, u_rail, u_secondary, u_missile, u_laser, u_i_rail, u_i_secondary, u_i_missile, u_i_laser, helis, helibullets, rockets, rockets_hits_list, ad_helis, ad_helis_hits_list, explosions, stats, play_button_mm, stats_button_mm, quit_button_mm, resume_button_esc, restart_button_esc, stats_button_esc, exit_button_esc, sb):
	"""Deals with all the mouse events."""
	# If mouse button down and game activity is false, get the position 
	# of the mouse, if mouse within the play_button_mm, game is started.
	if event.type == pygame.MOUSEBUTTONDOWN:
		if not stats.game_active and not stats.game_pause:
			mouse_x, mouse_y = pygame.mouse.get_pos()
			check_main_menu_mouse_click(ai_settings, screen, ship, shipbullets, shipmissiles, parachutes, u_rail, u_secondary, u_missile, u_laser, u_i_rail, u_i_secondary, u_i_missile, u_i_laser, helis, helibullets, rockets, rockets_hits_list, ad_helis, ad_helis_hits_list, explosions, stats, play_button_mm, stats_button_mm, quit_button_mm, sb, mouse_x, mouse_y)
	if event.type == pygame.MOUSEBUTTONDOWN:
		if stats.game_pause and not stats.game_active:
			mouse_x, mouse_y = pygame.mouse.get_pos()
			check_esc_mouse_click(ai_settings, screen, ship, shipbullets, shipmissiles, parachutes, u_rail, u_secondary, u_missile, u_laser, u_i_rail, u_i_secondary, u_i_missile, u_i_laser, helis, helibullets, rockets, rockets_hits_list, ad_helis, ad_helis_hits_list, explosions, resume_button_esc, restart_button_esc, stats_button_esc, exit_button_esc, stats, sb, mouse_x, mouse_y)
	
	# Mouse movement methods.
	mouse_movements(event, ai_settings, screen, ship, stats, sb)
	# Mouse weapon firing methods.
	mouse_weapon_fires(event, ai_settings, screen, ship, shipbullets, shiprailgun_sounds, shipmissiles, stats)
	

def mouse_movements(event, ai_settings, screen, ship, stats, sb):
	"""Handles all the mouse movements."""
	# Mouse will start working after 1 second of clicking the play_button_mm.
	mouse_work_time = float('{:.1f}'.format(ai_settings.mouse_start_time_click + ai_settings.mouse_starttime_nowork_interval))
	
	# Sets the mouse to be at its starting position (ship.rect.center).
	if not ai_settings.mouse_working and stats.game_active:
		print("Running")
		pygame.event.clear(pygame.MOUSEMOTION)
		pygame.mouse.set_pos([ship.rect.centerx, ship.rect.centery])
	
	# Sets mouse working to true, mouse should work when this is true.
	# By making it >= instead of ==, mouse will now always work,
	# previously it hangs or doesn't work at start (sometimes).
	if ai_settings.time_game >= mouse_work_time:
		ai_settings.mouse_working = True
		#print(event)
		print(pygame.MOUSEBUTTONDOWN)
		
	# If true, all movements for ship by mouse will be registered.
	if ai_settings.mouse_working:
		# Adds x, y values to ship rect coordinates if there is a mouse motion
		# to simulate mouse controlling the ship.
		# Must update the movements for all directions.
		# NOTE: This is as of writing, optimized to be smooth enough.
		# Change or suggest if otherwise.
		if event.type == pygame.MOUSEMOTION and stats.game_active:
			mouse_x, mouse_y = pygame.mouse.get_rel()
			# Up
			if mouse_y < 0 and ship.rect.top > ship.sb.topbracket_rect.bottom:
				ship.centery += mouse_y
			# Left
			if mouse_x < 0 and ship.rect.left > 0:
				ship.centerx += mouse_x
			# Down
			if mouse_y > 0 and ship.rect.bottom < ship.screen_rect.bottom:
				ship.centery += mouse_y
			# Right
			if mouse_x > 0 and ship.rect.right < ship.screen_rect.right:
				ship.centerx += mouse_x
			
def mouse_weapon_fires(event, ai_settings, screen, ship, shipbullets, shiprailgun_sounds, shipmissiles, stats):
	"""Handles all the mouse weapon fires."""
	# If true, all firing methods for ship by mouse will be registered.
	if ai_settings.mouse_working:
		# Sets ship firing mode to true if game is active and mouse button is down.
		# Also starts playing start sound of firing.
		#
		# 1 is LMB, which is for shipbullets.
		if event.type == pygame.MOUSEBUTTONDOWN and stats.game_active:
			if event.button == 1:
				if ship.upgrades_allow_bullets:
					ai_settings.shipbullet_time_fire = ai_settings.time_game
					ai_settings.shipbullets_constant_firing = True
				elif ship.upgrades_allow_missiles:
					ai_settings.shipmissile_time_fire = ai_settings.time_game
					ai_settings.shipmissiles_constant_firing = True
				# Plays the Minigun/Railgun sound when the upgrade is active (in the file function).
				gfsounds.shiprailgun_sound_start_internals(ai_settings, ship, shiprailgun_sounds)
		
		# Sets ship firing mode to false if game is active and mouse button is up.
		# Also starts playing end sound of firing, and stops playing firing sound.
		#
		# 1 is LMB, which is for shipbullets.
		if event.type == pygame.MOUSEBUTTONUP and stats.game_active:
			if event.button == 1:
				if ship.upgrades_allow_bullets:
					ai_settings.shipbullets_constant_firing = False
				elif ship.upgrades_allow_missiles:
					ai_settings.shipmissiles_constant_firing = False
				if ship.upgrades_allow_railguns:
					gfsounds.shiprailgun_sound_end_internals(ai_settings, ship, shiprailgun_sounds)
		
	
def check_main_menu_mouse_click(ai_settings, screen, ship, shipbullets, shipmissiles, parachutes, u_rail, u_secondary, u_missile, u_laser, u_i_rail, u_i_secondary, u_i_missile, u_i_laser, helis, helibullets, rockets, rockets_hits_list, ad_helis, ad_helis_hits_list, explosions, stats, play_button_mm, stats_button_mm, quit_button_mm, sb, mouse_x, mouse_y):
	"""Manages the button within the Main menu."""
	# Starts the game when the play_button is clicked.
	# Gives a True if mouse coordinates is in play_button_mm.rect.
	play_button_mm_clicked = play_button_mm.rect.collidepoint(mouse_x, mouse_y)
	if not stats.game_pause and not stats.game_active and play_button_mm_clicked:
		start_game(ai_settings, screen, ship, shipbullets, shipmissiles, parachutes, u_rail, u_secondary, u_missile, u_laser, u_i_rail, u_i_secondary, u_i_missile, u_i_laser, helis, helibullets, rockets, rockets_hits_list, ad_helis, ad_helis_hits_list, explosions, stats, sb)
	# Opens Statictics accumulated throughout player's gameplays.
	# Gives a True if mouse coordinates is in stats_button_mm.rect.
	stats_button_mm_clicked = stats_button_mm.rect.collidepoint(mouse_x, mouse_y)
	if stats_button_mm_clicked:
		pass
	# Quits the game entirely.
	# Gives a True if mouse coordinates is in quit_button_mm.rect.
	quit_button_mm_clicked = quit_button_mm.rect.collidepoint(mouse_x, mouse_y)
	if quit_button_mm_clicked:
		pygame.quit()
		sys.exit()
		
		
def check_esc_mouse_click(ai_settings, screen, ship, shipbullets, shipmissiles, parachutes, u_rail, u_secondary, u_missile, u_laser, u_i_rail, u_i_secondary, u_i_missile, u_i_laser, helis, helibullets, rockets, rockets_hits_list, ad_helis, ad_helis_hits_list, explosions, resume_button_esc, restart_button_esc, stats_button_esc, exit_button_esc, stats, sb, mouse_x, mouse_y):
	"""Manages the buttons within the ESC menu."""
	# Resumes the game.
	# Gives a True if mouse coordinates is in resume_button_esc.rect.
	resume_button_esc_clicked = resume_button_esc.rect.collidepoint(mouse_x, mouse_y)
	if resume_button_esc_clicked:
		stats.game_pause = False
		stats.game_active = True
		# Set mouse visibility to false and grab to true.
		pygame.mouse.set_visible(False)
		pygame.event.set_grab(True)
	# Restarts the current gameplay.
	# Gives a True if mouse coordinates is in restart_button_esc.rect.
	restart_button_esc_clicked = restart_button_esc.rect.collidepoint(mouse_x, mouse_y)
	if restart_button_esc_clicked:
		print("Restart clicked")
		stats.ship_left = 0
		stats.game_pause = False
		start_game(ai_settings, screen, ship, shipbullets, shipmissiles, parachutes, u_rail, u_secondary, u_missile, u_laser, u_i_rail, u_i_secondary, u_i_missile, u_i_laser, helis, helibullets, rockets, rockets_hits_list, ad_helis, ad_helis_hits_list, explosions, stats, sb)
	# Opens Statictics accumulated throughout player's gameplays.
	# Gives a True if mouse coordinates is in stats_button_esc.rect.
	stats_button_esc_clicked = stats_button_esc.rect.collidepoint(mouse_x, mouse_y)
	if stats_button_esc_clicked:
		print("Stats clicked")
		pass
	# Exits to the Main menu.
	# Gives a True if mouse coordinates is in quit_button_mm.rect.
	exit_button_esc_clicked = exit_button_esc.rect.collidepoint(mouse_x, mouse_y)
	if exit_button_esc_clicked:
		print("Exit clicked")
		stats.game_pause = False
		stats.game_active = False
		stats.ship_left = 0
		# Set mouse visibility to true and grab to false.
		pygame.mouse.set_visible(True)
		pygame.event.set_grab(False)
		
		
def start_game(ai_settings, screen, ship, shipbullets, shipmissiles, parachutes, u_rail, u_secondary, u_missile, u_laser, u_i_rail, u_i_secondary, u_i_missile, u_i_laser, helis, helibullets, rockets, rockets_hits_list, ad_helis, ad_helis_hits_list, explosions, stats, sb):
	"""Starts a new game, reset settings, remove projectiles and objects, start new wave, center ship, etc."""
	print("Game started")
	# Loads high score from json file.
	sb.loads_stats_from_json()
	
	# Sets game_active to True and reset statistics.
	stats.game_active = True
	stats.reset_stats()
	
	# Remove projectiles and objects from previous iteration of the game.
	shipbullets.empty()
	shipmissiles.empty()
	helis.empty()
	helibullets.empty()
	rockets.empty()
	ad_helis.empty()
	parachutes.empty()
	explosions.empty()
	u_rail.empty()
	u_secondary.empty()
	u_missile.empty()
	u_laser.empty()
	u_i_rail.empty()
	u_i_secondary.empty()
	u_i_missile.empty()
	u_i_laser.empty()
	
	# Centers the ship.
	ship.center_ship()
	
	"""
	# Sets the mouse to be at its starting position (ship.rect.center).
	pygame.event.clear(pygame.MOUSEMOTION)
	pygame.mouse.set_pos([ship.rect.centerx, ship.rect.centery])
	"""
	
	# Set mouse visibility to false and grab to true.
	pygame.mouse.set_visible(False)
	pygame.event.set_grab(True)
	# Set mouse working to false and get mouse_start_time_click to 
	# set it back to True.
	ai_settings.mouse_working = False
	ai_settings.mouse_start_time_click = ai_settings.time_game
	
	# Creates a wave of hostiles.
	if ai_settings.wave_hostile_spawn:
		if ai_settings.wave_heli_spawn:
			gfhostiles.create_wave_helicopter(ai_settings, screen, helis)
		if ai_settings.wave_rocket_spawn:
			gfhostiles.create_wave_rocket(ai_settings, screen, ship, rockets, rockets_hits_list)
		if ai_settings.wave_ad_heli_spawn:
			gfhostiles.create_wave_ad_heli(ai_settings, screen, ad_helis, ad_helis_hits_list)
			
	# Resets all Upgrades, but enable default weapons.
	gf_uni.remove_upgrades_all(ai_settings, ship, u_i_rail, u_i_secondary, u_i_missile, u_i_laser)
	"""
	# Sets the mouse to be at its starting position (ship.rect.center).
	if not ai_settings.mouse_working and stats.game_active:
		print("Running")
		pygame.event.clear(pygame.MOUSEMOTION)
		pygame.mouse.set_pos([ship.rect.centerx, ship.rect.centery])"""















	
def update_screen(ai_settings, screen, ship, shipbullets, shipmissiles, parachutes, u_rail, u_secondary, u_missile, u_laser, u_i_rail, u_i_secondary, u_i_missile, u_i_laser, helis, helibullets, rockets, ad_helis, explosions, stats, play_button_mm, stats_button_mm, quit_button_mm, resume_button_esc, restart_button_esc, stats_button_esc, exit_button_esc, sb, gameclock, bg):
	"""Updates the screen with new data from update_internals 
	and check_events in one iteration of them."""
	# Fill the screen with the color specified in ai_settings.
	#screen.fill(ai_settings.bg_color)
	bg.draw_background()
	
	# Draws all the projectiles and objects.
	#
	# Whatever object that is drawn first will be behind the next object
	# being drawn.
	shipbullets.draw(screen)
	shipmissiles.draw(screen)
	ship.blitme()
	parachutes.draw(screen)
	u_rail.draw(screen)
	u_secondary.draw(screen)
	u_missile.draw(screen)
	u_laser.draw(screen)
	explosions.draw(screen)
	helis.draw(screen)
	helibullets.draw(screen)
	rockets.draw(screen)
	ad_helis.draw(screen)
	
	# If game is not active and not paused, draw the Main menu.
	if not stats.game_active and not stats.game_pause:
		play_button_mm.draw_button()
		stats_button_mm.draw_button()
		quit_button_mm.draw_button()
	
	# If game is paused, draw the ESC menu.
	if not stats.game_active and stats.game_pause:
		resume_button_esc.draw_button()
		restart_button_esc.draw_button()
		stats_button_esc.draw_button()
		exit_button_esc.draw_button()
	
	# Draws all the scoreboard details onto the screen.
	sb.show_score()
	
	# Draws all the timing related details onto the screen.
	gameclock.show_game_time()
	u_i_rail.draw(screen)
	u_i_secondary.draw(screen)
	u_i_missile.draw(screen)
	u_i_laser.draw(screen)
	
	# Updates the contents of the entire display.
	pygame.display.flip()
	
	
	













	
def update_internals(ai_settings, screen, ship, shipbullets, shipbullet_sounds, shiprailgun_sounds, shipmissiles, shipmissile_sounds, shipexplode_sounds, parachutes, u_rail, u_secondary, u_missile, u_laser, u_i_rail, u_i_secondary, u_i_missile, u_i_laser, helis, helibullets, rockets, rockets_hits_list, ad_helis, ad_helis_hits_list, explosions, stats, sb, gameclock):
	"""Update the internals of the objects and projectiles."""
	# Update internals of ship.
	gfobjects.update_ship_internals(ai_settings, screen, ship, shipbullets, shiprailgun_sounds, shipexplode_sounds, parachutes, u_i_rail, u_i_secondary, u_i_missile, u_i_laser, helis, helibullets, rockets, rockets_hits_list, ad_helis, ad_helis_hits_list, explosions, stats, sb)
	# Update internals of ship's weapons.
	gfobjects.update_shipweapon_internals(ai_settings, screen, ship, shipbullets, shipbullet_sounds, shipmissiles, shipmissile_sounds, shipexplode_sounds, parachutes, helis, helibullets, rockets, rockets_hits_list, ad_helis, ad_helis_hits_list, explosions, stats, sb)
	# Update internals of helis together with helibullets.
	gfhostiles.update_heli_internals(ai_settings, screen, ship, shiprailgun_sounds, u_i_rail, u_i_secondary, u_i_missile, u_i_laser, helis, helibullets, explosions, stats, sb)
	# Update internals of rockets.
	gfhostiles.update_rocket_internals(ai_settings, screen, ship, rockets, rockets_hits_list, stats)
	# Update internals of ad_helis together with
	gfhostiles.update_ad_heli_internals(ai_settings, screen, ad_helis, ad_helis_hits_list, stats)
	# Update internals of parachutes.
	gfobjects.update_parachutes_internals(ai_settings, screen, ship, shipbullets, shipmissiles, parachutes, u_rail, u_secondary, u_missile, u_laser, ad_helis, stats, sb)
	# Update internals of drops.
	gfobjects.update_drops_internals(ai_settings, screen, ship, shipbullets, shiprailgun_sounds, shipmissiles, u_rail, u_secondary, u_missile, u_laser, u_i_rail, u_i_secondary, u_i_missile, u_i_laser, sb)
	# Update internals of explosions.
	explosions.update()
	# Update internals of sb/Scoreboard.
	update_score(stats, sb)
	# Update internals of time/timer.
	gfobjects.update_upgrade_timers(gameclock, u_i_rail, u_i_secondary, u_i_missile, u_i_laser)
	# Update internals of sounds.
	gfsounds.update_sounds_internals(ai_settings, ship, shiprailgun_sounds)


def update_score(stats, sb):
	"""Update and shows the score."""
	# Equate high score and score if score is greater than high score.
	if stats.score > stats.high_score:
		stats.high_score = stats.score

	# Updates the scoreboard with new statistics.
	sb.prep_score()
	sb.prep_high_score()
	sb.prep_level()
	sb.prep_ships()













