import unittest
from datetime import datetime, date, timedelta
from calculator import AgeCalculator

class TestAgeCalculator(unittest.TestCase):

    def test_standard_age(self):
        """Test calculation of age for a standard date where birthday has passed."""
        born = datetime(1990, 5, 15, 10, 30, 0)
        target = datetime(2023, 8, 20, 15, 45, 10)
        
        age = AgeCalculator.calculate_exact_age(born, target)
        self.assertEqual(age["years"], 33)
        self.assertEqual(age["months"], 3)
        self.assertEqual(age["days"], 5)
        self.assertEqual(age["hours"], 5)
        self.assertEqual(age["minutes"], 15)
        self.assertEqual(age["seconds"], 10)

    def test_birthday_not_yet_passed(self):
        """Test calculation when the birthday has not yet passed in the target year."""
        born = datetime(1990, 8, 25, 0, 0, 0)
        target = datetime(2023, 8, 20, 0, 0, 0)
        
        age = AgeCalculator.calculate_exact_age(born, target)
        self.assertEqual(age["years"], 32)
        self.assertEqual(age["months"], 11)
        self.assertEqual(age["days"], 26)

    def test_time_borrow_day(self):
        """Test time calculations that borrow a day (e.g. target time is earlier than born time)."""
        born = datetime(1990, 5, 15, 15, 0, 0)
        target = datetime(2023, 5, 16, 10, 0, 0)  # exactly 1 day later, but 5 hours earlier in day
        
        age = AgeCalculator.calculate_exact_age(born, target)
        self.assertEqual(age["years"], 33)
        self.assertEqual(age["months"], 0)
        self.assertEqual(age["days"], 0)
        self.assertEqual(age["hours"], 19)

    def test_leap_year_birth_leap_target(self):
        """Test Feb 29 to Feb 29 on next leap year (exactly 4 years)."""
        born = datetime(2000, 2, 29, 0, 0, 0)
        target = datetime(2004, 2, 29, 0, 0, 0)
        
        age = AgeCalculator.calculate_exact_age(born, target)
        self.assertEqual(age["years"], 4)
        self.assertEqual(age["months"], 0)
        self.assertEqual(age["days"], 0)

    def test_leap_year_birth_non_leap_target(self):
        """Test Feb 29 born on non-leap year (e.g. 1 year later on Feb 28)."""
        born = datetime(2000, 2, 29, 0, 0, 0)
        target = datetime(2001, 2, 28, 0, 0, 0)
        
        age = AgeCalculator.calculate_exact_age(born, target)
        self.assertEqual(age["years"], 1)
        self.assertEqual(age["months"], 0)
        self.assertEqual(age["days"], 0)

    def test_future_target_error(self):
        """Test that ValueError is raised if target date is before birth date."""
        born = datetime(2023, 8, 20, 0, 0, 0)
        target = datetime(2020, 8, 20, 0, 0, 0)
        
        with self.assertRaises(ValueError):
            AgeCalculator.calculate_exact_age(born, target)

    def test_time_breakdown(self):
        """Test equivalent metrics calculations (weeks, days, hours, etc.)."""
        born = datetime(2020, 1, 1, 0, 0, 0)
        target = datetime(2020, 1, 15, 12, 0, 0) # 14.5 days
        
        breakdown = AgeCalculator.calculate_time_breakdown(born, target)
        self.assertEqual(breakdown["days"], 14)
        self.assertEqual(breakdown["weeks"], 2.07)  # 14.5 / 7 rounded to 2 decimals
        self.assertEqual(breakdown["hours"], 14 * 24 + 12)
        self.assertEqual(breakdown["minutes"], (14 * 24 + 12) * 60)

    def test_next_birthday_normal(self):
        """Test next birthday calculation for normal dates."""
        born = datetime(1990, 5, 15, 10, 0, 0)
        target = datetime(2023, 8, 20, 12, 0, 0)
        
        next_bday, duration = AgeCalculator.get_next_birthday(born, target)
        self.assertEqual(next_bday.year, 2024)
        self.assertEqual(next_bday.month, 5)
        self.assertEqual(next_bday.day, 15)
        
        # Duration until next birthday
        expected_next = datetime(2024, 5, 15, 10, 0, 0)
        self.assertEqual(duration, expected_next - target)

    def test_next_birthday_leap_year(self):
        """Test next birthday calculation for someone born on Feb 29 in a non-leap target year."""
        born = datetime(2000, 2, 29, 12, 0, 0)
        target = datetime(2001, 2, 10, 12, 0, 0)
        
        next_bday, duration = AgeCalculator.get_next_birthday(born, target)
        # 2001 is not a leap year, so next birthday is March 1st
        self.assertEqual(next_bday.year, 2001)
        self.assertEqual(next_bday.month, 3)
        self.assertEqual(next_bday.day, 1)

if __name__ == "__main__":
    unittest.main()
