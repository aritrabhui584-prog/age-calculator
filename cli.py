import sys
import argparse
from datetime import datetime
from calculator import AgeCalculator

# ANSI terminal styles for premium look without dependencies
C_CYAN = "\033[36m"
C_GREEN = "\033[32m"
C_YELLOW = "\033[33m"
C_MAGENTA = "\033[35m"
C_BLUE = "\033[34m"
C_RED = "\033[31m"
C_BOLD = "\033[1m"
C_RESET = "\033[0m"

def print_banner():
    """Prints a beautiful CLI banner."""
    print(f"{C_BOLD}{C_CYAN}================================================={C_RESET}")
    print(f"{C_BOLD}{C_GREEN}             PRECISE Age Calculator CLI          {C_RESET}")
    print(f"{C_BOLD}{C_CYAN}================================================={C_RESET}\n")

def parse_date(date_str: str) -> datetime:
    """Parses date string of formats YYYY-MM-DD or YYYY-MM-DD HH:MM:SS."""
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d"):
        try:
            return datetime.strptime(date_str.strip(), fmt)
        except ValueError:
            continue
    raise ValueError(f"Date format must be YYYY-MM-DD or YYYY-MM-DD HH:MM:SS. Given: '{date_str}'")

def print_result_card(title: str, content: str, color: str = C_CYAN):
    """Prints a styled card/box in the terminal."""
    border = "=" * 49
    print(f"{color}{border}{C_RESET}")
    print(f"{C_BOLD}{color}| {title.center(45)} |{C_RESET}")
    print(f"{color}{border}{C_RESET}")
    for line in content.split('\n'):
        if line.strip():
            print(f"{color}|{C_RESET} {line.ljust(45)} {color}|{C_RESET}")
    print(f"{color}{border}{C_RESET}\n")

def print_detailed_breakdown(breakdown: dict):
    """Prints single-unit conversions inside a nice layout."""
    print(f"{C_BOLD}{C_YELLOW}---------------- DETAILED STATS -----------------{C_RESET}")
    print(f"  - Total Weeks   : {C_BOLD}{C_GREEN}{breakdown['weeks']:,} weeks{C_RESET}")
    print(f"  - Total Days    : {C_BOLD}{C_GREEN}{breakdown['days']:,} days{C_RESET}")
    print(f"  - Total Hours   : {C_BOLD}{C_GREEN}{breakdown['hours']:,} hours{C_RESET}")
    print(f"  - Total Minutes : {C_BOLD}{C_GREEN}{breakdown['minutes']:,} minutes{C_RESET}")
    print(f"  - Total Seconds : {C_BOLD}{C_GREEN}{breakdown['seconds']:,} seconds{C_RESET}")
    print(f"{C_YELLOW}-------------------------------------------------{C_RESET}\n")

def run_interactive():
    """Prompts the user interactively in the console."""
    print_banner()
    
    # Prompt for DOB
    while True:
        try:
            dob_input = input(f"{C_BOLD}Enter Date of Birth (YYYY-MM-DD) or 'q' to quit:{C_RESET} ").strip()
            if dob_input.lower() == 'q':
                sys.exit(0)
            dob = parse_date(dob_input)
            break
        except ValueError as e:
            print(f"{C_RED}Error: {e}{C_RESET}\n")

    # Prompt for optional Time of Birth
    while True:
        try:
            tob_input = input(f"{C_BOLD}Enter Time of Birth (HH:MM, 24-hr format) [Optional - Enter to skip]:{C_RESET} ").strip()
            if not tob_input:
                break
            # Combine DOB with entered time
            time_parts = datetime.strptime(tob_input, "%H:%M")
            dob = dob.replace(hour=time_parts.hour, minute=time_parts.minute, second=0)
            break
        except ValueError:
            print(f"{C_RED}Error: Time must be in HH:MM format (e.g., 14:30).{C_RESET}\n")

    display_results(dob, datetime.now())

def display_results(dob: datetime, target: datetime):
    """Calculates and displays the results."""
    try:
        # 1. Exact Age Card
        exact = AgeCalculator.calculate_exact_age(dob, target)
        age_str = (
            f"{exact['years']} Years, {exact['months']} Months, {exact['days']} Days\n"
            f"{exact['hours']} Hours, {exact['minutes']} Minutes, {exact['seconds']} Seconds"
        )
        print_result_card("EXACT AGE", age_str, C_CYAN)

        # 2. Detailed Breakdown
        breakdown = AgeCalculator.calculate_time_breakdown(dob, target)
        print_detailed_breakdown(breakdown)

        # 3. Next Birthday Countdown
        next_bday, time_left = AgeCalculator.get_next_birthday(dob, target)
        
        # Calculate days, hours, mins, secs remaining
        days_left = time_left.days
        hours_left = time_left.seconds // 3600
        mins_left = (time_left.seconds % 3600) // 60
        secs_left = time_left.seconds % 60
        
        day_of_week = next_bday.strftime("%A")
        formatted_date = next_bday.strftime("%d %B %Y")
        
        countdown_str = (
            f"In {days_left} Days, {hours_left} Hours, {mins_left} Mins, {secs_left} Secs\n"
            f"Day of Week: {day_of_week}\n"
            f"Date       : {formatted_date}"
        )
        print_result_card("NEXT BIRTHDAY COUNTDOWN", countdown_str, C_MAGENTA)
        
    except ValueError as e:
        print(f"{C_RED}Error during calculation: {e}{C_RESET}")

def main():
    parser = argparse.ArgumentParser(
        description="A professional and precise Python Age Calculator.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "-d", "--dob", 
        help="Date of Birth in format YYYY-MM-DD or 'YYYY-MM-DD HH:MM:SS'"
    )
    parser.add_argument(
        "-t", "--target", 
        help="Target date for calculation. Defaults to current system date/time."
    )
    parser.add_argument(
        "-i", "--interactive", 
        action="store_true", 
        help="Force interactive CLI mode."
    )

    args = parser.parse_args()

    # Determine whether to run interactive or argument-based
    if args.interactive or (not args.dob):
        run_interactive()
    else:
        try:
            dob = parse_date(args.dob)
            target = parse_date(args.target) if args.target else datetime.now()
            print_banner()
            print(f" DOB   : {C_BOLD}{C_GREEN}{dob.strftime('%Y-%m-%d %H:%M:%S')}{C_RESET}")
            print(f" Target: {C_BOLD}{C_GREEN}{target.strftime('%Y-%m-%d %H:%M:%S')}{C_RESET}\n")
            display_results(dob, target)
        except ValueError as e:
            print(f"{C_RED}Error: {e}{C_RESET}")
            sys.exit(1)

if __name__ == "__main__":
    main()
