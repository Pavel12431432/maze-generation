import random
import pygame

cols, rows = 32, 20
# define size for each tile when drawn
size = 25
# initialize maze array
maze = [[0] * rows for i in range(cols)]
# stack to handle backtracking
stack = [(0, 0)]
# set keeping track of visited tiles
visited = {(0, 0)}

# pygame stuff
pygame.init()
screen = pygame.display.set_mode((cols * size, rows * size), 0, 32)
pygame.display.set_caption('Maze generation')
clock = pygame.time.Clock()


# handle input
def inp():
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			quit()


# pick a valid random neighbor
def pickNeighbor(celly, cellx):
	neighbors = []
	# copy and pasted ifs
	if rows > cellx - 1 >= 0 <= celly < cols and not (celly, cellx - 1) in visited:
		neighbors.append((celly, cellx - 1))
	if rows > cellx + 1 >= 0 <= celly < cols and not (celly, cellx + 1) in visited:
		neighbors.append((celly, cellx + 1))
	if rows > cellx >= 0 <= celly - 1 < cols and not (celly - 1, cellx) in visited:
		neighbors.append((celly - 1, cellx))
	if rows > cellx >= 0 <= celly + 1 < cols and not (celly + 1, cellx) in visited:
		neighbors.append((celly + 1, cellx))

	# return random neighbor or None if all neighbors have been visited
	# random.choice raises error when passed an empty sequence
	return None if not neighbors else random.choice(neighbors)


# get walls to draw around a tile
def getNeighboringWalls(celly, cellx):
	neighbors = []
	# copy and pasted ifs
	if cols > cellx - 1 >= 0 <= celly < rows:
		# check if there should be a wall between tiles
		if not abs(maze[cellx][celly] - maze[cellx - 1][celly]) == 1:
			neighbors.append(((0, 0), (0, size)))
	if cols > cellx + 1 >= 0 <= celly < rows:
		if not abs(maze[cellx][celly] - maze[cellx + 1][celly]) == 1:
			neighbors.append(((size, 0), (size, size)))
	if cols > cellx >= 0 <= celly - 1 < rows:
		if not abs(maze[cellx][celly] - maze[cellx][celly - 1]) == 1:
			neighbors.append(((0, 0), (size, 0)))
	if cols > cellx >= 0 <= celly + 1 < rows:
		if not abs(maze[cellx][celly] - maze[cellx][celly + 1]) == 1:
			neighbors.append(((0, size), (size, size)))

	return neighbors


# draw function
def draw():
	screen.fill((0, 0, 0))
	# bad and slow code
	# to improve add array containing walls and remove unwanted ones
	# loops over every cell and checks which walls to draw
	for i in range(cols):
		for j in range(rows):
			# get a color for the current cell
			if stack[-1] == (i, j):
				# if the cell is the cell at the top of the stack draw purple
				color = (100, 0, 150)
			elif (i, j) in visited:
				# if cell is visited its green
				color = (0, 150, 0)
			else:
				# else black
				color = (0, 0, 0)
			pygame.draw.rect(screen, color, ((i * size, j * size), (size, size)))
			# get walls to draw
			if n := getNeighboringWalls(j, i):
				# draw each wall
				for wall in n:
					pos = (i * size, j * size)
					pygame.draw.line(screen, (255, 255, 255),
									 tuple(map(sum, zip(pos, wall[0]))),
									 tuple(map(sum, zip(pos, wall[1]))))
	pygame.display.update()


def loop():
	# check if valid neighbors exist
	if not (nextPos := pickNeighbor(*stack[-1])):
		return stack.pop(-1)
	maze[nextPos[0]][nextPos[1]] = len(stack)
	stack.append(nextPos)
	visited.add(nextPos)


if __name__ == '__main__':
	# create maze until all cells are visited
	while len(visited) < cols * rows:
		inp()
		loop()
		draw()
		# limit program to 30 fps
		clock.tick(30)
	print('Done!')
	# halts the program
	while True:
		inp()