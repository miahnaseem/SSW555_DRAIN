import unittest
import parseGEDCOM


class us36Test(unittest.TestCase):
    def testUS37(self):
        self.assertEqual(parseGEDCOM.checkUS37(),
            "US36: Recent Survivors:\n" +
            "@I47@ Travis /Swan/\n")


if __name__ == "__main__":
    unittest.main()
