import tkinter as tk

# Tooltip
class CreateToolTip(object):
        def __init__(self, widget, text = "widget info"):
                self.wait_time = 250     # in ms
                self.wrap_length = 360   # in px
                self.widget = widget
                self.text = text
                self.widget.bind("<Enter>", self.enter)
                self.widget.bind("<Leave>", self.leave)
                self.widget.bind("<ButtonPress>", self.leave)
                self.id = None
                self.top_window = None
        def enter(self, event = None):
                self.schedule()
        def leave(self, event = None):
                self.unschedule()
                self.hide_tip()
        def schedule(self):
                self.unschedule()
                self.id = self.widget.after(self.wait_time, self.show_tip)
        def unschedule(self):
                id = self.id
                self.id = None
                if id:
                        self.widget.after_cancel(id)
        def show_tip(self, event = None):
                x = y = 0
                x, y, cx, cy = self.widget.bbox("insert")
                x += self.widget.winfo_rootx() + 25
                y += self.widget.winfo_rooty() + 20
                # creates a top-level window
                self.top_window = tk.Toplevel(self.widget)
                # leaves only the label and removes the app window
                self.top_window.wm_overrideredirect(True)
                self.top_window.wm_geometry("+%d+%d" % (x, y))
                label = tk.Label(self.top_window, text = self.text, justify = tk.LEFT, background = "#ffffff", relief = tk.SOLID, borderwidth = 1, wraplength = self.wrap_length)
                label.pack(ipadx = 1)
        def hide_tip(self):
                top_window = self.top_window
                self.top_window = None
                if top_window:
                        top_window.destroy()

# general GUI
class GUI:
        def __init__(self, main_window):
                # window
                self.main_window = main_window
                main_window.title("Shining in the Dungeon (5e Dungeon Crawler)")
                main_window.minsize(1024, 768)
                main_window.maxsize(1024, 768)
                # main game frame
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
                self.status_labels = []
                self.char_num = 0
                # visual sub frame
                self.visuals_frame = tk.Frame(self.main_frame, height = 10, width = 80)
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
                self.message_pane = tk.Text(self.message_frame, height = 20, width = 80, state = "normal", fg = "black", bg = "white")
                self.message_pane.grid(row = 0, column = 0, sticky = "w", padx = 2, pady = 2)
                self.message_pane_scroll = tk.Scrollbar(self.message_frame, command = self.message_pane.yview)
                self.message_pane_scroll.grid(row = 0, column = 1, sticky = "nsew")
                self.message_pane["yscrollcommand"] = self.message_pane_scroll.set
                self.message_pane.insert(tk.END, "")
                self.message_pane.bind("<Control-x>", lambda e: "break") # disable cut
                self.message_pane.bind("<Control-c>", lambda e: "break") # disable copy
                self.message_pane.bind("<Control-v>", lambda e: "break") # disable paste
                self.message_pane.bind("<Button-3>", lambda e: "break")  # disable right-click
                # input sub frame
                self.input_frame = tk.Frame(self.main_frame)
                self.input_frame.grid(row = 4, column = 0, columnspan = 2)
                self.main_frame.tkraise()
        # write text to message pane
        def push_message(self, message):
                self.message_pane.config(state = "normal")
                self.message_pane.insert(tk.END, "\n")
                self.message_pane.insert(tk.END, message)
                self.message_pane.see(tk.END)
                self.message_pane.config(state = "disabled")
        # write text to message pane and wait for continue
        def push_prompt(self, message):
                self.message_pane.config(state = "normal")
                self.message_pane.insert(tk.END, "\n")
                self.message_pane.insert(tk.END, message)
                self.message_pane.see(tk.END)
                self.message_pane.config(state = "disabled")
                self.submit_var = tk.IntVar()
                self.continue_btn = tk.Button(self.input_frame, text = "Next", fg = "black", bg = "white", command = lambda: self.submit_var.set(1))
                self.continue_btn.grid(row = 0, column = 0)
                self.input_frame.bind("<Key>", lambda event: self.submit_var.set(1))
                self.input_frame.focus_set()
                self.input_frame.wait_variable(self.submit_var)
                self.clear_message()
                self.submit_var = ""
                self.input_frame.unbind("<Key>")
                self.continue_btn.destroy()
        # clear message pane
        def clear_message(self):
                self.message_pane.config(state = "normal")
                self.message_pane.delete("1.0", tk.END)
                self.message_pane.config(state = "disabled")
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
        def create_status(self, char):
                self.char_num += 1
                status = "%s\n%s/%s\n%s\n%s GP" % (char.name, char.hp, char.max_hp, char.get_char_class(), char.gold)
                self.status_pane = tk.Label(self.status_frame, text = status)
                self.status_pane.grid(row = 0, column = self.char_num)
                self.status_labels.append([self.status_pane, char])
                self.status_btn = tk.Button(self.status_frame, text = "Status", width = 6, fg = "black", bg = "white", command = lambda j = char: self.create_char_status(j))
                self.status_btn.grid(row = 1, column = self.char_num)
        # update PC statuses on status pane
        def update_status(self):
                for sl in self.status_labels:
                        sl[0].config(text = "%s\n%s/%s\n%s\n%s GP" % (sl[1].name, sl[1].hp, sl[1].max_hp, sl[1].get_char_class(), sl[1].gold))
        # populate input frame with text input and button, then destroy them once content was fetched
        def get_text_input(self):
                self.input_pane = tk.Entry(self.input_frame)
                self.input_pane.grid(row = 0, column = 0, sticky = "nsew")
                self.submit_var = tk.StringVar()
                self.input_btn = tk.Button(self.input_frame, text = "OK", width = 2, fg = "black", bg = "white", command = lambda: self.submit_var.set(1))
                self.input_btn.grid(row = 0, column = 1, sticky = "nsew")
                self.input_frame.bind("<Return>", lambda event: self.submit_var.set(1))
                self.input_frame.focus_set()
                self.input_frame.wait_variable(self.submit_var)
                input_val = self.input_pane.get()
                self.input_pane.delete(0, tk.END)
                self.submit_var = ""
                self.input_frame.unbind("<Return>")
                self.input_pane.destroy()
                self.input_btn.destroy()
                self.clear_message()
                return input_val
        # select amount of units from a pool (specifically for lay on hands)
        def get_amount_lay_on_hands(self, pool, max_healable):
                self.scale_pane = tk.Scale(self.input_frame, from_ = 1, to = min(pool, max_healable), orient = tk.HORIZONTAL)
                self.scale_pane.grid(row = 0, column = 0)
                self.submit_var = tk.StringVar()
                self.input_btn = tk.Button(self.input_frame, text = "OK", width = 2, fg = "black", bg = "white", command = lambda: self.submit_var.set(1))
                self.input_btn.grid(row = 0, column = 1)
                self.input_frame.bind("<Return>", lambda event: self.submit_var.set(1))
                self.input_frame.focus_set()
                self.input_frame.wait_variable(self.submit_var)
                input_val = self.scale_pane.get()
                self.submit_var = ""
                self.input_frame.unbind("<Return>")
                self.scale_pane.destroy()
                self.input_btn.destroy()
                self.clear_message()
                return input_val
        # select amount
        def get_amount(self, max_amount):
                self.scale_pane = tk.Scale(self.input_frame, from_ = 0, to = max_amount, resolution = 0.01, orient = tk.HORIZONTAL)
                self.scale_pane.grid(row = 0, column = 0)
                self.submit_var = tk.StringVar()
                self.input_btn = tk.Button(self.input_frame, text = "OK", width = 2, fg = "black", bg = "white", command = lambda: self.submit_var.set(1))
                self.input_btn.grid(row = 0, column = 1)
                self.input_frame.bind("<Return>", lambda event: self.submit_var.set(1))
                self.input_frame.focus_set()
                self.input_frame.wait_variable(self.submit_var)
                input_val = self.scale_pane.get()
                self.submit_var = ""
                self.input_frame.unbind("<Return>")
                self.scale_pane.destroy()
                self.input_btn.destroy()
                self.clear_message()
                return input_val
        # populate input frame with buttons from hashtable input, then destroy them once choice was fetched
        def get_dict_choice_input(self, choices):
                self.submit_var = tk.IntVar()
                self.input_choice_btns = []
                for key, value in choices.items():
                        self.input_choice_btn = tk.Button(self.input_frame, text = value, fg = "black", bg = "white", command = lambda j = key: self.submit_var.set(j))
                        self.input_choice_btn.grid(row = 0, column = (key))
                        self.input_choice_btns.append(self.input_choice_btn)
                self.input_frame.wait_variable(self.submit_var)
                input_val = self.submit_var.get()
                if input_val != 0:
                        self.clear_message()
                self.submit_var = ""
                for btn in self.input_choice_btns:
                        btn.destroy()
                return input_val
        # populate input frame with buttons from hashtable input (especially for adventure choice), then destroy them once choice was fetched
        def get_dict_choice_input_adv(self, choices):
                self.submit_var = tk.IntVar()
                self.input_choice_btns = []
                for key, value in choices.items():
                        self.input_choice_btn = tk.Button(self.input_frame, text = value[0], fg = "black", bg = "white", command = lambda j = key: self.submit_var.set(j))
                        self.input_choice_btn.grid(row = 0, column = (key))
                        self.input_choice_btns.append(self.input_choice_btn)
                self.input_frame.wait_variable(self.submit_var)
                input_val = self.submit_var.get()
                if input_val != 0:
                        self.clear_message()
                self.submit_var = ""
                for btn in self.input_choice_btns:
                        btn.destroy()
                return input_val
        # populate input frame with buttons from hashtable input (specially for shopping flow), then destroy them once choice was fetched
        def get_dict_choice_input_shop(self, choices):
                self.submit_var = tk.IntVar()
                self.input_choice_btns = []
                self.input_choice_exit_btn = tk.Button(self.input_frame, text = "exit", width = 4, fg = "black", bg = "white", command = lambda j = -1: self.submit_var.set(j))
                self.input_choice_exit_btn.grid(row = 0, column = 0)
                self.input_frame.bind("<space>", lambda event: self.submit_var.set(-1))
                self.input_choice_btns.append(self.input_choice_exit_btn)
                self.input_frame.focus_set()
                for key, value in choices.items():
                        self.input_choice_btn = tk.Button(self.input_frame, text = value, fg = "black", bg = "white", command = lambda j = key: self.submit_var.set(j))
                        self.input_choice_btn.grid(row = 0, column = (key))
                        self.input_choice_btns.append(self.input_choice_btn)
                self.input_frame.wait_variable(self.submit_var)
                input_val = self.submit_var.get()
                if input_val != 0:
                        self.clear_message()
                self.submit_var = ""
                self.input_frame.unbind("<space>")
                for btn in self.input_choice_btns:
                        btn.destroy()
                return input_val
        # populate input frame with buttons from hashtable input (specially for racial menu), then destroy them once choice was fetched
        def get_dict_choice_input_racial(self, choices):
                self.submit_var = tk.IntVar()
                self.input_choice_btns = []
                self.input_choice_reroll_btn = tk.Button(self.input_frame, text = "reroll", width = 6, fg = "black", bg = "white", command = lambda j = -1: self.submit_var.set(j))
                r = 0
                self.input_choice_reroll_btn.grid(row = r, column = 3, sticky = "nesw")
                self.input_choice_btns.append(self.input_choice_reroll_btn)
                r += 1
                for key, value in choices.items():
                        if key != 0:
                                self.input_choice_btn = tk.Button(self.input_frame, text = value, fg = "black", bg = "white", command = lambda j = key: self.submit_var.set(j))
                                if (key - 1) % 7 == 0:
                                        r += 1
                                self.input_choice_btn.grid(row = r, column = (key - 1) % 7, sticky = "nesw")
                                self.input_choice_btn_ttp = CreateToolTip(self.input_choice_btn, self.race_stats_lookup(key, 1))
                                self.input_choice_btns.append(self.input_choice_btn)
                self.input_frame.wait_variable(self.submit_var)
                input_val = self.submit_var.get()
                if input_val != 0:
                        self.clear_message()
                self.submit_var = ""
                for btn in self.input_choice_btns:
                        btn.destroy()
                return input_val
        # populate input frame with buttons from hashtable input (specially for subracial menu), then destroy them once choice was fetched
        def get_dict_choice_input_subracial(self, choices):
                self.submit_var = tk.IntVar()
                self.input_choice_btns = []
                for key, value in choices.items():
                        self.input_choice_btn = tk.Button(self.input_frame, text = value, fg = "black", bg = "white", command = lambda j = key: self.submit_var.set(j))
                        self.input_choice_btn.grid(row = 0, column = key)
                        self.input_choice_btn_ttp = CreateToolTip(self.input_choice_btn, self.race_stats_lookup(key, 2))
                        self.input_choice_btns.append(self.input_choice_btn)
                self.input_frame.wait_variable(self.submit_var)
                input_val = self.submit_var.get()
                if input_val != 0:
                        self.clear_message()
                self.submit_var = ""
                for btn in self.input_choice_btns:
                        btn.destroy()
                return input_val
        # populate input frame with buttons from array input (specially for shop's item listing), then destroy them once choice was fetched
        def get_list_choice_input_shop(self, choices):
                self.submit_var = tk.IntVar()
                self.input_choice_btns = []
                self.input_choice_skip_btn = tk.Button(self.input_frame, text = "exit", width = 4, fg = "black", bg = "white", command = lambda j = -1: self.submit_var.set(j))
                self.input_choice_skip_btn.grid(row = 0, column = 0)
                self.input_frame.bind("<space>", lambda event: self.submit_var.set(-1))
                self.input_frame.focus_set()
                self.input_choice_btns.append(self.input_choice_skip_btn)
                for i in choices:
                        if i[0] != "sold":
                                self.input_choice_btn = tk.Button(self.input_frame, text = i[0], width = len(i[0]), fg = "black", bg = "white", command = lambda j = i[1]: self.submit_var.set(j))
                                self.input_choice_btn.grid(row = 0, column = i[1])
                                self.input_choice_btn_ttp = CreateToolTip(self.input_choice_btn, str(i[2]))
                                self.input_choice_btns.append(self.input_choice_btn)
                self.input_frame.wait_variable(self.submit_var)
                input_val = self.submit_var.get()
                self.submit_var = ""
                self.input_frame.unbind("<space>")
                for btn in self.input_choice_btns:
                        btn.destroy()
                self.clear_message()
                return input_val
        # populate input frame with buttons from array input (specially for rest healing menu), then destroy them once choice was fetched
        def get_list_choice_input_rest_heal(self, choices):
                self.submit_var = tk.IntVar()
                self.input_choice_btns = []
                self.input_choice_skip_btn = tk.Button(self.input_frame, text = "back", width = 4, fg = "black", bg = "white", command = lambda j = 0: self.submit_var.set(j))
                self.input_choice_skip_btn.grid(row = 0, column = 0)
                self.input_choice_btns.append(self.input_choice_skip_btn)
                btn_text = ""
                i = 0
                for c in choices:
                        btn_text = "%s (%s)" % (c[0], c[1].name)
                        self.input_choice_btn = tk.Button(self.input_frame, text = btn_text, width = len(btn_text), fg = "black", bg = "white", command = lambda j = i: self.submit_var.set(j))
                        self.input_choice_btn.grid(row = 0, column = i + 1)
                        self.input_choice_btns.append(self.input_choice_btn)
                        i += 1
                self.input_frame.wait_variable(self.submit_var)
                input_val = self.submit_var.get()
                self.submit_var = ""
                for btn in self.input_choice_btns:
                        btn.destroy()
                self.clear_message()
                return input_val
         # populate input frame with buttons from array input, then destroy them once choice was fetched
        def get_list_choice_input(self, choices):
                self.submit_var = tk.IntVar()
                self.input_choice_btns = []
                i = 0
                for c in choices:
                        self.input_choice_btn = tk.Button(self.input_frame, text = c.name, width = len(c.name), fg = "black", bg = "white", command = lambda j = i: self.submit_var.set(j))
                        self.input_choice_btn.grid(row = 0, column = i)
                        self.input_choice_btns.append(self.input_choice_btn)
                        i += 1
                self.input_frame.wait_variable(self.submit_var)
                input_val = self.submit_var.get()
                self.submit_var = ""
                for btn in self.input_choice_btns:
                        btn.destroy()
                self.clear_message()
                return input_val
        # populate input frame with yes/no buttons, then destroy them once choice was fetched
        def get_binary_input(self):
                self.submit_var = tk.IntVar()
                self.input_yes_btn = tk.Button(self.input_frame, text = "Yes", width = 5, fg = "black", bg = "white", command = lambda: self.submit_var.set(1))
                self.input_yes_btn.grid(row = 0, column = 0)
                self.input_no_btn = tk.Button(self.input_frame, text = "No", width = 5, fg = "black", bg = "white", command = lambda: self.submit_var.set(0))
                self.input_no_btn.grid(row = 0, column = 1)
                self.input_frame.bind("<Key-1>", lambda event: self.submit_var.set(1))
                self.input_frame.bind("<Key-0>", lambda event: self.submit_var.set(0))
                self.input_frame.focus_set()
                self.input_frame.wait_variable(self.submit_var)
                input_val = self.submit_var.get()
                self.submit_var = ""
                self.input_frame.unbind("<Key-1>")
                self.input_frame.unbind("<Key-0>")
                self.input_yes_btn.destroy()
                self.input_no_btn.destroy()
                self.clear_message()
                return input_val
        # populate input frame with buttons from hashtable input for battle menu specifically, then destroy them once choice was fetched
        def get_battle_menu_choice_input(self, choices):
                self.submit_var = tk.IntVar()
                self.input_choice_btns = []
                for key, value in choices.items():
                        self.input_choice_btn = tk.Button(self.input_frame, text = value[0], width = len(value[0]), fg = "black", bg = "white", command = lambda j = key: self.submit_var.set(j))
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
        # create character status overlay
        def create_char_status(self, char):
                # pop-up status main frame
                char_stats = char.print_char_status()
                self.char_stats_frame = tk.Frame(self.main_window, borderwidth = 2, relief = tk.RAISED)
                self.char_stats_frame.place(x = 1, y = 1)
                self.char_stats_frame.bind("<Key>", lambda event: self.destroy_char_status())
                self.char_stats_frame.focus_set()
                # title
                self.char_stats_title_frame = tk.Frame(self.char_stats_frame, borderwidth = 1, relief = tk.GROOVE)
                self.char_stats_title_frame.pack(side = tk.TOP, fill = tk.BOTH)
                self.title_label = tk.Label(self.char_stats_title_frame, text = "%s's status" % (char.name), justify = tk.LEFT)
                self.title_label.grid(row = 0, column = 0)
                self.class_label = tk.Label(self.char_stats_title_frame, text = char.get_char_class(), justify = tk.LEFT)
                self.class_label.grid(row = 0, column = 1)
                self.race_label = tk.Label(self.char_stats_title_frame, text = "%s (%s)" % (char.get_char_race(), char.get_char_subrace()), justify = tk.LEFT)
                self.race_label.grid(row = 0, column = 2)
                self.xp_label = tk.Label(self.char_stats_title_frame, text = "Level: %s (XP: %s/%s)" % (char.level, char.xp, char.get_level_up_cap()), justify = tk.LEFT)
                self.xp_label.grid(row = 0, column = 3)
                self.done_btn = tk.Button(self.char_stats_title_frame, text = "Done", width = 4, fg = "black", bg = "white", command = lambda: self.destroy_char_status())
                self.done_btn.grid(row = 0, column = 4)
                # combat
                self.char_stats_combat_frame = tk.Frame(self.char_stats_frame, borderwidth = 1, relief = tk.GROOVE)
                self.char_stats_combat_frame.pack(side = tk.TOP, fill = tk.BOTH)
                self.combat_label = tk.Label(self.char_stats_combat_frame, text = char_stats[5], justify = tk.LEFT)
                self.combat_label.grid(row = 0, column = 0)
                # basic
                self.char_stats_basic_frame = tk.Frame(self.char_stats_frame, borderwidth = 1, relief = tk.GROOVE)
                self.char_stats_basic_frame.pack(side = tk.TOP, fill = tk.BOTH)
                self.abilities_label = tk.Label(self.char_stats_basic_frame, text = char_stats[0], justify = tk.LEFT)
                self.abilities_label.grid(row = 0, column = 0)
                self.scores_label = tk.Label(self.char_stats_basic_frame, text = char_stats[1], justify = tk.LEFT)
                self.scores_label.grid(row = 0, column = 1)
                self.mods_label = tk.Label(self.char_stats_basic_frame, text = char_stats[2], justify = tk.LEFT)
                self.mods_label.grid(row = 0, column = 2)
                self.saving_throws_label = tk.Label(self.char_stats_basic_frame, text = char_stats[3], justify = tk.LEFT)
                self.saving_throws_label.grid(row = 0, column = 3)
                self.skills_label = tk.Label(self.char_stats_basic_frame, text = char_stats[10], justify = tk.LEFT)
                self.skills_label.grid(row = 0, column = 4)
                # conditions
                self.char_stats_cond_frame = tk.Frame(self.char_stats_frame, borderwidth = 1, relief = tk.GROOVE)
                self.char_stats_cond_frame.pack(side = tk.TOP, fill = tk.BOTH)
                self.conditions_label = tk.Label(self.char_stats_cond_frame, text = char_stats[4], justify = tk.LEFT)
                self.conditions_label.grid(row = 0, column = 0)
                # resistances
                self.char_stats_resist_frame = tk.Frame(self.char_stats_frame, borderwidth = 1, relief = tk.GROOVE)
                self.char_stats_resist_frame.pack(side = tk.TOP, fill = tk.BOTH)
                self.resistances_label = tk.Label(self.char_stats_resist_frame, text = char_stats[11], justify = tk.LEFT)
                self.resistances_label.grid(row = 0, column = 0)
                # equipped
                self.char_stats_equip_frame = tk.Frame(self.char_stats_frame, borderwidth = 1, relief = tk.GROOVE)
                self.char_stats_equip_frame.pack(side = tk.TOP, fill = tk.BOTH)
                self.equipped_label = tk.Label(self.char_stats_equip_frame, text = char_stats[6], justify = tk.LEFT)
                self.equipped_label.grid(row = 0, column = 0)
                # inventory
                self.char_stats_inv_frame = tk.Frame(self.char_stats_frame, borderwidth = 1, relief = tk.GROOVE)
                self.char_stats_inv_frame.pack(side = tk.TOP, fill = tk.BOTH)
                self.inventory_label = tk.Label(self.char_stats_inv_frame, text = char_stats[7], justify = tk.LEFT)
                self.inventory_label.grid(row = 0, column = 0)
                # specials
                self.char_stats_specials_frame = tk.Frame(self.char_stats_frame, borderwidth = 1, relief = tk.GROOVE)
                self.char_stats_specials_frame.pack(side = tk.TOP, fill = tk.BOTH)
                self.specials_label = tk.Label(self.char_stats_specials_frame, text = char_stats[8], justify = tk.LEFT)
                self.specials_label.grid(row = 0, column = 0)
                # death saves
                self.char_stats_death_saves_frame = tk.Frame(self.char_stats_frame, borderwidth = 1, relief = tk.GROOVE)
                self.char_stats_death_saves_frame.pack(side = tk.TOP, fill = tk.BOTH)
                self.death_saves_label = tk.Label(self.char_stats_death_saves_frame, text = char_stats[9], justify = tk.LEFT)
                self.death_saves_label.grid(row = 0, column = 0)
        # remove character status overlay
        def destroy_char_status(self):
                self.char_stats_frame.unbind("<Key>")
                self.char_stats_frame.destroy()
        # disable battle menu button according to action economy rules
        def disable_button(self, btn):
                btn.configure(state = tk.DISABLED)
        '''
        Lookup for racial/subracial float text
        IN
        - race/subrace value (int)
        - race/subrace flag (int)
        OUT
        - stats text (string)
        '''
        def race_stats_lookup(self, race, flag):
                racial_stats = {
                        0: "N/A",
                        1: "+1 STR +1 DEX +1 CON +1 INT +1 WIS +1 CHA",
                        2: "+2 DEX",
                        3: "+2 CON",
                        4: "+2 INT",
                        5: "+2 DEX",
                        6: "+2 STR +1 CON",
                        7: "+2 STR +1 CHA",
                        8: "+2 CHA +1 INT",
                        9: "+2 DEX +1 WIS",
                        10: "+2 CON",
                        11: "+2 STR +1 CON",
                        12: "+2 CHA",
                        13: "+2 WIS +1 STR",
                        14: "+1 INT"
                        }
                subracial_stats = {
                        0: "N/A",
                        11: "N/A",
                        21: "+1 CHA",
                        22: "+1 CON",
                        23: "+1 WIS",
                        31: "+1 WIS",
                        32: "+2 STR",
                        33: "+1 STR",
                        41: "+1 DEX",
                        42: "+1 CON",
                        43: "+1 DEX",
                        51: "+1 INT",
                        52: "+1 WIS",
                        53: "+1 CHA",
                        61: "N/A",
                        71: "N/A",
                        81: "N/A",
                        91: "N/A",
                        101: "+1 DEX",
                        102: "+1 STR",
                        103: "+1 INT",
                        104: "+1 WIS",
                        111: "N/A",
                        121: "+1 STR",
                        122: "+1 WIS",
                        123: "+1 CON",
                        131: "N/A",
                        141: "+2 STR",
                        142: "+2 WIS"
                        }
                if flag == 1:
                        stats = racial_stats[race]
                elif flag == 2:
                        stats = subracial_stats[race]
                return stats