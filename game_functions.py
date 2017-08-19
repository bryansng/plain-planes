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
		
	
def check_play_button_mouse_click(ai_settings, screen, ship, shipbullets, helis, helibullets, stats, play_button, sb, mouse_x, mouse_y):
	"""Starts the game when the button is clicked within the play_button."""
	# Gives a True if mouse coordinates is in play_button.rect.
	button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
	if button_clicked:
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
	"""Specify the correct coordinates for the individual helicopters to 
	spawn and Adds the new helicopter into the list(helis)."""
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
	"""Updates the screen with new data from update_internals 
	and check_events in one iteration of them."""
	# Fill the screen with the color specified in ai_settings.
	screen.fill(ai_settings.bg_color)
	
	# Draws all the projectiles and objects.
	ship.blitme()
	shipbullets.draw(screen)
	helis.draw(screen)
	helibullets.draw(screen)
	
	# If game is not active, draw the play_button.
	if not stats.game_active:
		play_button.draw_button()
	
	# Draws all the scoreboard details onto the screen.
	sb.show_score()
	
	# Updates the contents of the entire display.
	pygame.display.flip()
	
	
	













	
def update_internals(ai_settings, screen, ship, shipbullets, helis, helibullets, stats, sb):
	"""Update the internals of the objects and projectiles."""
	# Update internals of ship from its class file.
	# Specifically, its movements.
	ship.update()
	# Update internals of shipbullets.
	update_shipbullet_internals(ai_settings, screen, ship, shipbullets, helis, stats)
	# Update internals of helis together with helibullets.
	update_heli_internals(ai_settings, screen, ship, helis, helibullets, stats, sb)
	# Update internals of sb/Scoreboard.
	update_score(stats, sb)
	



def fire_ship_bullet_internals(ai_settings, screen, ship, shipbullets):
	"""Gets time to fire between shots, creates shipbullet, adds and fire them on that time"""
	# Collects the ship_time_fire and adds the time interval for the 2nd shot.
	shipbullet_time_for_2nd_fire = float('{:.1f}'.format(ai_settings.shipbullet_time_fire + ai_settings.shipbullet_time_fire_interval))
	# Gets the current time in game.
	shipbullet_time_new = float('{:.1f}'.format(get_process_time()))
	# Spacebar or Mousebuttondown, constant_firing is set to True.
	# After that, if the bullet is less than the limit allowed and
	# time_new is greater than time_for_2nd_fire,
	# a bullet is created, added and fired.
	if ai_settings.shipbullets_constant_firing:
		if len(shipbullets) < ai_settings.shipbullets_allowed and shipbullet_time_new >= shipbullet_time_for_2nd_fire:
			ai_settings.shipbullet_time_fire = float('{:.1f}'.format(get_process_time()))
			new_bullet = ShipBullet(ai_settings, screen, ship)
			shipbullets.add(new_bullet)
	
	
def update_shipbullet_internals(ai_settings, screen, ship, shipbullets, helis, stats):
	"""Updates and handles whatever happens to shipbullet."""
	# Create, add, and fires bullet based on specified conditions.
	fire_ship_bullet_internals(ai_settings, screen, ship, shipbullets)
	# Updates internals of shipbullets in its class file.
	# Specifically, its movements.
	shipbullets.update()
	# Get screen rect.
	screen_rect = screen.get_rect()
	
	# Removes the bullets if rect.left passes the screen_rect.right.
	for bullet in shipbullets.copy():
		if bullet.rect.left >= screen_rect.right:
			shipbullets.remove(bullet)
			
	# Handles what happen if hostile and ship projectiles collides.
	check_hostile_shipprojectile_collision(ai_settings, shipbullets, helis, stats)
	
	
def check_hostile_shipprojectile_collision(ai_settings, shipbullets, helis, stats):
	"""Removes the shipbullets and the helis that collide with each other.
	Adds the score for destroying the hostile object."""
	# Removes the shipbullet and heli that collides.
	helicopter_shipbullet_collisions = pygame.sprite.groupcollide(shipbullets, helis, True, True)
	# If there is a collision, loop through the collided objects/helis and add
	# based on each individual collision.
	# NOTE: This is optimized to be very exact.
	if helicopter_shipbullet_collisions:
		for helis in helicopter_shipbullet_collisions.values():
			stats.score += ai_settings.helicopter_points








	
def update_heli_internals(ai_settings, screen, ship, helis, helibullets, stats, sb):
	"""Updates and handles whatever that happens to heli and helibullet."""
	# Update internals of heli from its class file.
	# Specifically, its movements.
	helis.update()
	# Get screen rect.
	screen_rect = screen.get_rect()
	
	# Removes heli once they reach the left side of the screen.
	for heli in helis.copy():
		if heli.rect.right <= screen_rect.left:
			helis.remove(heli)
	
	# Updates internals of helibullets.
	update_heli_bullet_internals(ai_settings, screen, ship, helis, helibullets, stats, sb)
	
	# NOTE: This is temporary
	# Creates a new wave when it detects the number of helis is zero.
	# Also increases the level by 1.
	if len(helis) == 0:
		create_wave_helicopter(ai_settings, screen, helis)
		stats.level += 1
	
	# Handles what happens if the hostileobject and ship collides.
	check_ship_hostileobject_collision(ai_settings, ship, helis, stats, sb)
	
	
def check_ship_hostileobject_collision(ai_settings, ship, helis, stats, sb):
	"""
	tldr: heli removed, ship removed, immunity counter runs if conditions met.
	
	Sets condition for how ship collide with heli, based on colliderect.
	If they overlap and immunity is false, heli that collided is removed, ship is removed and time_hit for immunity is set.
	"""
	# Get ship rect.
	ship_rect = ship.rect
	for heli in helis.sprites():
		# Boolean for collision or overlapping of rect between ship and heli.
		heli_overlap_ship = ship_rect.colliderect(heli)
		# If overlap and immunity false, heli and ship is removed, immunity 
		# counter starts.
		if heli_overlap_ship and not ship.immunity:
			# Gets the time_hit for immunity counter.
			ai_settings.ship_time_hit = float('{:.1f}'.format((get_process_time())))
			# Runs the method ship_hit for what will happen to the ship.
			ship_hit(ai_settings, ship, stats, sb)
			# Removes that particular heli in helis.
			helis.remove(heli)
	
	
def update_heli_bullet_internals(ai_settings, screen, ship, helis, helibullets, stats, sb):
	"""Updates and handles whatever that happens to helibullet."""
	# Update internals of helibullet from its class file.
	# Specifically, its movements.
	helibullets.update()
	
	# Creates, assign, add and fire a new heli bullet upon meeting the 
	# conditions of fire.
	fire_heli_bullets(ai_settings, screen, ship, helis, helibullets)
	
	# Get screen rect.
	screen_rect = screen.get_rect()
	# Removes the helibullets that leaves the left side of the screen.
	for bullet in helibullets.copy():
		if bullet.rect.right <= screen_rect.left:
			helibullets.remove(bullet)
			
	# Handles what happens if the hostileprojectile and ship collides.
	check_ship_hostileprojectile_collision(ai_settings, ship, helibullets, stats, sb)
	
	
def check_ship_hostileprojectile_collision(ai_settings, ship, helibullets, stats, sb):
	"""
	Based on Possibility 2,
	tldr: helibullet removed, ship removed, immunity counter runs if conditions 
	met.
	
	For each individual projectile in the sprite, if ship_rect contains that
	projectile, objectprojectile_inside_ship is set to True.
	
	If that is true and ship immunity is false,
	time_hit for immunity counter is set, ship_hit runs, helibullet is removed.
	"""
	
	# Possibility 1 (Works best because you can remove helibullets individually)
	
	# Get ship rect.
	ship_rect = ship.rect
	for helibullet in helibullets.sprites():
		# True if ship_rect contains the specific helibullet in the sprite.
		helicopterbullet_inside_ship = ship_rect.contains(helibullet)
		# If True and ship_immunity false, helibullet and ship is removed, immunity counter starts.
		if helicopterbullet_inside_ship and not ship.immunity:
			# Gets the time_hit for immunity counter.
			ai_settings.ship_time_hit = float('{:.1f}'.format((get_process_time())))
			# Runs the method ship_hit for what will happen to the ship.
			ship_hit(ai_settings, ship, stats, sb)
			# Removes that particular heli in helis.
			helibullets.remove(helibullet)
			
	# Check and handles the immunity and immunity counter.
	check_immunity(ai_settings, ship)
	
	# Possibility 2 (Doesn't work, because ship is not a sprite group)
	"""
	if not ship.immunity:
		ship_helicopterbullet_collisions = pygame.sprite.groupcollide(helibullets, ship, True, True)
		
	if ship_helicopterbullet_collisions:
		#time_hit = int(get_process_time())
		ship_hit(ai_settings, ship, stats)
	"""

	# Possibility 3 (Not suitable as it can't track individual helibullets)
	"""
	if pygame.sprite.spritecollideany(ship, helibullets) and not ship.immunity:
		ai_settings.ship_time_hit = float('{:.1f}'.format((get_process_time())))
		#print("Time Hit: " + str(ai_settings.ship_time_hit))
		ship_hit(ai_settings, ship, stats, sb)
	"""
	
		
def ship_hit(ai_settings, ship, stats, sb):
	"""Continues if there are still ships left, else, end game."""
	# If there are still ships left, immunity set to true for immunity counter,
	# ships left decreased by 1, and ship is centered.
	if stats.ship_left > 0:
		ship.immunity = True
		stats.ship_left -= 1
		ship.center_ship()
	# Else, game_active set to False, mouse set to visible again,
	# set_grab set to False
	# High score is dumped to json file so that upon clicking the statistics 
	# button, the statistics will be updated with the new high score that is 
	# newly acquired/achieved.
	else:
		stats.game_active = False
		pygame.mouse.set_visible(True)
		pygame.event.set_grab(False)
		sb.dumps_highscore_to_json()
		
		
def check_immunity(ai_settings, ship):
	"""Sets the ship immunity to false once the time of immunity is over."""
	# Extracts the ship_time_hit and adds the time_immune to it to get the
	# time_no_immune.
	# Also, gets the process time indefinitely.
	# NOTE: The time_no_immune can be optimized to run just once.
	ship_time_no_immune = float('{:.1f}'.format((ai_settings.ship_time_hit + ai_settings.ship_time_immune)))
	ship_time_new = float('{:.1f}'.format(get_process_time()))
	# If time_new equate time_no_immune, ship immunity is set to false.
	if ship_time_new == ship_time_no_immune:
		ship.immunity = False
		#print("Immunity set to False")
	
	
def get_process_time():
	# Returns the process time at the time of request or call of this method.
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
	# Get screen_rect and ship_rect for later.
	screen_rect = screen.get_rect()
	ship_rect = ship.rect
	for heli in helis.sprites():
		# Boolean return if screen_rect contains heli.
		heli_inside_screen = screen_rect.contains(heli)
		# Boolean return if the points ship_rect.centerx and heli.rect_centery
		# are in the ship_rect.
		# ship_rect.centerx will always be true since it follows the ship.
		# heli_rect.centery will be true if the ship moves into the heli's y,
		# since the y of the heli is always fixed, the condition for it to be
		# true would be if the ship moved into heli's y.
		heli_centery_in_ship = ship_rect.collidepoint(ship_rect.centerx , heli.rect.centery)
		# Get the x coordinate for which the bullet will start firing.
		heli_bullet_x_1 = get_heli_bullet_x_1(ai_settings)
		# If heli inside screen, followed after by if the heli.rect.x reach
		# the x for firing and if the ship is within heli's line of sight,
		# helibullets are created, added and fired.
		if heli_inside_screen:
			if heli.rect.x == heli_bullet_x_1 and heli_centery_in_ship:
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
	




























