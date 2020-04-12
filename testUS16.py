import unittest
import parseGEDCOM

class us16Test(unittest.TestCase):
    def testUS16(self):
        self.assertEqual(parseGEDCOM.checkUS16(),
        	"ANOMALY: INDIVIDUAL: US16: Individual (@I16@) does not have a matching family last name\n")

if __name__ == "__main__":
    unittest.main()
