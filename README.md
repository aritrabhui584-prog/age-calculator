# Precise Age Calculator 🐍⏱️

A professional, highly precise Python-based Age Calculator that provides a detailed breakdown of your age and a countdown to your next birthday. It features both a modern, dark-themed **Graphical User Interface (GUI)** and a beautiful **Command-Line Interface (CLI)**—all implemented using only the **Python Standard Library** for a zero-dependency, plug-and-play installation!

---

## ✨ Features

- **Exact Age Calculation**: Calculates your precise age down to the second in years, months, days, hours, minutes, and seconds.
- **Detailed Time Metrics**: Provides a complete conversion breakdown of your age in single-unit metrics (total weeks, days, hours, minutes, and seconds).
- **Next Birthday Countdown**: Tracks the remaining months, days, hours, minutes, and seconds until your next birthday, and shows what day of the week it will fall on.
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
             精密 Age Calculator CLI             
=================================================

=================================================
|                   EXACT AGE                   |
=================================================
| 30 Years, 8 Months, 1 Days                    |
| 5 Hours, 15 Minutes, 30 Seconds               |
=================================================

---------------- DETAILED STATS -----------------
  • Total Weeks   : 1,600.17 weeks
  • Total Days    : 11,201 days
  • Total Hours   : 268,829 hours
  • Total Minutes : 16,129,755 minutes
  • Total Seconds : 967,785,330 seconds
-------------------------------------------------

=================================================
|            NEXT BIRTHDAY COUNTDOWN            |
=================================================
| In 121 Days, 18 Hours, 44 Mins, 30 Secs       |
| Day of Week: Friday                           |
| Date       : 15 December 2026                 |
=================================================
```

---

## 📄 License
This project is licensed under the MIT License - feel free to use and adapt it for your own repositories!
