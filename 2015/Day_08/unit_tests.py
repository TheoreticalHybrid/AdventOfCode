import unittest
import solution

class TestMain(unittest.TestCase):
    def test_part1(self):
        testCases = []
        testCases.append((r'""', 0))
        testCases.append((r'"abc"', 3))
        testCases.append((r'"aaa\"aaa"', 7))
        testCases.append((r'"aaa\\aaa"', 7))
        testCases.append((r'"\x27"', 1))
        
        for testValue, expectedResult in testCases:
            self.assertEqual(solution.getNumCharacters(testValue), expectedResult, msg=f'Test {testValue} failed')

        allValues = [tc[0] for tc in testCases]
        self.assertEqual(solution.getCharacterDiscrepancy(allValues, False), 15, msg=f'Final Result Test failed')

    def test_part2(self):
        testCases = []
        testCases.append((r'""', 6))
        testCases.append((r'"abc"', 9))
        testCases.append((r'"aaa\"aaa"', 16))
        testCases.append((r'"aaa\\aaa"', 16))
        testCases.append((r'"\x27"', 11))

        for testValue, expectedResult in testCases:
            self.assertEqual(solution.getEncodedStringLength(testValue), expectedResult, msg=f'Test {testValue} failed')
        
        allValues = [tc[0] for tc in testCases]
        self.assertEqual(solution.getCharacterDiscrepancy(allValues, True), 25, msg=f'Final Result Test failed')

if __name__ == "__main__":
    unittest.main()