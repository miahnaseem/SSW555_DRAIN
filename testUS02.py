import unittest
import parseGEDCOM

class us02Test(unittest.TestCase):
    def testUS02(self):
        self.assertEqual(parseGEDCOM.checkUS02(), 
        	"ERROR: INDIVIDUAL: US02: @I2@: Marriage date 1998-05-03 is before Birth date 2070-07-04\n"+
        	"ERROR: INDIVIDUAL: US02: @I14@: Marriage date 1963-01-03 is before Birth date 1970-04-03\n"+
        	"ERROR: INDIVIDUAL: US02: @I17@: Marriage date 1900-11-11 is before Birth date 1974-11-01\n")

if __name__ == "__main__":
    unittest.main()
