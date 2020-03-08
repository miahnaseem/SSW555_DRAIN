import unittest
import parseGEDCOM

class us11Test(unittest.TestCase):
    def testUS11(self):
        self.assertEqual(parseGEDCOM.checkUS11(),
        	"ANOMALY: INDIVIDUAL: US11: Individual (@I17@) married to multiple people at the same time\n")

if __name__ == "__main__":
    unittest.main()
