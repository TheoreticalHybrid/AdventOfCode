import time
import os
import re

USE_LOGGING = False
USE_DEMO = False

def getInput(fileName):
    file = open(fileName, 'r')
    input =  [[int(x) for x in line.split()] for line in file.read().split("\n")]

    if USE_LOGGING: print(input)

    return input

def isValidReport(report, dampenerEnabled):
    valid = True

    increasing = False
    for i, value in enumerate(report[:-1]):        
        nextValue = report[i+1]

        if i == 0:
            if value == nextValue: #invalid configuration
                if dampenerEnabled:
                    #check removing this value
                    dampReport = report[1:]
                    if USE_LOGGING: print(f'Value [{value}] / NextValue [{nextValue}] - Removing THIS value ({value}) changes {report} to {dampReport}')
                    dampValid = isValidReport(dampReport, False)

                    if dampValid:
                        valid = True
                        break

                    #check removing next value
                    dampReport = report[:i+1] + report[i+2:]
                    if USE_LOGGING: print(f'Value [{value}] / NextValue [{nextValue}] - Removing NEXT value ({nextValue}) changes {report} to {dampReport}')
                    valid = isValidReport(dampReport, False)
                    break
                else:
                    valid = False
                    break

            increasing = value < nextValue
        
        diff = abs(value - nextValue)
        if diff == 0 or diff > 3 or (nextValue < value if increasing else nextValue > value):
            if dampenerEnabled:
                if i == 1: #check removing the first item in case it's causing the increase/decrease check to be wrong
                    dampReport = report[1:]
                    if USE_LOGGING: print(f'Value [{value}] / NextValue [{nextValue}] - Removing FIRST value ({report[0]}) changes {report} to {dampReport}')
                    valid = isValidReport(dampReport, False)

                    if valid:
                        break

                #check removing this value
                dampReport = report[:i] + report[i+1:]
                if USE_LOGGING: print(f'Value [{value}] / NextValue [{nextValue}] - Removing THIS value ({value}) changes {report} to {dampReport}')
                valid = isValidReport(dampReport, False)

                if valid:
                    break

                if value != nextValue:
                    #check removing next value
                    dampReport = report[:-1] if i+2 == len(report) else report[:i+1] + report[i+2:]
                    if USE_LOGGING: print(f'Value [{value}] / NextValue [{nextValue}] - Removing NEXT value ({nextValue}) changes {report} to {dampReport}')
                    valid = isValidReport(dampReport, False)
                    break
                
                break
            else:
                valid = False
                break

    return valid

def getValidReportCount(input, dampenerEnabled):
    validCount = 0

    for report in input:
        valid = isValidReport(report, dampenerEnabled)

        if USE_LOGGING: print(f'Report {report} is {'VALID' if valid else 'INVALID'}\n')
        if valid:
            validCount += 1

    return validCount

file = 'example.txt' if USE_DEMO else 'input1.txt'
input = getInput(file)

startTime = time.time()

solution = getValidReportCount(input, False)

endtime = time.time()
print(f'Part 1 Solution: ', solution)
print ('Part 1 Completion time: ', endtime - startTime)

#exit()

startTime = time.time()

solution = getValidReportCount(input, True)

endtime = time.time()
print(f'Part 2 Solution: ', solution)
print ('Part 2 Completion time: ', endtime - startTime)