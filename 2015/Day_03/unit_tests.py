import unittest
import solution

class TestMain(unittest.TestCase):
    def test_part1(self):
        testCases = []
        testCases.append(('>', 2))
        testCases.append(('^>v<', 4))
        testCases.append(('^v^v^v^v^v', 2))
        
        for testValue, expectedResult in testCases:
            self.assertEqual(solution.getHouseCount(testValue), expectedResult, msg=f'Test {testValue} failed')

    def test_part2(self):
        testCases = []
        testCases.append(('^v', 3))
        testCases.append(('^>v<', 3))
        testCases.append(('^v^v^v^v^v', 11))

        for testValue, expectedResult in testCases:
            self.assertEqual(solution.getRoboHouseCount(testValue), expectedResult, msg=f'Test {testValue} failed')

if __name__ == "__main__":
    unittest.main()