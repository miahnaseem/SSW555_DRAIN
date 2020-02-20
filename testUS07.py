import unittest
import parseGEDCOM

class Age150Test(unittest.TestCase):

    def testDeadAge(self):
        self.assertEqual(parseGEDCOM.checkUS07(), "ERROR: INDIVIDUAL: US07: @I20@: More than 150 years old at death - Birth 1800-07-28: Death 1980-10-27")
    def testAliveAge(self):
        self.assertEqual(parseGEDCOM.checkUS07(), "ERROR: INDIVIDUAL: US07: @I21@: More than 150 years old - Birth date 1760-05-10")

if __name__ == "__main__":
    unittest.main()
