import unittest
import parseGEDCOM

class us17Test(unittest.TestCase):
    def testUS07(self):
        self.assertEqual(parseGEDCOM.checkUS17(), 
        	"ANOMALY: FAMILY: US17: @F11@: Wife (@I17@) marries Child (@I26@)\n")

if __name__ == "__main__":
    unittest.main()
