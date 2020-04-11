import unittest
import parseGEDCOM

class us10Test(unittest.TestCase):
    def testUS28(self):
        self.assertEqual(parseGEDCOM.checkUS28(),
        	"US28: Siblings from oldest to youngest:\n" +
            "Family @F1@: @I1@, @I4@, @I5@\n" +
            "Family @F2@: @I16@, @I2@\n" +
            "Family @F3@: @I3@, @I8@\n" +
            "Family @F4@: @I20@, @I6@\n" +
            "Family @F5@: @I13@\n" +
            "Family @F6@: @I11@, @I10@\n" +
            "Family @F7@: \n" +
            "Family @F8@: @I26@\n" +
            "Family @F9@: @I17@\n" +
            "Family @F10@: @I21@\n" +
            "Family @F11@: \n" +
            "Family @F12@: \n" +
            "Family @F13@: \n" +
            "Family @F14@: \n" +
            "Family @F15@: @I30@, @I31@, @I32@, @I33@, @I34@, @I35@, @I36@, @I37@, @I38@, @I39@, @I40@, @I41@, @I42@, @I43@, @I44@\n")

if __name__ == "__main__":
    unittest.main()
