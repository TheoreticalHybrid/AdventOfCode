import unittest
import solution

class TestMain(unittest.TestCase):
    def test_part1(self):
        testCount = 1
        testCases = []
        #Comet
        testCases.append(((14, 10, 127, 1), 14))
        testCases.append(((14, 10, 127, 10), 140))
        testCases.append(((14, 10, 127, 11), 140))
        testCases.append(((14, 10, 127, 12), 140))
        testCases.append(((14, 10, 127, 138), 154))
        testCases.append(((14, 10, 127, 139), 168))
        testCases.append(((14, 10, 127, 1000), 1120))
        #Dancer
        testCases.append(((16, 11, 162, 1), 16))
        testCases.append(((16, 11, 162, 10), 160))
        testCases.append(((16, 11, 162, 11), 176))
        testCases.append(((16, 11, 162, 12), 176))
        testCases.append(((16, 11, 162, 138), 176))
        testCases.append(((16, 11, 162, 139), 176))
        testCases.append(((16, 11, 162, 174), 192))
        testCases.append(((16, 11, 162, 175), 208))
        testCases.append(((16, 11, 162, 1000), 1056))
        
        for testValue, expectedResult in testCases:
            self.assertEqual(solution.getDistanceAfterTime(*testValue), expectedResult, msg=f'Test {testCount} ({testValue}) failed')
            testCount += 1

        rDict = dict()
        rDict['Comet'] = (14, 10, 127)
        rDict['Dancer'] = (16, 11, 162)

        self.assertEqual(solution.getFastestReindeerDistanceAfterTime(rDict, 1000), 1120, msg='Final Test Failed')

    def test_part2(self):        
        rDict = dict()
        rDict['Comet'] = (14, 10, 127)
        rDict['Dancer'] = (16, 11, 162)

        self.assertEqual(solution.getBestReindeerScore(rDict, 1000), 689, msg='Final Test Failed')

if __name__ == "__main__":
    unittest.main()