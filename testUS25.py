import unittest
import parseGEDCOM

class us10Test(unittest.TestCase):
    def testUS25(self):
        self.assertEqual(parseGEDCOM.checkUS25(),
        	"ANOMALY: FAMILY: US25: Family @F2@ has multiple individuals with the same first name Edward\n" +
            "ANOMALY: FAMILY: US25: Family @F6@ has multiple individuals with the same first name Elizabeth\n")

if __name__ == "__main__":
    unittest.main()
