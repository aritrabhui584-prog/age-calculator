# Precise Age Calculator 🐍⏱️

A professional, highly precise Python-based Age Calculator that provides a detailed breakdown of your age and a countdown to your next birthday. It features both a modern, dark-themed **Graphical User Interface (GUI)** and a beautiful **Command-Line Interface (CLI)**—all implemented using only the **Python Standard Library** for a zero-dependency, plug-and-play installation!

---

## ✨ Features

- **Exact Age Calculation**: Calculates your precise age down to the second in years, months, days, hours, minutes, and seconds.
- **Detailed Time Metrics**: Provides a complete conversion breakdown of your age in single-unit metrics (total weeks, days, hours, minutes, and seconds).
- **Astrological & Birth Insights**: Identifies the day of the week you were born on, your Western Zodiac sign (with symbol and element), and your Chinese Zodiac animal.
- **Life Milestones Tracker**: Computes milestone milestones (e.g., 10,000 days, 1 billion seconds, and milestone birthdays) with exact dates and days remaining.
- **Next Birthday Countdown**: Tracks the remaining months, days, hours, minutes, and seconds until your next birthday, and shows what day of the week it will fall on.
- **Machine-Readable JSON Output**: Supports `--json` flag in CLI mode for seamless pipeline integration and scripting.
- **Live Ticking Mode**: The GUI and CLI automatically update the target time in real-time, allowing you to watch your age increment second-by-second.
- **Leap Year & Calendar Safe**: Handles the edge cases of different month lengths and leap years (such as birthdays on February 29th) mathematically and robustly.
- **Dual Mode (GUI & CLI)**: Automatically routes to the GUI when run normally, or to the CLI when command-line parameters are supplied or if running in a headless shell.

---

## 🛠️ Project Structure

```text
├── calculator.py         # Core business logic (precise age computations)
├── gui.py                # Modern Tkinter dark-themed graphical dashboard
├── cli.py                # Custom ANSI-styled terminal application
├── main.py               # Application router & entry point
├── test_calculator.py    # Test suite covering leap years and edge cases
└── .gitignore            # Git exclusion patterns
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.6 or higher.

No external packages or dependencies are required!

### Run the GUI
Simply run the main script. The system will detect your graphics environment and boot the dark-themed Tkinter dashboard:
```bash
python main.py
```

### Run the CLI
You can run the command-line interface in two ways:

1. **Interactive CLI**:
   ```bash
   python main.py -i
   # or run in a terminal where graphics are unavailable
   ```

2. **Argument-based CLI**:
   Pass your Date of Birth directly as an argument:
   ```bash
   # Date only
   python main.py -d 1995-12-15
   
   # Date and Time of Birth
   python main.py -d "1995-12-15 14:30:00"
   
   # Calculate age relative to a specific target date
   python main.py -d 1995-12-15 -t 2026-08-16

   # Output in machine-readable JSON format
   python main.py -d 1995-12-15 --json
   ```

---

## 🧪 Testing

To ensure calculations are robust and accurate (handling complex dates and times), a comprehensive suite of unit tests is included.

Run the test suite with:
```bash
python -m unittest test_calculator.py
```

---

## 🎨 Preview of Output Layouts

### CLI View Example
When run in the command line, results are rendered inside clean card borders:
```text
=================================================
             PRECISE Age Calculator CLI          
=================================================

 DOB   : 1995-05-15 00:00:00
 Target: 2026-11-16 20:20:36

=================================================
|                   EXACT AGE                   |
=================================================
| 31 Years, 6 Months, 1 Days                    |
| 20 Hours, 20 Minutes, 36 Seconds              |
=================================================

=================================================
|             BIRTH PROFILE & ZODIAC            |
=================================================
| Born On   : Monday                            |
| Zodiac    : Taurus ♉ (Earth Element)          |
| Chinese   : Year of the Pig 🐖                 |
=================================================

---------------- DETAILED STATS -----------------
  - Total Weeks   : 1,644.12 weeks
  - Total Days    : 11,508 days
  - Total Hours   : 276,212 hours
  - Total Minutes : 16,572,740 minutes
  - Total Seconds : 994,364,436 seconds
-------------------------------------------------

=================================================
|            NEXT BIRTHDAY COUNTDOWN            |
=================================================
| In 179 Days, 3 Hours, 39 Mins, 23 Secs        |
| Day of Week: Saturday                         |
| Date       : 15 May 2027                      |
=================================================

=================================================
|               UPCOMING MILESTONE              |
=================================================
| Next Goal : 1 Billion Seconds                 |
| Date      : 21 January 2027                   |
| Remaining : In 66 Days                        |
=================================================
```

---

## 📄 License
This project is licensed under the MIT License - feel free to use and adapt it for your own repositories!
