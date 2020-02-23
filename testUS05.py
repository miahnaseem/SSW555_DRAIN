import unittest
import parseGEDCOM

class us05Test(unittest.TestCase):
	def testUS05(self):
		self.assertEqual(parseGEDCOM.checkUS05(), 
			"ERROR: INDIVIDUAL: US05: @I16@: Death date 1970-07-02 is before marriage date 1999-09-07\n")

if __name__ == "__main__":
    unittest.main()