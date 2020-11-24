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

def my_round(num, block_size, offset):
	return int(block_size * math.floor((num) / block_size))

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

	hover_block_x = my_round(pg.mouse.get_pos()[0], block_size, x_offset)
	hover_block_y = my_round(pg.mouse.get_pos()[1], block_size, y_offset)

	for y in range(len(game_map)):
		for x in range(len(game_map[y])):

			if game_map[y][x] == '3':
				display.blit(grass_block, (x * block_size + x_offset, y * block_size + y_offset))

			elif game_map[y][x] == '2':
				display.blit(dirt_block, (x * block_size + x_offset, y * block_size + y_offset))

			elif game_map[y][x] == '1':
				display.blit(stone_block, (x * block_size + x_offset, y * block_size + y_offset))

			elif game_map[y][x] == 'b':
				display.blit(border_block, (x * block_size + x_offset, y * block_size + y_offset))

	try:
		if game_map[int((hover_block_y - y_offset) / block_size)][int((hover_block_x - x_offset) / block_size)] != 'b':
			if del_block:
				game_map[int((hover_block_y - y_offset) / block_size)][int((hover_block_x - x_offset) / block_size)] = '0'
			elif clicking:
				game_map[int((hover_block_y - y_offset) / block_size)][int((hover_block_x - x_offset) / block_size)] = num
	except IndexError: 
		pass

	if not del_block:
		display.blit(pg.transform.scale(selected_block, (block_size, block_size)), (hover_block_x, hover_block_y))

	if up:
		y_offset += block_size
	if down:
		y_offset -= block_size
	if left:
		x_offset += block_size
	if right:
		x_offset -= block_size

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
						x_offset -= block_size*2
						y_offset -= block_size*2
				else:
					up = True
			if event.key == pg.K_DOWN:
				keys = pg.key.get_pressed()
				if keys[pg.K_LSHIFT]:
					if block_size - 16 != 0:
						block_size -= 16
						x_offset += block_size/2
						y_offset += block_size/2
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

file_name = 'map_file'

map_file = open('assets/maps/' + file_name + '.txt', 'w')
for y in range(20):
	for x in range(100):
		map_file.write(game_map[y][x])
	map_file.write('\n')
map_file.close()

pg.display.quit()
pg.quit()