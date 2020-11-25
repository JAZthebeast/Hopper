import pygame as pg 
pg.init()

display = pg.display.set_mode((0, 0), pg.FULLSCREEN)
pg.display.set_caption('Hopper')

def load_map_file(path):
	f = open(path, 'r')
	data = f.read()
	f.close()
	data = data.split('\n')
	game_map = []
	for row in data:
		game_map.append(list(row))
	return game_map

game_map = load_map_file('assets/maps/grassyknoll.txt')

grass_block = pg.transform.scale(pg.image.load('assets/pictures/grass.png'), (64, 64))
dirt_block = pg.transform.scale(pg.image.load('assets/pictures/dirt.png'), (64, 64))
stone_block = pg.transform.scale(pg.image.load('assets/pictures/stone.png'), (64, 64))

player_idle = []
for i in range(2):
	player_idle.append(pg.transform.scale(pg.image.load('assets/animations/idle/idle_' + str(i) + '.png'), (64, 64)))

player_running = []
for i in range(2):
	player_running.append(pg.transform.scale(pg.image.load('assets/animations/running/running_' + str(i) + '.png'), (64, 64)))

player_crouch = pg.transform.scale(pg.image.load('assets/animations/crouch/crouch.png'), (64, 64))

player_pic = player_idle[0]

clock = pg.time.Clock()
frame = 0

block_size = 64	

float_scroll = [0, 0]

moving = [False, False]
facing = [False, True]
air_facing = [False, True]
crouch = False

ySpeed = 0
slow_speed = 1
air_time = 0
up_pressed = False

class Character_Sprite (pg.sprite.Sprite):
	def __init__(self, image, facing):
		super().__init__()
		self.picture = image
		self.image = self.picture
		self.rect = self.image.get_rect()
		self.facing = facing
	def update(self):
		if facing[0]:
			self.image = pg.transform.flip(self.picture, True, False)
		elif facing[1]:
			self.image = self.picture

def collision_test(player, blocks):
	collision_list = []
	for block in blocks:
		if player.colliderect(block):
			collision_list.append(block)
	return collision_list

def move(player, movement, blocks):
	collision_direction = {'left': False, 'right': False, 'top': False, 'bottom': False}

	player.x += movement[0]
	collision_list = collision_test(player, blocks)
	for block in collision_list:
		if movement[0] > 0:
			player.right = block.left
			collision_direction['right'] = True
		elif movement[0] < 0:
			player.left = block.right
			collision_direction['left'] = True

	player.y += movement[1]
	collision_list = collision_test(player, blocks)
	for block in collision_list:
		if movement[1] < 0:
			player.top = block.bottom
			collision_direction['top'] = True
		elif movement[1] > 0:
			player.bottom = block.top
			collision_direction['bottom'] = True
	return player, collision_direction

def animation(frame, animation_type, image, per_frames):
	for i in range(int(60 / per_frames)):
		if frame == per_frames * i:
			if image == animation_type[0]:
				image = animation_type[1]
				frame = frame
			elif image == animation_type[1]:
				image = animation_type[0]
				frame = frame
			else:
				image = animation_type[0]
				frame = 0
	return image, frame

bunny = Character_Sprite(player_pic, facing)
character_group = pg.sprite.Group()
character_group.add(bunny)

player_pos = pg.Rect(player_pic.get_rect())

starting_x = 128
player_pos.x = starting_x

running = True

while running:

	clock.tick(60)

	display.fill((0,255,255))

	float_scroll[0] += (player_pos.x - float_scroll[0] - 704) / 16
	float_scroll[1] += (player_pos.y - float_scroll[1] - 512) / 32
	scroll = float_scroll.copy()

	scroll[0] = int(float_scroll[0])
	scroll[1] = int(float_scroll[1])

	blocks = []
	for y in range(len(game_map)):
		for x in range(len(game_map[y])):

			if game_map[y][x] == '3':
				display.blit(grass_block, (x * block_size - scroll[0], y * block_size - scroll[1]))

			elif game_map[y][x] == '2':
				display.blit(dirt_block, (x * block_size - scroll[0], y * block_size - scroll[1]))

			elif game_map[y][x] == '1':
				display.blit(stone_block, (x * block_size - scroll[0], y * block_size - scroll[1]))

			if game_map[y][x] != '0' and game_map[y][x] != 'b':
				blocks.append(pg.Rect(x * block_size, y * block_size, block_size, block_size))

	player_movement = [0, 0]
	player_movement[1] += ySpeed
	if ySpeed < 16:
		ySpeed += .5
	if air_time < 5:
		slow_speed = 1
		air_facing = facing.copy()
	if crouch or air_facing != facing:
		slow_speed = 2
	if moving[0]:
		player_movement[0] -= 10 / slow_speed 
		facing[0] = True
		facing[1] = False
	if moving[1]:
		player_movement[0] += 10 / slow_speed
		facing[1] = True
		facing[0] = False

	player_pos, collision_direction = move(player_pos, player_movement, blocks)

	if collision_direction['bottom'] == True:
		ySpeed = 0
		air_time = 0
	if collision_direction['top'] == True:
		ySpeed = 0
		up_pressed = False
	if ySpeed != 0:
		air_time += 1

	if crouch:
		player_pic = player_crouch
	elif player_movement[0] != 0 and air_time < 5:
		player_pic, frame = animation(frame, player_running, player_pic, 15)
	elif air_time < 5:
		player_pic, frame = animation(frame, player_idle, player_pic, 30)

	bunny.rect.x = player_pos.x - scroll[0]
	bunny.rect.y = player_pos.y - scroll[1]
	bunny.picture = player_pic
	character_group.draw(display)

	if up_pressed:
		ySpeed -= 1
	if ySpeed <= -16:
		up_pressed = False

	frame += 1
	if frame > 60:
		frame = 0

	for event in pg.event.get():
		if event.type == pg.QUIT:
			running = False

		if event.type == pg.KEYDOWN:
			if event.key == pg.K_LEFT:
				moving[0] = True
			if event.key == pg.K_RIGHT:
				moving[1] = True
			if event.key == pg.K_UP and air_time < 5:
				ySpeed -= 12
				air_facing = facing.copy()
				up_pressed = True
			if event.key == pg.K_DOWN:
				crouch = True
			frame = 0

		if event.type == pg.KEYUP:
			if event.key == pg.K_LEFT:
				moving[0] = False
			if event.key == pg.K_RIGHT:
				moving[1] = False
			if event.key == pg.K_UP:
				up_pressed = False
			if event.key == pg.K_DOWN:
				crouch = False
			frame = 0

	character_group.update()
	pg.display.update()

pg.display.quit()
pg.quit()