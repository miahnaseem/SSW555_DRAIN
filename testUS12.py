import unittest
import parseGEDCOM

class us12Test(unittest.TestCase):
    def testUS12(self):
        self.assertEqual(parseGEDCOM.checkUS12(),
        	"ANOMALY: FAMILY: US12: @F1@ Parent is too old to have (@I1@)\n" +
            "ANOMALY: FAMILY: US12: @F1@ Parent is too old to have (@I4@)\n" +
            "ANOMALY: FAMILY: US12: @F1@ Parent is too old to have (@I5@)\n" +
            "ANOMALY: FAMILY: US12: @F2@ Parent is too old to have (@I2@)\n" +
            "ANOMALY: FAMILY: US12: @F2@ Parent is too old to have (@I16@)\n" +
            "ANOMALY: FAMILY: US12: @F3@ Parent is too old to have (@I3@)\n" +
            "ANOMALY: FAMILY: US12: @F3@ Parent is too old to have (@I8@)\n" +
            "ANOMALY: FAMILY: US12: @F4@ Parent is too old to have (@I6@)\n" +
            "ANOMALY: FAMILY: US12: @F4@ Parent is too old to have (@I20@)\n" +
            "ANOMALY: FAMILY: US12: @F5@ Parent is too old to have (@I13@)\n" +
            "ANOMALY: FAMILY: US12: @F6@ Parent is too old to have (@I10@)\n" +
            "ANOMALY: FAMILY: US12: @F6@ Parent is too old to have (@I11@)\n" +
            "ANOMALY: FAMILY: US12: @F8@ Parent is too old to have (@I26@)\n" +
            "ANOMALY: FAMILY: US12: @F9@ Parent is too old to have (@I17@)\n" +
            "ANOMALY: FAMILY: US12: @F10@ Parent is too old to have (@I21@)\n" +
            "ANOMALY: FAMILY: US12: @F15@ Parent is too old to have (@I30@)\n" +
            "ANOMALY: FAMILY: US12: @F15@ Parent is too old to have (@I31@)\n" +
            "ANOMALY: FAMILY: US12: @F15@ Parent is too old to have (@I32@)\n" +
            "ANOMALY: FAMILY: US12: @F15@ Parent is too old to have (@I33@)\n" +
            "ANOMALY: FAMILY: US12: @F15@ Parent is too old to have (@I34@)\n" +
            "ANOMALY: FAMILY: US12: @F15@ Parent is too old to have (@I35@)\n" +
            "ANOMALY: FAMILY: US12: @F15@ Parent is too old to have (@I36@)\n" +
            "ANOMALY: FAMILY: US12: @F15@ Parent is too old to have (@I37@)\n" +
            "ANOMALY: FAMILY: US12: @F15@ Parent is too old to have (@I38@)\n" +
            "ANOMALY: FAMILY: US12: @F15@ Parent is too old to have (@I39@)\n" +
            "ANOMALY: FAMILY: US12: @F15@ Parent is too old to have (@I40@)\n" +
            "ANOMALY: FAMILY: US12: @F15@ Parent is too old to have (@I41@)\n" +
            "ANOMALY: FAMILY: US12: @F15@ Parent is too old to have (@I42@)\n" +
            "ANOMALY: FAMILY: US12: @F15@ Parent is too old to have (@I43@)\n" +
            "ANOMALY: FAMILY: US12: @F15@ Parent is too old to have (@I44@)\n")

if __name__ == "__main__":
    unittest.main()