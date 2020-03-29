import unittest
import parseGEDCOM

class us21Test(unittest.TestCase):
    def testUS21(self):
        self.assertEqual(parseGEDCOM.checkUS21(), 
			"ANOMALY: FAMILY: US21: @F3@: Husband (@I6@) is not marked as male\n"+
			"ANOMALY: FAMILY: US21: @F13@: Husband (@I1@) is not marked as male\n"+
			"ANOMALY: FAMILY: US21: @F13@: Wife (@I10@) is not marked as female\n"+
			"ANOMALY: FAMILY: US21: @F14@: Husband (@I5@) is not marked as male\n")
if __name__ == "__main__":
    unittest.main()