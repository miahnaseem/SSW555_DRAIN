import unittest
import parseGEDCOM

class us01Test(unittest.TestCase):
    def testUS01(self):
        self.assertEqual(parseGEDCOM.checkUS02(), "ERROR: INDIVIDUAL: US01: @I2@: Birth date 2070-07-04 is after current date 2020-02-23")

if __name__ == "__main__":
    unittest.main()
