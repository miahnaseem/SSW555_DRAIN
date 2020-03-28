import unittest
import parseGEDCOM


class us32Test(unittest.TestCase):
    def testUS32(self):
        self.assertEqual(parseGEDCOM.checkUS32(),
            "Multiple birthdays:\n" +
            "['2004-10-12', '1952-01-01', '2027-07-07', '2030-10-10', '2032-02-18']\n" 

if __name__ == "__main__":
    unittest.main()