import unittest
import parseGEDCOM


class us08Test(unittest.TestCase):
    def testUS08(self):
        self.assertEqual(parseGEDCOM.checkUS08(),
            "ANOMALY: FAMILY: US08:  @F3@ : Child (@I3@) born 1972-08-03 before marriage on 1980-05-24\n"+
        	"ANOMALY: FAMILY: US08:  @F3@ : Child (@I8@) born 1973-03-05 before marriage on 1980-05-24\n"+
        	"ANOMALY: FAMILY: US08:  @F4@ : Child (@I20@) born 1800-07-28 before marriage on 1950-08-04\n")


if __name__ == "__main__":
    unittest.main()
