import unittest
import parseGEDCOM

class us23Test(unittest.TestCase):
    def testUS23(self):
        self.assertEqual(parseGEDCOM.checkUS23(), 
			"ERROR: INDIVIDUAL: US23: @I31@: Individual (@I31@) has the same name \"Dave /Martin/\" and birthdate 2027-07-07 as other individual(s) (@I30@)\n"+
			"ERROR: INDIVIDUAL: US23: @I32@: Individual (@I32@) has the same name \"Dave /Martin/\" and birthdate 2027-07-07 as other individual(s) (@I30@, @I31@)\n")
if __name__ == "__main__":
    unittest.main()
