import unittest
import parseGEDCOM

class us01Test(unittest.TestCase):
    def testUS01(self):
        self.assertEqual(parseGEDCOM.checkUS01(), 
        	"ERROR: INDIVIDUAL: US01: @I2@: Birth date 2070-07-04 is after current date 2020-03-29\n"+
        	"ERROR: INDIVIDUAL: US01: @I30@: Birth date 2027-07-07 is after current date 2020-03-29\n"+
			"ERROR: INDIVIDUAL: US01: @I31@: Birth date 2027-07-07 is after current date 2020-03-29\n"+
			"ERROR: INDIVIDUAL: US01: @I32@: Birth date 2027-07-07 is after current date 2020-03-29\n"+
			"ERROR: INDIVIDUAL: US01: @I33@: Birth date 2027-07-07 is after current date 2020-03-29\n"+
			"ERROR: INDIVIDUAL: US01: @I34@: Birth date 2027-07-07 is after current date 2020-03-29\n"+
			"ERROR: INDIVIDUAL: US01: @I35@: Birth date 2030-10-10 is after current date 2020-03-29\n"+
			"ERROR: INDIVIDUAL: US01: @I36@: Birth date 2030-10-10 is after current date 2020-03-29\n"+
			"ERROR: INDIVIDUAL: US01: @I37@: Birth date 2030-10-10 is after current date 2020-03-29\n"+
			"ERROR: INDIVIDUAL: US01: @I38@: Birth date 2030-10-10 is after current date 2020-03-29\n"+
			"ERROR: INDIVIDUAL: US01: @I39@: Birth date 2032-02-18 is after current date 2020-03-29\n"+
			"ERROR: INDIVIDUAL: US01: @I40@: Birth date 2032-02-18 is after current date 2020-03-29\n"+
			"ERROR: INDIVIDUAL: US01: @I41@: Birth date 2032-02-18 is after current date 2020-03-29\n"+
			"ERROR: INDIVIDUAL: US01: @I42@: Birth date 2032-02-18 is after current date 2020-03-29\n"+
			"ERROR: INDIVIDUAL: US01: @I43@: Birth date 2032-02-18 is after current date 2020-03-29\n"+
			"ERROR: INDIVIDUAL: US01: @I44@: Birth date 2032-02-18 is after current date 2020-03-29\n"+
			"ERROR: INDIVIDUAL: US01: @I44@: Marriage date 2020-05-10 is after current date 2020-03-29\n")

if __name__ == "__main__":
    unittest.main()
