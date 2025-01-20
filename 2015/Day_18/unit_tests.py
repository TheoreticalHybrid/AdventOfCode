import unittest
import solution

class TestMain(unittest.TestCase):
    def test_part1(self):
        testCount = 1
        testGrid = [[0,1,0,1,0,1],[0,0,0,1,1,0],[1,0,0,0,0,1],[0,0,1,0,0,0],[1,0,1,0,0,1],[1,1,1,1,0,0]]

        testCases = []
        testCases.append((1, ([[0,0,1,1,0,0],[0,0,1,1,0,1],[0,0,0,1,1,0],[0,0,0,0,0,0],[1,0,0,0,0,0],[1,0,1,1,0,0]], 11)))
        testCases.append((2, ([[0,0,1,1,1,0],[0,0,0,0,0,0],[0,0,1,1,1,0],[0,0,0,0,0,0],[0,1,0,0,0,0],[0,1,0,0,0,0]], 8)))
        testCases.append((3, ([[0,0,0,1,0,0],[0,0,0,0,0,0],[0,0,0,1,0,0],[0,0,1,1,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]], 4)))
        testCases.append((4, ([[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,1,1,0,0],[0,0,1,1,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]], 4)))
        
        for testValue, expectedResult in testCases:
            finishedGrid = solution.animateGrid(testGrid, testValue, False)
            self.assertEqual(finishedGrid, expectedResult[0], msg=f'Test {testCount} ({testValue}) failed')
            gridLightCount = sum([sum(r) for r in finishedGrid])
            self.assertEqual(gridLightCount, expectedResult[1], msg=f'Test {testCount} failed the number check')
            testCount += 1

    def test_part2(self):
        testCount = 1
        testGrid = [[0,1,0,1,0,1],[0,0,0,1,1,0],[1,0,0,0,0,1],[0,0,1,0,0,0],[1,0,1,0,0,1],[1,1,1,1,0,0]]

        testCases = []
        testCases.append((1, ([[1,0,1,1,0,1],[1,1,1,1,0,1],[0,0,0,1,1,0],[0,0,0,0,0,0],[1,0,0,0,1,0],[1,0,1,1,1,1]], 18)))
        testCases.append((2, ([[1,0,0,1,0,1],[1,0,0,0,0,1],[0,1,0,1,1,0],[0,0,0,1,1,0],[0,1,0,0,1,1],[1,1,0,1,1,1]], 18)))
        testCases.append((3, ([[1,0,0,0,1,1],[1,1,1,1,0,1],[0,0,1,1,0,1],[0,0,0,0,0,0],[1,1,0,0,0,0],[1,1,1,1,0,1]], 18)))
        testCases.append((4, ([[1,0,1,1,1,1],[1,0,0,0,0,1],[0,0,0,1,0,0],[0,1,1,0,0,0],[1,0,0,0,0,0],[1,0,1,0,0,1]], 14)))
        testCases.append((5, ([[1,1,0,1,1,1],[0,1,1,0,0,1],[0,1,1,0,0,0],[0,1,1,0,0,0],[1,0,1,0,0,0],[1,1,0,0,0,1]], 17)))
        
        for testValue, expectedResult in testCases:
            finishedGrid = solution.animateGrid(testGrid, testValue, True)
            self.assertEqual(finishedGrid, expectedResult[0], msg=f'Test {testCount} ({testValue}) failed')
            gridLightCount = sum([sum(r) for r in finishedGrid])
            self.assertEqual(gridLightCount, expectedResult[1], msg=f'Test {testCount} failed the number check')
            testCount += 1

if __name__ == "__main__":
    unittest.main()