import tkinter as tk

#GUI
class GUI:
        def __init__(self, main_window):
                # window
                self.main_window = main_window
                main_window.title("Shining in the Dungeon (5e Duel)")
                main_window.minsize(1024, 768)
                main_window.maxsize(1024, 768)
                # top frame
                self.main_frame = tk.Frame(main_window)
                self.main_frame.pack(side = tk.LEFT)
                # info sub frame
                self.info_frame = tk.Frame(self.main_frame, height = 5, width = 80)
                self.info_frame.grid(row = 0, column = 0)
                # information
                self.battle_pane = tk.Label(self.info_frame, text = "")
                self.battle_pane.grid(row = 0, column = 0)
                self.round_pane = tk.Label(self.info_frame, text = "")
                self.round_pane.grid(row = 0, column = 1)
                self.turn_pane = tk.Label(self.info_frame, text = "")
                self.turn_pane.grid(row = 0, column = 2)
                # status sub frame
                self.status_frame = tk.Frame(self.main_frame, height = 5, width = 80)
                self.status_frame.grid(row = 1, column = 0)
                # visual sub frame
                self.visuals_frame = tk.Frame(self.main_frame, height = 5, width = 80)
                self.visuals_frame.grid(row = 2, column = 0)
                # visualization
                self.visuals_pane = tk.Canvas(self.visuals_frame, height = 50, width = 80)
                self.visuals_pane.grid(row = 0, column = 0)
                self.visuals_pane.create_rectangle(50, 25, 150, 75, fill = "blue")
                # initiative board
                self.init_board_pane = tk.Label(self.visuals_frame, text = "")
                self.init_board_pane.grid(row = 0, column = 1)
                # quit button
                #self.quit_button = tk.Button(self.main_frame, text="Quit", width = 4, command = lambda: quit())
                #self.quit_button.grid(row = 1, column = 1)
                # message sub frame
                self.message_frame = tk.Frame(self.main_frame)
                self.message_frame.grid(row = 3, column = 0)
                # message box
                self.message_pane = tk.Text(self.message_frame, height = 20, width = 80)
                self.message_pane.grid(row = 0, column = 0, sticky = "nsew", padx = 2, pady = 2)
                self.message_pane_scroll = tk.Scrollbar(self.message_frame, command = self.message_pane.yview)
                self.message_pane_scroll.grid(row = 0, column = 1, sticky = "nsew")
                self.message_pane["yscrollcommand"] = self.message_pane_scroll.set
                self.message_pane.insert(tk.END, "")
                # input sub frame
                self.input_frame = tk.Frame(self.main_frame)
                self.input_frame.grid(row = 4, column = 0)
                self.main_frame.tkraise()
        # write text to message pane
        def push_message(self, message):
                #self.message_pane.delete("1.0", "end")
                self.message_pane.insert(tk.END, "\n")
                self.message_pane.insert(tk.END, message)
                self.message_pane.see(tk.END)
        # write battle info
        def push_battle_info(self, message):
                if self.battle_pane.winfo_exists == 1:
                        self.battle_pane.destroy()
                self.battle_pane.config(text = message)
        # update round info
        def update_round_info(self, message):
                if self.round_pane.winfo_exists == 1:
                        self.round_pane.destroy()
                self.round_pane.config(text = message)
        # update turn info
        def update_turn_info(self, message):
                if self.turn_pane.winfo_exists == 1:
                        self.turn_pane.destroy()
                self.turn_pane.config(text = message)
        # update initiative board
        def update_init_board(self, init_board):
                board = ""
                for i in range(len(init_board)):
                        board += init_board[i][1] + ": " + str(init_board[i][0]) + "\n"
                self.init_board_pane.config(text = board)
        # initialize status pane with PCs
        def create_status(self, char_groups):
                i = 0
                self.status_labels = []
                for ch in char_groups[0]:
                        i += 1
                        status = ch.name + "\n" + str(ch.hp) + "/" + str(ch.max_hp)
                        self.status_pane = tk.Label(self.status_frame, text = status)
                        self.status_pane.grid(row = 0, column = i)
                        self.status_labels.append([self.status_pane, ch])
        # update PC statuses on status pane
        def update_status(self):
                for sl in self.status_labels:
                        sl[0].config(text = sl[1].name + "\n" + str(sl[1].hp) + "/" + str(sl[1].max_hp))
        # populate input frame with text input and button, then destroy them once content was fetched
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
        # populate input frame with buttons from hashtable input, then destroy them once choice was fetched
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
        # populate input frame with buttons from array input, then destroy them once choice was fetched
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
        # populate input frame with yes/no buttons, then destroy them once choice was fetched
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
        # populate input frame with buttons from hashtable input for battle menu specifically, then destroy them once choice was fetched
        def get_battle_menu_choice_input(self, choices):
                self.submit_var = tk.IntVar()
                self.input_choice_btns = []
                for key, value in choices.items():
                        self.input_choice_btn = tk.Button(self.input_frame, text = value[0], width = len(value[0]), command = lambda j = key: self.submit_var.set(j))
                        self.input_choice_btn.grid(row = 0, column = (key))
                        self.input_choice_btns.append(self.input_choice_btn)
                        if value[1] < 1:
                                self.disable_button(self.input_choice_btn)
                self.input_frame.wait_variable(self.submit_var)
                input_val = self.submit_var.get()
                self.submit_var = ""
                for btn in self.input_choice_btns:
                        btn.destroy()
                return input_val
        # disable battle menu button according to action economy rules
        def disable_button(self, btn):
                btn.configure(state = tk.DISABLED)