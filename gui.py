import tkinter as tk

#GUI
class GUI:
        def __init__(self, main_window):
                self.main_window = main_window
                main_window.title("Shining in the Dungeon (5e Duel)")
                main_window.minsize(1024, 768)
                main_window.maxsize(1024, 768)
                self.status_pane = tk.Text(main_window)
                self.status_pane.grid(row = 4, column = 1)
                self.status_pane.insert("1.0", "status pane")
                self.test = tk.Label(main_window, text = "Test")
                self.test.grid(row = 2, column = 1)
                self.visualization_pane = tk.Canvas(main_window)
                self.visualization_pane.grid(row = 3, column = 1)
                self.message_pane = tk.Text(main_window)
                self.message_pane.grid(row = 1, column = 1)
                self.message_pane.insert(tk.END, "message pane")
        def push_message(self, message):
                #self.message_pane.delete("1.0", "end")
                self.message_pane.insert(tk.END, "\n")
                self.message_pane.insert(tk.END, message)