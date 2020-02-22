import unittest
import parseGEDCOM

class us02Test(unittest.TestCase):
    def testUS02(self):
        self.assertEqual(parseGEDCOM.checkUS02(), "ERROR: FAMILY: US09: @F5@: Birthday of (@I13@) on 2006-11-06 after husband's (@I12@) death on 1999-04-09\nERROR: FAMILY: US09: @F9@: Birthday of (@I17@) on 1974-11-01 after wife's (@I23@) death on 1973-02-05\nERROR: FAMILY: US09: @F10@: Birthday of (@I21@) on 1760-05-10 after husband's (@I25@) death on 1750-11-29 and wife's (@I24@) death on 1750-07-20\n")

if __name__ == "__main__":
    unittest.main()
