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

def check_keydown_events(event, ai_settings, screen, ship, shipbullets, helis, helibullets, stats):
	if event.key == pygame.K_q:
		sys.exit()
	if event.key == pygame.K_p:
		start_game(ai_settings, screen, ship, shipbullets, helis, helibullets, stats)
	if event.key == pygame.K_w or event.key == pygame.K_UP:
		ship.moving_up = True
	if event.key == pygame.K_a or event.key == pygame.K_LEFT:
		ship.moving_left = True
	if event.key == pygame.K_s or event.key == pygame.K_DOWN:
		ship.moving_down = True
	if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
		ship.moving_right = True
	if event.key == pygame.K_SPACE:
		ai_settings.shipbullet_time_fire = float('{:.1f}'.format(get_process_time()))
		ai_settings.shipbullets_constant_firing = True
		#fire_ship_bullet(ai_settings, screen, ship, shipbullets)
		
	
def check_keyup_events(event, ai_settings, ship, shipbullets):
	if event.key == pygame.K_w or event.key == pygame.K_UP:
		ship.moving_up = False
	if event.key == pygame.K_a or event.key == pygame.K_LEFT:
		ship.moving_left = False
	if event.key == pygame.K_s or event.key == pygame.K_DOWN:
		ship.moving_down = False
	if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
		ship.moving_right = False
	if event.key == pygame.K_SPACE:
		ai_settings.shipbullets_constant_firing = False
		
		
def check_events(ai_settings, screen, ship, shipbullets, helis, helibullets, stats, play_button):
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		if event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x, mouse_y = pygame.mouse.get_pos()
			check_play_button_mouse_click(ai_settings, screen, ship, shipbullets, helis, helibullets, stats, play_button, mouse_x, mouse_y)
		if event.type == pygame.KEYDOWN:
			check_keydown_events(event, ai_settings, screen, ship, shipbullets, helis, helibullets, stats)
		if event.type == pygame.KEYUP:
			check_keyup_events(event, ai_settings, ship, shipbullets)
	
def check_play_button_mouse_click(ai_settings, screen, ship, shipbullets, helis, helibullets, stats, play_button, mouse_x, mouse_y):
	button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
	if button_clicked and not stats.game_active:
		start_game(ai_settings, screen, ship, shipbullets, helis, helibullets, stats)
		
		
def start_game(ai_settings, screen, ship, shipbullets, helis, helibullets, stats):
	stats.game_active = True
	stats.reset_stats()
	
	shipbullets.remove()
	helis.remove()
	helibullets.remove()
	
	create_wave_helicopter(ai_settings, screen, helis)
	ship.center_ship()
	
	pygame.mouse.set_visible(False)
	










def create_wave_helicopter(ai_settings, screen, helis):
	wave_limit = 10
	for heli in range(wave_limit):
		create_helicopter(ai_settings, screen, helis)
	
def get_helicopter_x(ai_settings):
	random_x = randint((ai_settings.screen_width + 100), (ai_settings.screen_width + 2000))
	return random_x
	
def get_helicopter_y(ai_settings):
	random_y = randint(50, (ai_settings.screen_height - 50))
	return random_y
	
def create_helicopter(ai_settings, screen, helis):
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
	update_heli_internals(ai_settings, screen, ship, helis, helibullets, stats)
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








	
def update_heli_internals(ai_settings, screen, ship, helis, helibullets, stats):
	helis.update()
	screen_rect = screen.get_rect()
	
	for heli in helis.copy():
		if heli.rect.right <= screen_rect.left:
			helis.remove(heli)
	
	update_heli_bullet_internals(ai_settings, screen, ship, helis, helibullets, stats)
	
	if len(helis) == 0:
		create_wave_helicopter(ai_settings, screen, helis)
		stats.level += 1
	
	
def update_heli_bullet_internals(ai_settings, screen, ship, helis, helibullets, stats):
	helibullets.update()
	fire_heli_bullets(ai_settings, screen, ship, helis, helibullets)
	
	screen_rect = screen.get_rect()
	for bullet in helibullets.copy():
		if bullet.rect.right <= screen_rect.left:
			helibullets.remove(bullet)
			
	check_ship_hostileprojectile_collision(ai_settings, ship, helibullets, stats)
	
	
def check_ship_hostileprojectile_collision(ai_settings, ship, helibullets, stats):
	# Possibility 1 (Doesn't work)
	"""
	if not ship.immunity:
		ship_helicopterbullet_collisions = pygame.sprite.groupcollide(helibullets, ship, True, True)
		
	if ship_helicopterbullet_collisions:
		#time_hit = int(get_process_time())
		ship_hit(ai_settings, ship, stats)
	"""
	# Possibility 2
	"""
	ship_rect = ship.rect
	for helibullet in helibullets.sprites():
		helicopterbullet_inside_ship = ship_rect.contains(helibullet)
		if helicopterbullet_inside_ship:# and not ship.immunity:
			time_hit = int(get_process_time())
			ship_hit(ai_settings, ship, stats, time_hit)
			
	"""
	# Possibility 3
	
	if pygame.sprite.spritecollideany(ship, helibullets) and not ship.immunity:
		ai_settings.ship_time_hit = float('{:.1f}'.format((get_process_time())))
		#print("Time Hit: " + str(ai_settings.ship_time_hit))
		ship_hit(ai_settings, ship, stats)
		
	check_immunity(ai_settings, ship)
		
		
def ship_hit(ai_settings, ship, stats):
	if stats.ship_left > 0:
		#sleep(2)
		
		ship.immunity = True
		
		stats.ship_left -= 1
		
		ship.center_ship()
		
		#print("Ship left: " + str(stats.ship_left))
	else:
		stats.game_active = False
		pygame.mouse.set_visible(True)
		
		
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
	#print("Current score: " + str(stats.score))
	#print("High score: " + str(stats.high_score))
	if stats.score > stats.high_score:
		stats.high_score = stats.score
		
	sb.prep_score()
	sb.prep_high_score()
	sb.prep_level()
	sb.prep_ships()






























	
def fire_heli_bullets(ai_settings, screen, ship, helis, helibullets):
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
	new_heli_bullet = HelicopterBullet(ai_settings, screen, heli)
	new_heli_bullet.x = heli_bullet_x_1
	new_heli_bullet.rect.x = new_heli_bullet.x
	helibullets.add(new_heli_bullet)
	#helibullets.add(new_heli_bullet)
	
	
def get_heli_bullet_x_1(ai_settings):
	random_x = randint(0, ai_settings.screen_width)
	return random_x
	
	
def get_heli_bullet_x_2(ai_settings):
	random_x = randint(0, ai_settings.screen_width)
	return random_x
	




























