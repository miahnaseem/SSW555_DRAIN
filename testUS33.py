import unittest
import parseGEDCOM


class us33Test(unittest.TestCase):
    def testUS33(self):
        self.assertEqual(parseGEDCOM.checkUS33(),
            "US33: Orphans:\n" +
            "@I47@ Travis /Swan/\n")

if __name__ == "__main__":
    unittest.main()