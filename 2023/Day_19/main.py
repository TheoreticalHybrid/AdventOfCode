import time
from copy import deepcopy

USE_LOGGING = False
USE_DEMO = False
PART_ONE = False

WorkingWorkflows = {}

def getInput(fileName):
    file = open(fileName, 'r')

    input = [block.strip().split('\n') for block in file.read().split('\n\n')]

    workflows = {}
    for wf in input[0]:
        wfName, wfCriteria = wf.strip().split('{')
        workflows[wfName] = [c.split(':') for c in wfCriteria[:-1].split(',')]

    parts = [[int(r[2:]) for r in p[1:-1].split(',')] for p in input[1]]

    return (workflows, parts)

def simplifyWorkflows(wfs):
    simplifying = True
    while simplifying: # loop to remove workflows that only have one output
        removalKey = None
        for k in wfs.keys(): # for each key in the workflows dictionary
            wfRoutes = set([c[-1] for c in wfs[k]]) # get all unique outputs for a workflow (A, R, or another workflow)
            if len(wfRoutes) == 1: # if there's only one unique output
                reRoute = next(iter(wfRoutes)) # get that output
                # replace all references to it with the one ouput
                for key, value in wfs.items():
                    for c in value:
                        if c[-1] == k: c[-1] = reRoute
                removalKey = k # mark this workflow for deletion
                break # stop iterating over the workflows

        if removalKey: # if a workflow is marked for deletion
            del wfs[removalKey] # remove the workflow and reprocess
        else: # otherwise we've found all single-output workflows, move on
            simplifying = False

    simplifying = True
    while simplifying: # loop to remove workflows that are only routed to from one workflow's final criteria (where there's no condition)
        reverseRoutes = {} # key: workflow id, value: list of workflows that have this workflow as an output route
        conditionalEndpoints = [] # list of workflows that are referenced from criteria that have a condition
        for key, value in wfs.items(): # for each workflow
            if key not in reverseRoutes: reverseRoutes[key] = []
            for c in value: # for each workflow criteria
                destination = c[-1]
                if destination not in ('A','R'):
                    if destination not in reverseRoutes: reverseRoutes[destination] = []
                    reverseRoutes[destination].append(key)
                    if len(c) > 1: conditionalEndpoints.append(destination)
        
        simplifying = False
        subs = {} # this is for when keys that are being replaced also reference each other
        # get all workflows where it's referenced by less than 2 other workflows, 
        # it's not the starting workflow, and it's not referenced by a conditional criteria
        for deadWF,callingWFs in [(k,v) for k,v in reverseRoutes.items() if len(v) < 2 and k != 'in' and k not in conditionalEndpoints]:
            if len(callingWFs) == 1: # idk if there will be workflows that aren't referenced, but just in case
                replacingWF = callingWFs[0]
                
                if replacingWF in subs: # if the workflow that calls this dead workflow has already been killed, get the workflow that was calling that one
                    replacingWF = subs[replacingWF]
                
                if replacingWF not in wfs: break # something happened, most likely a dead loop, just reevaluate it all
                wfs[replacingWF] = wfs[replacingWF][:-1] + wfs[deadWF] # replace the reference to deadWF with the criteria for deadWF
                subs[deadWF] = replacingWF # keep a record of what workflow replaced the deadWF workflow with its criteria

            del wfs[deadWF] # delete the dead workflow
            simplifying = True # There were replacements made, reprocess

    return wfs

def evaluatePart(part):
    x,m,a,s = part

    visitedWFs = [] # Probably unnecessary, but adding loop detection
    thisWf = 'in'
    while thisWf not in visitedWFs:
        for condition in WorkingWorkflows[thisWf]:
            destination = condition[-1]
            if len(condition) > 1 and not eval(condition[0]): continue
            
            if destination == 'A': return True
            elif destination == 'R': return False
            else:
                visitedWFs.append(thisWf)
                thisWf = destination
                break
                    
    raise ValueError('Found a loop')

def flipCriteria(c):
    variable = c[0]
    value = int(c[2:])

    if c[1] == '<':
        return variable + '>' + str(value - 1) # need to shift the value to be the equivalent of changing it to >=
    else:
        return variable + '<' + str(value + 1) # need to shift the value to be the equivalent of changing it to <=

Criteria = []
TotalPossibilities = 0
def getAcceptableComboCount(wfKey):
    global Criteria
    global TotalPossibilities

    for condition in WorkingWorkflows[wfKey]:
        destination = condition[-1]
            
        if len(condition) > 1: Criteria.append(condition[0])
        
        if destination == 'R': # do nothing
            pass
        elif destination == 'A':
            xRanges, mRanges, aRanges, sRanges = [1,4000], [1,4000], [1,4000], [1,4000]
            
            for c in Criteria:
                thisRange = []
                match c[0]:
                    case 'x': thisRange = xRanges
                    case 'm': thisRange = mRanges
                    case 'a': thisRange = aRanges
                    case 's': thisRange = sRanges
                    
                if c[1] == '<': # need to adjust the upper bound
                    thisRange[1] = min(thisRange[1], int(c[2:]) - 1)
                else: # need to adjust the lower bound
                    thisRange[0] = max(thisRange[0], int(c[2:]) + 1)
            
            totalSet = (xRanges[1] - xRanges[0] + 1) * (mRanges[1] - mRanges[0] + 1) * (aRanges[1] - aRanges[0] + 1) * (sRanges[1] - sRanges[0] + 1) # + 1 for inclusive lower bound
            TotalPossibilities += totalSet
        else:
            getAcceptableComboCount(destination)
            
        Criteria.append(flipCriteria(Criteria.pop()))

    Criteria = Criteria[:(-1 * (len(WorkingWorkflows[wfKey]) - 1))]

startTime = time.time()

file = 'example.txt' if USE_DEMO else 'input1.txt'
workflows, parts = getInput(file)
WorkingWorkflows = simplifyWorkflows(workflows)

if not PART_ONE: getAcceptableComboCount('in')

solution = sum(sum(p) for p in parts if evaluatePart(p, workflows)) if PART_ONE else TotalPossibilities
# 167572528901520

endtime = time.time()
print(f'Solution: ', solution)
print ('Completion time: ', endtime - startTime)