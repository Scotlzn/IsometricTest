import pygame, sys, math

pygame.init()
WINDOW_SIZE = (800, 800)
DISPLAY_SIZE = (200, 200)
screen = pygame.display.set_mode(WINDOW_SIZE)
display = pygame.surface.Surface(DISPLAY_SIZE)
clock = pygame.time.Clock()

TITLE = "Isometric Test "
UPSCALE = WINDOW_SIZE[0] / DISPLAY_SIZE[0]
WIDTH, HEIGHT = 16, 8

origin_x = DISPLAY_SIZE[0] * 0.5
origin_y = 0

scroll = [0, 0]
direction = {'up': False, 'left': False, 'down': False, 'right': False}
speed = 100

def fix_mouse(mpos):
	x = math.floor(mpos[0] / UPSCALE)
	y = math.floor(mpos[1] / UPSCALE)
	return x, y

def convert_to_isometric(x, y):
	WIDTH, HEIGHT = 32, 32
	new_x = (x * 0.5 * WIDTH + y * -0.5 * WIDTH) + (origin_x - WIDTH * 0.5)
	new_y = (x * 0.25 * HEIGHT + y * 0.25 * HEIGHT)
	return new_x, new_y

def convert_to_grid(screen_x, screen_y):
	x = round(((screen_y - origin_y) / HEIGHT + (screen_x - origin_x) / WIDTH) / 2)
	y = round(((screen_y - origin_y) / HEIGHT - (screen_x - origin_x) / WIDTH) / 2)
	return x, y

tile_img = pygame.image.load('tile.png').convert()
tile_img.set_colorkey((27, 27, 27))

while True:

	dt = clock.tick(60) * .001

	display.fill('#5D3FD3')
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_w:
				direction['up'] = True
			if event.key == pygame.K_a:
				direction['left'] = True
			if event.key == pygame.K_s:
				direction['down'] = True
			if event.key == pygame.K_d:
				direction['right'] = True
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_w:
				direction['up'] = False
			if event.key == pygame.K_a:
				direction['left'] = False
			if event.key == pygame.K_s:
				direction['down'] = False
			if event.key == pygame.K_d:
				direction['right'] = False

	if direction['up']:
		scroll[1] += -speed * dt
	if direction['down']:
		scroll[1] += speed * dt
	if direction['left']:
		scroll[0] += -speed * dt
	if direction['right']:
		scroll[0] += speed * dt

	scroll[0] = round(scroll[0])
	scroll[1] = round(scroll[1])
	#print(scroll, dt)

	mouse_pos = fix_mouse(pygame.mouse.get_pos())

	rx, ry = convert_to_grid(mouse_pos[0] + scroll[0], mouse_pos[1] + scroll[1])
	selected_tile = (rx, ry)

	for y in range(8):
		for x in range(8):
			pos = convert_to_isometric(x, y)
			if (x, y) != selected_tile:
				display.blit(tile_img, (pos[0] - scroll[0], pos[1] - scroll[1]))
			else:
				display.blit(tile_img, (pos[0] - scroll[0], pos[1] - scroll[1] - 4))

	pygame.display.set_caption(TITLE + str(clock.get_fps()))
	surf = pygame.transform.scale(display, WINDOW_SIZE)
	screen.blit(surf, (0, 0))
	pygame.display.update()
