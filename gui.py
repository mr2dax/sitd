import tkinter as tk

#GUI
class GUI:
        def __init__(self, main_window):
                self.main_window = main_window
                main_window.title("Shining in the Dungeon (5e Duel)")
                main_window.minsize(1024, 768)
                main_window.maxsize(1024, 768)
                self.main_frame = tk.Frame(main_window)
                self.main_frame.pack(side = tk.LEFT)
                #self.status_pane = tk.Text(self.main_frame, height = 10, width = 100)
                #self.status_pane.grid(row = 0, column = 0)
                #self.status_pane.insert("1.0", "status pane")
                self.visualization_pane = tk.Canvas(self.main_frame)
                self.visualization_pane.grid(row = 0, column = 0)
                self.message_pane = tk.Text(self.main_frame, font = "Arial", height = 20, width = 80)
                self.message_pane.grid(row = 1, column = 0, sticky = "nsew", padx = 2, pady = 2)
                self.message_pane_scroll = tk.Scrollbar(self.main_frame, command = self.message_pane.yview)
                self.message_pane_scroll.grid(row = 1, column = 1, sticky = "nsew")
                self.message_pane["yscrollcommand"] = self.message_pane_scroll.set
                self.message_pane.insert(tk.END, "")
                self.input_pane = tk.Entry(self.main_frame)
                self.input_pane.grid(row = 2, column = 0, sticky = "nsew")
                self.input_btn = tk.Button(self.main_frame, text = "OK", width = 2, command = lambda: self.get_input())
                self.input_btn.grid(row = 2, column = 1, sticky = "nsew")
        def push_message(self, message):
                #self.message_pane.delete("1.0", "end")
                self.message_pane.insert(tk.END, "\n")
                self.message_pane.insert(tk.END, message)
        def get_input(self):
                return self.input_pane.get()