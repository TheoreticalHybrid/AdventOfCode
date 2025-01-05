import unittest
import solution

class TestMain(unittest.TestCase):
    def test_part1(self):
        testCases = []
        testCases.append((['AND',13,28], 12))
        testCases.append((['AND',50,17], 16))
        testCases.append((['OR',37,69], 101))
        testCases.append((['OR',15,88], 95))
        testCases.append((['LSHIFT',14,3], 112))
        testCases.append((['RSHIFT',36,1], 18))
        testCases.append((['NOT',0], 65535))
        testCases.append((['NOT',65535], 0))
        testCases.append((['NOT',43690], 21845))
        testCases.append((['LSHIFT',0,1], 0))
        
        for testValue, expectedResult in testCases:
            match testValue[0]:
                case 'AND':
                    self.assertEqual(solution.performBitwiseAnd(testValue[1], testValue[2]), expectedResult, msg=f'Test {testValue} failed')
                case 'OR':
                    self.assertEqual(solution.performBitwiseOr(testValue[1], testValue[2]), expectedResult, msg=f'Test {testValue} failed')
                case 'LSHIFT':
                    self.assertEqual(solution.performLeftShift(testValue[1], testValue[2]), expectedResult, msg=f'Test {testValue} failed')
                case 'RSHIFT':
                    self.assertEqual(solution.performRightShift(testValue[1], testValue[2]), expectedResult, msg=f'Test {testValue} failed')
                case 'NOT':
                    self.assertEqual(solution.performBitwiseNot(testValue[1]), expectedResult, msg=f'Test {testValue} failed')

        testInstructions = []
        testInstructions.append('x AND y -> d')
        testInstructions.append('x OR y -> e')
        testInstructions.append('123 -> x')
        testInstructions.append('x LSHIFT 2 -> f')
        testInstructions.append('y RSHIFT 2 -> g')
        testInstructions.append('NOT x -> h')
        testInstructions.append('NOT y -> i')
        testInstructions.append('456 -> y')

        self.assertEqual(solution.buildCircuit(testInstructions, 'd'), 72, msg=f'Test d failed')
        self.assertEqual(solution.buildCircuit(testInstructions, 'e'), 507, msg=f'Test e failed')
        self.assertEqual(solution.buildCircuit(testInstructions, 'f'), 492, msg=f'Test f failed')
        self.assertEqual(solution.buildCircuit(testInstructions, 'g'), 114, msg=f'Test g failed')
        self.assertEqual(solution.buildCircuit(testInstructions, 'h'), 65412, msg=f'Test h failed')
        self.assertEqual(solution.buildCircuit(testInstructions, 'i'), 65079, msg=f'Test i failed')
        self.assertEqual(solution.buildCircuit(testInstructions, 'x'), 123, msg=f'Test x failed')
        self.assertEqual(solution.buildCircuit(testInstructions, 'y'), 456, msg=f'Test y failed')

if __name__ == "__main__":
    unittest.main()