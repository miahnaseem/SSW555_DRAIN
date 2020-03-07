import unittest
import parseGEDCOM

class us10Test(unittest.TestCase):
    def testUS10(self):
        self.assertEqual(parseGEDCOM.checkUS10(),
        	"ANOMALY: FAMILY: US10: @F1@: Husband (@I2@) married before the age of 14\n"
        	"ANOMALY: FAMILY: US10: @F2@: Husband (@I14@) married before the age of 14\n"+
        	"ANOMALY: FAMILY: US10: @F6@: Husband (@I9@) and Wife (@I8@) married before the age of 14\n"+
        	"ANOMALY: FAMILY: US10: @F8@: Wife (@I17@) married before the age of 14\n")

if __name__ == "__main__":
    unittest.main()
