import unittest
import parseGEDCOM

class us14Test(unittest.TestCase):
    def testUS14(self):
        self.assertEqual(parseGEDCOM.checkUS14(), 
        	"ANOMALY: FAMILY: US14: Family ( @F15@ ) has 5 or more children born on 2027-07-07\n"+
			"ANOMALY: FAMILY: US14: Family ( @F15@ ) has 5 or more children born on 2032-02-18\n")

if __name__ == "__main__":
    unittest.main()
