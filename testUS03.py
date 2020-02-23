import unittest
import parseGEDCOM

class us03Test(unittest.TestCase):
    def testUS03(self):
        self.assertEqual(parseGEDCOM.checkUS02(), "ERROR: INDIVIDUAL: US03: @I4@: Death date 1994-11-10 is before Birth date 2004-10-12")

if __name__ == "__main__":
    unittest.main()
