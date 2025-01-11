import unittest
import solution

class TestMain(unittest.TestCase):
    def test_part1(self):
        testCases = []
        testCases.append(('hijklmmn', False))
        testCases.append(('abbceffg', False))
        testCases.append(('abbcegjk', False))
        testCases.append(('abcdffaa', True))
        testCases.append(('ghjaabcc', True))
        
        for testValue, expectedResult in testCases:
            self.assertEqual(solution.isValidPassword(testValue), expectedResult, msg=f'Test {testValue} failed')

        testCases = []
        testCases.append(('abcdefgh', 'abcdffaa'))
        testCases.append(('ghijklmn', 'ghjaabcc'))

        for testValue, expectedResult in testCases:
            self.assertEqual(solution.getNextPassword(testValue), expectedResult, msg=f'Test {testValue} failed')

    def test_part2(self):
        testCases = []
        #testCases.append(('', 0))

        for testValue, expectedResult in testCases:
            #self.assertEqual(solution.getFirstBasementIndex(testValue), expectedResult, msg=f'Test {testValue} failed')
            pass

if __name__ == "__main__":
    unittest.main()