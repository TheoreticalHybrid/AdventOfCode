import unittest
import solution

class TestMain(unittest.TestCase):
    def test_part1(self):
        testCount = 1
        testCases = []
        testCases.append(('Alice', 'Bob', 54))
        testCases.append(('Alice', 'Carol', -79))
        testCases.append(('Alice', 'David', -2))
        testCases.append(('Bob', 'Alice', 83))
        testCases.append(('Bob', 'Carol', -7))
        testCases.append(('Bob', 'David', -63))
        testCases.append(('Carol', 'Alice', -62))
        testCases.append(('Carol', 'Bob', 60))
        testCases.append(('Carol', 'David', 55))
        testCases.append(('David', 'Alice', 46))
        testCases.append(('David', 'Bob', -7))
        testCases.append(('David', 'Carol', 41))

        happyDict = solution.buildHappinessDictionary(testCases, False)
        
        for testPerson, testNeighbor, testHappinessValue in testCases:
            self.assertEqual(happyDict[testPerson][testNeighbor], testHappinessValue, msg=f'Test {testCount} ({testPerson}->{testNeighbor}) failed')
            testCount += 1

        self.assertEqual(solution.getOptimalSeatingValue(testCases, False), 330, msg=f'Full test failed')

        testCases = []
        testCases.append((['Alice','Bob','Carol','David'], 330))        
        testCases.append((['Alice','Carol','Bob','David'], -114))
        testCases.append((['Alice','Carol','David','Bob'], 22))
        testCases.append((['Alice','David','Carol','Bob'], 330))

        for testValue, expectedResult in testCases:
            self.assertEqual(solution.getHappinessValue(testValue, happyDict), expectedResult, msg=f'Test {testCount} ({testValue}) failed')
            testCount += 1

    def test_part2(self):
        testCount = 1
        testCases = []
        #testCases.append(('', 0))

        for testValue, expectedResult in testCases:
            #self.assertEqual(solution.getFirstBasementIndex(testValue), expectedResult, msg=f'Test {testCount} ({testValue}) failed')
            testCount += 1

if __name__ == "__main__":
    unittest.main()