import time
import os

useLogging = True

def getLetterValue(letter: chr) -> int:
    return ord(letter) - (96 if letter.islower() else 38) #Get the ascii value of the letter and adjust to fit priority

def getPackList(fileName):
    file = open(fileName, 'r')
    input =  [x.strip() for x in file.readlines()]

    if useLogging: print(input)

    return input

def intersection(list1, list2):
    return [value for value in list1 if value in list2][0]

def getPackDupeLetter(pack: str) -> chr:
    length = len(pack)
    compartment1 = pack[0:length//2]
    compartment2 = pack[length//2:]

    for letter in compartment1:
        if letter in compartment2:
            return letter

def getGroupDupeLetter(group):
    if useLogging: print(group)

    for letter in group[0]:
        if (letter in group[1] and letter in group[2]):
            return letter

#start of main
useDemo = False
partOne = False
solution = 0

startTime = time.time()

file = 'example.txt' if useDemo else 'input1.txt'
packs = getPackList(file)

if (partOne):
    for pack in packs:
        solution += getLetterValue(getPackDupeLetter(pack))
else:
    for x in range(len(packs)//3):
        startIndex = 3*x
        solution += getLetterValue(getGroupDupeLetter(packs[startIndex:startIndex+3]))

endtime = time.time()
print(f'Solution: ', solution)
print ('Completion time: ', endtime - startTime)