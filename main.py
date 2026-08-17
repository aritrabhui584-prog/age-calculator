import sys

def main():
    """
    Main entry point for the Age Calculator application.
    Automatically detects if command-line arguments are present.
    If yes, runs in CLI mode. If no, attempts to run the GUI.
    Falls back to interactive CLI if graphical environment is unavailable.
    """
    # If command-line arguments are passed, route to CLI
    if len(sys.argv) > 1:
        import cli
        cli.main()
    else:
        try:
            import gui
            gui.main()
        except Exception as e:
            # If Tkinter is not installed or X11/display is missing (e.g. headless Linux, SSH)
            print(f"Notice: GUI could not be loaded ({e}).")
            print("Falling back to interactive command-line interface...\n")
            import cli
            cli.run_interactive()

if __name__ == "__main__":
    main()
