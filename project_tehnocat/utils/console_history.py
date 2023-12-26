import sys
import atexit
import code
import os

if sys.platform in ["macOSX", "darwin"]:
    import gnureadline as readline
else:
    import readline


class HistoryConsole(code.InteractiveConsole):
    def __init__(self, locals=None, filename="<console>"):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.histfile = os.path.expanduser(
            os.path.join(current_dir, ".command_history")
        )
        if not os.path.exists(self.histfile):
            with open(self.histfile, 'w') as file:
                file.write('')

        code.InteractiveConsole.__init__(self, locals, filename)
        self.init_history(self.histfile)

    def init_history(self, histfile):
        # readline.set_auto_history(True)
        readline.parse_and_bind("tab: complete")
        readline.parse_and_bind("bind ^I rl_complete")
        if (
            os.name == "posix" or os.name == "darwin"
        ):  # Unix-like systems, including macOS
            readline.parse_and_bind("\\x1b[A: history-search-back")
        elif os.name == "nt":  # Windows
            readline.parse_and_bind('"[A": history-search-back')

        if hasattr(readline, "read_history_file"):
            try:
                readline.read_history_file(histfile)
            except FileNotFoundError:
                print("not found")
                pass
            atexit.register(self.save_history, histfile=self.histfile)

        # This should give previous command history on the start, but it does not work
        readline.clear_history()
        readline.read_history_file(self.histfile)
        readline.set_history_length(1000)
        # readline.insert_text("a")
        # print(readline.get_history_item(0))
        # print(readline.get_current_history_length())

    def save_history(self, histfile):
        readline.write_history_file(histfile)

    def add_history(self, hist):
        readline.add_history(hist)
