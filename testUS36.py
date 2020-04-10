import unittest
import parseGEDCOM


class us36Test(unittest.TestCase):
    def testUS36(self):
        self.assertEqual(parseGEDCOM.checkUS36(),
            "US36: Recent Deaths:\n"+
            "@I45@ Jayde /Bloom/ 2020-03-27\n" +
            "@I46@ Elizabeth /Swan/ 2020-03-29\n")


if __name__ == "__main__":
    unittest.main()
