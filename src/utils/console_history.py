import sys
import atexit
import code
import os
if sys.platform in ['macOSX', 'darwin']:
    import pyreadline as readline
else:
    import pyreadline

class HistoryConsole(code.InteractiveConsole):
    def __init__(self, locals=None, filename="<console>"):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.histfile = os.path.expanduser(os.path.join(current_dir, ".command_history"))
        code.InteractiveConsole.__init__(self, locals, filename)
        self.init_history(self.histfile)

    def init_history(self, histfile):
        #readline.set_auto_history(True)
        pyreadline.parse_and_bind("tab: complete")
        pyreadline.parse_and_bind("bind ^I rl_complete")
        if os.name == 'posix' or os.name == 'darwin':  # Unix-like systems, including macOS
            pyreadline.parse_and_bind("\\x1b[A: history-search-back")
        elif os.name == 'nt':  # Windows
            pyreadline.parse_and_bind("\"[A\": history-search-back")

        if hasattr(pyreadline, "read_history_file"):
            try:
                pyreadline.read_history_file(histfile)
                print(histfile)
            except FileNotFoundError:
                print("not found")
                pass
            atexit.register(self.save_history, histfile=self.histfile)

        # This should give previous command history on the start, but it does not work
        pyreadline.clear_history()
        pyreadline.read_history_file(self.histfile)
        pyreadline.set_history_length(1000)
        #readline.insert_text("a")
        #print(readline.get_history_item(0))
        #print(readline.get_current_history_length())

    def save_history(self, histfile):
        pyreadline.write_history_file(histfile)

    def add_history(self, hist):
        pyreadline.add_history(hist)