import unittest
import parseGEDCOM

class us17Test(unittest.TestCase):
    def testUS18(self):
        self.assertEqual(parseGEDCOM.checkUS18(), 
        	"ANOMALY: FAMILY: US18: @F12@: Individual (@I27@) is married to sibling (@I28@)\n")

if __name__ == "__main__":
    unittest.main()
