import unittest
import parseGEDCOM

class us42Test(unittest.TestCase):
    def testUS42(self):
        self.assertEqual(parseGEDCOM.checkUS42(), 
        	"ERROR: INDIVIDUAL: US42: @I48@ contains illegitimate birth date 31 APR 2000 which may cause the date to appear incorrectly.\n"+
        	"ERROR: INDIVIDUAL: US42: @I48@ contains illegitimate death date 35 FEB 2005 which may cause the date to appear incorrectly.\n"+
        	"ERROR: FAMILY: US42: @F17@ contains illegitimate marriage date 40 NOV 2002 which may cause the date to appear incorrectly.\n"+
        	"ERROR: FAMILY: US42: @F17@ contains illegitimate divorce date 70 DEC 2002 which may cause the date to appear incorrectly.\n")

if __name__ == "__main__":
    unittest.main()
