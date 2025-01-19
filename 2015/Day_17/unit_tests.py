import unittest
import solution

class TestMain(unittest.TestCase):
    def test_part1(self):
        testCount = 1
        testContainers = [20, 15, 10, 5, 5]

        self.assertEqual(solution.getContainerCombinations(25, testContainers), 4, msg=f'Final Test Failed')

    def test_part2(self):
        testCount = 1
        testContainers = [20, 15, 10, 5, 5]

        combos = solution.getContainerCombinationLists(25, testContainers)
        self.assertEqual(len(combos), 4, msg='New method not retrieving the correct number of combinations')
        minLength = len(min(combos, key=len))
        self.assertEqual(minLength, 2, msg='Minimum combo length is incorrect')
        self.assertEqual(len([c for c in combos if len(c) == minLength]), 3, msg='Final Test Failed')

if __name__ == "__main__":
    unittest.main()