import unittest
import solution

class TestMain(unittest.TestCase):
    def test_part1(self):
        testCases = []
        testCases.append(('(())', 0))
        testCases.append(('()()', 0))
        testCases.append(('(((', 3))
        testCases.append(('(()(()(', 3))
        testCases.append(('))(((((', 3))
        testCases.append(('())', -1))
        testCases.append(('))(', -1))
        testCases.append((')))', -3))
        testCases.append((')())())', -3))
        
        for testValue, expectedResult in testCases:
            self.assertEqual(solution.getEndingFloor(testValue), expectedResult, msg=f'Test {testValue} failed')

    def test_part2(self):
        testCases = []
        testCases.append((')', 1))
        testCases.append(('()())', 5))

        for testValue, expectedResult in testCases:
            self.assertEqual(solution.getFirstBasementIndex(testValue), expectedResult, msg=f'Test {testValue} failed')

if __name__ == "__main__":
    unittest.main()