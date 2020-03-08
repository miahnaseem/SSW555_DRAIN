import unittest
import parseGEDCOM

class us19Test(unittest.TestCase):
    def testUS19(self):
        self.assertEqual(parseGEDCOM.checkUS19(), 
        	"ERROR: FAMILY: US19: @F13@: Individual (@I1@) is married to first cousin (@I10@)")

if __name__ == "__main__":
    unittest.main()
