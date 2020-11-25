import pygame as pg, math

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

grass = pg.image.load('assets/pictures/grass.png')
dirt = pg.image.load('assets/pictures/dirt.png')
stone = pg.image.load('assets/pictures/stone.png')
border = pg.image.load('assets/pictures/border.png')

selected = 'grass'
selected_block = grass

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

def pixel_to_grid(px, py, block_size, x_offset, y_offset):
    return px // block_size + x_offset, py // block_size + y_offset

def grid_to_pixel(gx, gy, block_size, x_offset, y_offset):
    return (gx - x_offset) * block_size, (gy - y_offset) * block_size

running = True
while running:

	clock.tick(60)

	display.fill((0, 255, 255))

	grass_block = pg.transform.scale(grass, (block_size, block_size))
	dirt_block = pg.transform.scale(dirt, (block_size, block_size))
	stone_block = pg.transform.scale(stone, (block_size, block_size))
	border_block = pg.transform.scale(border, (block_size, block_size))

	if selected == 'grass':
		selected_block = grass_block
		num = '3'
	if selected == 'dirt':
		selected_block = dirt_block
		num = '2'
	if selected == 'stone':
		selected_block = stone_block
		num = '1'

	for y in range(len(game_map)):
		for x in range(len(game_map[y])):
			gx, gy = grid_to_pixel(x, y, block_size, x_offset, y_offset)
			if game_map[y][x] == '3':
				display.blit(grass_block, (gx, gy))

			elif game_map[y][x] == '2':
				display.blit(dirt_block, (gx, gy))

			elif game_map[y][x] == '1':
				display.blit(stone_block, (gx, gy))

			elif game_map[y][x] == 'b':
				display.blit(border_block, (gx, gy))

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
		display.blit(pg.transform.scale(selected_block, (block_size, block_size)), grid_to_pixel(hx, hy, block_size, x_offset, y_offset))

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
				selected = 'grass'
			if event.key == pg.K_2:
				selected = 'dirt'
			if event.key == pg.K_3:
				selected = 'stone'
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

make_map = input('Do you want to save this map? (y / n): ')

if make_map == 'y':
	map_name = input('What would you like to name it? ')
	map_name = map_name.replace(' ', '_')
	file_name = map_name

	map_file = open('assets/maps/' + file_name + '.txt', 'w')
	for y in range(20):
		for x in range(100):
			map_file.write(game_map[y][x])
		map_file.write('\n')
	map_file.close()

pg.quit()