import calendar
from datetime import datetime, date, timedelta
from typing import Dict, Any, Tuple

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
