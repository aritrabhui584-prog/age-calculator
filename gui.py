import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date
import calendar
from calculator import AgeCalculator

# Premium Dark Theme Color Palette (Catppuccin Mocha-inspired)
BG_MAIN = "#1e1e2e"       # Base background
BG_CARD = "#252538"       # Surface/Card background
FG_TEXT = "#cdd6f4"       # Default text color
FG_MUTED = "#a6adc8"      # Subtitle/Secondary text color
ACCENT_BLUE = "#89b4fa"   # Primary highlight
ACCENT_GREEN = "#a6e3a1"  # Success/Next birthday highlight
ACCENT_PINK = "#f38ba8"   # Warning/Accent text
BTN_HOVER = "#b4befe"      # Light purple/blue hover state
BORDER_COLOR = "#313244"   # Card border outline

MONTH_NAMES = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

class AgeCalculatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Precise Age Calculator")
        self.root.geometry("820x600")
        self.root.minsize(800, 580)
        self.root.configure(bg=BG_MAIN)

        self.live_update_job = None
        self.calculated_dob = None
        self.calculated_target = None
        self.is_live = False

        self.setup_styles()
        self.create_widgets()
        self.set_default_inputs()
        self.trigger_calculation()

    def setup_styles(self):
        """Sets up custom ttk styling for a modern flat appearance."""
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Configure style colors
        self.style.configure(".", background=BG_MAIN, foreground=FG_TEXT)
        self.style.configure("TFrame", background=BG_MAIN)
        self.style.configure("Card.TFrame", background=BG_CARD, relief="flat")
        
        self.style.configure("TLabel", background=BG_MAIN, foreground=FG_TEXT, font=("Segoe UI", 10))
        self.style.configure("CardTitle.TLabel", background=BG_CARD, foreground=ACCENT_BLUE, font=("Segoe UI", 12, "bold"))
        self.style.configure("CardValue.TLabel", background=BG_CARD, foreground=FG_TEXT, font=("Segoe UI", 15, "bold"))
        self.style.configure("CardSub.TLabel", background=BG_CARD, foreground=FG_MUTED, font=("Segoe UI", 10))
        self.style.configure("Header.TLabel", background=BG_MAIN, foreground=ACCENT_BLUE, font=("Segoe UI", 18, "bold"))

        # Combobox styling
        self.style.configure("TCombobox", fieldbackground=BG_CARD, background=BORDER_COLOR, foreground=FG_TEXT)
        self.root.option_add("*TCombobox*Listbox.background", BG_CARD)
        self.root.option_add("*TCombobox*Listbox.foreground", FG_TEXT)
        self.root.option_add("*TCombobox*Listbox.selectBackground", ACCENT_BLUE)
        self.root.option_add("*TCombobox*Listbox.selectForeground", BG_MAIN)

        # Radiobutton styling
        self.style.configure("TRadiobutton", background=BG_MAIN, foreground=FG_TEXT, font=("Segoe UI", 10))

    def create_widgets(self):
        """Creates and places the GUI layout."""
        # Top Title Banner
        title_frame = ttk.Frame(self.root)
        title_frame.pack(fill="x", padx=25, pady=(20, 10))
        title_lbl = ttk.Label(title_frame, text="PRECISE AGE CALCULATOR", style="Header.TLabel")
        title_lbl.pack(side="left")
        
        # Main content area divided into left (inputs) and right (results)
        content_frame = ttk.Frame(self.root)
        content_frame.pack(fill="both", expand=True, padx=25, pady=10)
        
        # Left Side (Inputs)
        input_pane = ttk.Frame(content_frame, width=320)
        input_pane.pack(side="left", fill="both", expand=False, padx=(0, 10))
        input_pane.pack_propagate(False)
        
        # Right Side (Results)
        result_pane = ttk.Frame(content_frame)
        result_pane.pack(side="right", fill="both", expand=True, padx=(10, 0))

        # --- Left Pane Contents ---
        # 1. Birth Date & Time Section
        dob_lbl = ttk.Label(input_pane, text="Date of Birth", font=("Segoe UI", 11, "bold"), foreground=ACCENT_BLUE)
        dob_lbl.pack(anchor="w", pady=(10, 5))
        
        dob_selectors = ttk.Frame(input_pane)
        dob_selectors.pack(fill="x", pady=5)
        
        self.dob_day = ttk.Combobox(dob_selectors, width=4, state="readonly")
        self.dob_month = ttk.Combobox(dob_selectors, width=12, state="readonly", values=MONTH_NAMES)
        self.dob_year = ttk.Combobox(dob_selectors, width=6, state="readonly")
        
        self.dob_day.pack(side="left", padx=(0, 5))
        self.dob_month.pack(side="left", padx=5)
        self.dob_year.pack(side="left", padx=5)
        
        # Watch month/year changes to update valid days
        self.dob_month.bind("<<ComboboxSelected>>", self.update_dob_days)
        self.dob_year.bind("<<ComboboxSelected>>", self.update_dob_days)

        tob_lbl = ttk.Label(input_pane, text="Time of Birth (Optional)", font=("Segoe UI", 10, "bold"), foreground=FG_MUTED)
        tob_lbl.pack(anchor="w", pady=(10, 5))
        
        tob_selectors = ttk.Frame(input_pane)
        tob_selectors.pack(fill="x", pady=5)
        
        self.tob_hour = ttk.Combobox(tob_selectors, width=4, state="readonly", values=[f"{i:02d}" for i in range(24)])
        self.tob_min = ttk.Combobox(tob_selectors, width=4, state="readonly", values=[f"{i:02d}" for i in range(60)])
        
        self.tob_hour.pack(side="left", padx=(0, 5))
        ttk.Label(tob_selectors, text=":").pack(side="left")
        self.tob_min.pack(side="left", padx=5)

        # Separator line
        self.draw_divider(input_pane, 20)

        # 2. Target Date Section
        target_title = ttk.Label(input_pane, text="Calculate At Date", font=("Segoe UI", 11, "bold"), foreground=ACCENT_BLUE)
        target_title.pack(anchor="w", pady=5)

        self.target_mode = tk.StringVar(value="now")
        r1 = ttk.Radiobutton(input_pane, text="Current Time (Live Tick)", variable=self.target_mode, value="now", command=self.toggle_target_inputs)
        r2 = ttk.Radiobutton(input_pane, text="Specific Past / Future Date", variable=self.target_mode, value="custom", command=self.toggle_target_inputs)
        r1.pack(anchor="w", pady=3)
        r2.pack(anchor="w", pady=3)

        self.target_selectors = ttk.Frame(input_pane)
        self.target_selectors.pack(fill="x", pady=10)

        self.target_day = ttk.Combobox(self.target_selectors, width=4, state="readonly")
        self.target_month = ttk.Combobox(self.target_selectors, width=12, state="readonly", values=MONTH_NAMES)
        self.target_year = ttk.Combobox(self.target_selectors, width=6, state="readonly")
        
        self.target_day.pack(side="left", padx=(0, 5))
        self.target_month.pack(side="left", padx=5)
        self.target_year.pack(side="left", padx=5)

        self.target_month.bind("<<ComboboxSelected>>", self.update_target_days)
        self.target_year.bind("<<ComboboxSelected>>", self.update_target_days)

        self.target_time_selectors = ttk.Frame(input_pane)
        self.target_time_selectors.pack(fill="x", pady=5)
        self.target_hour = ttk.Combobox(self.target_time_selectors, width=4, state="readonly", values=[f"{i:02d}" for i in range(24)])
        self.target_min = ttk.Combobox(self.target_time_selectors, width=4, state="readonly", values=[f"{i:02d}" for i in range(60)])
        
        self.target_hour.pack(side="left", padx=(0, 5))
        ttk.Label(self.target_time_selectors, text=":").pack(side="left")
        self.target_min.pack(side="left", padx=5)

        # 3. Calculate Action
        self.calc_btn = tk.Button(
            input_pane, 
            text="CALCULATE AGE", 
            command=self.trigger_calculation,
            font=("Segoe UI", 11, "bold"), 
            bg=ACCENT_BLUE, 
            fg=BG_MAIN, 
            activebackground=BTN_HOVER, 
            activeforeground=BG_MAIN,
            relief="flat", 
            cursor="hand2", 
            pady=10
        )
        self.calc_btn.pack(fill="x", pady=(25, 0))
        self.calc_btn.bind("<Enter>", lambda e: self.calc_btn.configure(bg=BTN_HOVER))
        self.calc_btn.bind("<Leave>", lambda e: self.calc_btn.configure(bg=ACCENT_BLUE))

        # --- Right Pane Contents (Output Cards) ---
        # 1. Exact Age Card
        self.age_card = ttk.Frame(result_pane, style="Card.TFrame")
        self.age_card.pack(fill="x", pady=(0, 15))
        self.add_card_border(self.age_card)
        
        ttk.Label(self.age_card, text="EXACT AGE", style="CardTitle.TLabel").pack(anchor="w", padx=20, pady=(15, 5))
        self.age_val_lbl = ttk.Label(self.age_card, text="-", style="CardValue.TLabel", justify="left")
        self.age_val_lbl.pack(anchor="w", padx=20, pady=(5, 5))
        self.age_sub_lbl = ttk.Label(self.age_card, text="-", style="CardSub.TLabel")
        self.age_sub_lbl.pack(anchor="w", padx=20, pady=(0, 15))

        # 2. Next Birthday Card
        self.bday_card = ttk.Frame(result_pane, style="Card.TFrame")
        self.bday_card.pack(fill="x", pady=15)
        self.add_card_border(self.bday_card)
        
        ttk.Label(self.bday_card, text="NEXT BIRTHDAY COUNTDOWN", style="CardTitle.TLabel", foreground=ACCENT_GREEN).pack(anchor="w", padx=20, pady=(15, 5))
        self.bday_val_lbl = ttk.Label(self.bday_card, text="-", style="CardValue.TLabel", foreground=ACCENT_GREEN)
        self.bday_val_lbl.pack(anchor="w", padx=20, pady=(5, 5))
        self.bday_sub_lbl = ttk.Label(self.bday_card, text="-", style="CardSub.TLabel")
        self.bday_sub_lbl.pack(anchor="w", padx=20, pady=(0, 15))

        # 3. Detailed Stats Card
        self.stats_card = ttk.Frame(result_pane, style="Card.TFrame")
        self.stats_card.pack(fill="both", expand=True, pady=(15, 0))
        self.add_card_border(self.stats_card)
        
        ttk.Label(self.stats_card, text="DETAILED STATISTICS", style="CardTitle.TLabel", foreground=ACCENT_PINK).pack(anchor="w", padx=20, pady=(15, 10))
        
        # Grid frame for clean key-value layout
        self.stats_grid = ttk.Frame(self.stats_card, style="Card.TFrame")
        self.stats_grid.pack(fill="both", expand=True, padx=20, pady=(0, 15))
        
        self.stat_labels = {}
        metrics = [("weeks", "Total Weeks"), ("days", "Total Days"), ("hours", "Total Hours"), ("minutes", "Total Minutes"), ("seconds", "Total Seconds")]
        for idx, (key, label_text) in enumerate(metrics):
            lbl = ttk.Label(self.stats_grid, text=label_text, style="CardSub.TLabel", font=("Segoe UI", 10, "bold"))
            lbl.grid(row=idx, column=0, sticky="w", pady=4)
            val = ttk.Label(self.stats_grid, text="-", style="CardSub.TLabel", foreground=FG_TEXT, font=("Segoe UI", 10, "bold"))
            val.grid(row=idx, column=1, sticky="w", padx=(15, 25), pady=4)
            self.stat_labels[key] = val

        # Astrological & Milestone insights
        extra_metrics = [
            ("born_day", "Born Weekday"),
            ("zodiac", "Zodiac Sign"),
            ("chinese", "Chinese Zodiac"),
            ("milestone", "Next Milestone")
        ]
        for idx, (key, label_text) in enumerate(extra_metrics):
            lbl = ttk.Label(self.stats_grid, text=label_text, style="CardSub.TLabel", font=("Segoe UI", 10, "bold"))
            lbl.grid(row=idx, column=2, sticky="w", pady=4)
            val = ttk.Label(self.stats_grid, text="-", style="CardSub.TLabel", foreground=FG_TEXT, font=("Segoe UI", 10, "bold"))
            val.grid(row=idx, column=3, sticky="w", padx=(15, 0), pady=4)
            self.stat_labels[key] = val

    def draw_divider(self, parent, pady):
        """Draws a clean subtle horizontal lines."""
        div = tk.Frame(parent, height=1, bg=BORDER_COLOR)
        div.pack(fill="x", pady=pady)

    def add_card_border(self, frame):
        """Draws clean borders around cards."""
        frame.configure(borderwidth=1, relief="solid")

    def toggle_target_inputs(self):
        """Enables/Disables custom target date inputs based on radio selection."""
        state = "normal" if self.target_mode.get() == "custom" else "disabled"
        for combobox in [self.target_day, self.target_month, self.target_year, self.target_hour, self.target_min]:
            combobox.configure(state=state if state == "disabled" else "readonly")

    def set_default_inputs(self):
        """Initializes inputs to reasonable defaults."""
        today = date.today()
        # Years for DOB: 1900 to now
        years = [str(y) for y in range(today.year, 1899, -1)]
        self.dob_year.configure(values=years)
        self.dob_year.set("2000")
        self.dob_month.set("January")
        self.update_dob_days()
        self.dob_day.set("01")

        self.tob_hour.set("00")
        self.tob_min.set("00")

        # Years for Target: 1900 to 2100
        target_years = [str(y) for y in range(today.year + 20, 1899, -1)]
        self.target_year.configure(values=target_years)
        self.target_year.set(str(today.year))
        self.target_month.set(MONTH_NAMES[today.month - 1])
        self.update_target_days()
        self.target_day.set(f"{today.day:02d}")
        self.target_hour.set(f"{datetime.now().hour:02d}")
        self.target_min.set(f"{datetime.now().minute:02d}")

        self.toggle_target_inputs()

    def update_dob_days(self, event=None):
        self._update_days(self.dob_year, self.dob_month, self.dob_day)

    def update_target_days(self, event=None):
        self._update_days(self.target_year, self.target_month, self.target_day)

    def _update_days(self, year_combo, month_combo, day_combo):
        """Updates day dropdown range based on selected month and year."""
        try:
            year = int(year_combo.get())
            month = MONTH_NAMES.index(month_combo.get()) + 1
        except ValueError:
            return

        _, max_days = calendar.monthrange(year, month)
        days = [f"{i:02d}" for i in range(1, max_days + 1)]
        
        current_selection = day_combo.get()
        day_combo.configure(values=days)
        if current_selection in days:
            day_combo.set(current_selection)
        else:
            day_combo.set(days[-1])

    def trigger_calculation(self):
        """Parses the UI inputs and triggers calculations."""
        # Cancel any active ticker job
        if self.live_update_job:
            self.root.after_cancel(self.live_update_job)
            self.live_update_job = None

        try:
            dob_y = int(self.dob_year.get())
            dob_m = MONTH_NAMES.index(self.dob_month.get()) + 1
            dob_d = int(self.dob_day.get())
            dob_h = int(self.tob_hour.get())
            dob_min = int(self.tob_min.get())
            self.calculated_dob = datetime(dob_y, dob_m, dob_d, dob_h, dob_min, 0)
        except (ValueError, TypeError) as e:
            messagebox.showerror("Invalid Input", "Please select valid Date of Birth components.")
            return

        if self.target_mode.get() == "now":
            self.is_live = True
            self.update_calculation_live()
        else:
            self.is_live = False
            try:
                tar_y = int(self.target_year.get())
                tar_m = MONTH_NAMES.index(self.target_month.get()) + 1
                tar_d = int(self.target_day.get())
                tar_h = int(self.target_hour.get())
                tar_min = int(self.target_min.get())
                self.calculated_target = datetime(tar_y, tar_m, tar_d, tar_h, tar_min, 0)
            except (ValueError, TypeError):
                messagebox.showerror("Invalid Input", "Please select valid Target Date components.")
                return

            if self.calculated_target < self.calculated_dob:
                messagebox.showerror("Invalid Date Range", "Target Date cannot be before Birth Date.")
                return

            self.perform_calculations(self.calculated_dob, self.calculated_target)

    def update_calculation_live(self):
        """Ticks calculation every second relative to current time."""
        now = datetime.now()
        if now < self.calculated_dob:
            self.age_val_lbl.configure(text="Not born yet")
            self.age_sub_lbl.configure(text="-")
            self.bday_val_lbl.configure(text="-")
            self.bday_sub_lbl.configure(text="-")
            for key in self.stat_labels:
                self.stat_labels[key].configure(text="-")
        else:
            self.perform_calculations(self.calculated_dob, now)
        
        self.live_update_job = self.root.after(1000, self.update_calculation_live)

    def perform_calculations(self, dob: datetime, target: datetime):
        """Invokes core age calculations and maps to UI widgets."""
        try:
            # 1. Exact Age
            exact = AgeCalculator.calculate_exact_age(dob, target)
            self.age_val_lbl.configure(
                text=f"{exact['years']} Years, {exact['months']} Months, {exact['days']} Days"
            )
            self.age_sub_lbl.configure(
                text=f"{exact['hours']} Hours, {exact['minutes']} Minutes, {exact['seconds']} Seconds"
            )

            # 2. Next Birthday Countdown
            next_bday, time_left = AgeCalculator.get_next_birthday(dob, target)
            days_left = time_left.days
            hours_left = time_left.seconds // 3600
            mins_left = (time_left.seconds % 3600) // 60
            secs_left = time_left.seconds % 60
            
            self.bday_val_lbl.configure(
                text=f"In {days_left} Days, {hours_left}h {mins_left}m {secs_left}s"
            )
            
            day_of_week = next_bday.strftime("%A")
            formatted_date = next_bday.strftime("%d %B %Y")
            self.bday_sub_lbl.configure(
                text=f"Will fall on: {day_of_week} ({formatted_date})"
            )

            # 3. Detailed stats
            stats = AgeCalculator.calculate_time_breakdown(dob, target)
            self.stat_labels["weeks"].configure(text=f"{stats['weeks']:,} wks")
            self.stat_labels["days"].configure(text=f"{stats['days']:,} days")
            self.stat_labels["hours"].configure(text=f"{stats['hours']:,} hrs")
            self.stat_labels["minutes"].configure(text=f"{stats['minutes']:,} mins")
            self.stat_labels["seconds"].configure(text=f"{stats['seconds']:,} secs")

            # 4. Astrological & Milestone insights
            zodiac = AgeCalculator.get_zodiac_sign(dob)
            chinese = AgeCalculator.get_chinese_zodiac(dob)
            self.stat_labels["born_day"].configure(text=AgeCalculator.get_day_of_birth(dob))
            self.stat_labels["zodiac"].configure(text=f"{zodiac['sign']} {zodiac['symbol']}")
            self.stat_labels["chinese"].configure(text=f"{chinese['animal']} {chinese['emoji']}")

            milestones = AgeCalculator.get_life_milestones(dob, target)
            upcoming = next((m for m in milestones if not m["reached"]), None)
            if upcoming:
                self.stat_labels["milestone"].configure(text=f"{upcoming['title']} (in {upcoming['days_diff']}d)")
            else:
                self.stat_labels["milestone"].configure(text="All achieved")

        except ValueError as e:
            # Fallback if any error occurs
            self.age_val_lbl.configure(text="Calculation Error")
            self.age_sub_lbl.configure(text=str(e))

def main():
    root = tk.Tk()
    app = AgeCalculatorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
