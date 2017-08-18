import sys
import pygame
import time

from time import sleep
from time import process_time

from random import randint

from bullet import ShipBullet
from bullet import HelicopterBullet
from hostile import Helicopter

#def fire_ship_bullet(ai_settings, screen, ship, shipbullets):
#	if ai_settings.shipbullets_constant_firing:
#		if len(shipbullets) < ai_settings.shipbullets_allowed:
#			new_bullet = ShipBullet(ai_settings, screen, ship)
#			shipbullets.add(new_bullet)

def check_keydown_events(event, ai_settings, screen, ship, shipbullets, helis, helibullets, stats, sb):
	"""Deals with all keydown events."""
	# Dumps highscore to json and exit game.
	if event.key == pygame.K_q:
		sb.dumps_highscore_to_json()
		sys.exit()
	# Starts the game upon pressing p during game_active = false.
	if event.key == pygame.K_p:
		start_game(ai_settings, screen, ship, shipbullets, helis, helibullets, stats, sb)
	# Event for WASD, controls the motion of the ships.
	if event.key == pygame.K_w or event.key == pygame.K_UP:
		ship.moving_up = True
	#if 
	if event.key == pygame.K_a or event.key == pygame.K_LEFT:
		ship.moving_left = True
	if event.key == pygame.K_s or event.key == pygame.K_DOWN:
		ship.moving_down = True
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
	if event.key == pygame.K_w or event.key == pygame.K_UP:
		ship.moving_up = False
	if event.key == pygame.K_a or event.key == pygame.K_LEFT:
		ship.moving_left = False
	if event.key == pygame.K_s or event.key == pygame.K_DOWN:
		ship.moving_down = False
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
			sb.dumps_highscore_to_json()
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
	# If mouse button down, get the position of the mouse, if mouse within the
	# play_button, game is started.
	if event.type == pygame.MOUSEBUTTONDOWN:
		mouse_x, mouse_y = pygame.mouse.get_pos()
		check_play_button_mouse_click(ai_settings, screen, ship, shipbullets, helis, helibullets, stats, play_button, sb, mouse_x, mouse_y)
	
	
	mouse_work_time = float('{:.1f}'.format(ai_settings.mouse_start_time_click + ai_settings.mouse_starttime_nowork_interval))
	#print("Work time: " + str(mouse_work_time))
	mouse_time_new = float('{:.1f}'.format(get_process_time()))
	#print("Time new: " + str(mouse_time_new))
	
	if mouse_time_new >= mouse_work_time:
		ai_settings.mouse_working = True
	
	if ai_settings.mouse_working:
		# Sets ship firing mode to true if game is active and mouse button is down.
		if event.type == pygame.MOUSEBUTTONDOWN and stats.game_active:
			ai_settings.shipbullets_constant_firing = True
		# Sets ship firing mode to false if game is active and mouse button is up.
		if event.type == pygame.MOUSEBUTTONUP and stats.game_active:
			ai_settings.shipbullets_constant_firing = False
		# Adds x, y values to ship rect coordinates if there is a mouse motion
		# to simulate mouse controlling the ship.
		if event.type == pygame.MOUSEMOTION and stats.game_active:
			mouse_x, mouse_y = pygame.mouse.get_rel()
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
			# Up
			elif mouse_y < 0 and ship.rect.top > ship.sb.topbracket_rect.bottom:
				ship.centery += mouse_y
			# Left
			elif mouse_x < 0 and ship.rect.left > 0:
				ship.centerx += mouse_x
			# Down
			elif mouse_y > 0 and ship.rect.bottom < ship.screen_rect.bottom:
				ship.centery += mouse_y
			# Right
			elif mouse_x > 0 and ship.rect.right < ship.screen_rect.right:
				ship.centerx += mouse_x
			
		
	
def check_play_button_mouse_click(ai_settings, screen, ship, shipbullets, helis, helibullets, stats, play_button, sb, mouse_x, mouse_y):
	"""Starts the game when the button is clicked within the play_button."""
	# Gives a True if mouse coordinates is in play_button.rect.
	button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
	if button_clicked and not stats.game_active:
		start_game(ai_settings, screen, ship, shipbullets, helis, helibullets, stats, sb)
		
		
def start_game(ai_settings, screen, ship, shipbullets, helis, helibullets, stats, sb):
	"""Starts a new game, reset settings, remove projectiles and objects, start new wave, center ship, etc."""
	# Loads high score from json file.
	sb.loads_highscore_from_json()
	
	# Sets game_active to True and reset statistics.
	stats.game_active = True
	stats.reset_stats()
	
	# Remove projectiles and objects from previous iteration of the game.
	shipbullets.remove()
	helis.remove()
	helibullets.remove()
	
	# Creates a new wave of objects/hostiles.
	create_wave_helicopter(ai_settings, screen, helis)
	ship.center_ship()
	
	# Set mouse visibility to false and grab to true.
	pygame.mouse.set_visible(False)
	pygame.event.set_grab(True)
	# Set the default coordinates of the mouse in game.
	pygame.mouse.set_pos([ship.rect.centerx, ship.rect.centery])
	# Set mouse working to false and get mouse_start_time_click to 
	# set it back to True.
	mouse_working = False
	ai_settings.mouse_start_time_click = float('{:.1f}'.format(get_process_time()))
	
	










def create_wave_helicopter(ai_settings, screen, helis):
	"""Spawns a new wave of helicopters."""
	# Sets helicopter limit to 10.
	helicopter_wave_limit = 10
	# Adds and creates helicopter depending on the wave limit.
	for heli in range(helicopter_wave_limit):
		create_helicopter(ai_settings, screen, helis)
	
def get_helicopter_x(ai_settings):
	"""Returns a x coordinate from the specified values."""
	random_x = randint((ai_settings.screen_width + 100), (ai_settings.screen_width + 2000))
	return random_x
	
def get_helicopter_y(ai_settings):
	"""Returns a y coordinate from the specified values."""
	# 58 is because of the top bracket.
	# Screen_height - 50 is so that it spawns more naturally.
	random_y = randint(58, (ai_settings.screen_height - 50))
	return random_y
	
def create_helicopter(ai_settings, screen, helis):
	"""Specify the correct coordinates for the individual helicotpers to 
	spawn and Adds the helicopter into the list(helis)."""
	new_heli = Helicopter(ai_settings, screen)
	
	new_heli.centerx = get_helicopter_x(ai_settings)
	new_heli.centery = get_helicopter_y(ai_settings)
	
	new_heli.rect.centerx = new_heli.centerx
	new_heli.rect.centery = new_heli.centery
	
	helis.add(new_heli)
	
	# These methods of assigning does not work.
	# Because these values are not updated in helis.update()
	# We will need to use the float values made in hostile146 to do it.
	# Unless we assign the variables below to hostile146 for updates.
	# The above is just a theory.
	
	#heli_x = get_helicopter_x(ai_settings)
	#heli_y = get_helicopter_y(ai_settings)
	
	#new_heli.rect.x = heli_x
	#new_heli.rect.y = heli_y




















	
	
def update_screen(ai_settings, screen, ship, shipbullets, helis, helibullets, stats, play_button, sb):
	screen.fill(ai_settings.bg_color)
	
	ship.blitme()
	shipbullets.draw(screen)
	helis.draw(screen)
	helibullets.draw(screen)
	
	if not stats.game_active:
		play_button.draw_button()
		pygame.mouse.set_visible(True)
		
	sb.show_score()
	
	pygame.display.flip()
	
	
	













	
def update_internals(ai_settings, screen, ship, shipbullets, helis, helibullets, stats, sb):
	ship.update()
	update_shipbullet_internals(ai_settings, screen, ship, shipbullets, helis, stats)
	update_heli_internals(ai_settings, screen, ship, helis, helibullets, stats, sb)
	update_score(stats, sb)
	



def fire_ship_bullet_internals(ai_settings, screen, ship, shipbullets):
	shipbullet_time_for_2nd_fire = float('{:.1f}'.format(ai_settings.shipbullet_time_fire + ai_settings.shipbullet_time_fire_interval))
	#print("Time for 2nd fire: " + str(shipbullet_time_for_2nd_fire)) 
	shipbullet_time_new = float('{:.1f}'.format(get_process_time()))
	#print("Time new: " + str(shipbullet_time_new))
	#print(len(shipbullets))
	if ai_settings.shipbullets_constant_firing:
		if len(shipbullets) < ai_settings.shipbullets_allowed and shipbullet_time_new >= shipbullet_time_for_2nd_fire:
			ai_settings.shipbullet_time_fire = float('{:.1f}'.format(get_process_time()))
			new_bullet = ShipBullet(ai_settings, screen, ship)
			shipbullets.add(new_bullet)
	
	
def update_shipbullet_internals(ai_settings, screen, ship, shipbullets, helis, stats):
	fire_ship_bullet_internals(ai_settings, screen, ship, shipbullets)
	shipbullets.update()
	screen_rect = screen.get_rect()
	
	for bullet in shipbullets.copy():
		if bullet.rect.left >= screen_rect.right:
			shipbullets.remove(bullet)
			
	check_hostile_shipprojectile_collision(ai_settings, shipbullets, helis, stats)
	
	
def check_hostile_shipprojectile_collision(ai_settings, shipbullets, helis, stats):
	helicopter_shipbullet_collisions = pygame.sprite.groupcollide(shipbullets, helis, True, True)
	
	if helicopter_shipbullet_collisions:
		for helis in helicopter_shipbullet_collisions.values():
			stats.score += ai_settings.helicopter_points








	
def update_heli_internals(ai_settings, screen, ship, helis, helibullets, stats, sb):
	helis.update()
	screen_rect = screen.get_rect()
	
	for heli in helis.copy():
		if heli.rect.right <= screen_rect.left:
			helis.remove(heli)
	
	update_heli_bullet_internals(ai_settings, screen, ship, helis, helibullets, stats, sb)
	
	if len(helis) == 0:
		create_wave_helicopter(ai_settings, screen, helis)
		stats.level += 1
	
	
def update_heli_bullet_internals(ai_settings, screen, ship, helis, helibullets, stats, sb):
	helibullets.update()
	fire_heli_bullets(ai_settings, screen, ship, helis, helibullets)
	
	screen_rect = screen.get_rect()
	for bullet in helibullets.copy():
		if bullet.rect.right <= screen_rect.left:
			helibullets.remove(bullet)
			
	check_ship_hostileobject_collision(ai_settings, ship, helis, stats, sb)
	check_ship_hostileprojectile_collision(ai_settings, ship, helibullets, stats, sb)
	
def check_ship_hostileobject_collision(ai_settings, ship, helis, stats, sb):
	ship_rect = ship.rect
	for heli in helis.sprites():
		heli_overlap_ship = ship_rect.colliderect(heli)
		if heli_overlap_ship and not ship.immunity:
			ai_settings.ship_time_hit = float('{:.1f}'.format((get_process_time())))
			ship_hit(ai_settings, ship, stats, sb)
			helis.remove(heli)
	
	
def check_ship_hostileprojectile_collision(ai_settings, ship, helibullets, stats, sb):
	# Possibility 1 (Doesn't work)
	"""
	if not ship.immunity:
		ship_helicopterbullet_collisions = pygame.sprite.groupcollide(helibullets, ship, True, True)
		
	if ship_helicopterbullet_collisions:
		#time_hit = int(get_process_time())
		ship_hit(ai_settings, ship, stats)
	"""
	# Possibility 2

	ship_rect = ship.rect
	for helibullet in helibullets.sprites():
		helicopterbullet_inside_ship = ship_rect.contains(helibullet)
		if helicopterbullet_inside_ship and not ship.immunity:
			ai_settings.ship_time_hit = float('{:.1f}'.format((get_process_time())))
			ship_hit(ai_settings, ship, stats, sb)
			helibullets.remove(helibullet)
			

	# Possibility 3 (Not suitable as it can't track individual helibullets)
	"""
	if pygame.sprite.spritecollideany(ship, helibullets) and not ship.immunity:
		ai_settings.ship_time_hit = float('{:.1f}'.format((get_process_time())))
		#print("Time Hit: " + str(ai_settings.ship_time_hit))
		ship_hit(ai_settings, ship, stats, sb)
	"""
		
	check_immunity(ai_settings, ship)
		
		
def ship_hit(ai_settings, ship, stats, sb):
	if stats.ship_left > 0:
		#sleep(2)
		
		ship.immunity = True
		
		stats.ship_left -= 1
		
		ship.center_ship()
		
		#print("Ship left: " + str(stats.ship_left))
	else:
		stats.game_active = False
		pygame.mouse.set_visible(True)
		pygame.event.set_grab(False)
		sb.dumps_highscore_to_json()
		
		
def check_immunity(ai_settings, ship):
	ship_time_no_immune = float('{:.1f}'.format((ai_settings.ship_time_hit + ai_settings.ship_time_immune)))
	#print("Time no immune: " + str(time_no_immune))
	ship_time_new = float('{:.1f}'.format(get_process_time()))
	#print("Time current: " + str(time_new))
	if ship_time_new == ship_time_no_immune:
		ship.immunity = False
		#print("Immunity set to False")
	
	
def get_process_time():
	process_time = time.process_time()
	return process_time








def update_score(stats, sb):
	"""Update and shows the score."""
	#print("Current score: " + str(stats.score))
	#print("High score: " + str(stats.high_score))
	
	# Equate high score and score if score is greater than high score.
	if stats.score > stats.high_score:
		stats.high_score = stats.score

	# Updates the scoreboard with new statistics.
	sb.prep_score()
	sb.prep_high_score()
	sb.prep_level()
	sb.prep_ships()






























	
def fire_heli_bullets(ai_settings, screen, ship, helis, helibullets):
	"""Creates, assign, add and fire a new heli bullet upon meeting the 
	conditions of fire."""
	# Test if heli rect is inside the screen, if so,
	# create bullets at designated x.
	screen_rect = screen.get_rect()
	ship_rect = ship.rect
	for heli in helis.sprites():
		heli_inside_screen = screen_rect.contains(heli)
		heli_centery_in_ship = ship_rect.collidepoint(ship_rect.centerx , heli.rect.centery)
		heli_bullet_x_1 = get_heli_bullet_x_1(ai_settings)
		if heli_inside_screen:
			if heli.rect.x == heli_bullet_x_1 and heli_centery_in_ship:# and ship.rect.centery == heli.rect.centery:
				create_heli_bullet(ai_settings, screen, heli, helibullets, heli_bullet_x_1)
	
	
def create_heli_bullet(ai_settings, screen, heli, helibullets, heli_bullet_x_1):
	"""Creates a new bullet, assign it the x coordinate for which it will
	start firing at and adds it to the list(helibullets)."""
	new_heli_bullet = HelicopterBullet(ai_settings, screen, heli)
	# Extracts the x coordinate from get_heli_bullet_x_1 and assigns it to
	# each individual new heli bullet.
	new_heli_bullet.x = heli_bullet_x_1
	new_heli_bullet.rect.x = new_heli_bullet.x
	helibullets.add(new_heli_bullet)
	
	
def get_heli_bullet_x_1(ai_settings):
	"""Returns a x coordinate for the helibullet to start fire at."""
	random_x = randint(0, ai_settings.screen_width)
	return random_x
	




























