import unittest
import parseGEDCOM


class us24Test(unittest.TestCase):
    def testUS24(self):
        self.assertEqual(parseGEDCOM.checkUS24(),
            "ANOMALY: FAMILY: US24: @F16@: Family has same husband name, wife name, and marriage date as family @F14@")


if __name__ == "__main__":
    unittest.main()
