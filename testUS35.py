import unittest
import parseGEDCOM


class us35Test(unittest.TestCase):
    def testUS35(self):
        self.assertEqual(parseGEDCOM.checkUS35(),
            "US35: Recent Births:\n"+
            "@I33@ Dave4 /Martin/ 2020-04-07\n" + 
            "@I36@ Dave7 /Martin/ 2020-04-01\n")
if __name__ == "__main__":
    unittest.main()

    
