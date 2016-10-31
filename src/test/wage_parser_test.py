'''
Created on Oct 30, 2016

@author: petteri.raisanen
'''
import unittest
from wage_parser import normalize_time, calculate_hours, Hours, normalize_hours,\
    calculate_overtime_pay


class WageParserTest(unittest.TestCase):

    def setUp(self):
        pass


    def tearDown(self):
        pass

    def __assertHours(self, hours, date, num_hours, evening_hours = 0, overtime_hours = 0):
        self.assertEqual(hours.date, date)
        self.assertEqual(hours.hours, num_hours)
        self.assertEqual(hours.evening_hours, evening_hours)
        self.assertEqual(hours.overtime_hours, overtime_hours)

    def testNormalizeTime(self):
        self.assertEqual(normalize_time("6:00"), 6)
        self.assertEqual(normalize_time("6:30"), 6.5)
        self.assertEqual(normalize_time("12:30"), 12.5)
        self.assertEqual(normalize_time("23:00"), 23)
        self.assertEqual(normalize_time("6"), 6)
        self.assertEqual(normalize_time("06"), 6)
        self.assertEqual(normalize_time("0"), 0)
        self.assertEqual(normalize_time("19:45:00"), 19.75)

        with self.assertRaises(ValueError):
            normalize_time("XYZZY")

        with self.assertRaises(ValueError):
            normalize_time("-2:00")

        # We don't support floats in the hours part. 
        with self.assertRaises(ValueError):
            normalize_time("6.50:45")

        with self.assertRaises(ValueError):
            normalize_time("24:00")

        with self.assertRaises(ValueError):
            normalize_time("24:30")

        with self.assertRaises(ValueError):
            normalize_time("25:00")

    def test_calculate_hours(self):
        self.assertEqual(calculate_hours(8, 16), (8, 0, 0))
        self.assertEqual(calculate_hours(12, 16.5), (4.5, 0, 0))
        self.assertEqual(calculate_hours(14, 20), (6, 2, 0))
        self.assertEqual(calculate_hours(16, 0), (8, 6, 0))

        # overtime 
        self.assertEqual(calculate_hours(8, 18), (10, 0, 2))

        # evening hours should be zero since overtime takes precedence:
        self.assertEqual(calculate_hours(16, 8), (16, 0, 8))
        self.assertEqual(calculate_hours(23, 12), (13, 0, 5))

    def test_normalize_hours(self):
        hours = [Hours("1.10.2016", "8:00", "10:00"),
                 Hours("2.10.2016", "8:00", "12:00"),
                 Hours("1.10.2016", "12:00", "13:00"),
                 Hours("3.10.2016", "8:00", "16:00"),
                 Hours("1.10.2016", "13:30", "14:00"),
                 Hours("2.10.2016", "14:00", "16:00")]

        # TODO: Overlap
        # 1.10 = 3.5 h
        # 2.10 = 6 h
        # 3.10 = 8h
        normalized = normalize_hours(hours)

        self.assertEqual(len(normalized), 3)
        self.__assertHours(normalized[0], "1.10.2016", 3.5)
        self.__assertHours(normalized[1], "2.10.2016", 6)
        self.__assertHours(normalized[2], "3.10.2016", 8)

    def test_normalize_hours_with_evening_hours(self):
        hours = [Hours("1.10.2016", "8:00", "10:00"),
                 Hours("2.10.2016", "8:00", "12:00"),
                 Hours("1.10.2016", "18:00", "23:00")]

        normalized = normalize_hours(hours)

        self.assertEqual(len(normalized), 2)
        self.__assertHours(normalized[0], "1.10.2016", 7, 5)
        self.__assertHours(normalized[1], "2.10.2016", 4)

    def test_normalize_hours_with_overtime(self):
        hours = [Hours("1.10.2016", "8:00", "16:00"),
                 Hours("2.10.2016", "8:00", "12:00"),
                 Hours("1.10.2016", "16:00", "00:00")]

        normalized = normalize_hours(hours)

        self.assertEqual(len(normalized), 2)
        self.__assertHours(normalized[0], "1.10.2016", 16, 0, 8)
        self.__assertHours(normalized[1], "2.10.2016", 4)

    def test_to_dollars(self):
        self.assertEqual(Hours("1.10.2016", "8:00", "16:00").to_dollars(), 30)
        self.assertEqual(Hours("1.10.2016", "8:00", "12:00").to_dollars(), 15)

        self.assertEqual(Hours("1.10.2016", "12:00", "20:00").to_dollars(), 32.30)
        self.assertEqual(Hours("1.10.2016", "18:00", "00:00").to_dollars(), 29.40)

        self.assertEqual(Hours("1.10.2016", "08:00", "20:00").to_dollars(), 50.625)
        self.assertEqual(Hours("1.10.2016", "08:00", "00:00").to_dollars(), 80.625)

    def test_calculate_overtime_pay(self):
        # the return values are in cents:
        self.assertEquals(calculate_overtime_pay(0), 0)
        self.assertEquals(calculate_overtime_pay(1), 375 * 0.25)
        self.assertEquals(calculate_overtime_pay(2), 375 * 0.25 * 2)
        self.assertEquals(calculate_overtime_pay(3), (375 * 0.25 * 2) + (375 * 0.50))
        self.assertEquals(calculate_overtime_pay(5), (375 * 0.25 * 2) + (375 * 0.50 * 2) + (375 * 1))
        self.assertEquals(calculate_overtime_pay(10), (375 * 0.25 * 2) + (375 * 0.50 * 2) + (375 * 1 * 6))

if __name__ == "__main__":
    unittest.main()