import calendar
from datetime import datetime, date, timedelta
from typing import Dict, Any, Tuple, List, Union

class AgeCalculator:
    """Core calculation logic for precise age calculation."""

    @staticmethod
    def add_months(source_date: date, months: int) -> date:
        """Add months to a date, handling leap years and varying month lengths by clipping."""
        month = source_date.month - 1 + months
        year = source_date.year + month // 12
        month = month % 12 + 1
        day = min(source_date.day, calendar.monthrange(year, month)[1])
        return date(year, month, day)

    @classmethod
    def calculate_exact_age(cls, born: datetime, target: datetime) -> Dict[str, int]:
        """
        Calculates exact age in years, months, days, hours, minutes, seconds.
        
        Args:
            born: datetime object of birth date/time.
            target: datetime object of calculation target date/time.
            
        Returns:
            Dict containing 'years', 'months', 'days', 'hours', 'minutes', 'seconds'.
        """
        if target < born:
            raise ValueError("Target date/time cannot be before birth date/time.")

        # 1. Calculate years, months, days using the date components
        born_date = born.date()
        target_date = target.date()

        # Optimize search starting point
        guess_years = target_date.year - born_date.year - 1
        total_months = max(0, guess_years * 12)
        
        while True:
            next_date = cls.add_months(born_date, total_months + 1)
            if next_date > target_date:
                break
            total_months += 1

        years = total_months // 12
        months = total_months % 12
        anniversary_date = cls.add_months(born_date, total_months)
        days = (target_date - anniversary_date).days

        # 2. Adjust for time component
        # We compare time components at target vs born
        born_time = born.time()
        target_time = target.time()

        # Convert times to seconds since midnight
        born_sec = born_time.hour * 3600 + born_time.minute * 60 + born_time.second
        target_sec = target_time.hour * 3600 + target_time.minute * 60 + target_time.second

        time_diff_sec = target_sec - born_sec

        if time_diff_sec < 0:
            # We must borrow a day
            days -= 1
            time_diff_sec += 86400  # seconds in a day
            
            # If days becomes negative, we must borrow a month
            if days < 0:
                total_months -= 1
                years = total_months // 12
                months = total_months % 12
                anniversary_date = cls.add_months(born_date, total_months)
                # Recalculate days with the new anniversary date, remembering we borrowed 1 day for time
                days = (target_date - anniversary_date).days - 1

        hours = time_diff_sec // 3600
        minutes = (time_diff_sec % 3600) // 60
        seconds = time_diff_sec % 60

        return {
            "years": years,
            "months": months,
            "days": days,
            "hours": hours,
            "minutes": minutes,
            "seconds": seconds
        }

    @staticmethod
    def calculate_time_breakdown(born: datetime, target: datetime) -> Dict[str, Any]:
        """
        Calculates age represented in different single-unit metrics.
        
        Returns:
            Dict containing total weeks, days, hours, minutes, seconds.
        """
        if target < born:
            raise ValueError("Target date/time cannot be before birth date/time.")

        delta = target - born
        
        total_seconds = int(delta.total_seconds())
        total_minutes = total_seconds // 60
        total_hours = total_seconds // 3600
        total_days = delta.days
        total_weeks = total_seconds / (7 * 86400)

        return {
            "weeks": round(total_weeks, 2),
            "days": total_days,
            "hours": total_hours,
            "minutes": total_minutes,
            "seconds": total_seconds
        }

    @staticmethod
    def get_next_birthday(born: datetime, target: datetime) -> Tuple[datetime, timedelta]:
        """
        Calculates the next birthday datetime and the duration until it.
        
        Args:
            born: datetime object of birth date/time.
            target: datetime object of calculation target date/time.
            
        Returns:
            Tuple of (next_birthday_datetime, timedelta_until_next_birthday).
        """
        # Try target year first
        try:
            bday_this_year = datetime(
                target.year, born.month, born.day, 
                born.hour, born.minute, born.second
            )
        except ValueError:
            # Must be Feb 29 in a non-leap year, default to March 1st
            bday_this_year = datetime(
                target.year, 3, 1, 
                born.hour, born.minute, born.second
            )

        if bday_this_year >= target:
            next_bday = bday_this_year
        else:
            # Birthday has passed, look at next year
            try:
                next_bday = datetime(
                    target.year + 1, born.month, born.day, 
                    born.hour, born.minute, born.second
                )
            except ValueError:
                # Feb 29 in a non-leap year
                next_bday = datetime(
                    target.year + 1, 3, 1, 
                    born.hour, born.minute, born.second
                )

        duration = next_bday - target
        return next_bday, duration

    @staticmethod
    def get_day_of_birth(born: Union[datetime, date]) -> str:
        """Returns the weekday name of birth (e.g. 'Monday', 'Friday')."""
        return born.strftime("%A")

    @staticmethod
    def get_zodiac_sign(born: Union[datetime, date]) -> Dict[str, str]:
        """
        Calculates the Western Zodiac sign, astrological symbol, and classical element.
        
        Args:
            born: datetime or date object.
            
        Returns:
            Dict containing 'sign', 'symbol', and 'element'.
        """
        month = born.month
        day = born.day

        # Zodiac date ranges: (end_month, end_day, sign, symbol, element)
        zodiac_dates = [
            ((1, 20), (2, 18), "Aquarius", "♒", "Air"),
            ((2, 19), (3, 20), "Pisces", "♓", "Water"),
            ((3, 21), (4, 19), "Aries", "♈", "Fire"),
            ((4, 20), (5, 20), "Taurus", "♉", "Earth"),
            ((5, 21), (6, 20), "Gemini", "♊", "Air"),
            ((6, 21), (7, 22), "Cancer", "♋", "Water"),
            ((7, 23), (8, 22), "Leo", "♌", "Fire"),
            ((8, 23), (9, 22), "Virgo", "♍", "Earth"),
            ((9, 23), (10, 22), "Libra", "♎", "Air"),
            ((10, 23), (11, 21), "Scorpio", "♏", "Water"),
            ((11, 22), (12, 21), "Sagittarius", "♐", "Fire"),
        ]

        for (start_m, start_d), (end_m, end_d), sign, symbol, element in zodiac_dates:
            if (month == start_m and day >= start_d) or (month == end_m and day <= end_d):
                return {"sign": sign, "symbol": symbol, "element": element}

        # Capricorn spans December 22 to January 19
        return {"sign": "Capricorn", "symbol": "♑", "element": "Earth"}

    @staticmethod
    def get_chinese_zodiac(born: Union[datetime, date]) -> Dict[str, str]:
        """
        Calculates Chinese Zodiac animal and emoji based on birth year.
        
        Args:
            born: datetime or date object.
            
        Returns:
            Dict containing 'animal' and 'emoji'.
        """
        animals = [
            ("Rat", "🐀"), ("Ox", "🐂"), ("Tiger", "🐅"), ("Rabbit", "🐇"),
            ("Dragon", "🐉"), ("Snake", "🐍"), ("Horse", "🐎"), ("Goat", "🐐"),
            ("Monkey", "🐒"), ("Rooster", "🐓"), ("Dog", "🐕"), ("Pig", "🐖")
        ]
        # Reference: Year 4 AD was year of the Rat
        idx = (born.year - 4) % 12
        animal, emoji = animals[idx]
        return {"animal": animal, "emoji": emoji}

    @classmethod
    def get_life_milestones(cls, born: datetime, target: datetime) -> List[Dict[str, Any]]:
        """
        Calculates notable life milestone moments (e.g. 10,000 days, 1 billion seconds, key ages).
        
        Args:
            born: datetime object of birth date/time.
            target: datetime object of target date/time.
            
        Returns:
            List of milestone dictionaries sorted chronologically.
        """
        milestones = []

        # Day milestones
        for day_count in [1000, 5000, 10000, 15000, 20000, 25000]:
            m_date = born + timedelta(days=day_count)
            milestones.append({
                "title": f"{day_count:,} Days",
                "date": m_date,
                "reached": target >= m_date,
                "days_diff": abs((target - m_date).days)
            })

        # Second milestones (1 Billion seconds ~ 31.7 years)
        one_billion_sec = born + timedelta(seconds=1_000_000_000)
        milestones.append({
            "title": "1 Billion Seconds",
            "date": one_billion_sec,
            "reached": target >= one_billion_sec,
            "days_diff": abs((target - one_billion_sec).days)
        })

        # Year milestones (18, 21, 30, 40, 50, 60, 75, 100)
        for year in [18, 21, 30, 40, 50, 60, 75, 100]:
            try:
                m_date = datetime(born.year + year, born.month, born.day, born.hour, born.minute, born.second)
            except ValueError:
                # Feb 29 fallback
                m_date = datetime(born.year + year, 3, 1, born.hour, born.minute, born.second)
            milestones.append({
                "title": f"Age {year}",
                "date": m_date,
                "reached": target >= m_date,
                "days_diff": abs((target - m_date).days)
            })

        milestones.sort(key=lambda m: m["date"])
        return milestones

