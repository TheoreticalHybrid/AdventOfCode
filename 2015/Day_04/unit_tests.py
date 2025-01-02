import unittest
import solution

class TestMain(unittest.TestCase):
    def test_part1(self):
        testCases = []
        testCases.append(('abcdef', 609043))
        testCases.append(('pqrstuv', 1048970))
        
        for testValue, expectedResult in testCases:
            self.assertEqual(solution.getLowestHashNumber(testValue, '00000'), expectedResult, msg=f'Test {testValue} failed')

    def test_part2(self):
        testCases = []
        #testCases.append(('', 0))

        for testValue, expectedResult in testCases:
            #self.assertEqual(solution.getFirstBasementIndex(testValue), expectedResult, msg=f'Test {testValue} failed')
            pass

if __name__ == "__main__":
    unittest.main()