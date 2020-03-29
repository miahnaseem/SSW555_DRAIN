import unittest
import parseGEDCOM


class us29Test(unittest.TestCase):
    def testUS29(self):
        self.assertEqual(parseGEDCOM.checkUS29(),
            "US29: Deceased:\n" +
            "@I4@ James /Bloom/ 1994-11-10\n" +
            "@I9@ William /Turner/ 2002-08-04\n" +
            "@I12@ Eric /Alister/ 1999-04-09\n" +
            "@I16@ David /Test/ 1970-07-02\n" +
            "@I18@ Charlie /Swan/ 1990-11-09\n" +
            "@I19@ Serena /Prince/ 2000-09-01\n" +
            "@I20@ Leanna /Swan/ 1980-10-27\n" +
            "@I23@ Wanda /Smith/ 1973-02-05\n" +
            "@I24@ Annabeth /Chase/ 1750-07-20\n" +
            "@I25@ Percy /Nakajima/ 1750-11-29\n")


if __name__ == "__main__":
    unittest.main()
