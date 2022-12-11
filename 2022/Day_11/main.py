import math
import time
from typing import List

USE_LOGGING = False
USE_DEMO = False
PART_ONE = False

ModMagic = 1 #No shame in needing help, looked up some help on the math magic for part 2

class Monkey:
    def __init__(self, items: List[int], inspectionFunction, modVal, passMonkey, failMonkey):
        self.Items = items
        self.InspectionFunction = inspectionFunction
        self.ModVal = modVal
        self.PassMonkey = passMonkey
        self.FailMonkey = failMonkey
        self.InspectionCounter = 0

    def InspectItem(self, old):
        self.InspectionCounter += 1
        output = eval(self.InspectionFunction)
        return math.floor(output/3) if PART_ONE else output%ModMagic

    def GetMonkeyReciever(self, value):
        return self.PassMonkey if value % self.ModVal == 0 else self.FailMonkey

MonkeyBarrel: List[Monkey] = []

def modTest(input, modValue, passValue, failValue):
    return passValue if input % modValue == 0 else failValue

def getInput(fileName):
    global ModMagic
    file = open(fileName, 'r')
    
    input = file.read().split("\n\n")
    monkeyTraits = [[t.split(":")[1].strip() for t in m.strip().split("\n")[1:]] for m in input]

    for m in monkeyTraits:
        startingItems = [int(i) for i in m[0].split(", ")] 
        op1 = m[1].split(" = ")[1]
        modNumber = int(m[2].split()[-1])
        passAction = int(m[3].split()[-1])
        failAction = int(m[4].split()[-1])

        ModMagic = ModMagic * modNumber

        monk = Monkey(startingItems, op1, modNumber, passAction, failAction)
        MonkeyBarrel.append(monk)

def observeRounds(roundCount):
    for r in range(roundCount):
        for m in MonkeyBarrel:
            for item in m.Items:
                item = m.InspectItem(item)

                target = m.GetMonkeyReciever(item)
                MonkeyBarrel[target].Items.append(item)

            m.Items.clear()

#start of main
solution = 0

startTime = time.time()

file = 'example.txt' if USE_DEMO else 'input1.txt'

input = getInput(file)
observeRounds(20 if PART_ONE else 10000)

counts = []
for m in MonkeyBarrel:    
    if USE_LOGGING: print(f'Monkey: {m.InspectionCounter}')
    counts.append(m.InspectionCounter)

top2 = sorted(counts, reverse=True)[:2]
solution = top2[0] * top2[1]

endtime = time.time()
print('Solution: ', solution)
print ('Completion time: ', endtime - startTime)