import time

USE_LOGGING = False
USE_DEMO = False
PART_ONE = True

solutions = {}

def getInput(fileName):
    file = open(fileName, 'r')

    #input = [(a,[int(c) for c in b.split(',')]) for a,b in [line.strip().split() for line in file.readlines()]]
    input = [line for line in file.readlines()]

    if False and USE_LOGGING:
        for line in input: print(line)
        print()

    return input

def getPossibleArrangement_X(springMap, springList):
    possibilities = 0

    # First split the map into single character sections?
    mapSections = []
    # I'm sure there's an easier way to do this, but here we go
    currentString = None
    for c in springMap:
        if currentString is None or currentString[-1] == c:
            currentString = c if currentString is None else currentString + c
        else:
            mapSections.append(currentString)
            currentString = c
    mapSections.append(currentString)
    if USE_LOGGING: print(mapSections)

    # Next find the possible matches for damaged springs
    possibleMatches = []
    for i, ds in enumerate(springList):
        # maybe iterate over every map section, and list of possible chunks that would fit the ds value, and if there is only one when done then remove it from mapSections
        sectionIndexes = []
        sectionChunk = ''
        sectionNumber = 0
        sectionPossibilities = []
        for j, section in enumerate(mapSections):
            if section[0] == '.':
                if not sectionChunk == '':
                    # not sure about this section number check, the intent is not to evaluate chunk 1 of 3 for damaged spring number 2 of 3
                    #if sectionNumber >= i and len(sectionChunk) >= ds: sectionPossibilities.append((sectionChunk, sectionIndexes))
                    if len(sectionChunk) >= ds and ('?' in sectionChunk or len(sectionChunk) == ds): 
                        sectionPossibilities.append((sectionChunk, sectionIndexes))
                    sectionNumber += 1
                    sectionIndexes = []
                    sectionChunk = ''
            else:
                sectionChunk += section
                sectionIndexes.append(j)
        if len(sectionChunk) >= ds and ('?' in sectionChunk or len(sectionChunk) == ds): sectionPossibilities.append((sectionChunk, sectionIndexes))
        possibleMatches.append((ds, sectionPossibilities))

    print()
    for pm in possibleMatches:
        print(f'\t{pm}')
    print()

    # Moving away from this solution for now, going to try something more direct that will probably be terrible for part 2

    return possibilities

def checkSolution(proposed, map, rList):
    if len(proposed) != len(map):
        print(f'\t{proposed} is a different length than {map}')
        return False
    elif len(''.join(filter(lambda x: x == '#', proposed))) != sum(rList):
        print(f'\t{proposed} does not have the correct number of hashes ({sum(rList)}): {rList}')
        return False
    else:
        for i,c in enumerate(map):
            if c in ('.', '#'):
                if proposed[i] != c:
                    print(f'\t{map} expects a {c} at position [{i}] but {proposed} has a {proposed[i]}')
                    return False

        mapSections = []
        # I'm sure there's an easier way to do this, but here we go
        currentString = None
        for c in proposed:
            if currentString is None or currentString[-1] == c:
                currentString = c if currentString is None else currentString + c
            else:
                mapSections.append(currentString)
                currentString = c
        mapSections.append(currentString)

        listIndex = 0
        for section in mapSections:
            if section[0] == '#':
                if len(section) != rList[listIndex]:
                    print(f'\tList index {listIndex} expected a section of length {rList[listIndex]} but {proposed} has a section of length {len(section)}')
                    return False
                else:
                    listIndex += 1
    return True

def getPossibleArrangementCount(solutionKey, solutionList, springMap, springList, prefix):
    global solutions
    possibilities = 0

    localPrefix = prefix

    for i, c in enumerate(springMap):
        # if number of required characters (sum of springlist) + number of required characters between them (length of springList - 1) 
        # is greater than the remaining length of springMap, then it is impossible that springMap can satisfy the requirements of springList
        if sum(springList) + len(springList) - 1 > len(springMap) - i: break
        stopIndex = i+springList[0]
        if stopIndex > len(springMap): break
        if c in ('#', '?'):
            subString = springMap[i:stopIndex]
            if '.' not in subString and (stopIndex == len(springMap) or springMap[stopIndex] in ('.', '?')):
                if len(springList) == 1:
                    if '#' not in springMap[stopIndex:]:
                        tempPrefix = localPrefix + subString.replace('?', '#')
                        tempSuffix = '.' * len(springMap[stopIndex:])
                        s = tempPrefix + tempSuffix
                        # checkSolution(s, solutionKey, solutionList)
                        solutions[solutionKey].append(tempPrefix + tempSuffix)
                        possibilities += 1
                    localPrefix += '.' if c == '?' else '#'
                else:
                    possibilities += getPossibleArrangementCount(solutionKey, solutionList, springMap[stopIndex+1:], springList[1:], localPrefix + subString.replace('?', '#') + '.') # springMap[stopIndex+1:] is to cover the spacer character
                    localPrefix += '.' if c == '?' else '#'
                
                #if '#' in subString:
                if subString[0] == '#':
                    break
            else:
                if c == '#': break
                else: localPrefix += '.'
        else: localPrefix += '.'

    return possibilities

def getPossibleArrangements(input):
    springMap, springList = input.strip().split()
    springList = [int(c) for c in springList.split(',')]
    if USE_LOGGING: print(f'Checking {springMap} : {springList}')
    
    solutions[springMap] = []
    possibilities = getPossibleArrangementCount(springMap, springList, springMap, springList, '')

    if USE_LOGGING: print(f'\t{springMap} has {possibilities} possibilities')

    for s in solutions[springMap]:
        if USE_LOGGING: print(f'\t{s}')
        # if len(''.join(filter(lambda x: x == '#', s))) != sum(springList): print(f'\t{springMap} --- {s}')

    return possibilities

startTime = time.time()

file = 'example.txt' if USE_DEMO else 'input1.txt'
input = getInput(file)
solution = sum([getPossibleArrangements(row) for row in input])

endtime = time.time()
print(f'Solution: ', solution)
print ('Completion time: ', endtime - startTime)