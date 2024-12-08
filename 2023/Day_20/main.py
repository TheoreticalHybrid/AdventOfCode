import time
from copy import deepcopy
import itertools

USE_LOGGING = True
USE_DEMO = False
PART_ONE = False

class Module:
    def __init__(self, name, mType, id):
        self.Name = name
        self.Broadcaster = False
        self.Flipper = False
        self.Outputs = []
        self.IsOn = False
        self.Connections = {}
        self.Id = id
        match mType:
            case 'b':
                self.Broadcaster = True
            case '%':
                self.Flipper = True
            case '&':
                pass

    def addOutputs(self, outs):
        self.Outputs += outs

    def addConnection(self, c):
        self.Connections[c] = False

    def process(self, HighPulse, connectionSource):
        if self.Broadcaster:
            return zip(self.Outputs, itertools.repeat(HighPulse), itertools.repeat(self.Name))
        elif self.Flipper:
            if not HighPulse:
                self.IsOn = not self.IsOn
                return zip(self.Outputs, itertools.repeat(self.IsOn), itertools.repeat(self.Name))
            else: return []
        else:
            self.Connections[connectionSource] = HighPulse
            pulse = all([v for k,v in self.Connections.items()])
            return zip(self.Outputs, itertools.repeat(not pulse), itertools.repeat(self.Name))
        
    def printMap(self, map):
        print(f'{self.Name} ({map[self.Name]}):\n')
        outputs = [map[o] for o in self.Outputs]
        if self.Broadcaster:
            print(f'\tLow -> {outputs}')
        elif self.Flipper:
            print(f'\t-High->?\n\t\t-> X')
            print(f'\t-Low->?:')
            print(f'\t\tOn: Low -> {outputs}')
            print(f'\t\tOff: High -> {outputs}')
        else:
            print(f'\tMemory all High: Low -> {outputs}')
            print(f'\tMemory has Low: High -> {outputs}')

def getInput(fileName):
    file = open(fileName, 'r')

    mappings = {}
    modules: dict[str, Module] = {}
    counter = 0
    for line in file.readlines(): # get the modules/mappings
        module, output = line.split('->')
        module = module.strip()
        output = output.strip()
        key = module[1:] if module[0] in ('%', '&') else module
        mappings[key] = [o.strip() for o in output.split(',')]
        modules[key] = Module(key, module[0], counter)
        counter += 1

    for k in mappings:
        modules[k].addOutputs(mappings[k])
        for v in mappings[k]:
            if v in modules:
                modules[v].addConnection(k)

    return modules

def getPulseValue(modules: dict[str, Module], buttonPressLimit):
    lowPulseCount, highPulseCount = 0, 0

    pressNumber = 0
    while pressNumber < buttonPressLimit if PART_ONE else True:
        pressNumber += 1
        pulseQueue = [('broadcaster', False, 'button')]
        while pulseQueue:
            mName, pulse, sender = pulseQueue.pop(0)
            if USE_LOGGING: 
                if True: print(f'{sender} -{'high' if pulse else 'low'}-> {mName}')
                else: print(f'Button Press: {pressNumber}')
            
            if PART_ONE:
                if pulse: highPulseCount += 1
                else: lowPulseCount += 1
            else: # While I could run my computer for who knows how long, this isn't a reasonable solution
                if mName == 'rx' and not pulse: return pressNumber

            if mName in modules:
                pulseQueue = pulseQueue + list(modules[mName].process(pulse, sender))

    return lowPulseCount * highPulseCount

def buildTree(modules: dict[str, Module]):
    moduleQueue = ['broadcaster']
    idMap = {}
    visited = []

    counter = 0
    while moduleQueue:
        mName = moduleQueue.pop(0)
        idMap[mName] = counter
        visited.append(mName)
        counter += 1
        if mName in modules:
            moduleQueue = moduleQueue + [o for o in modules[mName].Outputs if o not in visited and o not in moduleQueue]
        
    for mName in visited:
        if mName in modules:
            modules[mName].printMap(idMap)


def getMinimumButtonCount(modules: dict[str, Module]):
    moduleQueue = ['broadcaster']
    painDict = {} # key = module name, value = minimum number of button presses to have a low pulse output

    # If a module is sending a high signal to a flipper, just don't send it

    while moduleQueue:
        mName = moduleQueue.pop(0)
        if mName == 'broadcaster':
            painDict[mName] = 1
        else:
            pass
        
        moduleQueue = moduleQueue + modules[mName].Outputs


startTime = time.time()

file = 'example.txt' if USE_DEMO else 'input1.txt'
input = getInput(file)

if not PART_ONE: buildTree(input)
solution = getPulseValue(input, 1000) if PART_ONE else 0

endtime = time.time()
print(f'Solution: ', solution)
print ('Completion time: ', endtime - startTime)