import unittest
import parseGEDCOM

class us10Test(unittest.TestCase):
    def testUS25(self):
        self.assertEqual(parseGEDCOM.checkUS25(),
        	"ERROR: FAMILY: US25: Family @F15@ has multiple individuals with the same first name Dave and birthday 2027-07-07\n" +
            "ERROR: FAMILY: US25: Family @F15@ has multiple individuals with the same first name Dave11 and birthday 2032-02-18\n")

if __name__ == "__main__":
    unittest.main()
