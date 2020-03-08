import unittest
import parseGEDCOM

class us13Test(unittest.TestCase):
    def testUS13(self):
        self.assertEqual(parseGEDCOM.checkUS13(),
        	"ANOMALY: FAMILY: US13: @F2@Individual (@I2@) spacing is too large from sibling (@I16@)\n")

if __name__ == "__main__":
    unittest.main()