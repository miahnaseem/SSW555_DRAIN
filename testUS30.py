import unittest
import parseGEDCOM


class us30Test(unittest.TestCase):
    def testUS30(self):
        self.assertEqual(parseGEDCOM.checkUS30(),
            "Living and Married:\n" +
            "@I1@ Adeline /Bloom/ 01 JAN 2020\n" +
            "@I2@ Nicholas /Bloom/ 3 MAY 1998\n" +
            "@I3@ Cassandra /Swan/ 3 MAY 1998\n" +
            "@I5@ Jayde /Bloom/ 08 MAR 2020\n" +
            "@I6@ John /Swan/ 24 MAY 1980\n" +
            "@I7@ Selina /Moon/ 24 MAY 1980\n" +
            "@I8@ Elizabeth /Swan/ 08 MAR 2020\n" +
            "@I10@ Ariel /Turner/ 01 JAN 2020\n" +
            "@I11@ Lysandra /Turner/ 10 MAY 2020\n" +
            "@I14@ Edward /Bloom/ 3 JAN 1963\n" +
            "@I15@ Fiona /Green/ 3 JAN 1963\n" +
            "@I17@ Kevinne /Draw/ 11 NOV 1900\n" +
            "@I21@ Ryan /Nakajima/ 11 NOV 1900\n" +
            "@I22@ Cosmo /Draw/ 7 OCT 1970\n" +
            "@I26@ Neko /Nakajima/ 01 SEP 2019\n" +
            "@I27@ Lionel /Swan/ 02 NOV 1972\n" +
            "@I28@ Kathy /Swan/ 02 NOV 1972\n" +
            "@I29@ Jonathan /Martin/ 10 MAY 2020\n")


if __name__ == "__main__":
    unittest.main()
