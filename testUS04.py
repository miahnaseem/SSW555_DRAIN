import unittest
import parseGEDCOM

class us04Test(unittest.TestCase):
	def testUS04(self):
		self.assertEqual(parseGEDCOM.checkUS04(), "ERROR: FAMILY: US04: @F7@: Divorce date 1982-11-11 is before marriage date 1999-09-07")