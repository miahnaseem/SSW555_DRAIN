import unittest
import parseGEDCOM

class us26Test(unittest.TestCase):
    def testUS26(self):
        self.assertEqual(parseGEDCOM.checkUS26(), 
        	"ERROR: INDIVIDUAL: US26: Individual @I50@ is listed but does not appear in a family.\n")

if __name__ == "__main__":
    unittest.main()
