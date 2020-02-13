import random
import math
import string

class Character:
        "Character creation."
        def __init__(self, name, str, dex, con, wis, int, cha, starting_lvl):
                self.str = str
                self.dex = dex
                self.con = con
                self.wis = wis
                self.int = int
                self.cha = cha
                self.starting_lvl = starting_lvl
                self.player_id = random_str(10)
                self.level = 1
                self.char_class = 0
                self.hd_cnt = 1
                self.hd = 0
                self.xp = 0
                self.gold = 0
                self.prof_bonus = 2
                self.attacks = 1
                self.bonus_attack = False
                self.str_mod = math.floor((self.str - 10) / 2)
                self.dex_mod = math.floor((self.dex - 10) / 2)
                self.con_mod = math.floor((self.con - 10) / 2)
                self.wis_mod = math.floor((self.wis - 10) / 2)
                self.int_mod = math.floor((self.int - 10) / 2)
                self.cha_mod = math.floor((self.cha - 10) / 2)
                self.ranged_att_mod = self.dex_mod + self.prof_bonus
                self.melee_att_mod = self.str_mod + self.prof_bonus
                self.ranged_dmg_mod = max(0, self.dex_mod)
                self.melee_dmg_mod = max(0, self.str_mod)
                self.dmg_die = 1
                self.dmg_die_cnt = 1
                self.dmg_die_offhand = 1
                self.dmg_die_cnt_offhand = 1
                self.ac = 10 + self.dex_mod
                self.init_mod = self.dex_mod
                self.max_hp = 0
                self.hp = 0
                self.temp_hp = 0
                self.str_st = self.str_mod
                self.str_st_adv = False
                self.dex_st = self.dex_mod
                self.dex_st_adv = False
                self.con_st = self.con_mod
                self.con_st_adv = False
                self.wis_st = self.wis_mod
                self.wis_st_adv = False
                self.int_st = self.int_mod
                self.int_st_adv = False
                self.cha_st = self.cha_mod
                self.cha_st_adv = False
                self.death_st = 0
                self.death_st_success = 0
                self.death_st_fail = 0
                self.athl = self.str_mod
                self.acro = self.dex_mod
                self.perc = self.wis_mod
                self.inv = self.int_mod
                self.reroll_dmg = False
                self.offhand_dmg_mod = False
                self.eq_weapon_main = "unarmed strike"
                self.eq_weapon_offhand = "nothing"
                self.eq_armor = "nothing"
                self.ranged = False
                self.fighting_style = 0
                if name == "":
                        self.name = "Rick"
                else:
                    self.name = name
                self.action = 1
                self.bonus_action = 1
                self.reaction = 1
                self.free_action = 1
                self.actions = {}
                self.bonus_actions = {}
                self.specials = {}
                self.conditions = {
                        "flee": False,
                        "down": False,
                        "dead": False,
                        "dodge": False,
                        "prone": False,
                        "grappled": False
                        }
                self.grappled_by = ""
                self.grappling = ""
                if self.starting_lvl > 2:
                        self.level_up(self.starting_lvl - 1)
        def action_economy(self):
                self.actions = {
                        1: "attack",
                        2: "dodge",
                        3: "disengage"
                        }
                if self.str >= 13:
                        self.actions[4] = "shove"
                if self.str >= 13 and (self.fighting_style in [2, 3, 5] or self.char_class == 2):
                        self.actions[5] = "grapple"
                if self.char_class == 5:
                        self.actions[7] = "lay on hands"
                ba = 0
                if self.bonus_attack:
                        ba += 1
                        self.bonus_actions[ba] = "attack"
                if self.char_class == 2:
                        ba += 1
                        self.bonus_actions[ba] = "second wind"
        def deaths_door(self):
                death_st = roll_dice(20, 0, 0)
                if death_st[1] == 1:
                        self.conditions["down"] = False
                        self.hp = 1
                        print(self.name + " is back up!")
                elif death_st[1] == -1:
                        if self.death_st_fail == 2:
                                self.death_st_fail += 1
                        else:
                                self.death_st_fail += 2
                else:
                        if death_st[0] < 10:
                                self.death_st_fail += 1
                        elif death_st[0] >= 10:
                                self.death_st_success += 1
                print("Death Saving Throw: " + str(death_st[0]) + " (S:" + str(self.death_st_success) + ",F:" + str(self.death_st_fail) + ")")
                if self.death_st_fail > 2:
                        self.conditions["dead"] = True
                        print(self.name + " just died. RIP")
                if self.death_st_success > 2:
                        self.hp = 0
                        print(self.name + " has stabilized.")
        def print_char_status(self):
                print(vars(self))
        def reset_until_next_turn_conditions(self):
                if self.conditions["prone"] and not self.conditions["grappled"]:
                        self.conditions["prone"] = False
                        print(self.name + " stood up.")
                        if 3 not in self.actions:
                                self.actions[3] = "disengage"
                if self.conditions["dodge"]:
                        self.conditions["dodge"] = False
                        print("Dodge ended.")
                if self.conditions["flee"]:
                        self.conditions["flee"] = False
                        print(self.name + " couldn't run away.")
                if (self.fighting_style == 4 or self.char_class == 2) and 1 not in self.bonus_actions:
                        self.bonus_actions[1] = "attack"
        def print_conditions(self):
                print(self.conditions)
        def print_actions(self):
                print(self.actions)
        def print_bonus_actions(self):
                print(self.bonus_actions)
        def gen_starting_gold(self, char_class):
                gold_die = {
                        1: 5,
                        2: 5,
                        3: 2,
                        4: 4,
                        5: 5
                        }
                for i in range(gold_die[char_class]):
                        self.gold += roll_dice(4, 0, 0)[0]
                if char_class != 2:
                        self.gold *= 10
        def gen_class(self, inv, class_choice):
                if class_choice == 1:
                        self.char_class = 1
                        self.hd = 10
                        self.hp = self.con_mod + self.hd
                        self.max_hp = self.hp
                        self.athl += self.prof_bonus
                        self.acro += self.prof_bonus
                        self.second_wind = True
                        self.second_wind_cnt = 1
                        self.str_st += self.prof_bonus
                        self.con_st += self.prof_bonus
                        self.gen_fighting_style(inv)
                elif class_choice == 2:
                        self.char_class = 2
                        self.hd = 10
                        self.hp = self.con_mod + self.hd
                        self.max_hp = self.hp
                        self.bonus_attack = True
                        self.acro += self.prof_bonus
                        self.perc += self.prof_bonus
                        self.str_st += self.prof_bonus
                        self.dex_st += self.prof_bonus
                elif class_choice == 3:
                        self.char_class = 3
                        self.hd = 12
                        self.hp = self.con_mod + self.hd
                        self.max_hp = self.hp
                        self.athl += self.prof_bonus
                        self.acro += self.prof_bonus
                        self.str_st += self.prof_bonus
                        self.con_st += self.prof_bonus
                        self.specials["rage"] = 2
                elif class_choice == 4:
                        self.char_class = 4
                        self.hd = 8
                        self.hp = self.con_mod + self.hd
                        self.max_hp = self.hp
                        self.bonus_attack = True
                        self.acro += self.prof_bonus * 2
                        self.perc += self.prof_bonus * 2
                        self.dex_st += self.prof_bonus
                        self.int_st += self.prof_bonus
                        self.specials["sneak attack"] = [6, 1]
                elif class_choice == 5:
                        self.char_class = 5
                        self.hd = 10
                        self.hp = self.con_mod + self.hd
                        self.max_hp = self.hp
                        self.athl += self.prof_bonus
                        self.perc += self.prof_bonus
                        self.wis_st += self.prof_bonus
                        self.cha_st += self.prof_bonus
                print("You have " + str(self.gold) + " GP to spend.")
                starting_shop = Shop()
                self.gen_starting_equipment(inv, class_choice, self.fighting_style)
        def gen_fighting_style(self, inv):
                styles = {
                        1: "sword and board (defense)",
                        2: "great weapon fighting",
                        3: "dueling",
                        4: "two-weapon fighting",
                        5: "archery"
                        }
                if self.char_class == 5:
                        style.pop(5)
                print(styles)
                style_choice = int(input("Choose your fighting style: "))
                if self.char_class != 5:
                        if style_choice == 1:
                                self.fighting_style = 1
                        elif style_choice == 2:
                                self.fighting_style = 2
                                self.reroll_dmg = True
                        elif style_choice == 3:
                                self.fighting_style = 3
                                self.melee_dmg_mod += 2
                        elif style_choice == 4:
                                self.fighting_style = 4
                                self.offhand_dmg_mod = True
                                self.bonus_attack = True
                        elif style_choice == 5:
                                self.fighting_style = 5
                                self.ranged_att_mod += 2
                                self.ranged = True
                else:
                        if style_choice == 1:
                                self.fighting_style = 1
                                self.ac += 1
                        elif style_choice == 2:
                                self.fighting_style = 2
                                self.reroll_dmg = True
                        elif style_choice == 3:
                                self.fighting_style = 3
                                self.melee_dmg_mod += 2
                        elif style_choice == 4:
                                self.fighting_style = 4
                                self.offhand_dmg_mod = True
                                self.bonus_attack = True
        def gen_starting_equipment(self, inv, class_choice, style_choice):
                if class_choice == 1:
                        if style_choice == 1:
                                inv.add_item("longsword")
                                inv.add_item("shield")
                                inv.add_item("medium armor")
                                self.eq_weapon_main = "longsword"
                                self.dmg_die = 8
                                self.dmg_die_cnt = 1
                                self.eq_weapon_offhand = "shield"
                                self.ac += 2
                                self.eq_armor = "medium armor"
                                if self.dex_mod <= 2:
                                        self.ac += 5 + 1
                                else:
                                        self.ac = 10 + 2 + 5 + 1
                        elif style_choice == 2:
                                inv.add_item("greatsword")
                                inv.add_item("heavy armor")
                                self.eq_weapon_main = "greatsword"
                                self.dmg_die = 6
                                self.dmg_die_cnt = 2
                                self.eq_armor = "heavy armor"
                                if self.dex_mod <= 0:
                                        self.ac = 18
                                else:
                                        self.ac += 8 - self.dex_mod
                        elif style_choice == 3:
                                inv.add_item("longsword")
                                inv.add_item("heavy armor")
                                self.eq_weapon_main = "longsword"
                                self.dmg_die = 8
                                self.dmg_die_cnt = 1
                                self.eq_armor = "heavy armor"
                                if self.dex_mod <= 0:
                                        self.ac = 18
                                else:
                                        self.ac += 8 - self.dex_mod
                        elif style_choice == 4:
                                inv.add_item("rapier")
                                inv.add_item("scimitar")
                                inv.add_item("light armor")
                                self.eq_weapon_main = "shortsword"
                                self.eq_weapon_offhand = "scimitar"
                                self.dmg_die = 8
                                self.dmg_die_cnt = 1
                                self.dmg_die_offhand = 6
                                self.dmg_die_cnt_offhand = 1
                                self.eq_armor = "light armor"
                                self.ac += 2
                        elif style_choice == 5:
                                inv.add_item("longbow")
                                inv.add_item("arrow")
                                inv.add_item("medium armor")
                                self.eq_weapon_main = "longbow"
                                self.dmg_die = 8
                                self.dmg_die_cnt = 1
                                self.eq_armor = "medium armor"
                                if self.dex_mod <= 2:
                                        self.ac += 5
                                else:
                                        self.ac = 10 + 2 + 5
                elif class_choice == 2:
                        inv.add_item("quarterstaff")
                        self.dmg_die = 8
                        self.dmg_die_cnt = 1
                        self.dmg_die_offhand = 4
                        self.dmg_die_cnt_offhand = 1
                        self.eq_weapon_main = "quarterstaff"
                        self.eq_weapon_offhand = "unarmed strike"
                        if self.wis_mod > 0:
                                self.ac += self.wis_mod
                elif class_choice == 3:
                        inv.add_item("greataxe")
                        self.dmg_die = 12
                        self.dmg_die_cnt = 1
                        self.eq_weapon_main = "greataxe"
                        if self.con_mod > 0:
                                self.ac += self.con_mod
                elif class_choice == 4:
                        inv.add_item("shortsword")
                        inv.add_item("shortsword")
                        inv.add_item("light armor")
                        self.dmg_die = 6
                        self.dmg_die_cnt = 1
                        self.dmg_die_offhand = 6
                        self.dmg_die_cnt_offhand = 1
                        self.eq_weapon_main = "shortsword"
                        self.eq_weapon_offhand = "shortsword"
                        self.eq_armor = "light armor"
                        self.ac += 2
                elif class_choice == 5:
                        inv.add_item("warhammer")
                        inv.add_item("heavy armor")
                        inv.add_item("shield")
                        self.eq_weapon_main = "warhammer"
                        self.eq_weapon_offhand = "shield"
                        self.dmg_die = 8
                        self.dmg_die_cnt = 1
                        self.eq_armor = "heavy armor"
                        if self.dex_mod <= 0:
                                self.ac = 18
                        else:
                                self.ac += 8 - self.dex_mod
                        self.ac += 2
        def level_up(self, levels):
                for l in levels:
                        self.level += 1
                        self.hd_cnt += 1
                        rolled_hp = roll_dice(self.hd, self.con_mod, 0)[0]
                        self.max_hp += rolled_hp
                        self.hp += rolled_hp
                        if self.level == 2:
                                if self.char_class == 1:
                                        self.specials["action surge"] = 1
                                if self.char_class == 2:
                                        self.specials["ki"] = self.level
                                if self.char_class == 3:
                                        self.specials["reckless attack"] = True
                                        self.dex_st_adv = True
                                if self.char_class == 4:
                                        self.bonus_actions[3] = "disengage"
                                if self.char_class == 5:
                                        self.specials["divine smite"] = [2, 0, 0, 0, 0]
                                        self.lay_on_hands_pool_max += 5
                                        self.lay_on_hands_pool += 5
                                        gen_fighting_style(inv)
                        if self.level == 3:
                                if self.char_class == 1:
                                        pass
                                if self.char_class == 2:
                                        self.specials["ki"] = self.level
                                        self.specials["deflect missiles"] = True
                                if self.char_class == 3:
                                        self.specials["rage"] = 3
                                if self.char_class == 4:
                                        self.specials["sneak attack"] = [6, math.ceil(self.level / 2)]
                                if self.char_class == 5:
                                        self.specials["divine smite"] = [3, 0, 0, 0, 0]
                                        self.lay_on_hands_pool_max += 5
                                        self.lay_on_hands_pool += 5
                        if self.level == 4:
                                self.asi_choice()
                                if self.char_class == 1:
                                        pass
                                if self.char_class == 2:
                                        self.specials["ki"] = self.level
                                if self.char_class == 3:
                                        pass
                                if self.char_class == 4:
                                        self.specials["sneak attack"] = [6, math.ceil(self.level / 2)]
                                if self.char_class == 5:
                                        self.lay_on_hands_pool_max += 5
                                        self.lay_on_hands_pool += 5
                        if self.level == 5:
                                self.prof_bonus_up()
                                if self.char_class != 4:
                                        self.attacks = 2
                                if self.char_class == 1:
                                        pass
                                if self.char_class == 2:
                                        self.specials["ki"] = self.level
                                        self.specials["stunning strike"] = True
                                        self.specials["uncanny dodge"] = True
                                if self.char_class == 3:
                                        pass
                                if self.char_class == 4:
                                        pass
                                if self.char_class == 5:
                                        self.specials["divine smite"] = [4, 2, 0, 0, 0]
                                        self.lay_on_hands_pool_max += 5
                                        self.lay_on_hands_pool += 5

class Fighter(Character):
        "Child for fighter class."
        def __init__(self, name, str, dex, con, wis, int, cha, starting_lvl):
                super().__init__(name, str, dex, con, wis, int, cha, starting_lvl)
                self.char_class = 1
                self.second_wind = True
                self.second_wind_cnt = 1

class Monk(Character):
        "Child for monk class."
        def __init__(self, name, str, dex, con, wis, int, cha, starting_lvl):
                super().__init__(name, str, dex, con, wis, int, cha, starting_lvl)
                self.char_class = 2

class Barbarian(Character):
        "Child for barbarian class."
        def __init__(self, name, str, dex, con, wis, int, cha, starting_lvl):
                super().__init__(name, str, dex, con, wis, int, cha, starting_lvl)
                self.char_class = 3

class Rogue(Character):
        "Child for rogue class."
        def __init__(self, name, str, dex, con, wis, int, cha, starting_lvl):
                super().__init__(name, str, dex, con, wis, int, cha, starting_lvl)
                self.char_class = 4

class Paladin(Character):
        "Child for paladin class."
        def __init__(self, name, str, dex, con, wis, int, cha, starting_lvl):
                super().__init__(name, str, dex, con, wis, int, cha, starting_lvl)
                self.char_class = 5
                self.lay_on_hands = True
                self.lay_on_hands_pool_max = 5
                self.lay_on_hands_pool = self.lay_on_hands_pool_max

class Inventory:
        "Inventory creation."
        def __init__(self, owner):
                self.owner = owner
                self.inv = {"nothing": 0}
        def add_item(self, item):
                self.inv[item] = 1
        def print_inv(self):
                print(vars(self))

class Dungeon:
        "Dungeon creation."
        def __init__(self, enc_cnt, pc_list):
                self.enc_cnt = enc_cnt
                self.pc_list = pc_list
                self.short_rest_cnt = 1
                self.long_rest_cnt = 2
        def get_respite_options(self):
                respite_options = {
                        1: "Short rest",
                        2: "Long rest"
                }
                if self.short_rest_cnt < 1:
                        respite_options.pop(1)
                if self.long_rest_cnt < 1:
                        respite_options.pop(2)
                print("- (0) => pass")
                for key, value in respite_options.items():
                        print("- (" + str(key) + ") => " + value)
                rest = int(input("Out of initiative order. What would you like to do?\n"))
                if rest == 1 and rest in respite_options:
                        self.short_rest()
                elif rest == 2 and rest in respite_options:
                        self.long_rest()
        def short_rest(self):
                for pc in self.pc_list:
                        if not pc.conditions["dead"] and pc.conditions["down"]:
                                wake_up = roll_dice(4, 0, 0)[0]
                                if wake_up == 1:
                                        pc.conditions["down"] = False
                        if pc.hp < pc.max_hp and not pc.conditions["dead"] and not pc.conditions["down"]:
                                while pc.hp < pc.hp_max and pc.hd_cnt != 0:
                                        pc.hp = min(pc.hp + roll_dice(pc.hd, pc.con_mod, 0), pc.max_hp)
                        if not pc.conditions["dead"] and not pc.conditions["down"] and pc.second_wind:
                                pc.second_wind_cnt = 1
                self.short_rest_cnt = 0
        def long_rest(self):
                for pc in self.pc_list:
                        if not pc.conditions["dead"]:
                                pc.hp = pc.max_hp
                                pc.hd_cnt = max(math.floor(pc.level / 2), 1)
                                pc.conditions["down"] = False
                        if not pc.conditions["dead"] and pc.second_wind:
                                pc.second_wind_cnt = 1
                self.long_rest_cnt -= 1
                self.short_rest_cnt = 1
        def end_dungeon(self):
                print("\n======")
                print("= GG =")
                print("======")
        def start_battle(self, enc, allies, enemies):
                print("\n|||||||||||")
                print("|Battle #" + str(enc + 1) + "|")
                print("|||||||||||\n")
                battle = Battle(allies, enemies)
                print("Roll initiative.")
                return battle

class Battle:
        "Battle creation."
        def __init__(self, allies, enemies):
                self.allies = allies
                self.enemies = enemies
                self.init_order = []
                self.participants = {}
                self.id_list = {}
                self.current_init = 0
                self.next_init = 1
                self.round = 0
                self.turn_end = False
                self.pcs_won = False
                self.pcs_fled = False
                self.foes_fled = False
        def initiative(self):
                for ally in self.allies:
                        if not ally.conditions["dead"] or not ally.conditions["down"]:
                                init_roll = roll_dice(20, ally.init_mod, 0)
                                self.init_order.append([init_roll[0], ally.init_mod, ally.name, ally])
                for enemy in self.enemies:
                        init_roll = roll_dice(20, enemy.init_mod, 0)
                        self.init_order.append([init_roll[0], enemy.init_mod, enemy.name, enemy])
                self.init_order.append([-100, 0 ,"Round End", ""])
                self.init_order.sort(reverse=True)
                self.build_participants()
                self.build_id_list()
                return self.init_order
        def build_participants(self):
                for a in self.allies:
                        if not a.conditions["dead"] or not a.conditions["down"]:
                                self.participants[a.name] = a
                for e in self.enemies:
                        self.participants[e.name] = e
        def build_id_list(self):
                for a in self.allies:
                        if not a.conditions["dead"] or not a.conditions["down"]:
                                self.id_list[a.player_id] = a
                for e in self.enemies:
                        self.id_list[e.player_id] = e
        def get_first_init(self):
                self.round += 1
                print("========")
                print("Round " + str(self.round))
                print("========")
                return self.init_order[0][3]
        def get_next_init(self):
                return self.init_order[self.next_init][3]
        def get_current_init(self):
                print( self.init_order[self.current_init][2] + "'s turn.")
                return self.init_order[self.current_init][3]
        def set_next_init(self):
                if self.init_order[self.current_init + 1][0] == -100:
                        self.current_init = 0
                        self.next_init = 1
                        self.round += 1
                        print("========")
                        print("Round " + str(self.round))
                        print("========")
                else:
                        self.current_init += 1
                print("--------")
        def get_targets(self, attacker):
                i = 1
                if attacker in self.allies:
                        enemies_list = {}
                        for e in self.enemies:
                                if not e.conditions["down"]:
                                        enemies_list[i] = e.name
                                i += 1
                        return enemies_list
                elif attacker in self.enemies:
                        allies_list = {}
                        for a in self.allies:
                                if not a.conditions["down"]:
                                        allies_list[i] = a.name
                                i += 1
                        return allies_list
        def get_target_by_name(self, name):
                return self.participants[name]
        def get_char_by_id(self, id):
                return self.id_list[id]
        def get_char_hp_by_name(self, name):
                char = self.participants[name]
                return char.hp, char.max_hp
        def get_hp_init_board(self):
                hp_init_board = []
                for i in range(len(self.participants)):
                        hp_init_board.append([self.init_order[i][0], self.init_order[i][2], self.get_char_hp_by_name(self.init_order[i][2])[0], self.get_char_hp_by_name(self.init_order[i][2])[1]])
                for j in range(len(hp_init_board)):
                        print(hp_init_board[j][1] + "'s HP: " + str(hp_init_board[j][2]) + "/" + str(hp_init_board[j][3]))
                print("--------\n")
        def check_turn_end(self):
                if self.init_order[self.current_init + 1][0] == -100:
                        self.turn_end = True
                if self.init_order[self.current_init - 1][0] == -100:
                        self.turn_end = False
        def end(self):
                print("Duel has ended. *jingle*")
                print("---------------")
                if self.pcs_fled:
                        print(self.allies[0].name + "'s team fled from combat.")
                if self.foes_fled:
                        print("Your foes have managed to run away.")
                else:
                        winner_team = []
                        loser_team = []
                        everyone = self.allies + self.enemies
                        for eo in everyone:
                                if eo.conditions["dead"] or eo.conditions["down"]:
                                        loser_team.append(eo)
                                        eo.death_st_success = 0
                                        eo.death_st_fail = 0
                                else:
                                        winner_team.append(eo)
                                        eo.death_st_success = 0
                                        eo.death_st_fail = 0
                        if winner_team[0] in self.allies:
                                self.pcs_won = True
                                loot = 0
                                for lt in loser_team:
                                        loot += lt.gold
                                xp = 0
                                print(winner_team[0].name + "'s team stands victorious: +" + str(loot) + " GP " + "+" + str(xp) + " XP gained.")
                return True
        def check_end(self):
                end = False
                allies_cnt = 0
                allies_down = 0
                allies_fled = 0
                enemies_down = 0
                enemies_cnt = 0
                enemies_fled = 0
                for a in self.allies:
                        allies_cnt += 1
                        if a.conditions["down"]:
                                allies_down += 1
                        if a.conditions["flee"] and not a.conditions in ["grappled", "prone"]:
                                allies_fled += 1
                for e in self.enemies:
                        enemies_cnt += 1
                        if e.conditions["down"]:
                                enemies_down += 1
                        if e.conditions["flee"] and not e.conditions in ["grappled", "prone"]:
                                enemies_fled += 1
                if allies_cnt == allies_down or enemies_cnt == enemies_down:
                        end = True
                else:
                        end = False
                if allies_cnt == allies_fled and allies_cnt != allies_down and self.turn_end:
                        end = True
                        self.pcs_fled = True
                if enemies_cnt == enemies_fled and enemies_cnt != enemies_down and self.turn_end:
                        end = True
                        self.foes_fled = True
                return end

class Shop:
        "Shop creation."
        def __init__(self):
                # name: [cost, dmg, dmg type, weight, light/heavy, finesse, hands, thrown]
                self.simple_melee_weapons = {
                        "club": [0.1, 4, "b", 2, 1, False, 1, False],
                        "dagger": [2, 4, "p", 1, 1, True, 1, True],
                        "greatclub": [0.2, 8, "b", 10, 0, 0, 2, False],
                        "handaxe": [5, 6, "s", 2, 1, 0, 1, True],
                        "javelin": [0.5, 6, "p", 2, 0, 0, 1, True],
                        "light hammer": [2, 4, "b", 4, 1, 0, 1, False],
                        "mace": [5, 6, "b", 4, 0, 0, 1, False],
                        "quarterstaff": [0.2, 6, "b", 4, 0, 0, 1.5, False],
                        "sickle": [1, 4, "s", 2, 1, 0, 1, False],
                        "spear": [1, 6, "p", 3, 0, 0, 1.5, True]
                        }
                # name: [cost, dmg, dmg type, weight, finesse, hands, load]
                self.simple_ranged_weapons = {
                        "light crossbow": [25, 8, "p", 5, False, 2, True],
                        "dart": [0.05, 4, "p", 0.25, True, 1, False],
                        "shortbow": [25, 6, "p", 2, False, 2, False],
                        "sling": [0.1, 4, "b", 0, False, 1, False]
                        }

def gen_stats():
        stre = 0
        dex = 0
        con = 0
        wis = 0
        inte = 0
        cha = 0
        roll = 0
        min = 6
        for i in range(4):
                roll = roll_dice(6, 0, 0)[0]
                if roll < min:
                        min = roll
                stre += roll
        stre -= min
        min = 6
        for i in range(4):
                roll = roll_dice(6, 0, 0)[0]
                if roll < min:
                        min = roll
                dex += roll
        dex -= min
        min = 6
        for i in range(4):
                roll = roll_dice(6, 0, 0)[0]
                if roll < min:
                        min = roll
                con += roll
        con -= min
        min = 6
        for i in range(4):
                roll = roll_dice(6, 0, 0)[0]
                if roll < min:
                        min = roll
                wis += roll
        wis -= min
        min = 6
        for i in range(4):
                roll = roll_dice(6, 0, 0)[0]
                if roll < min:
                        min = roll
                inte += roll
        inte -= min
        min = 6
        for i in range(4):
                roll = roll_dice(6, 0, 0)[0]
                if roll < min:
                        min = roll
                cha += roll
        cha -= min
        print("============")
        print("Rolled stats\n" + "Strength: " + str(stre) + "\n" + "Dexterity: " + str(dex) + "\n" + "Constitution: " + str(con) + "\n" + "Wisdom: " + str(wis) + "\n" + "Intelligence: " + str(inte) + "\n" + "Charisma: " + str(cha) + "\n")
        return stre, dex, con, wis, inte, cha

def roll_dice(dice, mod, type):
        if type == -1:
                roll = min(random.randint(1, dice), random.randint(1, dice))
        elif type == 1:
                roll = max(random.randint(1, dice), random.randint(1, dice))
        else:
                roll = random.randint(1, dice)
        if roll == 1:
                crit = -1
        elif roll == 20:
                crit = 1
        else:
                crit = 0
        return roll + mod, crit

def random_str(length):
        chars = string.ascii_lowercase
        return "".join(random.choice(chars) for i in range(length))

def get_adv_disadv(source, target):
        roll_mod = 0
        if target.conditions["prone"] and not source.ranged:
                roll_mod += 1
        if target.conditions["prone"] and source.ranged:
                roll_mod -= 1
        elif target.conditions["dodge"]:
                roll_mod -= 1
        if roll_mod < -1:
                roll_mod = -1
        elif roll_mod > 1:
                roll_mod = 1
        if roll_mod == 1:
                print("Rolling with advantage.")
        elif roll_mod == -1:
                print("Rolling with disadvantage.")
        elif roll_mod == 0:
                print("Straight roll.")
        return roll_mod

def turn(attacker, battle):
        if not attacker.conditions["down"]:
                attacker.reset_until_next_turn_conditions()
                print("Action. Make your choice:")
                print("- (0) => pass")
                for key, value in attacker.actions.items():
                        print("- (" + str(key) + ") => " + value)
                action = int(input())
                roll_mod = 0
                if action in attacker.actions and action == 1:
                        targets = battle.get_targets(attacker)
                        if len(targets) != 0:
                                defender = target_selector(attacker, battle, targets)
                                roll_mod = get_adv_disadv(attacker, defender)
                                for i in range(attacker.attacks):
                                        attack(attacker, defender, 1, roll_mod, battle)
                        else:
                                print("Noone to attack.")
                elif action in attacker.actions and action == 2:
                        attacker.conditions["dodge"] = True
                        print(attacker.name + " is taking a defensive stance.")
                        if attacker.fighting_style == 4 or attacker.char_class == 2:
                                attacker.bonus_actions.pop(1)
                elif action in attacker.actions and action == 3:
                        attacker.conditions["flee"] = True
                        print(attacker.name + " has disengaged and is about to flee from combat.")
                        if attacker.fighting_style == 4 or attacker.char_class == 2:
                                attacker.bonus_actions.pop(1)
                elif action in attacker.actions and action == 4:
                        targets = battle.get_targets(attacker)
                        if len(targets) != 0:
                                defender = target_selector(attacker, battle, targets)
                                for i in range(attacker.attacks):
                                        shove(attacker, defender)
                                if attacker.fighting_style == 4 or attacker.char_class == 2:
                                        attacker.bonus_actions.pop(1)
                        else:
                                print("Noone to shove.")
                elif action in attacker.actions and action == 5:
                        targets = battle.get_targets(attacker)
                        if len(targets) != 0:
                                defender = target_selector(attacker, battle, targets)
                                roll_mod = get_adv_disadv(attacker, defender)
                                for i in range(attacker.attacks):
                                        grapple(attacker, defender, roll_mod)
                                if attacker.fighting_style == 4 or attacker.char_class == 2:
                                        attacker.bonus_actions.pop(1)
                        else:
                                print("Noone to grapple.")
                elif action in attacker.actions and action == 6:
                        escape_grapple(attacker, battle)
                        if attacker.fighting_style == 4 or attacker.char_class == 2:
                                attacker.bonus_actions.pop(1)
                elif action in attacker.actions and action == 7:
                        current_hp = attacker.hp
                        lay_on_hands_heal = attacker.lay_on_hands_pool
                        attacker.hp = min(attacker.hp + lay_on_hands_heal, attacker.max_hp)
                        if current_hp + lay_on_hands_heal > attacker.max_hp:
                                actual_heal = lay_on_hands_heal - ((current_hp + lay_on_hands_heal) - attacker.max_hp)
                        else:
                                actual_heal = lay_on_hands_heal
                        print(attacker.name + " healed " + str(actual_heal) + " HP.")
                        attacker.lay_on_hand_pool = min(0, attacker.lay_on_hands_pool - actual_heal) 
                        if attacker.lay_on_hand_pool == 0:
                                attacker.actions.pop(action)
                if len(attacker.bonus_actions) != 0:
                        print("Bonus action. Make your choice:")
                        print("- (0) => pass")
                        for key, value in attacker.bonus_actions.items():
                                print("- (" + str(key) + ") => " + value)
                        bonus_action = int(input())
                        if bonus_action in attacker.bonus_actions and bonus_action == 1 and attacker.bonus_attack:
                                targets = battle.get_targets(attacker)
                                if len(targets) != 0:
                                        defender = target_selector(attacker, battle, targets)
                                        roll_mod = get_adv_disadv(attacker, defender)
                                        attack(attacker, defender, 2, roll_mod, battle)
                                else:
                                        print("Noone to attack.")
                        elif bonus_action in attacker.bonus_actions and (bonus_action == 1 or bonus_action == 2):
                                current_hp = attacker.hp
                                second_wind_heal = roll_dice(10, attacker.level, 0)[0]
                                attacker.hp = min(attacker.hp + second_wind_heal, attacker.max_hp)
                                if current_hp + second_wind_heal > attacker.max_hp:
                                        actual_heal = second_wind_heal - ((current_hp + second_wind_heal) - attacker.max_hp)
                                else:
                                        actual_heal = second_wind_heal
                                print(attacker.name + " healed " + str(actual_heal) + " HP.")
                                attacker.second_wind = False
                                attacker.bonus_actions.pop(bonus_action)
                        elif bonus_action in attacker.bonus_actions and bonus_action == 3:
                                attacker.conditions["flee"] = True
                                print(attacker.name + " has disengaged and is about to flee from combat.")
        elif attacker.conditions["down"] and not attacker.conditions["dead"] and attacker.death_st_success < 3:
                attacker.deaths_door()
        elif attacker.conditions["down"] and attacker.conditions["dead"]:
                print(attacker.name + " is dead.")
        elif attacker.conditions["down"] and not attacker.conditions["dead"] and attacker.death_st_success == 3:
                print(attacker.name + " is taking a rest.")

def target_selector(source, battle, targets):
        print("Choose target: ")
        for key, value in targets.items():
                print("- (" + str(key) + ") => " + value)
        target_choice = int(input())
        print("")
        return battle.get_target_by_name(targets[target_choice])

def attack(source, target, type, adv_disadv, battle):
        if type == 1:
                print(source.name + " attacks " + target.name + " with " + source.eq_weapon_main + ".")
        elif type == 2:
                print(source.name + " attacks " + target.name + " with " + source.eq_weapon_offhand + ".")
        if source.ranged:
                att_mod = source.ranged_att_mod
                dmg_mod = source.ranged_dmg_mod
        elif source.fighting_style == 4 or source.char_class == 2:
                att_mod = max(source.ranged_att_mod, source.melee_att_mod)
                dmg_mod = max(source.ranged_dmg_mod, source.melee_dmg_mod)
        else:
                att_mod = source.melee_att_mod
                dmg_mod = source.melee_dmg_mod
        if type == 2 and source.fighting_style != 4 and source.char_class != 6:
                dmg_mod = min(0, max(source.ranged_dmg_mod, source.melee_dmg_mod))
        to_hit = roll_dice(20, att_mod, adv_disadv)
        crit = to_hit[1]
        if crit == 1:
                to_hit_conf = roll_dice(20, att_mod, adv_disadv)
                to_hit_conf_flag = False
                if to_hit_conf[0] < target.ac and to_hit_conf[1] != 1:
                        crit = 0
                else:
                        to_hit_conf_flag = True
        dmg = 0
        if to_hit[0] >= target.ac or crit == 1:
                dmg = calc_dmg(source, crit, dmg_mod, type)
                if crit == 0:
                        print("Hit: " + str(to_hit[0]) + " vs AC " + str(target.ac) + " \nDamage: " + str(dmg) + "\n")
                elif crit == 1:
                        print("Critical hit: " + str(to_hit[0]) + " vs AC " + str(target.ac))
                        print("Critical hit confirmation: " + str(to_hit_conf[0]) + " vs AC " + str(target.ac))
                        if not to_hit_conf_flag:
                                print("Damage: " + str(dmg) + "\n")
                        else:
                                print("2x dice damage: " + str(dmg) + "\n")
        elif to_hit[0] < target.ac or crit == -1:
                if crit == 0:
                        print("Miss: " + str(to_hit[0]) + " vs AC " + str(target.ac) + "\n")
                elif crit == -1:
                        print("Critical miss\n")
        target.hp -= dmg
        if target.hp <= 0:
                target.conditions["down"] = True
                print(target.name + " is down.")
                if target.grappling != "":
                        release_grapple(target, battle)
                if target.max_hp * -1 >= target.hp:
                        print("Death blow! " + target.name + " falls dead. RIP")
                        target.conditions["dead"] = True

def shove(source, target):
        att_check = roll_dice(20, source.athl, 0)[0]
        def_check = roll_dice(20, max(target.athl, target.acro), 0)[0]
        print("Contested check: " + str(att_check) + " vs " + str(def_check))
        if att_check > def_check:
                target.conditions["prone"] = True
                if target.char_class in [1, 4, 5] or (target.char_class == 2 and target.level < 2) or (target.char_class == 3 and target.level < 5):
                        target.actions.pop(3)
                print(target.name + " was knocked prone.")
        else:
                print("Shove attempt failed.")

def grapple(source, target, adv_disadv):
        att_mod = max(source.ranged_att_mod, source.melee_att_mod)
        to_hit = roll_dice(20, att_mod, adv_disadv)
        print("Hit: " + str(to_hit[0]) + " vs AC " + str(target.ac) + "\n")
        if to_hit[0] > target.ac:
                target.conditions["grappled"] = True
                target.grappled_by = source.player_id
                source.grappling = target.player_id
                target.actions.pop(3)
                target.actions[6] = "escape grapple"
                print(target.name + " is grappled by " + source.name + ".")
                if source.fighting_style in [2, 5]:
                        source.actions.pop(1)
        else:
                print(source.name + " failed to grapple " + target.name + ".")

def release_grapple(grappler, battle):
        grapplee = battle.get_char_by_id(grappler.grappling)
        grapplee.grappled_by = ""
        grapplee.conditions["grappled"] = False
        grappler.grappling = ""
        grapplee.actions[3] = "disengage"
        grapplee.actions.pop(6)
        if grappler.fighting_style in [2, 5]:
                grappler.actions[1] = "attack"

def escape_grapple(grapplee, battle):
        grappler = battle.get_char_by_id(grapplee.grappled_by)
        att_check = roll_dice(20, max(grapplee.athl, grapplee.acro), 0)[0]
        def_check = roll_dice(20, grappler.athl, 0)[0]
        print("Contested check: " + str(att_check) + " vs " + str(def_check))
        if att_check > def_check:
                grapplee.grappled_by = ""
                grapplee.conditions["grappled"] = False
                grappler.grappling = ""
                grapplee.actions[3] = "disengage"
                grapplee.actions.pop(6)
                if grappler.fighting_style in [2, 5]:
                        grappler.actions[1] = "attack"
                print(grapplee.name + " has escaped the grapple.")
        else:
                print("Grapple escape attempt failed.")

def calc_dmg(source, crit, dmg_mod, type):
        dmg = 0
        die_cnt = 1
        dmg_die = 1
        if type == 1:
                die_cnt = source.dmg_die_cnt
                dmg_die = source.dmg_die
        if type == 2:
                die_cnt = source.dmg_die_cnt_offhand
                dmg_die = source.dmg_die_offhand
        if type == 3:
                die_cnt = source.dmg_die_cnt
                dmg_die = source.dmg_die
        if crit == 1:
                die_cnt *= 2
        else:
                die_cnt *= 1
        for i in range(die_cnt):
                dmg_roll = roll_dice(dmg_die, 0, 0)[0]
                dmg_reroll = 0
                if (dmg_roll == 1 or dmg_roll == 2) and source.reroll_dmg:
                        dmg_reroll = roll_dice(dmg_die, 0, 0)[0]
                dmg += max(dmg_roll, dmg_reroll)
        dmg += dmg_mod
        return dmg

def gen_char(name, starting_level):
        stats = gen_stats()
        classes = {
                1: "fighter",
                2: "monk",
                3: "barbarian",
                4: "rogue",
                5: "paladin"
                }
        print(classes)
        class_choice = int(input("choose your class: "))
        if class_choice == 1:
                char = Fighter(name, stats[0], stats[1], stats[2], stats[3], stats[4], stats[5], starting_level)
        if class_choice == 2:
                char = Monk(name, stats[0], stats[1], stats[2], stats[3], stats[4], stats[5], starting_level)
        if class_choice == 3:
                char = Barbarian(name, stats[0], stats[1], stats[2], stats[3], stats[4], stats[5], starting_level)
        if class_choice == 4:
                char = Rogue(name, stats[0], stats[1], stats[2], stats[3], stats[4], stats[5], starting_level)
        if class_choice == 5:
                char = Paladin(name, stats[0], stats[1], stats[2], stats[3], stats[4], stats[5], starting_level)
        inv = Inventory(char.player_id)
        char.gen_starting_gold(char.char_class)
        char.gen_class(inv, char.char_class)
        char.action_economy()
        return char

def init_chars():
        starting_level = 1
        name = input("Name your hero: ")
        if name == "":
                name = "Rick"
        print(name)
        p1_char = gen_char(name, starting_level)
        print("")
        
        name = "Elisa"
        print(name)
        p2_char = gen_char(name, starting_level)
        print("")
        
        name = "Bandit"
        print(name)
        p3_char = gen_char(name, starting_level)
        print("")
        
        name = "Rogue"
        print(name)
        p4_char = gen_char(name, starting_level)
        
        allies = [p1_char, p2_char]
        enemies = [p3_char, p4_char]
        return allies, enemies

def main():
        print("====================================")
        print("= Shining in the Dungeon (5e Duel) =")
        print("====================================\n")
        chars = init_chars()
        allies = chars[0]
        enemies = chars[1]
        encounters = 10
        dungeon = Dungeon(encounters, allies)
        for enc in range(dungeon.enc_cnt):
                battle = dungeon.start_battle(enc, allies, enemies)
                for i in battle.initiative():
                        if i[0] != -100:
                                print(i[2] + ": " + str(i[0]))
                print("")
                attacker = battle.get_first_init()
                battle_end = False
                while not battle_end:
                        battle.get_hp_init_board()
                        attacker = battle.get_current_init()
                        turn(attacker, battle)
                        if battle.check_end():
                                battle.get_hp_init_board()
                                battle_end = battle.end()
                        else:
                                battle.set_next_init()
                                battle.check_turn_end()
                if battle.pcs_won or battle.pcs_fled or battle.foes_fled:
                        dungeon.get_respite_options()
                else:
                        break
        dungeon.end_dungeon()

main()

#TODO: after every 2nd battle pcs level up
#TODO: implement specials (rage, action surge, sneak attack, deflect missiles, ki, stunning strike, divine smite, lay on hands on others)
#TODO: tkinter (action-bonus action-special-skip menu)
#TODO: 1 merchant before level 5
#TODO: use equipped weapons, shield and armor instead of fighting style
#TODO: eqiupment chooser and equipper routines
