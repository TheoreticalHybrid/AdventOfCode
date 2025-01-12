import unittest
import solution

class TestMain(unittest.TestCase):
    def test_part1(self):
        testCount = 1
        testCases = []
        #testCases.append(('', 0))
        
        for testValue, expectedResult in testCases:
            #self.assertEqual(solution.getEndingFloor(testValue), expectedResult, msg=f'Test {testCount} ({testValue}) failed')
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