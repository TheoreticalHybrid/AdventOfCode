import sys
import time
from pathlib import Path

from functools import reduce
from operator import mul

options = [opt for opt in sys.argv[1:] if opt.startswith("-")]
arguments = [arg for arg in sys.argv[1:] if not arg.startswith("-")]

USE_LOGGING = '-v' in options
USE_DEMO = '-d' in options

if '-f' in options:
    #Ask for user input to keep going
    userInput = input("File: ")
    my_file = Path(userInput)
    if not my_file.is_file():
        raise SystemExit(f"File {userInput} is not found")

def getProblemInput(fileName):
    problemData = dict()
    with open(fileName, 'r') as file:
        for line in file.readlines():
            words = line.strip().split(' ')
            name, capacity, durability, flavor, texture, calories = words[0][0:-1], int(words[2][0:-1]), int(words[4][0:-1]), int(words[6][0:-1]), int(words[8][0:-1]), int(words[10])
            problemData[name] = (capacity, durability, flavor, texture, calories)

    return problemData

def getOptimalIngredientScore(ingredientDictionary, partTwo):
    goalTotal = 100
    
    # First build a dictionary of all possible property calculations for each ingredient
    # This is so we're not doing duplicate calculations, and instead just looking up the answer, when doing the brute force iteration later
    maxNumber = goalTotal - (len(ingredientDictionary) - 1)
    amountRange = range(1, maxNumber + 1)
    ingredientAmountCalcs = dict()
    for key in ingredientDictionary:
        ingredientAmountCalcs[key] = [tuple(x * y for y in ingredientDictionary[key]) for x in amountRange]

    # As clunky as this looks, it generates every permutation of the ingredient distributions to check
    options = []
    for _ in range(len(ingredientDictionary) - 1):
        if not any(options):
            for i in range(1, maxNumber + 1):
                options.append((i,))
        else:
            newOptions = []
            for o in options:
                for j in range(1, (maxNumber - sum(o)) + 1):
                    newOptions.append(o + (j,))

            options = newOptions

    # for final ingredient, add the remainder
    for i,o in enumerate(options):
        s = sum(o)
        remainder = goalTotal - s
        options[i] = o + (remainder,)

    bestScore = 0
    for option in options:
        capacities = []
        durabilities = []
        flavors = []
        textures = []
        calories = []
        for i, key in enumerate(ingredientAmountCalcs):
            cap, d, f, t, cal = ingredientAmountCalcs[key][option[i] - 1]
            capacities.append(cap)
            durabilities.append(d)
            flavors.append(f)
            textures.append(t)
            calories.append(cal)

        calSum = max(sum(calories), 0)

        if not partTwo or calSum == 500:
            capSum = max(sum(capacities), 0)
            durSum = max(sum(durabilities), 0)
            flavSum = max(sum(flavors), 0)
            texSum = max(sum(textures), 0)

            score = capSum * durSum * flavSum * texSum
            if score > bestScore: bestScore = score

    return bestScore        

if __name__ == "__main__":
    exampleFile = 'example2.txt'
    file = exampleFile if USE_DEMO else 'input.txt'
    problemInput = getProblemInput(file)
    #exit()

    startTime = time.time()

    solution = getOptimalIngredientScore(problemInput, False)

    endtime = time.time()
    print(f'Part 1 Solution: ', solution)
    print('Part 1 Completion time: ', endtime - startTime)

    print('---------PART TWO---------')
    startTime = time.time()

    solution = getOptimalIngredientScore(problemInput, True)

    endtime = time.time()
    print(f'Part 2 Solution: ', solution)
    print ('Part 2 Completion time: ', endtime - startTime)