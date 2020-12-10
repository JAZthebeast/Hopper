import pygame as pg

grass_block = pg.image.load('pictures/grass.png')
dirt_block = pg.image.load('pictures/dirt.png')
stone_block = pg.image.load('pictures/stone.png')

solid_blocks = {
				
				grass_block: 3, 
				dirt_block: 2,
				stone_block: 1,
				
				}