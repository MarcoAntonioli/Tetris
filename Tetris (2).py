import pygame
from random import randint

def setup(screen, n): #create the startup screen with lines
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

def shape_builder(screen, shape, xpos, ypos, dim): #this shit will draw any shape if you feed in the right matrix from get_shape
	shape_sq = []
	middle = dim*4
	y = 0
	x = middle
	xmax = x
	for i in range(11):
		if shape[i]:
			pygame.draw.rect(screen, (255, 0, 255), (x + xpos, y + ypos - dim*4, dim, dim))
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

def check_collisions(shape_sq, sq_list, dim):
	for sq in shape_sq:		#check if there are any collisions with existing blocks
		if sq[1] + dim > dim*20:
			return True
		if not 0 <= sq[0] <= dim*9:
			return True
		for coordinate in sq_list:
			if sq[0] >= coordinate[0] and sq[0] < coordinate[0] + dim: #check for x collisions
				if sq[1] + dim <= coordinate[1] + dim and sq[1] + dim >= coordinate[1]: #check for y collisions
					return True

def inplace(screen, sq_list): #we need to make screen global LOL
	for sq in sq_list: #draw a square for each square we have in the list
		pygame.draw.rect(screen, (255, 0, 255), sq)

def init():
	pygame.init() #init of pygame
	running = True
	pygame.display.set_caption("TETRIS")

	n = 300 #init of screen variables 
	dim = n//10
	screen = pygame.display.set_mode([n, 2*n])

	rotation = 0 	#init of useful variables
	shape = get_shape()
	x = 0
	y = 0

	sq_list = []
	input = 0
	clock = 10 #number from 1 to inf to establish how frequntly register key presses

	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

		if input > 0: 	#a clock to slow down the registration fo key presses
			input += 1
			if input == clock:
				input = 0

		speed = 2 	#speed is set here so when you stop pressing K_DOWN it comes back to normal
					#from the way I programmed the y part down there, speed cannot exceed 

		setup(screen, n) #setup the screen to be black + lines (everything else gets erased)
		
		inplace(screen, sq_list) #represents the cubes that are not moving, the hitbox needs to be done

		shape_sq = shape_builder(screen, shape[rotation], x, y, dim) #call me, not worth it to explain it here, it is just stupid and messy


		keys = pygame.key.get_pressed() #get the keys pressed during the game
		
		if keys[pygame.K_LEFT] and not input: #go left by 1 square (dim)
			input += 1
			for sq in shape_sq:
				sq[0] -= dim
			if not check_collisions(shape_sq, sq_list, dim):
				x -= dim
				shape_sq = shape_builder(screen, shape[rotation], x, y, dim)
		
		if keys[pygame.K_RIGHT] and not input: #go right by 1 square (dim)
			input += 1
			for sq in shape_sq:
				sq[0] += dim
			if not check_collisions(shape_sq, sq_list, dim):
				x += dim
				shape_sq = shape_builder(screen, shape[rotation], x, y, dim)

		if keys[pygame.K_UP] and not input: #change rotation if possible
			input += 1
			try:
				rotation += 1
				shape[rotation]
			except:
				rotation = 0

		if keys[pygame.K_DOWN]: #accelerate descent
			speed = 10

		y += speed 

		if check_collisions(shape_sq, sq_list, dim):
			y = y//dim * dim	#y could be any value, not a multiple of dim, set it as a multiple
			shape_sq = shape_builder(screen, shape[rotation], x, y, dim)	#add the squares of this last shape to the list of squares, we run the command again to use the correct y
			sq_list += shape_sq 
			
			shape = get_shape() #set everything as default 
			x = 0
			y = 0
			rotation = 0

		pygame.display.flip() #update screen

	pygame.quit()

init()






