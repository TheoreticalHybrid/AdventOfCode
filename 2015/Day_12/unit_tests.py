import unittest
import solution

class TestMain(unittest.TestCase):
    def test_part1(self):
        testCount = 1
        testCases = []
        testCases.append(('[1,2,3]', 6))
        testCases.append(('{"a":2,"b":4}', 6))
        testCases.append(('[[[3]]]', 3))
        testCases.append(('{"a":{"b":4},"c":-1}', 3))
        testCases.append(('{"a":[-1,1]}', 0))
        testCases.append(('[-1,{"a":1}]', 0))
        testCases.append(('[]', 0))
        testCases.append((r'{}', 0))
        
        for testValue, expectedResult in testCases:
            self.assertEqual(solution.getSumOfNumbers(testValue), expectedResult, msg=f'Test {testCount} ({testValue}) failed')
            testCount += 1

    def test_part2(self):
        testCount = 1
        testCases = []
        testCases.append(('[1,2,3,-2]', 4))
        testCases.append(('{"d":"red","e":[1,2,3,4],"f":5}', 0))
        testCases.append(('[1,{"c":"red","b":2},3]', 4))
        testCases.append(('[1,"red",5]', 6))
        testCases.append(('{"e":[1,2,3], "a":"red"}', 0))
        testCases.append(('{"e":[1,2,3], "f":{"a":"red", "b":7}, "g":"foo"}', 6))
        testCases.append(('{"e":[1,2,3], "f":{"a":[1,2,3]}, "g":"red"}', 0))

        for testValue, expectedResult in testCases:
            self.assertEqual(solution.getSumOfNumbersIgnoringRedObjects(testValue), expectedResult, msg=f'Test {testCount} ({testValue}) failed')
            testCount += 1

if __name__ == "__main__":
    unittest.main()