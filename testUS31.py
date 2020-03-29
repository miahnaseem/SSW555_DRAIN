import unittest
import parseGEDCOM


class us31Test(unittest.TestCase):
    def testUS31(self):
        self.assertEqual(parseGEDCOM.checkUS31(),
            "US31: Living and Single:\n"+
            "@I13@ Fredrick /Alister/\n" +
            "@I30@ Dave /Martin/\n" +
            "@I31@ Dave /Martin/\n" +
            "@I32@ Dave3 /Martin/\n" +
            "@I33@ Dave4 /Martin/\n" +     
            "@I34@ Dave5 /Martin/\n" +
            "@I35@ Dave6 /Martin/\n" + 
            "@I36@ Dave7 /Martin/\n" +
            "@I37@ Dave8 /Martin/\n" +
            "@I38@ Dave9 /Martin/\n" +
            "@I39@ Dave10 /Martin/\n"+ 
            "@I40@ Dave11 /Martin/\n"+
            "@I41@ Dave11 /Martin/\n"+ 
            "@I42@ Dave13 /Martin/\n"+
            "@I43@ Dave14 /Martin/\n"+ 
            "@I44@ Dave15 /Martin/\n")

if __name__ == "__main__":
    unittest.main()