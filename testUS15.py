import unittest
import parseGEDCOM

class us15Test(unittest.TestCase):
    def testUS15(self):
        self.assertEqual(parseGEDCOM.checkUS15(), 
        	"ANOMALY: FAMILY: US15: Family ( @F15@ ) has 15 or more children\n")

if __name__ == "__main__":
    unittest.main()
