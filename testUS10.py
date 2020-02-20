import unittest
import parseGEDCOM

class Age150Test(unittest.TestCase):

    def testBoth14(self):
        self.assertEqual(parseGEDCOM.checkUS10(), "ANOMALY: FAMILY: US10: @I9@, @I8@: Husband and Wife married before the age of 14")
    def testHusb14(self):
        self.assertEqual(parseGEDCOM.checkUS07(), "ANOMALY: FAMILY: US10: @I14@: Husband married before the age of 14")
    def testWife14(self):
        self.assertEqual(parseGEDCOM.checkUS07(), "ANOMALY: FAMILY: US10: @I17@: Wife married before the age of 14")

if __name__ == "__main__":
    unittest.main()
