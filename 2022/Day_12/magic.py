import string
from collections import defaultdict, deque

directions = [(0,1),(1,0),(0,-1),(-1,0)]

with open("input1.txt") as f:
    s = f.read().strip()


grid = [list(x) for x in s.split("\n")]
gridHeight = len(grid)
gridLength = len(grid[0])

startX,startY = [(i,j) for i in range(gridHeight) for j in range(gridLength) if grid[i][j] == "S"][0]
targetX,targetY = [(i,j) for i in range(gridHeight) for j in range(gridLength) if grid[i][j] == "E"][0]

grid[startX][startY] = "a"
grid[targetX][targetY] = "z"

grid = [[ord(cell) - ord("a") for cell in row] for row in grid]

distances = defaultdict(lambda : 1000000)

part = 1
# part 1:
if part == 1:
    queue = deque([(startX,startY)])
# part 2:
else:
    queue = deque([(i,j) for i in range(gridHeight) for j in range(gridLength) if grid[i][j] == 0])

for x,y in queue:
    distances[x,y] = 0
    
answer = 100000
while len(queue) > 0:
    coord = queue.popleft()
    currentX,currentY = coord
    newDistance = distances[currentX,currentY] + 1

    if (currentX,currentY) == (targetX,targetY):
        answer = distances[targetX,targetY]
        print(answer)
        break
    for directionX,directionY in directions:
        newX,newY = currentX+directionX,currentY+directionY
        if newX in range(gridHeight) and newY in range(gridLength):
            if grid[currentX][currentY] >= grid[newX][newY] - 1:
                if newDistance < distances[newX,newY]:
                    queue.append((newX,newY))
                    distances[newX,newY] = newDistance