import unittest
import solution

class TestMain(unittest.TestCase):
    def test_part1(self):
        testCases = []
        testCases.append(([[2,3,4]], 58))
        testCases.append(([[1,1,10]], 43))
        
        for testValue, expectedResult in testCases:
            self.assertEqual(solution.getWrappingPaperOrder(testValue), expectedResult, msg=f'Test {testValue} failed')

    def test_part2(self):
        testCases = []
        testCases.append(([[2,3,4]], 34))
        testCases.append(([[1,1,10]], 14))

        for testValue, expectedResult in testCases:
            self.assertEqual(solution.getRibbonOrder(testValue), expectedResult, msg=f'Test {testValue} failed')

if __name__ == "__main__":
    unittest.main()