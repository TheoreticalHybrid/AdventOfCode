import unittest
import solution

class TestMain(unittest.TestCase):
    def test_part1(self):
        testInput = []
        testInput.append('London to Dublin = 464')
        testInput.append('London to Belfast = 518')
        testInput.append('Dublin to Belfast = 141')

        testLocations = solution.processMapData(testInput)
        self.assertIn('London', testLocations)
        self.assertIn('Dublin', testLocations)
        self.assertIn('Belfast', testLocations)

        testCases = [] #Expected successes
        testCases.append((('London', 'Dublin'), 464))
        testCases.append((('London', 'Belfast'), 518))
        testCases.append((('Dublin', 'Belfast'), 141))
        testCases.append((('Dublin', 'London'), 464))
        testCases.append((('Belfast', 'London'), 518))
        testCases.append((('Belfast', 'Dublin'), 141))
        
        for testValue, expectedResult in testCases:
            self.assertEqual(solution.getDistance(*testValue), expectedResult, msg=f'Test {testValue} failed')
            pass

        testCases = [] #Expected Exceptions
        testCases.append((('London', 'Kansas City'), 1337)) # 2nd Location not recognized as route from 1st Location
        testCases.append((('Kansas City', 'London'), 1988)) # 1st Location not recognized

        for testValue, expectedResult in testCases:
            with self.assertRaises(KeyError):
                solution.getDistance(*testValue)

        fullTestExpectedValue = (['London', 'Dublin', 'Belfast'], 605)
        shortestDistances = solution.getBestRoutes(testLocations, True)
        self.assertIn(fullTestExpectedValue, shortestDistances, msg=f'Full test failed')

    def test_part2(self):
        testInput = []
        testInput.append('London to Dublin = 464')
        testInput.append('London to Belfast = 518')
        testInput.append('Dublin to Belfast = 141')

        testLocations = solution.processMapData(testInput)
        self.assertIn('London', testLocations)
        self.assertIn('Dublin', testLocations)
        self.assertIn('Belfast', testLocations)

        fullTestExpectedValue = (['Dublin', 'London', 'Belfast'], 982)
        longestDistances = solution.getBestRoutes(testLocations, False)
        self.assertIn(fullTestExpectedValue, longestDistances, msg=f'Full test failed')

if __name__ == "__main__":
    unittest.main()