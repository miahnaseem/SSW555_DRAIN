import unittest
import parseGEDCOM

class us22Test(unittest.TestCase):
    def testUS22(self):
        self.assertEqual(parseGEDCOM.checkUS22(), 
			"")
if __name__ == "__main__":
    unittest.main()