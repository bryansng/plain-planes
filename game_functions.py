import sys
import pygame
import time

from time import process_time

from random import randint

from bullet import ShipBullet
from bullet import HelicopterBullet
from hostile import Helicopter
from hostile import Rocket

from gf_objects import *
from gf_hostiles import *

#def fire_ship_bullet(ai_settings, screen, ship, shipbullets):
#	if ai_settings.shipbullets_constant_firing:
#		if len(shipbullets) < ai_settings.shipbullets_allowed:
#			new_bullet = ShipBullet(ai_settings, screen, ship)
#			shipbullets.add(new_bullet)

def check_keydown_events(event, ai_settings, screen, ship, shipbullets, helis, helibullets, stats, sb):
	"""Deals with all keydown events."""
	# Dumps highscore to json and exit game.
	if event.key == pygame.K_q:
		sb.dumps_stats_to_json()
		sys.exit()
	# Starts the game upon pressing p during game_active = false.
	if event.key == pygame.K_p:
		start_game(ai_settings, screen, ship, shipbullets, helis, helibullets, stats, sb)
	# Event for WASD, controls the motion of the ships.
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
		ai_settings.shipbullet_time_fire = float('{:.1f}'.format(get_process_time()))
		ai_settings.shipbullets_constant_firing = True
		#fire_ship_bullet(ai_settings, screen, ship, shipbullets)
		
	
def check_keyup_events(event, ai_settings, ship, shipbullets):
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
	if event.key == pygame.K_SPACE:
		ai_settings.shipbullets_constant_firing = False
		
		
def check_events(ai_settings, screen, ship, shipbullets, helis, helibullets, stats, play_button, sb):
	"""Deals with all the events."""
	for event in pygame.event.get():
		# Dumps highscore to json and exit game upon clicking the 'x'.
		if event.type == pygame.QUIT:
			sb.dumps_stats_to_json()
			sys.exit()
		# Checks all key down events for the keyboard.
		if event.type == pygame.KEYDOWN:
			check_keydown_events(event, ai_settings, screen, ship, shipbullets, helis, helibullets, stats, sb)
		# Checks all key up events for the keyboard.
		if event.type == pygame.KEYUP:
			check_keyup_events(event, ai_settings, ship, shipbullets)
		
		# Checking all mouse events in a separate method.
		check_mouse_events(event, ai_settings, screen, ship, shipbullets, helis, helibullets, stats, play_button, sb)


def check_mouse_events(event, ai_settings, screen, ship, shipbullets, helis, helibullets, stats, play_button, sb):
	"""Deals with all the mouse events."""
	# If mouse button down and game activity is false, get the position 
	# of the mouse, if mouse within the play_button, game is started.
	if event.type == pygame.MOUSEBUTTONDOWN and not stats.game_active:
		mouse_x, mouse_y = pygame.mouse.get_pos()
		check_play_button_mouse_click(ai_settings, screen, ship, shipbullets, helis, helibullets, stats, play_button, sb, mouse_x, mouse_y)
	
	# Mouse movement method.
	mouse_movements(event, ai_settings, screen, ship, shipbullets, helis, helibullets, stats, play_button, sb)

def mouse_movements(event, ai_settings, screen, ship, shipbullets, helis, helibullets, stats, play_button, sb):
	"""Handles all the mouse movements."""
	# Mouse will start working after 1 second of clicking the play_button.
	mouse_work_time = float('{:.1f}'.format(ai_settings.mouse_start_time_click + ai_settings.mouse_starttime_nowork_interval))
	mouse_time_new = float('{:.1f}'.format(get_process_time()))
	
	# Sets mouse working to true, mouse should work when this is true.
	if mouse_time_new == mouse_work_time:
		ai_settings.mouse_working = True
		
	# If mouse_working is false, keep setting the mouse to be at ship.rect.center.
	if not ai_settings.mouse_working and stats.game_active:
		pygame.mouse.set_pos([ship.rect.centerx, ship.rect.centery])
		
	# If true, all movement for ship by mouse will be registered.
	if ai_settings.mouse_working:
		# Sets ship firing mode to true if game is active and mouse button is down.
		if event.type == pygame.MOUSEBUTTONDOWN and stats.game_active:
			ai_settings.shipbullets_constant_firing = True
		# Sets ship firing mode to false if game is active and mouse button is up.
		if event.type == pygame.MOUSEBUTTONUP and stats.game_active:
			ai_settings.shipbullets_constant_firing = False
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
				
			# This whole shit is redundant.
			"""
			# Up Left
			if mouse_y < 0 and ship.rect.top > ship.sb.topbracket_rect.bottom:
				if mouse_x < 0 and ship.rect.left > 0:
					ship.centerx += mouse_x
					ship.centery += mouse_y
			# Up Right
			if mouse_y < 0 and ship.rect.top > ship.sb.topbracket_rect.bottom:
				if mouse_x > 0 and ship.rect.right < ship.screen_rect.right:
					ship.centerx += mouse_x
					ship.centery += mouse_y
			# Down Left   
			if mouse_y > 0 and ship.rect.bottom < ship.screen_rect.bottom:
				if mouse_x < 0 and ship.rect.left > 0:
					ship.centerx += mouse_x
					ship.centery += mouse_y
			# Down Right
			if mouse_y > 0 and ship.rect.bottom < ship.screen_rect.bottom:
				if mouse_x > 0 and ship.rect.right < ship.screen_rect.right:
					ship.centerx += mouse_x
					ship.centery += mouse_y
			"""
		
	
def check_play_button_mouse_click(ai_settings, screen, ship, shipbullets, helis, helibullets, stats, play_button, sb, mouse_x, mouse_y):
	"""Starts the game when the button is clicked within the play_button."""
	# Gives a True if mouse coordinates is in play_button.rect.
	button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
	if button_clicked:
		start_game(ai_settings, screen, ship, shipbullets, helis, helibullets, stats, sb)
		
		
def start_game(ai_settings, screen, ship, shipbullets, helis, helibullets, stats, sb):
	"""Starts a new game, reset settings, remove projectiles and objects, start new wave, center ship, etc."""
	# Loads high score from json file.
	sb.loads_stats_from_json()
	
	# Sets game_active to True and reset statistics.
	stats.game_active = True
	stats.reset_stats()
	
	# Remove projectiles and objects from previous iteration of the game.
	shipbullets.remove()
	helis.remove()
	helibullets.remove()
	
	# Creates a new wave of objects/hostiles.
	"""create_wave_helicopter(ai_settings, screen, helis)"""
	ship.center_ship()
	
	# Set mouse visibility to false and grab to true.
	pygame.mouse.set_visible(False)
	pygame.event.set_grab(True)
	# Set mouse working to false and get mouse_start_time_click to 
	# set it back to True.
	mouse_working = False
	ai_settings.mouse_start_time_click = float('{:.1f}'.format(get_process_time()))
















	
def update_screen(ai_settings, screen, ship, shipbullets, helis, helibullets, rockets, stats, play_button, stats_button, exit_button, sb, bg):
	"""Updates the screen with new data from update_internals 
	and check_events in one iteration of them."""
	# Fill the screen with the color specified in ai_settings.
	screen.fill(ai_settings.bg_color)
	bg.draw_background()
	
	# Draws all the projectiles and objects.
	ship.blitme()
	shipbullets.draw(screen)
	helis.draw(screen)
	helibullets.draw(screen)
	rockets.draw(screen)
	
	# If game is not active, draw the play_button.
	if not stats.game_active:
		play_button.draw_button()
		stats_button.draw_button()
		exit_button.draw_button()
		#restart_button.draw_button()
		#settings_button.draw_button()
	
	# Draws all the scoreboard details onto the screen.
	sb.show_score()
	
	# Updates the contents of the entire display.
	pygame.display.flip()
	
	
	













	
def update_internals(ai_settings, screen, ship, shipbullets, helis, helibullets, rockets, rockets_hits_list, stats, sb):
	"""Update the internals of the objects and projectiles."""
	# Update internals of ship from its class file.
	# Specifically, its movements.
	ship.update()
	# Update internals of shipbullets.
	update_shipbullet_internals(ai_settings, screen, ship, shipbullets, helis, helibullets, rockets, rockets_hits_list, stats)
	# Update internals of helis together with helibullets.
	update_heli_internals(ai_settings, screen, ship, helis, helibullets, stats, sb)
	# Update internals of rockets.
	update_rocket_internals(ai_settings, screen, ship, rockets, rockets_hits_list, stats)
	# Update internals of sb/Scoreboard.
	update_score(stats, sb)


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











