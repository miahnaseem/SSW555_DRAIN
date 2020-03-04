import unittest
import parseGEDCOM

class us06Test(unittest.TestCase):
    def testUS06(self):
        self.assertEqual(parseGEDCOM.checkUS06(), 
        	"ERROR: INDIVIDUAL: US06: @I16@: Death date 1970-07-02 is before divorce date 1982-11-11\n")

if __name__ == "__main__":
    unittest.main()
