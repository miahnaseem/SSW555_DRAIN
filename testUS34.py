import unittest
import parseGEDCOM


class us34Test(unittest.TestCase):
    def testUS34(self):
        self.assertEqual(parseGEDCOM.checkUS34(),
            "US34: Large Age Differences:\n"+
            "@I2@, born on 2070-07-04, married @I3@, born on 1972-08-03, on 1998-05-03.\n" + 
            "@I14@, born on 1970-04-03, married @I15@, born on 1948-06-04, on 1963-01-03.\n" + 
            "@I6@, born on 1950-12-27, married @I7@, born on 1913-08-25, on 1980-05-24.\n" + 
            "@I16@, born on 1975-04-05, married @I17@, born on 2010-11-01, on 1999-09-07.\n" + 
            "@I21@, born on 1760-05-10, married @I17@, born on 2010-11-01, on 1900-11-11.\n" + 
            "@@I26@, born on 1999-08-09, married @I17@, born on 2010-11-01, on 2019-09-01.\n" + 
            "@I5@, born on 2004-10-12, married @I8@, born on 1973-03-05, on 2020-03-08.\n")

if __name__ == "__main__":
    unittest.main()







