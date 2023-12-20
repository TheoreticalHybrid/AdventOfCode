import time
import sys
from heapq import heappop, heappush

USE_LOGGING = False
USE_DEMO = False
PART_ONE = False

def getInput(fileName):
	file = open(fileName, 'r')

	input = [[int(c) for c in line.strip()] for line in file.readlines()]

	if USE_LOGGING:
		for step in input: print(step)

	return input

def run(map):
	xMoves, yMoves = ['l','r'], ['u','d']
	endPoint = (len(map) - 1, len(map[0]) - 1)
	maxSteps = 3 if PART_ONE else 10
	minSteps = 1 if PART_ONE else 4
	
	q = [(0, 0, 0, 'x')]
	visited = set()
	leastCostDict = {}
	
	while q:
		nodeCost, nodeX, nodeY, previousMovement = heappop(q)
		if (nodeX, nodeY) == endPoint: return nodeCost
		
		visited.add((nodeX, nodeY, previousMovement))
		for direction in (yMoves+xMoves if previousMovement == 'x' else (yMoves if previousMovement in xMoves else xMoves)):
			cost = 0
			
			for distance in range(1, maxSteps + 1):
				xShift = 0 if direction in yMoves else (1 if direction == 'r' else -1)
				yShift = 0 if direction in xMoves else (1 if direction == 'd' else -1)
				nextX = nodeX + (xShift * distance)
				nextY = nodeY + (yShift * distance)
				
				if 0 <= nextX < len(map) and 0 <= nextY < len(map[0]):
					cost += map[nextX][nextY]
					if distance < minSteps: continue
					newCost = nodeCost + cost
					if leastCostDict.get((nextX, nextY, direction), sys.maxsize) <= newCost: continue
					leastCostDict[(nextX, nextY, direction)] = newCost					
					if (nextX, nextY, direction) not in visited: heappush(q, (newCost, nextX, nextY, direction))
				else: break

startTime = time.time()

file = 'example.txt' if USE_DEMO else 'input1.txt'
input = getInput(file)

solution = run(input)

endtime = time.time()
print(f'Solution: ', solution)
print ('Completion time: ', endtime - startTime)