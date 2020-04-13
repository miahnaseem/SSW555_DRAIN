import unittest
import parseGEDCOM

class us27Test(unittest.TestCase):
    def testUS27(self):
        self.assertEqual(parseGEDCOM.checkUS27(), 
			"")
if __name__ == "__main__":
    unittest.main()