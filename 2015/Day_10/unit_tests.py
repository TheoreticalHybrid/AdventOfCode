import unittest
import solution

class TestMain(unittest.TestCase):
    def test_part1(self):
        testCases = []
        testCases.append(('1', '11'))
        testCases.append(('11', '21'))
        testCases.append(('21', '1211'))
        testCases.append(('1211', '111221'))
        testCases.append(('111221', '312211'))
        
        for testValue, expectedResult in testCases:
            self.assertEqual(solution.applySequence(testValue), expectedResult, msg=f'Test {testValue} failed')

        self.assertEqual(solution.repeatSequence('1', 5), '312211', msg=f'Full test failed')
        
    def test_part2(self):
        testCases = []
        #testCases.append(('', 0))

        for testValue, expectedResult in testCases:
            #self.assertEqual(solution.getFirstBasementIndex(testValue), expectedResult, msg=f'Test {testValue} failed')
            pass

if __name__ == "__main__":
    unittest.main()