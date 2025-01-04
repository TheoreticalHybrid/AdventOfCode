import unittest
import solution

class TestMain(unittest.TestCase):
    def test_part1(self):
        testCases = []
        testCases.append(('ugknbfddgicrmopn', True))
        testCases.append(('aaa', True))
        testCases.append(('jchzalrnumimnmhp', False))
        testCases.append(('haegwjzuvuyypxyu', False))
        testCases.append(('dvszwmarrgswjxmb', False))
        
        for testValue, expectedResult in testCases:
            self.assertEqual(solution.stringIsNice(testValue), expectedResult, msg=f'Test {testValue} failed')

    def test_part2(self):
        testCases = []
        testCases.append(('qjhvhtzxzqqjkmpb', True))
        testCases.append(('xxyxx', True))
        testCases.append(('uurcxstgmygtbstg', False))
        testCases.append(('ieodomkazucvgmuy', False))

        for testValue, expectedResult in testCases:
            self.assertEqual(solution.stringIsNicePartTwo(testValue), expectedResult, msg=f'Test {testValue} failed')

if __name__ == "__main__":
    unittest.main()