import unittest
import parseGEDCOM

class us02Test(unittest.TestCase):
    def testUS02(self):
        self.assertEqual(parseGEDCOM.checkUS02(), "ERROR: INDIVIDUAL: US02: @I17@: Marriage is before Birth date 1974-11-01")

if __name__ == "__main__":
    unittest.main()
