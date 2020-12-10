import pygame as pg, math
pg.init()

def load_map_file(path):
	f = open(path, 'r')
	data = f.read()
	f.close()
	data = data.split('\n')
	game_map = []
	for row in data:
		game_map.append(list(row))
	return game_map, path

if input('Would you like to open a previously saved map? (y / n): ') == 'y':
	game_map, path = load_map_file('../assets/maps/' + str(input('What was it\'s name? ')) + '.txt')
	old_map = True
else:
	game_map = []
	for y in range(20):
		game_map_row = []
		for x in range(100):
			if y == 0 or y == 19:
				game_map_row.append('b')
			elif x == 0 or x == 99:
				game_map_row.append('b')
			else:
				game_map_row.append('0')
		game_map.append(game_map_row)
		old_map = False

display = pg.display.set_mode((0, 0), pg.FULLSCREEN)
pg.display.set_caption('Hopper Map Creator')

clock = pg.time.Clock()

zoom_in = False
zoom_out = False

up = False
down = False
left = False
right = False

clicking = False
del_block = False

block_size = 16

x_offset = 0
y_offset = 0

grass_block = pg.image.load('../assets/pictures/grass.png')
dirt_block = pg.image.load('../assets/pictures/dirt.png')
stone_block = pg.image.load('../assets/pictures/stone.png')
spike_block = pg.image.load('../assets/pictures/spike.png')
border_block = pg.image.load('../assets/pictures/border.png')
selector = pg.image.load('../assets/pictures/selector.png')

selected_block = grass_block

def pixel_to_grid(px, py, block_size, x_offset, y_offset):
    return px // block_size + x_offset, py // block_size + y_offset
def grid_to_pixel(gx, gy, block_size, x_offset, y_offset):
	return (gx - x_offset) * block_size, (gy - y_offset) * block_size
def scale_pic(image, block_size):
	return pg.transform.scale(image, (block_size, block_size))

running = True
while running:

	clock.tick(60)

	display.fill((0, 255, 255))

	if selected_block == grass_block:
		num = '3'
	if selected_block == dirt_block:
		num = '2'
	if selected_block == stone_block:
		num = '1'
	if selected_block == spike_block:
		num = 's'

	for y in range(len(game_map)):
		for x in range(len(game_map[y])):
			gx, gy = grid_to_pixel(x, y, block_size, x_offset, y_offset)
			if game_map[y][x] == '3':
				display.blit(scale_pic(grass_block, block_size), (gx, gy))
			elif game_map[y][x] == '2':
				display.blit(scale_pic(dirt_block, block_size), (gx, gy))
			elif game_map[y][x] == '1':
				display.blit(scale_pic(stone_block, block_size), (gx, gy))
			elif game_map[y][x] == 's':
				display.blit(scale_pic(spike_block, block_size), (gx, gy))
			elif game_map[y][x] == 'b':
				display.blit(scale_pic(border_block, block_size), (gx, gy))

	hx, hy = pixel_to_grid(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1], block_size, x_offset, y_offset)

	try:
		if game_map[hy][hx] != 'b':
			if del_block:
				game_map[hy][hx] = '0'
			elif clicking:
				game_map[hy][hx] = num
	except IndexError: 
		pass

	if not del_block:
		display.blit(scale_pic(selected_block, block_size), grid_to_pixel(hx, hy, block_size, x_offset, y_offset))
	display.blit(scale_pic(selector, block_size), grid_to_pixel(hx, hy, block_size, x_offset, y_offset))

	if up:
		y_offset -= 1
	if down:
		y_offset += 1
	if left:
		x_offset -= 1
	if right:
		x_offset += 1

	for event in pg.event.get():
		if event.type == pg.QUIT:
			running = False
		if event.type == pg.MOUSEBUTTONDOWN:
			if pg.mouse.get_pressed()[0]:
				clicking = True
			if pg.mouse.get_pressed()[2]:
				del_block = True
		if event.type == pg.MOUSEBUTTONUP:
			clicking = False
			del_block = False
		if event.type == pg.KEYDOWN:
			if event.key == pg.K_1:
				selected_block = grass_block
			if event.key == pg.K_2:
				selected_block = dirt_block
			if event.key == pg.K_3:
				selected_block = stone_block
			if event.key == pg.K_4:
				selected_block = spike_block
			if event.key == pg.K_UP:
				keys = pg.key.get_pressed()
				if keys[pg.K_LSHIFT]:
					if block_size + 16 != 80:
						block_size += 16
				else:
					up = True
			if event.key == pg.K_DOWN:
				keys = pg.key.get_pressed()
				if keys[pg.K_LSHIFT]:
					if block_size - 16 != 0:
						block_size -= 16
				else:
					down = True
			if event.key == pg.K_LEFT:
				left = True
			if event.key == pg.K_RIGHT:
				right = True

		if event.type == pg.KEYUP:
			if event.key == pg.K_UP:
				up = False
			if event.key == pg.K_DOWN:
				down = False
			if event.key == pg.K_LEFT:
				left = False
			if event.key == pg.K_RIGHT:
				right = False

	pg.display.update()

pg.display.quit()
pg.quit()

make_map = input('Do you want to save this map? (y / n): ')

if make_map == 'y':
	if not old_map:
		map_name = input('What would you like to name it? ')
		map_name = map_name.replace(' ', '_')
		file_name = map_name
		map_file = open('../assets/maps/' + file_name + '.txt', 'w')
	elif old_map:
		map_file = open(path, 'w')

	for y in range(20):
		for x in range(100):
			map_file.write(game_map[y][x])
		map_file.write('\n')
	map_file.close()