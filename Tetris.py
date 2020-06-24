import pygame
from random import randint
from copy import deepcopy

def setup(n): #create the startup screen with lines
	screen.fill((0, 0, 0))
	for i in range(n//10, n, n//10):
		pygame.draw.line(screen, (125, 125, 125), (i, 0), (i, 2*n),  1)
	for i in range(n//10, 2*n, n//10):
		pygame.draw.line(screen, (125, 125, 125), (0, i), (n, i),  1)

def get_shape():
	_ = False
	O = True
	L =[[_,
		 O,_,_,
		 O,_,_,
		 O,O,_,_],
		[_,
		 _,_,_,
		 _,_,O,
		 O,O,O,_],
		[_,
		 O,O,_,
		 _,O,_,
		 _,O,_,_],
		[_,
		 _,_,_,
		 O,O,O,
		 O,_,_,_]]

	S =[[_,
		 _,_,_,
		 _,O,O,
		 O,O,_,_],
		[_,
		 O,_,_,
		 O,O,_,
		 _,O,_,_]]

	Z =[[_,
		 _,_,_,
		 O,O,_,
		 _,O,O,_],
		[_,
		 _,O,_,
		 O,O,_,
		 O,_,_,_]]

	I =[[O,
		 O,_,_,
		 O,_,_,
		 O,_,_,_],
		[_,
		 _,_,_,
		 _,_,_,
		 O,O,O,O]]

	T =[[_,
		 _,_,_,
		 _,O,_,
		 O,O,O,_],
		[_,
		 _,O,_,
		 O,O,_,
		 _,O,_,_],
		[_,
		 _,_,_,
		 O,O,O,
		 _,O,_,_],
		[_,
		 O,_,_,
		 O,O,_,
		 O,_,_,_]]

	Q =[[_,
		 _,_,_,
		 O,O,_,
		 O,O,_,_]]

	J =[[_,
		 _,O,_,
		 _,O,_,
		 O,O,_,_],
		[_,
		 _,_,_,
		 O,O,O,
		 _,_,O,_],
		[_,
		 O,O,_,
		 O,_,_,
		 O,_,_,_],
		[_,
		 _,_,_,
		 O,_,_,
		 O,O,O,_]]

	shapes = [L, S, Z, I, T, Q, J]

	return shapes[randint(0, len(shapes) - 1)]

def get_color():
	colors = [(255, 255, 255), (255, 0, 0), (0, 255, 255), (255, 255, 0), (0, 255, 0), (0, 0, 255)]
	return colors[randint(0, len(colors) - 1)]

def shape_builder(shape, color, xpos, ypos): #this shit will draw any shape if you feed in the right matrix from get_shape
	shape_sq = []
	middle = dim*4
	y = 0
	x = middle
	xmax = x
	for i in range(11):
		if shape[i]:
			pygame.draw.rect(screen, color, (x + xpos, y + ypos - dim*4, dim, dim))
			shape_sq.append([x + xpos, y + ypos - dim*4, dim, dim])
		x += dim
		if i == 0:
			y = dim
			x = middle
		if i == 3:
			y = dim*2
			x = middle
		if i == 6:
			y = dim*3
			x = middle
		if i == 10:
			y = 0
			x = middle
	return shape_sq #return xmax for max width (collisions), return shape_sq for position of squares in shape 

def check_collisions(shape_sq, sq_list):
	for sq in shape_sq:		#check if there are any collisions 
		
		if sq[1] + dim > dim*20: #check for floor collisions
			return True
		
		if not 0 <= sq[0] <= dim*9: #check for wall collisions
			return True
		
		for coordinate in sq_list:
			if sq[0] >= coordinate[0] and sq[0] < coordinate[0] + dim: #check for x collisions with blocks
				if sq[1] + dim <= coordinate[1] + dim and sq[1] + dim >= coordinate[1]: #check for y collisions with blocks
					return True

def inplace(sq_list, color_list): 
	i = 0 
	l = [[] for i in range(20)] #create empty lists for each line

	for sq in sq_list: #draw a square for each square we have in the list
		pygame.draw.rect(screen, color_list[i], sq)
		i += 1
		l[sq[1]//dim].append(sq) #add the squares to the correct line (sq[1]//dim gives the line)

	for line in l: #check for each line
		if len(line) == 10: #if the line has the max length (10) then it is complete
			for sq in line:
				color_list.pop(sq_list.index(sq)) #this is exageratly stupid and complicated for no reason
				sq_list.remove(sq) #remove each square from that line
			
			for sq in sq_list: 
				if sq[1] < l.index(line) * dim: #from the total list of squares, those whose height 
					sq[1] += dim		  		#is higher (lower) than the line removed, bring them down 

def check_loss(sq_list):
	for sq in sq_list:
		if sq[1] < 0:
			return True

def init():
	pygame.init() #init of pygame
	running = True
	pygame.display.set_caption("TETRIS")

	n = 300 #init of screen variables 
	global dim
	global screen
	dim = n//10
	screen = pygame.display.set_mode([n, 2*n])
	clock = pygame.time.Clock()
	clock_operations_per_second = 1000

	rotation = 0 	#init of useful variables
	shape = get_shape()
	color = get_color()
	color_list = []
	x = 0
	y = 0

	sq_list = []
	input = 0
	wait = 10 #number from 1 to inf to establish how frequntly register key presses

	while running:

		clock.tick(clock_operations_per_second)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

		if input > 0: 	#a clock to slow down the registration fo key presses
			input += 1
			if input == wait:
				input = 0

		speed = 2 	#speed is set here so when you stop pressing K_DOWN it comes back to normal
					#from the way I programmed the y part down there, speed cannot exceed dim

		setup(n) #setup the screen to be black + lines (everything else gets erased)
		
		inplace(sq_list, color_list) #represents the cubes that are not moving, the hitbox needs to be done

		shape_sq = shape_builder(shape[rotation], color, x, y) #call me, not worth it to explain it here, it is just stupid and messy


		keys = pygame.key.get_pressed() #get the keys pressed during the game
		
		if keys[pygame.K_LEFT] and not input: #go left by 1 square (dim)
			input += 1
			l1 = deepcopy(shape_sq)
			for sq in l1:
				sq[0] -= dim

			if not check_collisions(l1, sq_list):
				x -= dim
				shape_sq = shape_builder(shape[rotation], color, x, y)
		
		if keys[pygame.K_RIGHT] and not input: #go right by 1 square (dim)
			input += 1
			l2 = deepcopy(shape_sq)
			for sq in l2:
				sq[0] += dim	

			if not check_collisions(l2, sq_list):
				x += dim
				shape_sq = shape_builder(shape[rotation], color, x, y)

		if keys[pygame.K_UP] and not input: #change rotation if possible
			input += 1
			i = 0
			try:
				rotation += 1
				shape_sq = shape_builder(shape[rotation], color, x, y)
				while check_collisions(shape_sq, sq_list):
					if i < 3:
						x -= dim
						i += 1
						shape_sq = shape_builder(shape[rotation], color, x, y)
					if i == 3:
						x += 3*dim
						rotation -= 1
						shape_sq = shape_builder(shape[rotation], color, x, y)
			except:
				rotation = 0
				shape_sq = shape_builder(shape[rotation], color, x, y)
				while check_collisions(shape_sq, sq_list):
					if i < 3:
						x -= dim
						i += 1
						shape_sq = shape_builder(shape[rotation], color, x, y)
					if i == 3:
						x += 3*dim
						rotation -= 1
						shape_sq = shape_builder(shape[rotation], color, x, y)

		if keys[pygame.K_DOWN]: #accelerate descent
			speed = 10

		y += speed

		if check_collisions(shape_sq, sq_list):
			y = y//dim * dim	#y could be any value, not a multiple of dim, set it as a multiple
			shape_sq = shape_builder(shape[rotation], color, x, y)	#add the squares of this last shape to the list of squares, we run the command again to use the correct y
			
			sq_list += shape_sq 
			color_list += [color] * len(shape_sq)
			
			shape = get_shape() #set everything as default 
			color = get_color()
			x = 0
			y = 0
			rotation = 0

		if check_loss(sq_list):
			break

		pygame.display.flip() #update screen

	pygame.quit()

init()






