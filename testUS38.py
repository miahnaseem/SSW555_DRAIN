import unittest
import parseGEDCOM

class us38Test(unittest.TestCase):
    def testUS38(self):
        self.assertEqual(parseGEDCOM.checkUS38(),
            "US38: Upcoming Birthdays:\n"+
            "@I21@ has an upcoming birthday on 05-10\n")

if __name__ == "__main__":
    unittest.main()
