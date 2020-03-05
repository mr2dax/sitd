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
                self.quit_button = tk.Button(self.main_frame, text="Quit", width = 4, command = lambda: quit())
                self.quit_button.grid(row = 0, column = 1)
                self.message_pane = tk.Text(self.main_frame, height = 20, width = 80)
                self.message_pane.grid(row = 1, column = 0, sticky = "nsew", padx = 2, pady = 2)
                self.message_pane_scroll = tk.Scrollbar(self.main_frame, command = self.message_pane.yview)
                self.message_pane_scroll.grid(row = 1, column = 1, sticky = "nsew")
                self.message_pane["yscrollcommand"] = self.message_pane_scroll.set
                self.message_pane.insert(tk.END, "")
                self.input_frame = tk.Frame(self.main_frame)
                self.input_frame.grid(row = 2, column = 0)
                self.menu_frame = tk.Frame(self.main_frame)
                self.menu_frame.grid(row = 3, column = 0)
                self.main_frame.tkraise()
        def push_message(self, message):
                #self.message_pane.delete("1.0", "end")
                self.message_pane.insert(tk.END, "\n")
                self.message_pane.insert(tk.END, message)
                self.message_pane.see(tk.END)
        def get_text_input(self):
                self.input_pane = tk.Entry(self.input_frame)
                self.input_pane.grid(row = 0, column = 0, sticky = "nsew")
                self.submit_var = tk.StringVar()
                self.input_btn = tk.Button(self.input_frame, text = "OK", width = 2, command = lambda: self.submit_var.set(1))
                self.input_btn.grid(row = 0, column = 1, sticky = "nsew")
                self.input_frame.wait_variable(self.submit_var)
                input_val = self.input_pane.get()
                self.input_pane.delete(0, tk.END)
                self.submit_var = ""
                self.input_pane.destroy()
                self.input_btn.destroy()
                return input_val
        def get_dict_choice_input(self, choices):
                self.submit_var = tk.IntVar()
                self.input_choice_btns = []
                for key, value in choices.items():
                        self.input_choice_btn = tk.Button(self.input_frame, text = value, width = len(value), command = lambda j = key: self.submit_var.set(j))
                        self.input_choice_btn.grid(row = 0, column = (key))
                        self.input_choice_btns.append(self.input_choice_btn)
                self.input_frame.wait_variable(self.submit_var)
                input_val = self.submit_var.get()
                self.submit_var = ""
                for btn in self.input_choice_btns:
                        btn.destroy()
                return input_val
        def get_list_choice_input(self, choices):
                self.submit_var = tk.IntVar()
                self.input_choice_btns = []
                self.input_choice_skip_btn = tk.Button(self.input_frame, text = "skip", width = 4, command = lambda j = -1: self.submit_var.set(j))
                self.input_choice_skip_btn.grid(row = 0, column = 0)
                self.input_choice_btns.append(self.input_choice_skip_btn)
                for i in choices:
                        if i[0] != "sold":
                                self.input_choice_btn = tk.Button(self.input_frame, text = i[0], width = len(i[0]), command = lambda j = i[1]: self.submit_var.set(j))
                                self.input_choice_btn.grid(row = 0, column = i[1])
                                self.input_choice_btns.append(self.input_choice_btn)
                self.input_frame.wait_variable(self.submit_var)
                input_val = self.submit_var.get()
                self.submit_var = ""
                for btn in self.input_choice_btns:
                        btn.destroy()
                return input_val
        def get_yesno_input(self):
                self.submit_var = tk.IntVar()
                self.input_yes_btn = tk.Button(self.input_frame, text = "Yes", width = 5, command = lambda: self.submit_var.set(1))
                self.input_yes_btn.grid(row = 0, column = 0)
                self.input_no_btn = tk.Button(self.input_frame, text = "No", width = 5, command = lambda: self.submit_var.set(0))
                self.input_no_btn.grid(row = 0, column = 1)
                self.input_frame.wait_variable(self.submit_var)
                input_val = self.submit_var.get()
                self.submit_var = ""
                self.input_yes_btn.destroy()
                self.input_no_btn.destroy()
                return input_val