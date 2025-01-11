import sys
import time
from pathlib import Path

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
    problemData = ''
    with open(fileName, 'r') as file:
        problemData = file.read()

    return problemData

def isValidPassword(pw):
    # Passwords may not contain the letters i, o, or l
    if 'i' in pw or 'o' in pw or 'l' in pw: return False

    # Passwords must include one increasing straight of at least three letters, like abc
    pwContainsIncreasingStraight = False
    for i in range(1,7):
        charOrd = ord(pw[i])
        if ord(pw[i-1]) == (charOrd - 1) and ord(pw[i+1]) == (charOrd + 1):
            pwContainsIncreasingStraight = True
            break

    if not pwContainsIncreasingStraight: return False

    # Passwords must contain at least two different, non-overlapping pairs of letters, like aa
    for i,c in enumerate(pw[0:-1]):
        if pw[i+1] == c:
            for j in range(i+2, 7):
                if pw[j] == pw[j+1]: return True

    return False

def getNextPassword(startingPw):
    foundNextValidPw = False
    pwList = list(startingPw)

    while not foundNextValidPw:
        for i in range(7, -1, -1):
            c = pwList[i]
            if c == 'z': pwList[i] = 'a'
            else:
                nextC = chr(ord(c) + 1)
                if nextC in ['i', 'o', 'l']:
                    nextC = chr(ord(nextC) + 1)

                pwList[i] = nextC
                foundNextValidPw = isValidPassword(''.join(pwList))
                break

    return ''.join(pwList)

if __name__ == "__main__":
    exampleFile = 'example2.txt'
    file = exampleFile if USE_DEMO else 'input.txt'
    problemInput = getProblemInput(file)
    #exit()

    startTime = time.time()

    solution = getNextPassword(problemInput)

    endtime = time.time()
    print(f'Part 1 Solution: ', solution)
    print('Part 1 Completion time: ', endtime - startTime)

    print('---------PART TWO---------')
    startTime = time.time()

    solution = getNextPassword(solution)

    endtime = time.time()
    print(f'Part 2 Solution: ', solution)
    print ('Part 2 Completion time: ', endtime - startTime)