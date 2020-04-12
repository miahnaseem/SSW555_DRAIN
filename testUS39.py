import unittest
import parseGEDCOM

class us39Test(unittest.TestCase):
    def testUS39(self):
        self.assertEqual(parseGEDCOM.checkUS39(),
            "US39: Upcoming Anniversaries:\n"+
            "@F1@ has an upcoming anniversary on 05-03\n"+
            "@F15@ has an upcoming anniversary on 05-10\n")

if __name__ == "__main__":
    unittest.main()
