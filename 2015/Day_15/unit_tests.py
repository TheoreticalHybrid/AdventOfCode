import unittest
import solution

class TestMain(unittest.TestCase):
    def test_part1(self):
        testCount = 1
        ingredients = dict()
        ingredients['Butterscotch'] = (-1, -2, 6, 3, 8)
        ingredients['Cinnamon'] = (2, 3, -2, -1, 3)

        self.assertEqual(solution.getOptimalIngredientScore(ingredients, False), 62842880, msg=f'Final test failed')

    def test_part2(self):
        testCount = 1
        ingredients = dict()
        ingredients['Butterscotch'] = (-1, -2, 6, 3, 8)
        ingredients['Cinnamon'] = (2, 3, -2, -1, 3)

        self.assertEqual(solution.getOptimalIngredientScore(ingredients, True), 57600000, msg=f'Final test failed')

if __name__ == "__main__":
    unittest.main()