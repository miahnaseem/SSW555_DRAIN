import unittest
import parseGEDCOM

class us12Test(unittest.TestCase):
    def testUS12(self):
        self.assertEqual(parseGEDCOM.checkUS12(),
        	"ANOMALY: FAMILY: US12:  @F4@ Parent is too old to hav (@I20@)\n")

if __name__ == "__main__":
    unittest.main()