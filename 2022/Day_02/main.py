import time
import os

scoringMap = {
    "Rock"      : 1,
    "Paper"     : 2,
    "Scissors"  : 3
}

#Return what the input would lose to
loserMap = {
    "Rock"      : "Paper",
    "Paper"     : "Scissors",
    "Scissors"  : "Rock"
}

#Return what the input would beat
winnerMap = {
    "Rock"      : "Scissors",
    "Paper"     : "Rock",
    "Scissors"  : "Paper"
}

translationMap = {
    "A" : "Rock",
    "B" : "Paper",
    "C" : "Scissors",
    "X" : "Rock",
    "Y" : "Paper",
    "Z" : "Scissors"
}

def getMoveList1(fileName, log = False):
    file = open(fileName, 'r')
    input =  [tuple(map(lambda move: translationMap[move], x.strip().split(" "))) for x in file.readlines()]

    if log: print(input)

    return input

def getMoveList2(fileName, log = False):
    file = open(fileName, 'r')
    input =  [tuple(x.strip().split(" ")) for x in file.readlines()]

    if log: print(input)

    return input

def getMoveScore(myMove, theirMove):
    score = scoringMap[myMove]

    if (myMove == theirMove):
        score += 3
    elif (winnerMap[myMove] == theirMove):
        score += 6

    return score

def getTotalScore1(input):
    score = 0

    for fight in input:
        score += getMoveScore(fight[1], fight[0])

    return score

outcomeScoreMap = {
    "X" : 0,
    "Y" : 3,
    "Z" : 6
}

def getTotalScore2(input):
    score = 0

    for fight in input:
        outcome = fight[1]
        theirMove = translationMap[fight[0]]
        
        score += outcomeScoreMap[outcome]
        
        if (outcome == "Y"):
            score += scoringMap[theirMove]
        elif (outcome == "X"):
            score += scoringMap[winnerMap[theirMove]]
        else:
            score += scoringMap[loserMap[theirMove]]

    return score


useDemo = False
useLogging = False

startTime = time.time()

file = 'example.txt' if useDemo else 'input1.txt'
#moves = getMoveList1(file, useLogging)
#solution = getTotalScore1(moves)

moves = getMoveList2(file, useLogging)
solution = getTotalScore2(moves)

endtime = time.time()
print(f'Solution: ', solution)
print ('Completion time: ', endtime - startTime)