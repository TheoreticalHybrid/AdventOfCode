import time
import os
from typing import List

USE_LOGGING = False
USE_DEMO = False
PART_ONE = False

class MyFile:
    def __init__(self, size: int, name: str):
        self.Size = size
        self.Name = name

    def print(self):
        print()

class MyDirectory:
    def __init__(self, name: str, parent):
        self.Name = name
        self.Parent: MyDirectory = parent
        self.Children: List[MyDirectory] = []
        self.Files: List[MyFile] = []
        self.Depth = 0 if parent is None else parent.Depth + 1
        self.Size = 0

    def print(self):
        print("% s% s - % s" % (("\t"*self.Depth),self.Name,self.Size))
        for f in self.Files: print("% s% s - % s" % (("\t"*(self.Depth+1)),f.Name, f.Size))
        for c in self.Children: c.print()

    def calcSize(self):
        for child in self.Children: child.calcSize()
        self.Size = sum(f.Size for f in self.Files) + sum(d.Size for d in self.Children)

ROOT = MyDirectory("/", None)

def getInput(fileName):
    file = open(fileName, 'r')
    input = [x.strip().split(" ") for x in file.readlines()]

    if USE_LOGGING: print(input)

    return input

def readTerminal(terminal):
    currentDirectory = ROOT
    
    for line in terminal:        
        if line[0] == "$":
            if USE_LOGGING: print("Command")

            if line[1] == "cd":
                if line[2] == "/":
                    if USE_LOGGING: print("\tChange Directory to Root")
                    currentDirectory = ROOT #redundant so far, but better to be complete
                elif line[2] == "..":
                    if USE_LOGGING: print("\tChange Directory to Parent")

                    if currentDirectory.Parent is None: raise Exception("Can't cd to parent, there isn't one. Current Directory is ", currentDirectory.Name)
                    else: currentDirectory = currentDirectory.Parent
                else:
                    if USE_LOGGING: print("\tChange Directory to ", line[2])
                    childDirectory = next(filter(lambda d: d.Name == line[2], currentDirectory.Children), None)

                    if childDirectory is None: raise Exception("Can't cd to child, it wasn't found. Current Directory is ", currentDirectory.Name)
                    else: currentDirectory = childDirectory

            elif line[1] == "ls":
                if USE_LOGGING: print("\tls")
                #I don't think I actually need to do anything with this

        elif line[0] == "dir":
            if USE_LOGGING: print("Directory ", line[1])
            currentDirectory.Children.append(MyDirectory(line[1], currentDirectory))
        else: #file
            if USE_LOGGING: print("File % s (% s)" % (line[1], line[0]))
            currentDirectory.Files.append(MyFile(int(line[0]), line[1]))

def getSmallDirSum(myDirectory: MyDirectory, targetSize: int):
    sum = myDirectory.Size if myDirectory.Size <= targetSize else 0

    for child in myDirectory.Children:
        sum += getSmallDirSum(child, targetSize)

    return sum

def getSmallestDeleteCandidate(myDirectory: MyDirectory, targetSize: int):
    smallestOption = myDirectory.Size if myDirectory.Size > targetSize else 0

    for child in myDirectory.Children:
        smallestChild = getSmallestDeleteCandidate(child, targetSize)
        if smallestChild > 0 and smallestChild < smallestOption: smallestOption = smallestChild

    return smallestOption


#start of main
solution = 0
totalSize = 70000000
unusedSpaceTarget = 30000000

startTime = time.time()

file = 'example.txt' if USE_DEMO else 'input1.txt'

terminal = getInput(file)
readTerminal(terminal)
ROOT.calcSize()
if USE_LOGGING: ROOT.print()

freeSpace = totalSize - ROOT.Size

solution = getSmallDirSum(ROOT, 100000) if PART_ONE else getSmallestDeleteCandidate(ROOT, unusedSpaceTarget - freeSpace)

endtime = time.time()
print('Solution: ', solution)
print ('Completion time: ', endtime - startTime)