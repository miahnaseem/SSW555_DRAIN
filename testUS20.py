import unittest
import parseGEDCOM

class us20Test(unittest.TestCase):
    def testUS20(self):
        self.assertEqual(parseGEDCOM.checkUS20(), 
        	"ANOMALY: FAMILY: US20: @F14@: Individual (@I5@) is married to parent's sibling (@I8@)\n")

if __name__ == "__main__":
    unittest.main()
