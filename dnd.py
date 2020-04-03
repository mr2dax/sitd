# Imports
import random
import math
import string
import tkinter as tk
import gui
import time

# Classes
'''
General character prototype, don't use
IN
- name (string)
- strength (int)
- dexterity (int)
- constitution (int)
- wisdom (int)
- intelligence (int)
- charisma (int)
- starting level (int)
- race (int)
- subrace (int)
- npc (bool)
- ui (object)
OUT
- character (object)
'''
class Character:
        "Character creation."
        def __init__(self, name, str, dex, con, int, wis, cha, starting_lvl, race, subrace, npc, ui):
                self.str = str
                self.dex = dex
                self.con = con
                self.wis = wis
                self.int = int
                self.cha = cha
                self.starting_lvl = starting_lvl
                self.player_id = random_str(10)
                self.inv = Inventory(self.player_id, ui)
                self.level = 1
                self.npc = npc
                self.race = race
                self.subrace = subrace
                self.char_class = 0
                self.hd_max = 1
                self.hd_cnt = 1
                self.hd = 0
                self.xp = 0
                self.gold = 0
                self.prof_bonus = 2
                self.attacks = 1
                self.attack_adv = False
                self.help_adv = False
                self.attack_disadv = False
                self.bonus_attack = False
                self.str_mod = math.floor((self.str - 10) / 2)
                self.dex_mod = math.floor((self.dex - 10) / 2)
                self.con_mod = math.floor((self.con - 10) / 2)
                self.wis_mod = math.floor((self.wis - 10) / 2)
                self.int_mod = math.floor((self.int - 10) / 2)
                self.cha_mod = math.floor((self.cha - 10) / 2)
                self.main_hand_prof = False
                self.main_str_att_mod = self.str_mod
                self.main_dex_att_mod = self.dex_mod
                self.main_str_dmg_mod = self.str_mod
                self.main_dex_dmg_mod = self.dex_mod
                self.off_hand_prof = False
                self.off_str_att_mod = self.str_mod
                self.off_dex_att_mod = self.dex_mod
                self.off_str_dmg_mod = self.str_mod
                self.off_dex_dmg_mod = self.dex_mod
                self.dmg_die_main = 1
                self.dmg_die_cnt_main = 1
                self.dmg_die_type_main = "b"
                self.ench_main = 0
                self.dmg_die_off = 1
                self.dmg_die_cnt_off = 1
                self.dmg_die_type_off = "b"
                self.ench_off = 0
                self.ac = 10 + self.dex_mod
                self.init_mod = self.dex_mod
                self.max_hp = 0
                self.hp = 0
                self.temp_hp = 0
                # save: [mod, bonus, adv, disadv]
                self.saving_throws = {
                        "str": [self.str_mod, 0, False, False],
                        "dex": [self.dex_mod, 0, False, False],
                        "con": [self.con_mod, 0, False, False],
                        "wis": [self.wis_mod, 0, False, False],
                        "int": [self.int_mod, 0, False, False],
                        "cha": [self.cha_mod, 0, False, False]
                        }
                self.death_st = 0
                self.death_st_success = 0
                self.death_st_fail = 0
                self.max_carry = self.str * 15
                self.carry = 0
                # skill: [mod, bonus, adv, disadv]
                self.skills = {
                        "athletics": [self.str_mod, 0, False, False],
                        "acrobatics": [self.dex_mod, 0, False, False],
                        "perception": [self.wis_mod, 0, False, False],
                        "investigation": [self.int_mod, 0, False, False],
                        "stealth": [self.dex_mod, 0, False, False],
                        "persuasion": [self.cha_mod, 0, False, False]
                }
                self.reroll_dmg = False
                self.offhand_dmg_mod = False
                self.eq_weapon_main = "unarmed strike"
                self.eq_weapon_main_finesse = False
                self.eq_weapon_offhand = "nothing"
                self.eq_weapon_offhand_finesse = False
                self.eq_armor = "unarmored"
                self.ranged = False
                self.fighting_style = 0
                if name == "":
                        self.name = "Rick"
                else:
                    self.name = name
                self.battle_menu_options = {
                        1: ["action", 1],
                        2: ["bonus action", 1],
                        3: ["special", 1],
                        4: ["done", 1]
                        }
                self.actions = {}
                self.bonus_actions = {}
                self.specials = {}
                self.reaction_cnt = 1
                self.reactions = {}
                self.turn_done = False
                self.conditions = {
                        "flee": False,
                        "down": False,
                        "dead": False,
                        "dodge": False,
                        "prone": False,
                        "grappled": False,
                        "helped": False,
                        "blinded": False,
                        "deafened": False,
                        "charmed": False,
                        "exhaustion": False,
                        "frightened": False
                        }
                self.grappled_by = ""
                self.grappling = ""
                self.helpee = ""
                if self.starting_lvl > 2:
                        self.level_up(self.starting_lvl - 1, ui)
        def battle_menu(self, ui):
                if self.conditions["down"] or self.conditions["dead"]:
                        act_choice = 4
                else:
                        if not self.npc:
                                act_choice = ui.get_battle_menu_choice_input(self.battle_menu_options)
                        else:
                                act_choice = ai.choose(self, self.battle_menu_options.keys(), 1)
                return act_choice
        # build the character's actions, bonus actions & specials
        def action_economy(self):
                # actions (main)
                # regardless of class, any character can perform the below actions
                self.actions = {
                        0: "back", # back to main (battle) menu
                        1: "attack", # weapon attack
                        2: "dodge", # defend (adv on DEX STs, disadv on incoming attacks)
                        3: "disengage", # spend action to flee from battle without opportunity attacks from enemies
                        8: "help", # assist a teammate in his/her next action (ability check or attack)
                        9: "use potion" # chug a potion or force-feed it to a downed ally, if character has a potion
                        }
                # only characters with ample STR can attempt to shove (variant rule)
                if self.str >= 13:
                        self.actions[4] = "shove"
                # only characters with ample STR and a free hand can attempt to grapple (variant rule)
                if self.str >= 13 and (self.eq_weapon_main == "unarmed strike" or self.eq_weapon_offhand in ["unarmed strike", "nothing"] or self.eq_weapon_main == self.eq_weapon_offhand):
                        self.actions[5] = "grapple"
                # paladin only touch heal
                if self.char_class == 5:
                        self.actions[7] = "lay on hands"
                # bonus actions (swift actions)
                self.bonus_actions = {
                        0: "back" # back to main (battle) menu 
                        }
                # only characters with eligible weapon setup can perform a weapon attack as a bonus action (2 light weapons equipped) or properly outfitted monks
                if self.bonus_attack:
                        self.bonus_actions[1] = "attack"
                # fighter only self heal
                if self.char_class == 1:
                        self.bonus_actions[2] = "second wind"
                # barbarian only self buff
                if self.char_class == 3:
                        self.bonus_actions[3] = "rage"
                # rogue only (as part of cunning action ability from 2nd level)
                if self.char_class == 4:
                        self.bonus_actions[4] = "disengage"
                # specials (no action required)
                self.specials = {
                        0: "back" # back to main (battle) menu 
                        }
        def deaths_door(self, ui):
                death_st = roll_dice(20, 0, 0, ui)
                if death_st[1] == 1:
                        self.conditions["down"] = False
                        self.hp = 1
                        self.death_st_success = 0
                        self.death_st_fail = 0
                        ui.push_prompt(self.name + " is back up!")
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
                ui.push_prompt(self.name + " - Death Saving Throw: " + str(death_st[0]) + " (S:" + str(self.death_st_success) + ",F:" + str(self.death_st_fail) + ")")
                if self.death_st_fail > 2:
                        self.conditions["dead"] = True
                        self.death_st_success = 0
                        self.death_st_fail = 0
                        ui.push_prompt(self.name + " just died. RIP")
                if self.death_st_success > 2:
                        self.hp = 0
                        self.death_st_success = 0
                        self.death_st_fail = 0
                        ui.push_prompt(self.name + " has stabilized.")
        def receive_healing(self, healer, heal_amount, ui):
                current_hp = self.hp
                if self.hp < 0:
                        self.hp = 0
                        self.conditions["down"] = False
                        self.death_st_success = 0
                        self.death_st_fail = 0
                        ui.push_prompt(self.name + " is back up!")
                self.hp = min(self.hp + heal_amount, self.max_hp)
                if current_hp + heal_amount > self.max_hp:
                        actual_heal = heal_amount - ((current_hp + heal_amount) - self.max_hp)
                else:
                        actual_heal = heal_amount
                ui.update_status()
                if healer.name == self.name:
                        ui.push_prompt("%s healed self for %s HP." % (healer.name, actual_heal))
                else:
                        ui.push_prompt("%s healed %s for %s HP." % (healer.name, self.name, actual_heal))
                return actual_heal
        # return formatted character stats
        def print_char_status(self):
                abilities = "Abilities\nStrengh\nDexterity\nConstitution\nIntelligence\nWisdom\nCharisma"
                score_tup = (self.str, self.dex, self.con, self.int, self.wis, self.cha)
                scores = "Scores\n%s\n%s\n%s\n%s\n%s\n%s" % score_tup
                mod_tup = ("{0:+}".format(self.str_mod), "{0:+}".format(self.dex_mod), "{0:+}".format(self.con_mod),
                        "{0:+}".format(self.int_mod), "{0:+}".format(self.wis_mod), "{0:+}".format(self.cha_mod))
                mods = "Modifiers\n%s\n%s\n%s\n%s\n%s\n%s" % mod_tup
                sts_tup = ("{0:+}".format(self.saving_throws["str"][0] + self.saving_throws["str"][1]) + " (%s,%s)" % (self.saving_throws["str"][2], self.saving_throws["str"][3]),
                        "{0:+}".format(self.saving_throws["dex"][0] + self.saving_throws["dex"][1]) + " (%s,%s)" % (self.saving_throws["dex"][2], self.saving_throws["dex"][3]),
                        "{0:+}".format(self.saving_throws["con"][0] + self.saving_throws["con"][1]) + " (%s,%s)" % (self.saving_throws["con"][2], self.saving_throws["con"][3]),
                        "{0:+}".format(self.saving_throws["int"][0] + self.saving_throws["int"][1]) + " (%s,%s)" % (self.saving_throws["int"][2], self.saving_throws["int"][3]),
                        "{0:+}".format(self.saving_throws["wis"][0] + self.saving_throws["wis"][1]) + " (%s,%s)" % (self.saving_throws["wis"][2], self.saving_throws["wis"][3]),
                        "{0:+}".format(self.saving_throws["cha"][0] + self.saving_throws["cha"][1]) + " (%s,%s)" % (self.saving_throws["cha"][2], self.saving_throws["cha"][3]))
                sts = "Saving Throws (adv,disadv)\n%s\n%s\n%s\n%s\n%s\n%s" % sts_tup
                skill_names = [key for key, value in self.skills.items()]
                skills_tup = (skill_names[0].capitalize() + ": {0:+}".format(self.skills["athletics"][0] + self.skills["athletics"][1]) + " (%s,%s)" % (self.skills["athletics"][2], self.skills["athletics"][3]),
                        skill_names[1].capitalize() + ": {0:+}".format(self.skills["acrobatics"][0] + self.skills["acrobatics"][1]) + " (%s,%s)" % (self.skills["acrobatics"][2], self.skills["acrobatics"][3]),
                        skill_names[4].capitalize() + ": {0:+}".format(self.skills["stealth"][0] + self.skills["stealth"][1]) + " (%s,%s)" % (self.skills["stealth"][2], self.skills["stealth"][3]), 
                        skill_names[3].capitalize() + ": {0:+}".format(self.skills["investigation"][0] + self.skills["investigation"][1]) + " (%s,%s)" % (self.skills["investigation"][2], self.skills["investigation"][3]),
                        skill_names[2].capitalize() + ": {0:+}".format(self.skills["perception"][0] + self.skills["perception"][1]) + " (%s,%s)" % (self.skills["perception"][2], self.skills["perception"][3]),
                        skill_names[5].capitalize() + ": {0:+}".format(self.skills["persuasion"][0] + self.skills["persuasion"][1]) + " (%s,%s)" % (self.skills["persuasion"][2], self.skills["persuasion"][3]))
                skills = "Skills (adv,disadv)\n%s\n%s\n%s\n%s\n%s\n%s" % skills_tup
                cond_list = [" " +  key for key, value in self.conditions.items() if value]
                conditions = "Conditions:"
                for cond in cond_list:
                        conditions += cond
                if self.char_class == 3:
                        if self.raging:
                                conditions += " raging"
                if self.grappled_by != "":
                        conditions += "\nGrappled by: " + battle.get_char_by_id(self.grappled_by).name
                if self.grappling != "":
                        conditions += "\nGrappling: " + battle.get_char_by_id(self.grappling).name
                if self.helpee != "":
                        conditions += "\nHelping: " + battle.get_char_by_id(self.helpee).name
                combat = "Hit Points: " + str(self.hp) + "/" + str(self.max_hp) + " (Temp HP: " + str(self.temp_hp) + ")\n"
                combat += "Hit Dice: " + str(self.hd_cnt) + "/" + str(self.hd_max) + " (d" + str(self.hd) + ")\n"
                combat += "Armor Class: " + str(self.ac) + ", Initiative: " + str(self.init_mod) + "\n"
                combat += "Attacks: x" + str(self.attacks) + ", Bonus attack: "
                if self.bonus_attack:
                        combat += "Yes"
                else:
                        combat += "No"
                combat += "\nAdvantage: "
                if self.attack_adv:
                        combat += "Yes"
                else:
                        combat += "No"
                combat += ", Disadvantage: "
                if self.attack_disadv:
                        combat += "Yes"
                else:
                        combat += "No"
                combat += "\nMain Hand:\n"
                if self.ranged:
                        combat += "To hit: " + "{0:+}".format(self.main_dex_att_mod + self.ench_main) + ", Damage: " + str(self.dmg_die_cnt_main) + "d" + str(self.dmg_die_main) + "{0:+}".format(self.main_dex_dmg_mod + self.ench_main)
                elif self.eq_weapon_main_finesse:
                        combat += "To hit: " + "{0:+}".format(max(self.main_dex_att_mod, self.main_str_att_mod) + self.ench_main) + ", Damage: " + str(self.dmg_die_cnt_main) + "d" + str(self.dmg_die_main) + "{0:+}".format(max(self.main_dex_dmg_mod, self.main_str_dmg_mod) + self.ench_main)
                else:
                        combat += "To hit: " + "{0:+}".format(self.main_str_att_mod + self.ench_main) + ", Damage: " + str(self.dmg_die_cnt_main) + "d" + str(self.dmg_die_main) + "{0:+}".format(self.main_str_dmg_mod + self.ench_main)
                if self.dmg_die_type_main == "b":
                        combat += " (bludgeoning)"
                elif self.dmg_die_type_main == "s":
                        combat += " (slashing)"
                elif self.dmg_die_type_main == "p":
                        combat += " (piercing)"
                combat += "\nOff Hand:\n"
                if not self.bonus_attack:
                        combat += "-"
                else:
                        if self.eq_weapon_offhand_finesse:
                                combat += "To hit: " + "{0:+}".format(max(self.off_dex_att_mod, self.off_str_att_mod) + self.ench_off) + ", Damage: " + str(self.dmg_die_cnt_off) + "d" + str(self.dmg_die_off) + "{0:+}".format(max(self.off_dex_dmg_mod, self.off_str_dmg_mod) + self.ench_off)
                        else:
                                combat += "To hit: " + "{0:+}".format(self.off_str_att_mod + self.ench_off) + ", Damage: " + str(self.dmg_die_cnt_off) + "d" + str(self.dmg_die_off) + "{0:+}".format(self.off_str_dmg_mod + self.ench_off)
                        if self.dmg_die_type_off == "b":
                                combat += " (bludgeoning)"
                        elif self.dmg_die_type_off == "s":
                                combat += " (slashing)"
                        elif self.dmg_die_type_off == "p":
                                combat += " (piercing)"
                equipped = "Equipped\nMain Hand: " + self.eq_weapon_main + "\nOff Hand: " + self.eq_weapon_offhand + "\nArmor: " + self.eq_armor
                inventory = "Inventory\n"
                inventory += "Gold: " + str(self.gold) + " GP\nCarry weight: " + str(self.carry) + "/" + str(self.max_carry) + " lbs.\n"
                for key, value in self.inv.inv.items():
                        inventory += key + " (" + str(value[1]) + ")\n"
                specials = "Specials\n"
                if self.char_class == 1 or (self.char_class in [5, 6] and self.level > 1):
                        specials += "Fighting Style: " + self.get_fighting_style() + "\n"
                if self.char_class == 1:
                        specials += "Second Wind: " + str(self.second_wind_cnt) + " (1d10+" + str(self.level) + ")\n"
                elif self.char_class == 3:
                        specials += "Rages: " + str(self.rage_cnt) + "\n"
                elif self.char_class == 4:
                        specials += "Sneak Attack: " + str(self.sneak_damage[1]) + "d" + str(self.sneak_damage[0]) + "\n"
                elif self.char_class == 5:
                        specials += "Lay on Hands: " + str(self.lay_on_hands_pool) + "/" + str(self.lay_on_hands_pool_max) + "\n"
                death_saves = "Death Saves\nFails: " + str(self.death_st_fail) + "\nSuccesses: " + str(self.death_st_success)
                return abilities, scores, mods, sts, conditions, combat, equipped, inventory, specials, death_saves, skills
        # reset conditions that would have ended since last turn (until the start of its next turn effects)
        def reset_until_start_of_next_turn(self, ui):
                if self.conditions["prone"] and not self.conditions["grappled"]:
                        self.conditions["prone"] = False
                        ui.push_prompt(self.name + " stood up.")
                        if 3 not in self.actions:
                                self.actions[3] = "disengage"
                if self.conditions["dodge"]:
                        self.conditions["dodge"] = False
                        ui.push_prompt("Dodge ended.")
                if self.conditions["flee"]:
                        self.conditions["flee"] = False
                        ui.push_prompt(self.name + " couldn't run away.")
                if self.helpee != "":
                        stop_help(self.helpee)
                        self.helpee = ""
                if self.bonus_attack and 1 not in self.bonus_actions:
                        self.bonus_actions[1] = "attack"
                self.battle_menu_options = {
                        1: ["action", 1],
                        2: ["bonus action", 1],
                        3: ["special", 1],
                        4: ["done", 1]
                        }
                self.reaction_cnt = 1
                if self.char_class == 3:
                        self.got_attacked = False
                        self.did_attack = False
                if self.char_class == 4:
                        self.sneak_attack = True
        def reset_until_end_of_current_turn(self, all_items, ui):
                if self.char_class == 3:
                        if self.raging and (not self.got_attacked and not self.did_attack):
                                self.rage_off(all_items, ui)
        def gen_starting_gold(self, char_class, ui):
                gold_die = {
                        1: 5,
                        2: 5,
                        3: 2,
                        4: 4,
                        5: 5,
                        6: 5
                        }
                for _ in range(gold_die[char_class]):
                        self.gold += roll_dice(4, 0, 0, ui)[0]
                if char_class != 2:
                        self.gold *= 10
                ui.update_status()
        def gen_starting_equipment(self, all_items, ui):
                starting_shop = Shop(all_items, ui)
                starting_shop.shopping_flow(self, ui)
        def gen_class(self, class_choice, ui):
                if class_choice == 1:
                        self.char_class = 1
                        self.hd = 10
                        self.hp = self.con_mod + self.hd
                        self.max_hp = self.hp
                        self.second_wind = True
                        self.second_wind_cnt = 1
                        self.skills["athletics"][0] += self.prof_bonus
                        self.skills["acrobatics"][0] += self.prof_bonus
                        self.saving_throws["str"][0] += self.prof_bonus
                        self.saving_throws["con"][0] += self.prof_bonus
                        self.gen_fighting_style(self.inv, ui)
                elif class_choice == 2:
                        self.char_class = 2
                        self.hd = 10
                        self.hp = self.con_mod + self.hd
                        self.max_hp = self.hp
                        self.bonus_attack = True
                        self.eq_weapon_main_finesse = True
                        self.eq_weapon_offhand_finesse = True
                        self.eq_weapon_offhand = "unarmed strike"
                        self.skills["acrobatics"][0] += self.prof_bonus
                        self.skills["perception"][0] += self.prof_bonus
                        self.saving_throws["str"][0] += self.prof_bonus
                        self.saving_throws["dex"][0] += self.prof_bonus
                elif class_choice == 3:
                        self.char_class = 3
                        self.hd = 12
                        self.hp = self.con_mod + self.hd
                        self.max_hp = self.hp
                        self.skills["athletics"][0] += self.prof_bonus
                        self.skills["acrobatics"][0] += self.prof_bonus
                        self.saving_throws["str"][0] += self.prof_bonus
                        self.saving_throws["con"][0] += self.prof_bonus
                        self.bonus_actions["rage"] = 2
                elif class_choice == 4:
                        self.char_class = 4
                        self.hd = 8
                        self.hp = self.con_mod + self.hd
                        self.max_hp = self.hp
                        self.skills["stealth"][0] += self.prof_bonus * 2
                        self.skills["acrobatics"][0] += self.prof_bonus * 2
                        self.saving_throws["dex"][0] += self.prof_bonus
                        self.saving_throws["int"][0] += self.prof_bonus
                        self.sneak_damage = [6, 1]
                elif class_choice == 5:
                        self.char_class = 5
                        self.hd = 10
                        self.hp = self.con_mod + self.hd
                        self.max_hp = self.hp
                        self.skills["athletics"][0] += self.prof_bonus
                        self.skills["persuasion"][0] += self.prof_bonus
                        self.saving_throws["wis"][0] += self.prof_bonus
                        self.saving_throws["cha"][0] += self.prof_bonus
                elif class_choice == 6:
                        self.char_class = 6
                        self.hd = 10
                        self.hp = self.con_mod + self.hd
                        self.max_hp = self.hp
                        self.skills["acrobatics"][0] += self.prof_bonus
                        self.skills["perception"][0] += self.prof_bonus
                        self.saving_throws["str"][0] += self.prof_bonus
                        self.saving_throws["dex"][0] += self.prof_bonus
                ui.update_status()
        def gen_fighting_style(self, inv, ui):
                styles = {
                        1: "defense",
                        2: "great weapon fighting",
                        3: "dueling",
                        4: "two-weapon fighting",
                        5: "archery"
                        }
                if self.char_class == 5:
                        styles.pop(5)
                if self.char_class == 6:
                        styles.pop(2)
                ui.push_message("Choose your fighting style.")
                style_choice = int(ui.get_dict_choice_input(styles))
                if self.char_class == 1:
                        if style_choice == 1:
                                self.fighting_style = 1
                        elif style_choice == 2:
                                self.fighting_style = 2
                        elif style_choice == 3:
                                self.fighting_style = 3
                        elif style_choice == 4:
                                self.fighting_style = 4
                        elif style_choice == 5:
                                self.fighting_style = 5
                elif self.char_class == 5:
                        if style_choice == 1:
                                self.fighting_style = 1
                        elif style_choice == 2:
                                self.fighting_style = 2
                        elif style_choice == 3:
                                self.fighting_style = 3
                        elif style_choice == 4:
                                self.fighting_style = 4
                elif self.char_class == 6:
                        if style_choice == 1:
                                self.fighting_style = 1
                        elif style_choice == 3:
                                self.fighting_style = 3
                        elif style_choice == 4:
                                self.fighting_style = 4
                        elif style_choice == 5:
                                self.fighting_style = 5
        def equip(self, eq_uneq, item, type, item_list, all_items, everything, all_melee_weapons, all_ranged_weapons, ui):
                # stats for currently equipped armor, shield and/or weapon
                curr_armor_ac = 0
                curr_armor_ench = 0
                curr_shield_ac = 0
                curr_shield_ench = 0
                curr_main_weapon_ench = 0
                curr_off_weapon_ench = 0
                if self.eq_armor != "unarmored":
                        curr_armor_ac = all_items.armors[self.eq_armor][1]
                        curr_armor_ench = all_items.armors[self.eq_armor][2]
                if self.eq_weapon_offhand in all_items.shields:
                        curr_shield_ac = all_items.shields[self.eq_weapon_offhand][1]
                        curr_shield_ench = all_items.shields[self.eq_weapon_offhand][2]
                if self.eq_weapon_main != "unarmed strike":
                        curr_main_weapon_ench = everything[self.eq_weapon_main][3]
                if self.eq_weapon_offhand not in ["unarmed strike", "nothing", "shield"]:
                        curr_off_weapon_ench = everything[self.eq_weapon_offhand][3]
                # equip
                if eq_uneq == 1:
                        # melee or ranged weapon
                        if type in [1, 2]:
                                # stats of the weapon to be equipped
                                dmg_die = item_list[item][1]
                                dmg_die_cnt = item_list[item][2]
                                ench = item_list[item][3]
                                dmg_type = item_list[item][4]
                                light_heavy = item_list[item][6]
                                finesse = item_list[item][7]
                                hands = item_list[item][8]
                                if type == 1:
                                        thrown = item_list[item][9]
                                elif type == 2:
                                        load = item_list[item][9]
                                # stats of the weapon that is currently equipped in main hand
                                if self.eq_weapon_main == "unarmed strike":
                                        eq_main_light_heavy = 0
                                else:
                                        eq_main_light_heavy = everything[self.eq_weapon_main][6]
                                # stats of the weapon that is currently equipped in the off-hand
                                if self.eq_weapon_offhand in ["nothing", "unarmed strike"]:
                                        eq_off_light_heavy = 0
                                else:
                                        eq_off_light_heavy = everything[self.eq_weapon_offhand][6]
                                # 1. nothing in main hand, shield in off-hand and weapon to equip is one-handed or versatile (1.5 hands)
                                if self.eq_weapon_main == "unarmed strike" and self.eq_weapon_offhand == "shield" and hands < 2:
                                        self.eq_weapon_main = item
                                        self.dmg_die_main = dmg_die
                                        self.dmg_die_cnt_main = dmg_die_cnt
                                        self.dmg_die_type_main = dmg_type
                                        self.ench_main = ench
                                        self.bonus_attack = False
                                        self.eq_weapon_main_finesse = finesse
                                # 2. something or nothing in main hand, nothing in off-hand
                                elif self.eq_weapon_offhand in ["nothing", "unarmed strike"]:
                                        # nothing in main hand, then equip to main hand
                                        if self.eq_weapon_main == "unarmed strike":
                                                self.eq_weapon_main = item
                                                self.dmg_die_main = dmg_die
                                                # if versatile, then raise main hand damage die by one grade
                                                if hands == 1.5:
                                                        self.dmg_die_main += 2
                                                        self.eq_weapon_offhand = item
                                                elif hands == 2:
                                                        self.eq_weapon_offhand = item
                                                self.dmg_die_cnt_main = dmg_die_cnt
                                                self.dmg_die_type_main = dmg_type
                                                self.ench_main = ench
                                                self.eq_weapon_main_finesse = finesse
                                        # something in main hand, then equip to off-hand if not 2-handed weapon
                                        elif self.eq_weapon_main != "unarmed strike" and hands < 2:
                                                self.eq_weapon_offhand = item
                                                self.dmg_die_off = dmg_die
                                                self.dmg_die_cnt_off = dmg_die_cnt
                                                self.dmg_die_type_off = dmg_type
                                                self.ench_off = ench
                                                self.eq_weapon_offhand_finesse = finesse
                                                # check for two-weapon fighting
                                                if light_heavy and eq_main_light_heavy:
                                                        self.bonus_attack = True
                                                else:
                                                        self.bonus_attack = False
                                        # something in main hand, but want to equip 2-handed, then switch weapons in main hand
                                        elif self.eq_weapon_main != "unarmed strike" and hands == 2:
                                                self.eq_weapon_main = item
                                                self.eq_weapon_offhand = item
                                                self.dmg_die_main = dmg_die
                                                self.dmg_die_cnt_main = dmg_die_cnt
                                                self.dmg_die_type_main = dmg_type
                                                self.ench_main = ench
                                                self.eq_weapon_main_finesse = finesse
                                                self.eq_weapon_offhand_finesse = finesse
                                # 3. something in main hand, something in off-hand
                                elif self.eq_weapon_main != "unarmed strike" and self.eq_weapon_offhand != "nothing":
                                        # unequip off-hand (shield or weapon) and equip item on main hand
                                        if hands == 2:
                                                self.ac -= 2
                                                self.dmg_die_off = 1
                                                self.dmg_die_cnt_off = 1
                                                self.dmg_die_type_off = "b"
                                                self.ench_off = 0
                                                self.eq_weapon_offhand = item
                                                self.eq_weapon_main_finesse = finesse
                                                self.eq_weapon_offhand_finesse = finesse
                                        self.eq_weapon_main = item
                                        self.dmg_die_main = dmg_die
                                        self.dmg_die_cnt_main = dmg_die_cnt
                                        self.dmg_die_type_main = dmg_type
                                        self.ench_main = ench
                                        self.eq_weapon_main_finesse = finesse
                                        # check for two-weapon fighting
                                        if light_heavy and eq_off_light_heavy:
                                                self.bonus_attack = True
                                        else:
                                                self.bonus_attack = False
                                # 4. nothing in main hand, weapon or shield in off-hand and weapon to equip is 2-handed
                                elif self.eq_weapon_main == "unarmed strike" and self.eq_weapon_offhand != "nothing" and hands == 2:
                                        self.eq_weapon_main = item
                                        if self.eq_weapon_offhand == "shield":
                                                self.ac -= 2
                                        else:
                                                self.dmg_die_off = 1
                                                self.dmg_die_cnt_off = 1
                                                self.dmg_die_type_off = "b"
                                                self.ench_off = 0
                                        self.eq_weapon_offhand = item
                                        self.dmg_die_main = dmg_die
                                        self.dmg_die_cnt_main = dmg_die_cnt
                                        self.dmg_die_type_main = dmg_type
                                        self.ench_main = ench
                                        self.bonus_attack = False
                                        self.eq_weapon_main_finesse = finesse
                                        self.eq_weapon_offhand_finesse = finesse
                                else:
                                        ui.push_prompt("Impossible to equip.")
                                # set ranged
                                if type == 2:
                                        self.ranged = True
                                elif type == 1:
                                        self.ranged = False
                        # armor or shield
                        elif type == 3:
                                # stats of the armor/shield to be equipped
                                armor_class = item_list[item][1]
                                armor_ench = item_list[item][2]
                                str_req = item_list[item][3]
                                armor_type = item_list[item][4]
                                # light armor: unlimited +/- DEX bonus
                                if armor_type == 0:
                                        self.eq_armor = item
                                        self.ac = armor_class + self.dex_mod + armor_ench + curr_shield_ac + curr_shield_ench
                                # medium armor: +2 max / unlimited negative DEX bonus
                                elif armor_type == 1:
                                        self.eq_armor = item
                                        if self.dex_mod <= 2:
                                                self.ac = armor_class + self.dex_mod + armor_ench + curr_shield_ac + curr_shield_ench
                                        else:
                                                self.ac = armor_class + 2 + armor_ench + curr_shield_ac + curr_shield_ench
                                # heavy armor: no +/- DEX bonus
                                elif armor_type == 2:
                                        if item not in ["chain mail", "splint", "plate"]:
                                                self.eq_armor = item
                                                self.ac = armor_class + armor_ench + curr_shield_ac + curr_shield_ench
                                        elif (item == "chain mail" and self.str >= str_req) or (item in ["splint", "plate"] and self.str >= str_req):
                                                self.eq_armor = item
                                                self.ac = armor_class + armor_ench + curr_shield_ac + curr_shield_ench
                                        else:
                                                ui.push_prompt("Not strong enough to don a " + item + ".")
                                # shield: + cumulative AC
                                elif armor_type == 3:
                                        # nothing in off-hand, equip to off-hand
                                        if self.eq_weapon_offhand in ["nothing", "unarmed strike"]:
                                                self.ac += armor_class + armor_ench
                                        # already a shield equipped, unequip shield first then equip the new one
                                        elif self.eq_weapon_offhand in all_items.shields:
                                                self.ac -= curr_shield_ac - curr_shield_ench + armor_class + armor_ench
                                        else:
                                                # unequip 2-handed weapon
                                                if all_melee_weapons[self.eq_weapon_main][8] == 2 or (self.ranged and all_ranged_weapons[self.eq_weapon_main][8] == 2):
                                                        self.eq_weapon_main = "unarmed strike"
                                                        self.dmg_die_main = 1
                                                        self.dmg_die_cnt_main = 1
                                                        self.dmg_die_type_main = "b"
                                                        self.ench_main = 0
                                                        self.dmg_die_off = 1
                                                        self.dmg_die_cnt_off = 1
                                                        self.dmg_die_type_off = "b"
                                                        self.ench_off = 0
                                                        self.ranged = False
                                                # one-hand if weapon held is versatile
                                                elif all_melee_weapons[self.eq_weapon_main][8] == 1.5:
                                                        self.dmg_die_main = all_melee_weapons[self.eq_weapon_main][1]
                                                # unequip off-hand weapon
                                                else:
                                                        self.dmg_die_off = 1
                                                        self.dmg_die_cnt_off = 1
                                                        self.dmg_die_type_off = "b"
                                                        self.ench_off = 0
                                                        self.bonus_attack = False
                                                self.ac += armor_class + armor_ench
                                        self.eq_weapon_offhand = item
                                else:
                                        ui.push_prompt("Equip failed.")
                        # class specific adjustments
                        # fighter
                        if self.char_class == 1:
                                # fighters are proficient with all weapons and armor
                                self.main_hand_prof = True
                                self.main_str_att_mod = self.str_mod + self.prof_bonus
                                self.main_dex_att_mod = self.dex_mod + self.prof_bonus
                                self.main_str_dmg_mod = self.str_mod
                                self.main_dex_dmg_mod = self.dex_mod
                                self.off_hand_prof = True
                                self.off_str_att_mod = self.str_mod + self.prof_bonus
                                self.off_dex_att_mod = self.dex_mod + self.prof_bonus
                                self.off_str_dmg_mod = self.str_mod
                                self.off_dex_dmg_mod = self.dex_mod
                                # defense: +1 AC if wearing armor
                                if self.fighting_style == 1 and self.eq_armor != "unarmored" and type == 3:
                                        if armor_type != 3:
                                                self.ac += 1
                                # great weapon fighting: reroll 1s and 2s on dmg
                                elif self.fighting_style == 2 and self.eq_weapon_main == self.eq_weapon_offhand:
                                        self.reroll_dmg = True
                                # dueling: +2 dmg if no other weapon in off-hand
                                elif self.fighting_style == 3 and self.eq_weapon_main != "unarmed strike" and (self.eq_weapon_offhand in ["nothing", "unarmed strike"] or all_melee_weapons[self.eq_weapon_main][8] == 1.5 or self.eq_weapon_offhand in all_items.shields):
                                        self.main_str_dmg_mod = self.str_mod + 2
                                        self.main_dex_dmg_mod = self.dex_mod + 2
                                        if all_melee_weapons[self.eq_weapon_main][8] == 1.5:
                                                self.dmg_die_main = all_melee_weapons[self.eq_weapon_main][1]
                                # two weapon fighting: add dmg mod to bonus attack
                                elif self.fighting_style == 4 and self.bonus_attack:
                                        self.offhand_dmg_mod = True
                                # archery: +2 to attack mod with ranged weapons
                                elif self.fighting_style == 5 and self.ranged:
                                        self.dex_att_mod = self.dex_mod + self.prof_bonus + 2
                        # monk
                        elif self.char_class == 2:
                                # monk weapons
                                monk_weapon_main = False
                                monk_weapon_offhand = False
                                if self.eq_weapon_main == "unarmed strike":
                                        monk_weapon_main = True
                                else:
                                        monk_weapon_main = all_melee_weapons[self.eq_weapon_main][10]
                                if self.eq_weapon_offhand in ["unarmed strike", "nothing"]:
                                        monk_weapon_offhand = True
                                elif self.eq_weapon_offhand in all_items.shields:
                                        monk_weapon_offhand = False
                                else:
                                        monk_weapon_offhand = all_melee_weapons[self.eq_weapon_offhand][10]
                                # monks get their WIS mod to AC, martial arts die, unarmed finesse and bonus action unarmed strike if they don't wear armor or shield, and only wielding monk weapons
                                if self.eq_armor != "unarmored" or self.eq_weapon_offhand in all_items.shields or not monk_weapon_main or not monk_weapon_offhand:
                                        if self.eq_weapon_main == "unarmed strike":
                                                self.bonus_attack = False
                                                self.offhand_dmg_mod = False
                                                self.dmg_die_off = 1
                                                self.dmg_die_cnt_off = 1
                                                self.dmg_die_type_off = "b"
                                                self.ench_off = 0
                                                self.eq_weapon_main_finesse = False
                                        if self.eq_armor == "unarmored":
                                                self.ac = self.dex_mod
                                # monks are proficient with simple weapons and shortswords only, no armor and shield proficiencies
                                if monk_weapon_main or self.eq_weapon_main == "shortsword" or monk_weapon_offhand or self.eq_weapon_offhand == "shortsword":
                                        if monk_weapon_main:
                                                self.eq_weapon_main_finesse = True
                                                self.main_hand_prof = True
                                                self.main_str_att_mod = self.str_mod + self.prof_bonus
                                                self.main_dex_att_mod = self.dex_mod + self.prof_bonus
                                                self.main_str_dmg_mod = self.str_mod
                                                self.main_dex_dmg_mod = self.dex_mod
                                        if monk_weapon_offhand:
                                                self.eq_weapon_offhand_finesse = True
                                                self.off_hand_prof = True
                                                self.off_str_att_mod = self.str_mod + self.prof_bonus
                                                self.off_dex_att_mod = self.dex_mod + self.prof_bonus
                                                self.off_str_dmg_mod = self.str_mod
                                                self.off_dex_dmg_mod = self.dex_mod
                                else:
                                        self.main_hand_prof = False
                                        self.main_str_att_mod = self.str_mod
                                        self.main_dex_att_mod = self.dex_mod
                                        self.main_str_dmg_mod = self.str_mod
                                        self.main_dex_dmg_mod = self.dex_mod
                                        self.off_hand_prof = False
                                        self.off_str_att_mod = self.str_mod
                                        self.off_dex_att_mod = self.dex_mod
                                        self.off_str_dmg_mod = self.str_mod
                                        self.off_dex_dmg_mod = self.dex_mod
                                if self.eq_weapon_main == self.eq_weapon_offhand == "greatclub":
                                        self.bonus_attack = False
                                        self.eq_weapon_main_finesse = False
                                if self.eq_armor != "unarmored" or self.eq_weapon_offhand == "shield":
                                        for s in self.skills.keys():
                                                self.skills[s][3] = True
                                        for st in self.saving_throws.keys():
                                                self.saving_throws[st][3] = True
                                        self.attack_disadv = True
                        # barbarian
                        elif self.char_class == 3:
                                # barbarians are proficient in all weapons
                                self.main_hand_prof = True
                                self.main_str_att_mod = self.str_mod + self.prof_bonus
                                self.main_dex_att_mod = self.dex_mod + self.prof_bonus
                                self.main_str_dmg_mod = self.str_mod
                                self.main_dex_dmg_mod = self.dex_mod
                                self.off_hand_prof = True
                                self.off_str_att_mod = self.str_mod + self.prof_bonus
                                self.off_dex_att_mod = self.dex_mod + self.prof_bonus
                                self.off_str_dmg_mod = self.str_mod
                                self.off_dex_dmg_mod = self.dex_mod
                                # barbarians get to add their CON mod to AC if not wearing any armor, shield bonuses apply though
                                if self.eq_armor == "unarmored":
                                        barb_shield_mod = 0
                                        barb_shield_ench = 0
                                        if self.eq_weapon_offhand in all_items.shields:
                                                barb_shield_mod = all_items.shields[self.eq_weapon_offhand][1]
                                                barb_shield_ench = all_items.shields[self.eq_weapon_offhand][2]
                                        if self.con_mod > 0:
                                                self.ac = 10 + self.dex_mod + self.con_mod + barb_shield_mod + barb_shield_ench
                                        else:
                                                self.ac = 10 + self.dex_mod + barb_shield_mod + barb_shield_ench
                                # barbarians are not proficient in heavy armor
                                elif all_items.armors[self.eq_armor][4] == 2:
                                        for s in self.skills.keys():
                                                self.skills[s][3] = True
                                        for st in self.saving_throws.keys():
                                                self.saving_throws[st][3] = True
                                        self.attack_disadv = True
                        # rogue
                        elif self.char_class == 4:
                                # rogues are proficient in: simple weapons, hand crossbows, longswords, rapiers, shortswords, light armor
                                if self.eq_weapon_main in all_items.simple_melee_weapons or self.eq_weapon_main in ["shortsword", "hand crossbow", "longsword", "rapier"]:
                                        self.main_hand_prof = True
                                        self.main_str_att_mod = self.str_mod + self.prof_bonus
                                        self.main_dex_att_mod = self.dex_mod + self.prof_bonus
                                        self.main_str_dmg_mod = self.str_mod
                                        self.main_dex_dmg_mod = self.dex_mod
                                if self.eq_weapon_offhand in all_items.simple_melee_weapons or self.eq_weapon_offhand in ["shortsword", "hand crossbow", "longsword", "rapier"]:
                                        self.off_hand_prof = True
                                        self.off_str_att_mod = self.str_mod + self.prof_bonus
                                        self.off_dex_att_mod = self.dex_mod + self.prof_bonus
                                        self.off_str_dmg_mod = self.str_mod
                                        self.off_dex_dmg_mod = self.dex_mod
                                if self.eq_armor != "unarmored" or self.eq_weapon_offhand == "shield":
                                        if self.eq_armor == "unarmored":
                                                armor_type = 0
                                        else:
                                                armor_type = all_items.armors[self.eq_armor][4]
                                        if armor_type in [1, 2] or self.eq_weapon_offhand == "shield":
                                                for s in self.skills.keys():
                                                        self.skills[s][3] = True
                                                for st in self.saving_throws.keys():
                                                        self.saving_throws[st][3] = True
                                                self.attack_disadv = True
                        # paladin
                        elif self.char_class == 5:
                                # paladins are proficient in all weapons and armor
                                self.main_hand_prof = True
                                self.main_str_att_mod = self.str_mod + self.prof_bonus
                                self.main_dex_att_mod = self.dex_mod + self.prof_bonus
                                self.main_str_dmg_mod = self.str_mod
                                self.main_dex_dmg_mod = self.dex_mod
                                self.off_hand_prof = True
                                self.off_str_att_mod = self.str_mod + self.prof_bonus
                                self.off_dex_att_mod = self.dex_mod + self.prof_bonus
                                self.off_str_dmg_mod = self.str_mod
                                self.off_dex_dmg_mod = self.dex_mod
                                # defense: +1 AC if wearing armor
                                if self.fighting_style == 1 and self.eq_armor != "unarmored" and type == 3:
                                        if armor_type != 3:
                                                self.ac += 1
                                # dueling: +2 dmg if no other weapon in off-hand
                                elif self.fighting_style == 3 and self.eq_weapon_main != "unarmed strike" and (self.eq_weapon_offhand in ["nothing", "unarmed strike"] or all_melee_weapons[self.eq_weapon_main][8] == 1.5) and type == 1:
                                        self.main_str_dmg_mod = self.str_mod + 2
                                        self.main_dex_dmg_mod = self.dex_mod + 2
                                        if all_melee_weapons[self.eq_weapon_main][8] == 1.5:
                                                self.dmg_die_main = all_melee_weapons[self.eq_weapon_main][1]
                                # two weapon fighting: add dmg mod to bonus attack
                                elif self.fighting_style == 4 and self.bonus_attack:
                                        self.offhand_dmg_mod = True
                                # archery: +2 to attack mod with ranged weapons
                                elif self.fighting_style == 5 and self.ranged:
                                        self.dex_att_mod = self.dex_mod + self.prof_bonus + 2
                        # ranger
                        elif self.char_class == 6:
                                # rangers are proficient in all weapons
                                self.main_hand_prof = True
                                self.main_str_att_mod = self.str_mod + self.prof_bonus
                                self.main_dex_att_mod = self.dex_mod + self.prof_bonus
                                self.main_str_dmg_mod = self.str_mod
                                self.main_dex_dmg_mod = self.dex_mod
                                self.off_hand_prof = True
                                self.off_str_att_mod = self.str_mod + self.prof_bonus
                                self.off_dex_att_mod = self.dex_mod + self.prof_bonus
                                self.off_str_dmg_mod = self.str_mod
                                self.off_dex_dmg_mod = self.dex_mod
                                # defense: +1 AC if wearing armor
                                if self.fighting_style == 1 and self.eq_armor != "unarmored" and type == 3:
                                        if armor_type != 3:
                                                self.ac += 1
                                # great weapon fighting: reroll 1s and 2s on dmg
                                elif self.fighting_style == 2 and self.eq_weapon_main == self.eq_weapon_offhand:
                                        self.reroll_dmg = True
                                # dueling: +2 dmg if no other weapon in off-hand
                                elif self.fighting_style == 3 and self.eq_weapon_main != "unarmed strike" and (self.eq_weapon_offhand in ["nothing", "unarmed strike"] or all_melee_weapons[self.eq_weapon_main][8] == 1.5) and type == 1:
                                        self.main_str_dmg_mod = self.str_mod + 2
                                        self.main_dex_dmg_mod = self.dex_mod + 2
                                        if all_melee_weapons[self.eq_weapon_main][8] == 1.5:
                                                self.dmg_die_main = all_melee_weapons[self.eq_weapon_main][1]
                                # two weapon fighting: add dmg mod to bonus attack
                                elif self.fighting_style == 4 and self.bonus_attack:
                                        self.offhand_dmg_mod = True
                                # rangers are not proficient in heavy armor
                                elif all_items.armors[self.eq_armor][4] == 2:
                                        for s in self.skills.keys():
                                                self.skills[s][3] = True
                                        for st in self.saving_throws.keys():
                                                self.saving_throws[st][3] = True
                                        self.attack_disadv = True
                # unequip
                elif eq_uneq == 0:
                        # melee or ranged weapon
                        if type in [1, 2]:
                                # when unequipping main hand weapon, also "take off" off-hand (in case of versatile, dual wield or 2-handed), if not a shield
                                if item == self.eq_weapon_main and self.eq_weapon_offhand not in all_items.shields:
                                        self.eq_weapon_main = "unarmed strike"
                                        self.dmg_die_main = 1
                                        self.dmg_die_cnt_main = 1
                                        self.dmg_die_type_main = "b"
                                        self.ench_main = 0
                                        self.eq_weapon_offhand = "nothing"
                                        self.dmg_die_off = 1
                                        self.dmg_die_cnt_off = 1
                                        self.dmg_die_type_off = "b"
                                        self.ench_off = 0
                                        self.eq_weapon_main_finesse = False
                                        self.eq_weapon_offhand_finesse = False
                                        self.bonus_attack = False
                                        self.offhand_dmg_mod = False
                                        self.reroll_dmg = False
                                        self.ranged == False
                                        self.main_hand_prof = True
                                        self.main_str_att_mod = self.str_mod + self.prof_bonus
                                        self.main_dex_att_mod = self.dex_mod + self.prof_bonus
                                        self.main_str_dmg_mod = self.str_mod
                                        self.main_dex_dmg_mod = self.dex_mod
                                        self.off_hand_prof = False
                                        self.off_str_att_mod = self.str_mod
                                        self.off_dex_att_mod = self.dex_mod
                                        self.off_str_dmg_mod = self.str_mod
                                        self.off_dex_dmg_mod = self.dex_mod
                                # when unequipping main hand weapon and off-hand has a shield, then unequip main hand only
                                elif item == self.eq_weapon_main and self.eq_weapon_offhand in all_items.shields:
                                        self.eq_weapon_main = "unarmed strike"
                                        self.dmg_die_main = 1
                                        self.dmg_die_cnt_main = 1
                                        self.dmg_die_type_main = "b"
                                        self.ench_main = 0
                                        self.eq_weapon_main_finesse = False
                                        self.ranged == False
                                        self.main_hand_prof = True
                                        self.main_str_att_mod = self.str_mod + self.prof_bonus
                                        self.main_dex_att_mod = self.dex_mod + self.prof_bonus
                                        self.main_str_dmg_mod = self.str_mod
                                        self.main_dex_dmg_mod = self.dex_mod
                                # unequip off-hand weapon
                                elif item == self.eq_weapon_offhand:
                                        self.eq_weapon_offhand = "nothing"
                                        self.dmg_die_off = 1
                                        self.dmg_die_cnt_off = 1
                                        self.dmg_die_type_off = "b"
                                        self.ench_off = 0
                                        self.eq_weapon_offhand_finesse = False
                                        self.bonus_attack = False
                                        self.offhand_dmg_mod = False
                                        self.off_hand_prof = False
                                        self.off_str_att_mod = self.str_mod
                                        self.off_dex_att_mod = self.dex_mod
                                        self.off_str_dmg_mod = self.str_mod
                                        self.off_dex_dmg_mod = self.dex_mod
                        # armor or shield
                        elif type == 3:
                                if item in all_items.armors:
                                        self.eq_armor = "unarmored"
                                        self.ac = 10 + self.dex_mod
                                elif item in all_items.shields:
                                        self.eq_weapon_offhand = "nothing"
                                        self.ac -= all_items.shields[item][1] - all_items.shields[item][2]
                                for s in self.skills.keys():
                                        self.skills[s][3] = False
                                for st in self.saving_throws.keys():
                                        self.saving_throws[st][3] = False
                                self.attack_disadv = False
                        else:
                                ui.push_prompt("Unequip failed.")
                        # class specific adjustments
                        # fighter
                        if self.char_class == 1:
                                pass
                        # monk
                        elif self.char_class == 2:
                                if self.eq_weapon_main == "unarmed strike":
                                        self.main_hand_prof = True
                                        self.main_str_att_mod = self.str_mod + self.prof_bonus
                                        self.main_dex_att_mod = self.dex_mod + self.prof_bonus
                                        self.main_str_dmg_mod = self.str_mod
                                        self.main_dex_dmg_mod = self.dex_mod
                                if self.eq_weapon_offhand in ["nothing", "unarmed strike"]:
                                        self.off_hand_prof = True
                                        self.off_str_att_mod = self.str_mod + self.prof_bonus
                                        self.off_dex_att_mod = self.dex_mod + self.prof_bonus
                                        self.off_str_dmg_mod = self.str_mod
                                        self.off_dex_dmg_mod = self.dex_mod
                                if self.eq_armor == "unarmored":
                                        if self.wis_mod > 0:
                                                self.ac = 10 + self.dex_mod + self.wis_mod
                                        else:
                                                self.ac = 10 + self.dex_mod
                        # barbarian
                        elif self.char_class == 3:
                                if self.eq_armor == "unarmored":
                                        barb_shield_mod = 0
                                        barb_shield_ench = 0
                                        if self.eq_weapon_offhand in all_items.shields:
                                                barb_shield_mod = all_items.shields[self.eq_weapon_offhand][1]
                                                barb_shield_ench = all_items.shields[self.eq_weapon_offhand][2]
                                        if self.con_mod > 0:
                                                self.ac = 10 + self.dex_mod + self.con_mod + barb_shield_mod + barb_shield_ench
                                        else:
                                                self.ac = 10 + self.dex_mod + barb_shield_mod + barb_shield_ench
                        # rogue
                        elif self.char_class == 4:
                                if self.eq_weapon_main == "unarmed strike":
                                        self.main_hand_prof = False
                                        self.main_str_att_mod = self.str_mod
                                        self.main_dex_att_mod = self.dex_mod
                                        self.main_str_dmg_mod = self.str_mod
                                        self.main_dex_dmg_mod = self.dex_mod
                                if self.eq_weapon_offhand in ["nothing", "unarmed strike"]:
                                        self.off_hand_prof = False
                                        self.off_str_att_mod = self.str_mod
                                        self.off_dex_att_mod = self.dex_mod
                                        self.off_str_dmg_mod = self.str_mod
                                        self.off_dex_dmg_mod = self.dex_mod
                        # paladin
                        elif self.char_class == 5:
                                pass
                        # ranger
                        elif self.char_class == 6:
                                pass
        def level_up(self, levels, ui):
                for lvl in levels:
                        self.level = 1 + lvl
                        self.hd_cnt += 1 + lvl
                        self.hd_max += 1 + lvl
                        rolled_hp = roll_dice(self.hd, self.con_mod, 0, ui)[0]
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
                                        self.sneak_damage = [6, math.ceil(self.level / 2)]
                                if self.char_class == 5:
                                        self.divine_smite = [2, 0, 0, 0, 0]
                                        self.lay_on_hands_pool_max += 5
                                        self.lay_on_hands_pool += 5
                                        self.gen_fighting_style(self.inv, ui)
                                if self.char_class == 6:
                                        self.gen_fighting_style(self.inv, ui)
                        if self.level == 3:
                                if self.char_class == 1:
                                        pass
                                if self.char_class == 2:
                                        self.specials["ki"] = self.level
                                        #self.specials["deflect missiles"] = True
                                if self.char_class == 3:
                                        self.rage_cnt = 3
                                if self.char_class == 4:
                                        self.sneak_damage = [6, math.ceil(self.level / 2)]
                                if self.char_class == 5:
                                        self.divine_smite = [3, 0, 0, 0, 0]
                                        self.lay_on_hands_pool_max += 5
                                        self.lay_on_hands_pool += 5
                                if self.char_class == 6:
                                        pass
                        if self.level == 4:
                                #self.asi_choice()
                                if self.char_class == 1:
                                        pass
                                if self.char_class == 2:
                                        self.specials["ki"] = self.level
                                if self.char_class == 3:
                                        pass
                                if self.char_class == 4:
                                        self.sneak_damage = [6, math.ceil(self.level / 2)]
                                if self.char_class == 5:
                                        self.lay_on_hands_pool_max += 5
                                        self.lay_on_hands_pool += 5
                                if self.char_class == 6:
                                        pass
                        if self.level == 5:
                                #self.prof_bonus_up()
                                if self.char_class != 4:
                                        self.attacks = 2
                                if self.char_class == 1:
                                        pass
                                if self.char_class == 2:
                                        self.specials["ki"] = self.level
                                        #self.specials["stunning strike"] = True
                                        #self.specials["uncanny dodge"] = True
                                if self.char_class == 3:
                                        pass
                                if self.char_class == 4:
                                        self.sneak_damage = [6, math.ceil(self.level / 2)]
                                if self.char_class == 5:
                                        self.divine_smite = [4, 2, 0, 0, 0]
                                        self.lay_on_hands_pool_max += 5
                                        self.lay_on_hands_pool += 5
                                if self.char_class == 6:
                                        pass
        def get_char_class(self):
                classes = {
                        1: "fighter",
                        2: "monk",
                        3: "barbarian",
                        4: "rogue",
                        5: "paladin",
                        6: "ranger"
                        }
                return classes[self.char_class]
        def get_char_race(self):
                races = {
                        1: "human",
                        2: "halfling",
                        3: "dwarf",
                        4: "gnome",
                        5: "elf",
                        6: "half-orc"
                        }
                return races[self.race]
        def get_char_subrace(self):
                subraces = {
                        11: "vanilla",
                        21: "lightfoot",
                        22: "stout",
                        23: "ghostwise",
                        31: "hill",
                        32: "mountain",
                        33: "duergar",
                        41: "forest",
                        42: "rock",
                        43: "svirfneblin",
                        51: "high elf",
                        52: "wood elf",
                        53: "drow",
                        61: "vanilla"
                        }
                return subraces[self.subrace]
        def get_fighting_style(self):
                styles = {
                        0: "none",
                        1: "defense",
                        2: "great weapon fighting",
                        3: "dueling",
                        4: "two-weapon fighting",
                        5: "archery"
                        }
                return styles[self.fighting_style]

'''
Fighter (Character child)
IN
- name (string)
- strength (int)
- dexterity (int)
- constitution (int)
- wisdom (int)
- intelligence (int)
- charisma (int)
- starting level (int)
- race (int)
- subrace (int)
- npc (bool)
- ui (object)
OUT
- fighter (object)
'''
class Fighter(Character):
        "Child for fighter class."
        def __init__(self, name, str, dex, con, int, wis, cha, starting_lvl, race, subrace, npc, ui):
                super().__init__(name, str, dex, con, int, wis, cha, starting_lvl, race, subrace, npc, ui)
                self.char_class = 1
                self.second_wind = True
                self.second_wind_cnt = 1
                self.main_hand_prof = True
                self.main_str_att_mod = self.str_mod + self.prof_bonus

'''
Monk (Character child)
IN
- name (string)
- strength (int)
- dexterity (int)
- constitution (int)
- wisdom (int)
- intelligence (int)
- charisma (int)
- starting level (int)
- race (int)
- subrace (int)
- npc (bool)
- ui (object)
OUT
- monk (object)
'''
class Monk(Character):
        "Child for monk class."
        def __init__(self, name, str, dex, con, int, wis, cha, starting_lvl, race, subrace, npc, ui):
                super().__init__(name, str, dex, con, int, wis, cha, starting_lvl, race, subrace, npc, ui)
                self.char_class = 2
                self.dmg_die_main = 4
                self.dmg_die_cnt_main = 1
                self.dmg_die_type_main = "b"
                self.ench_main = 0
                self.dmg_die_off = 4
                self.dmg_die_cnt_off = 1
                self.dmg_die_type_off = "b"
                self.ench_off = 0
                self.eq_weapon_main_finesse = True
                self.eq_weapon_offhand_finesse = True
                self.bonus_attack = True
                self.offhand_dmg_mod = True
                self.main_hand_prof = True
                self.off_hand_prof = True
                if self.wis_mod > 0:
                        self.ac = 10 + self.dex_mod + self.wis_mod
                else:
                        self.ac = 10 + self.dex_mod

'''
Barbarian (Character child)
IN
- name (string)
- strength (int)
- dexterity (int)
- constitution (int)
- wisdom (int)
- intelligence (int)
- charisma (int)
- starting level (int)
- race (int)
- subrace (int)
- npc (bool)
- ui (object)
OUT
- barbarian (object)
'''
class Barbarian(Character):
        "Child for barbarian class."
        def __init__(self, name, str, dex, con, int, wis, cha, starting_lvl, race, subrace, npc, ui):
                super().__init__(name, str, dex, con, int, wis, cha, starting_lvl, race, subrace, npc, ui)
                self.char_class = 3
                self.main_hand_prof = True
                self.main_str_att_mod = self.str_mod + self.prof_bonus
                self.raging = False
                self.got_attacked = False
                self.did_attack = False
                self.rage_cnt = 2
                self.rage_mod = 2
                if self.con_mod > 0:
                        self.ac = 10 + self.dex_mod + self.con_mod
                else:
                        self.ac = 10 + self.dex_mod
        def rage_on(self, all_items, ui):
                if self.eq_armor == "unarmored":
                        armor_type = 0
                else:
                        armor_type = all_items.armors[self.eq_armor][4]
                if armor_type != 2 and self.rage_cnt > 0:
                        self.raging = True
                        self.rage_cnt -= 1
                        self.skills["athletics"][2] = True
                        self.saving_throws["str"][2] = True
                        self.main_str_dmg_mod += self.rage_mod
                        self.off_str_dmg_mod += self.rage_mod
                        self.bonus_actions.pop(3)
                        self.bonus_actions[3] = "end rage"
                        ui.push_prompt( self.name + " would like to rage.")
                elif armor_type == 2 and self.rage_cnt > 0:
                        self.raging = True
                        self.rage_cnt -= 1
                        self.bonus_actions.pop(3)
                        self.bonus_actions[3] = "end rage"
                        ui.push_prompt("Warning: raging in heavy armor.")
                else:
                        ui.push_prompt("No rages left.")
        def rage_off(self, all_items, ui):
                if self.eq_armor == "unarmored":
                        armor_type = 0
                else:
                        armor_type = all_items.armors[self.eq_armor][4]
                if armor_type != 2:
                        self.skills["athletics"][2] = False
                        self.saving_throws["str"][2] = False
                        self.main_str_dmg_mod -= self.rage_mod
                        self.off_str_dmg_mod -= self.rage_mod
                self.raging = False
                if self.rage_cnt > 0:
                        self.bonus_actions.pop(3)
                        self.bonus_actions[3] = "rage"
                else:
                        self.bonus_actions.pop(3)
                ui.push_prompt("Rage ended.")

'''
Rogue (Character child)
IN
- name (string)
- strength (int)
- dexterity (int)
- constitution (int)
- wisdom (int)
- intelligence (int)
- charisma (int)
- starting level (int)
- race (int)
- subrace (int)
- npc (bool)
- ui (object)
OUT
- rogue (object)
'''
class Rogue(Character):
        "Child for rogue class."
        def __init__(self, name, str, dex, con, int, wis, cha, starting_lvl, race, subrace, npc, ui):
                super().__init__(name, str, dex, con, int, wis, cha, starting_lvl, race, subrace, npc, ui)
                self.char_class = 4
                self.sneak_damage = []
                self.sneak_attack = False

'''
Paladin (Character child)
IN
- name (string)
- strength (int)
- dexterity (int)
- constitution (int)
- wisdom (int)
- intelligence (int)
- charisma (int)
- starting level (int)
- race (int)
- subrace (int)
- npc (bool)
- ui (object)
OUT
- paladin (object)
'''
class Paladin(Character):
        "Child for paladin class."
        def __init__(self, name, str, dex, con, int, wis, cha, starting_lvl, race, subrace, npc, ui):
                super().__init__(name, str, dex, con, int, wis, cha, starting_lvl, race, subrace, npc, ui)
                self.char_class = 5
                self.lay_on_hands = True
                self.lay_on_hands_pool_max = 5
                self.lay_on_hands_pool = self.lay_on_hands_pool_max
                self.divine_smite = []
                self.main_hand_prof = True
                self.main_str_att_mod = self.str_mod + self.prof_bonus

'''
Ranger (Character child)
IN
- name (string)
- strength (int)
- dexterity (int)
- constitution (int)
- wisdom (int)
- intelligence (int)
- charisma (int)
- starting level (int)
- race (int)
- subrace (int)
- npc (bool)
- ui (object)
OUT
- ranger (object)
'''
class Ranger(Character):
        "Child for ranger class."
        def __init__(self, name, str, dex, con, int, wis, cha, starting_lvl, race, subrace, npc, ui):
                super().__init__(name, str, dex, con, int, wis, cha, starting_lvl, race, subrace, npc, ui)
                self.char_class = 6
                self.main_hand_prof = True
                self.main_str_att_mod = self.str_mod + self.prof_bonus

'''
Monster (Character child)
IN
- monster (dict)
- ui (object)
OUT
- monster (object)
'''
class Monster(Character):
        "Child for monsters."
        def __init__(self, monster, ui):
                super(Monster, self).__init__(monster["attrs"][0], monster["attrs"][1], monster["attrs"][2], monster["attrs"][3], monster["attrs"][4], monster["attrs"][5], monster["attrs"][6], 1, 0, 0, True, ui)
                self.str = monster["attrs"][1]
                self.dex = monster["attrs"][2]
                self.con = monster["attrs"][3]
                self.wis = monster["attrs"][4]
                self.int = monster["attrs"][5]
                self.cha = monster["attrs"][6]
                self.npc = True
                self.hd_cnt = monster["attrs"][8]
                self.hd = monster["attrs"][7]
                self.prof_bonus = 2
                self.attacks = monster["attrs"][10]
                self.multiattack = monster["attrs"][9]
                self.main_hand_prof = True
                self.main_str_att_mod = self.str_mod + self.prof_bonus
                self.main_dex_att_mod = self.dex_mod + self.prof_bonus
                if self.attacks < 2:
                        self.dmg_die_main = monster["attacks"][0][2]
                        self.dmg_die_cnt_main = monster["attacks"][0][3]
                        self.dmg_die_type_main = monster["attacks"][0][1]
                        self.ench_main = 0
                else:
                        pass
                self.max_hp = 0
                for _ in range(self.hd_cnt):
                        self.max_hp += roll_dice(self.hd, self.con_mod, 0, ui)[0]
                self.hp = max(1, self.max_hp)
                self.max_hp = max(1, self.hp)
                # save: [mod, bonus, adv, disadv]
                self.saving_throws = {
                        "str": [self.str_mod, monster["stmods"][0], False, False],
                        "dex": [self.dex_mod, monster["stmods"][1], False, False],
                        "con": [self.con_mod, monster["stmods"][2], False, False],
                        "wis": [self.wis_mod, monster["stmods"][3], False, False],
                        "int": [self.int_mod, monster["stmods"][4], False, False],
                        "cha": [self.cha_mod, monster["stmods"][5], False, False]
                        }
                # skill: [mod, bonus, adv, disadv]
                self.skills = {
                        "athletics": [self.str_mod, monster["skills"][0], False, False],
                        "acrobatics": [self.dex_mod, monster["skills"][1], False, False],
                        "perception": [self.wis_mod, monster["skills"][2], False, False],
                        "investigation": [self.int_mod, monster["skills"][3], False, False],
                        "stealth": [self.dex_mod, monster["skills"][4], False, False],
                        "persuasion": [self.cha_mod, monster["skills"][5], False, False]
                }
                if self.attacks < 2:
                        self.eq_weapon_main = monster["attacks"][0][0]
                        self.eq_weapon_main_finesse = True
                self.name = monster["attrs"][0]

'''
Inventory for PCs/NPCs
IN
- owner (string)
- ui (object)
OUT
- inventory (object)
'''
class Inventory:
        "Inventory creation."
        def __init__(self, owner, ui):
                # player id
                self.owner = owner
                # name: type, quantity
                self.inv = {}
        def add_item(self, item, type):
                if item in self.inv:
                        self.inv[item][1] += 1
                else:
                        self.inv[item] = [type, 1]
        def get_potions(self):
                potions = {}
                i = 0
                for key, value in self.inv.items():
                        if value[0] == 4:
                                potions[i] = key
                                i += 1
                return potions
        def remove_item(self, item):
                if self.inv[item][1] > 1:
                        self.inv[item][1] -= 1
                else:
                        self.inv.pop(item)

'''
Dungeon: consecutive battles, looting, resting and some skill checks.
IN
- encounter count (int)
- PCs (list)
- available monsters (list)
- ui (object)
OUT
- dungeon (object)
'''
class Dungeon:
        "Dungeon creation."
        def __init__(self, enc_cnt, pc_list, avail_monsters, ui):
                self.enc_cnt = enc_cnt
                self.pc_list = pc_list
                self.short_rest_cnt = 1
                self.long_rest_cnt = 2
                self.avail_monsters = avail_monsters
        def get_respite_options(self, ui):
                respite_options = {
                        0: "Pass",
                        1: "Short rest",
                        2: "Long rest"
                        }
                if self.short_rest_cnt < 1:
                        respite_options.pop(1)
                if self.long_rest_cnt < 1:
                        respite_options.pop(2)
                ui.push_message("Out of initiative order. What would you like to do?")
                rest = int(ui.get_dict_choice_input(respite_options))
                if rest == 1 and rest in respite_options:
                        self.short_rest(ui)
                elif rest == 2 and rest in respite_options:
                        self.long_rest()
        def short_rest(self, ui):
                for pc in self.pc_list:
                        if not pc.conditions["dead"] and pc.conditions["down"]:
                                wake_up = roll_dice(4, 0, 0, ui)[0]
                                if wake_up == 1:
                                        pc.conditions["down"] = False
                        if pc.hp < pc.max_hp and not pc.conditions["dead"] and not pc.conditions["down"]:
                                while pc.hp < pc.max_hp and pc.hd_cnt != 0:
                                        pc.hp = min(pc.hp + roll_dice(pc.hd, pc.con_mod, 0, ui), pc.max_hp)
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
        def end_dungeon(self, ui):
                ui.push_prompt("GG")
                quit()
        def start_battle(self, enc, allies, enemies, ui):
                ui.push_battle_info("Battle #" + str(enc + 1))
                battle = Battle(allies, enemies, ui)
                return battle

'''
Battle
IN
- allies (list)
- enemies (list)
- ui (object)
OUT
- battle (object)
'''
class Battle:
        "Battle creation."
        def __init__(self, allies, enemies, ui):
                self.allies = allies
                self.enemies = enemies
                self.init_order = []
                self.participants = {}
                self.id_list = {}
                self.current_init = 0
                self.next_init = 1
                self.round = 0
                self.round_end = False
                self.pcs_won = False
                self.pcs_fled = False
                self.foes_fled = False
        def initiative(self, ui):
                for ally in self.allies:
                        if not ally.conditions["dead"] or not ally.conditions["down"]:
                                init_roll = roll_dice(20, ally.init_mod, 0, ui)
                                self.init_order.append([init_roll[0], ally.init_mod, ally.name, ally])
                for enemy in self.enemies:
                        init_roll = roll_dice(20, enemy.init_mod, 0, ui)
                        self.init_order.append([init_roll[0], enemy.init_mod, enemy.name, enemy])
                self.init_order.append([-100, 0 ,"Round End", ""])
                self.init_order.sort(reverse = True)
                self.build_participants()
                self.build_id_list()
                self.get_hp_init_board(ui)
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
        def get_first_init(self, ui):
                self.round += 1
                ui.update_round_info("Round " + str(self.round))
                return self.init_order[0][3]
        def get_next_init(self):
                return self.init_order[self.next_init][3]
        def get_current_init(self, ui):
                ui.update_turn_info(self.init_order[self.current_init][2] + "'s turn")
                return self.init_order[self.current_init][3]
        def set_next_init(self, ui):
                if self.init_order[self.current_init + 1][0] == -100:
                        self.current_init = 0
                        self.next_init = 1
                        self.round += 1
                        ui.update_round_info("Round " + str(self.round))
                else:
                        self.current_init += 1
        def get_targets(self, attacker):
                i = 1
                if attacker in self.allies:
                        enemies_dict = {}
                        for e in self.enemies:
                                if not e.conditions["down"]:
                                        enemies_dict[i] = e.name
                                i += 1
                        return enemies_dict
                elif attacker in self.enemies:
                        allies_dict = {}
                        for a in self.allies:
                                if not a.conditions["down"]:
                                        allies_dict[i] = a.name
                                i += 1
                        return allies_dict
        def get_allies(self, attacker, self_target):
                i = 1
                if attacker in self.enemies:
                        enemies_dict = {}
                        for e in self.enemies:
                                if not e.conditions["dead"]:
                                        enemies_dict[i] = e.name
                                if attacker.name == e.name and self_target == 0:
                                        enemies_dict.pop(i)
                                i += 1
                        return enemies_dict
                elif attacker in self.allies:
                        allies_dict = {}
                        for a in self.allies:
                                if not a.conditions["dead"]:
                                        allies_dict[i] = a.name
                                if attacker.name == a.name and self_target == 0:
                                        allies_dict.pop(i)
                                i += 1
                        return allies_dict
        def get_target_by_name(self, name):
                return self.participants[name]
        def get_char_by_id(self, id):
                return self.id_list[id]
        def get_char_hp_by_name(self, name):
                char = self.participants[name]
                return char.hp, char.max_hp
        def get_hp_init_board(self, ui):
                hp_init_board = []
                for i in range(len(self.participants)):
                        hp_init_board.append([self.init_order[i][0], self.init_order[i][2]])
                ui.update_init_board(hp_init_board)
        def check_round_end(self):
                if self.init_order[self.current_init + 1][0] == -100:
                        self.round_end = True
                if self.init_order[self.current_init - 1][0] == -100:
                        self.round_end = False
        def end(self, ui):
                ui.push_message("Duel has ended. *jingle*\n")
                if self.pcs_fled:
                        ui.push_message(self.allies[0].name + "'s team fled from combat.")
                if self.foes_fled:
                        ui.push_message("Your foes have managed to run away.")
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
                                ui.push_message(winner_team[0].name + "'s team stands victorious: +" + str(loot) + " GP " + "+" + str(xp) + " XP gained.")
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
                if allies_cnt == allies_fled and allies_cnt != allies_down and self.round_end:
                        end = True
                        self.pcs_fled = True
                if enemies_cnt == enemies_fled and enemies_cnt != enemies_down and self.round_end:
                        end = True
                        self.foes_fled = True
                return end

'''
Item compendium: all the weapons, armor and items in the game.
IN
  N/A
OUT
- all items (object)
'''
class AllItems:
        "Item listing."
        def __init__(self):
                # name: [cost, dmg die, dmg die cnt, ench, dmg type, weight, light/heavy, finesse, hands, thrown, monk weapon]
                self.simple_melee_weapons = {
                        "club": [0.1, 4, 1, 0, "b", 2, 1, False, 1, False, True],
                        "dagger": [2, 4, 1, 0, "p", 1, 1, True, 1, True, True],
                        "greatclub": [0.2, 8, 1, 0, "b", 10, 0, False, 2, False, False],
                        "handaxe": [5, 6, 1, 0, "s", 2, 1, False, 1, True, True],
                        "javelin": [0.5, 6, 1, 0, "p", 2, 0, False, 1, True, True],
                        "light hammer": [2, 4, 1, 0, "b", 4, 1, False, 1, False, True],
                        "mace": [5, 6, 1, 0, "b", 4, 0, False, 1, False, True],
                        "quarterstaff": [0.2, 6, 1, 0, "b", 4, 0, False, 1.5, False, True],
                        "sickle": [1, 4, 1, 0, "s", 2, 1, False, 1, False, True],
                        "spear": [1, 6, 1, 0, "p", 3, 0, False, 1.5, True, True]
                        }
                # name: [cost, dmg die, dmg die cnt, ench, dmg type, weight, light/heavy, finesse, hands, load]
                self.simple_ranged_weapons = {
                        "light crossbow": [25, 8, 1, 0, "p", 5, 0, False, 2, True],
                        "dart": [0.05, 4, 1, 0, "p", 0.25, 0, True, 1, False],
                        "shortbow": [25, 6, 1, 0, "p", 2, 0, False, 2, False],
                        "sling": [0.1, 4, 1, 0, "b", 0, 0, False, 1, False]
                        }
                # name: [cost, dmg die, dmg die cnt, ench, dmg type, weight, light/heavy, finesse, hands, thrown, monk weapon]
                self.martial_melee_weapons = {
                        "battleaxe": [10, 8, 1, 0, "s", 4, 0, False, 1.5, False, False],
                        "flail": [10, 8, 1, 0, "b", 2, 0, False, 1, False, False],
                        "glaive": [20, 10, 1, 0, "s", 6, 2, False, 2, False, False],
                        "greataxe": [30, 12, 1, 0, "s", 7, 2, False, 2, False, False],
                        "greatsword": [50, 6, 2, 0, "s", 6, 2, False, 2, False, False],
                        "halberd": [20, 10, 1, 0, "s", 6, 2, False, 2, False, False],
                        "lance": [10, 12, 1, 0, "p", 6, 2, False, 2, False, False],
                        "longsword": [15, 8, 1, 0, "s", 3, 0, False, 1.5, False, False],
                        "maul": [10, 6, 2, 0, "b", 10, 2, False, 2, False, False],
                        "morningstar": [15, 8, 1, 0, "p", 4, 0, False, 1, False, False],
                        "pike": [5, 10, 1, 0, "p", 18, 2, False, 2, False, False],
                        "rapier": [25, 8, 1, 0, "p", 2, 0, True, 1, False, False],
                        "scimitar": [25, 6, 1, 0, "s", 3, 1, True, 1, False, False],
                        "shortsword": [10, 6, 1, 0, "p", 2, 1, True, 1, False, True],
                        "trident": [5, 6, 1, 0, "p", 4, 0, False, 1.5, True, False],
                        "war pick": [5, 8, 1, 0, "p", 2, 0, False, 1, False, False],
                        "warhammer": [15, 8, 1, 0, "b", 2, 0, False, 1.5, False, False],
                        "whip": [2, 4, 1, 0, "s", 3, 0, True, 1, False, False]
                        }
                # name: [cost, dmg die, dmg die cnt, ench, dmg type, weight, light/heavy, finesse, hands, load]
                self.martial_ranged_weapons = {
                        "blowgun": [10, 1, 1, 0, "p", 1, 0, False, 1, True],
                        "hand crossbow": [75, 6, 1, 0, "p", 3, 1, False, 1, True],
                        "heavy crossbow": [50, 10, 1, 0, "p", 18, 2, False, 2, True],
                        "longbow": [50, 8, 1, 0, "p", 2, 2, False, 2, False],
                        "net": [1, 0, 0, 0, "-", 3, 0, False, 1, False]
                        }
                # name: [cost, ac, ench, str, type, stealth disadv, weight]
                self.armors = {
                        "padded": [5, 11, 0, 0, 0, True, 8],
                        "leather": [10, 11, 0, 0, 0, False, 10],
                        "studded leather": [45, 12, 0, 0, 0, False, 13],
                        "hide": [10, 12, 0, 0, 1, False, 12],
                        "chain shirt": [50, 13, 0, 0, 1, False, 20],
                        "scale mail": [50, 14, 0, 0, 1, True, 45],
                        "breastplate": [400, 14, 0, 0, 1, False, 20],
                        "half plate": [750, 15, 0, 0, 1, True, 40],
                        "ring mail": [30, 14, 0, 0, 2, True, 40],
                        "chain mail": [75, 16, 0, 13, 2, True, 55],
                        "splint": [200, 17, 0, 15, 2, True, 60],
                        "plate": [1500, 18, 0, 15, 2, True, 65]
                        }
                # name: [cost, ac, ench, str, type, stealth disadv, weight]
                self.shields = {
                        "shield": [10, 2, 0, 0, 3, False, 6]
                        }
                # name: [cost, die, die cnt, mod, weight]
                self.potions = {
                        "potion of healing": [50, 4, 2, 2, 0.5],
                        "potion of greater healing": [225, 4, 4, 4, 0.5]
                        }
                # all melee weapons
                self.all_melee_weapons = {**self.simple_melee_weapons, **self.martial_melee_weapons}

'''
Beastiary: all the monsters available in this game.
IN
  N/A
OUT
- monster manual (object)
'''
class MonsterManual:
        "Monster listing"
        def __init__(self):
                # monster index {
                #       attributes: [name, str, dex, con, int, wis, cha, hd, hd_mul, multiattack?, # of attacks],
                #       attacks: [[attack 1 name, dmg type, dmg die, dmg die cnt, add dmg dc, dc type, save type, add dmg type, add dmg die, add die cnt, status ailment, obtain DC, escape DC], [attack 2 ...]],
                #       skills: [athletics, acrobatics, perception, investigation, stealth, persuasion],
                #       saving throw modifiers: [str, dex, con, int, wis, cha],
                #       damage resistances/immunities/vulnerabilities: [[dmg type 1, degree], [dmg type 2, degree]],
                #       condition immunities: [condition 1, condition 2 ...]}
                self.monsters = {
                        1: {
                                "attrs": ["Gray Ooze", 12, 6, 16, 1, 6, 2, 8, 3, False, 1],
                                "attacks": [["Pseudopod", "b", 6, 1, 0, "-", 0, "a", 6, 2, "-", 0, 0]],
                                "skills": [0, 0, 0, 0, 2, 0],
                                "stmods": [0, 0, 0, 0, 0, 0],
                                "dmgres": [["a", 1], ["c", 1], ["f", 1], ["s", 1]],
                                "condimm": ["blinded", "charmed", "deafened", "exhaustion", "frightened", "prone"]
                                },
                        2: {
                                "attrs": ["Green Slime", 8, 6, 4, 1, 6, 2, 8, 1, False, 1],
                                "attacks": [["Slime Attack", "b", 4, 1, 10, "dex", 0, "a", 10, 1, "-", 0, 0]],
                                "skills": [0, 0, 0, 0, 2, 0],
                                "stmods": [0, 0, 0, 0, 0, 0],
                                "dmgres": [["a", 1], ["c", 1], ["f", 1], ["s", 1]],
                                "condimm": ["blinded", "charmed", "deafened", "exhaustion", "frightened", "prone"]
                                },
                        3: {
                                "attrs": ["Giant Slug", 15, 10, 13, 1, 9, 2, 8, 5, False, 1],
                                "attacks": [["Tongue", "s", 6, 1, 0, "-", 0, "a", 8, 1, "-", 0, 0]],
                                "skills": [0, 0, 0, 0, 0, 0],
                                "stmods": [0, 0, 0, 0, 0, 0],
                                "dmgres": [],
                                "condimm": []
                                },
                        4: {
                                "attrs": ["Hunter Worm", 15, 9, 17, 1, 7, 3, 6, 5, False, 1],
                                "attacks": [["Bite", "p", 6, 1, 0, "-", 0, "-", 0, 0, "gr/r/worm", 0, 12]],
                                "skills": [0, 0, 0, 0, 0, 0],
                                "stmods": [0, 0, 0, 0, 2, 0],
                                "dmgres": [],
                                "condimm": []
                                },
                        5: {
                                "attrs": ["Ape", 16, 14, 14, 6, 12, 7, 8, 3, True, 2],
                                "attacks": [["Fist", "b", 6, 1, 0, "-", 0, "-", 0, 0, "-", 0, 0], ["Rock", "b", 6, 1, 0, "-", 0, "-", 0, 0, "-", 0, 0]],
                                "skills": [2, 0, 2, 0, 0, 0],
                                "stmods": [0, 0, 0, 0, 2, 0],
                                "dmgres": [],
                                "condimm": []
                                },
                        6: {
                                "attrs": ["Giant Wasp", 10, 14, 10, 1, 10, 3, 8, 3, False, 1],
                                "attacks": [["Sting", "p", 6, 1, 11, "con", 0.5, "v", 0, 0, "p", 0, 0]],
                                "skills": [0, 0, 0, 0, 0, 0],
                                "stmods": [0, 0, 0, 0, 0, 0],
                                "dmgres": [],
                                "condimm": []
                                },
                        7: {
                                "attrs": ["Giant Bat", 15, 16, 11, 2, 12, 6, 10, 4, False, 1],
                                "attacks": [["Bite", "p", 6, 1, 0, "-", 0, "-", 0, 0, "-", 0, 0]],
                                "skills": [0, 0, 0, 0, 0, 0],
                                "stmods": [0, 0, 0, 0, 0, 0],
                                "dmgres": [],
                                "condimm": []
                                }
                        }

'''
Shop: trade weapons, armor and items.
IN
- all items (object)
- ui (object)
OUT
- shop (object)
'''
class Shop:
        "Shop creation."
        def __init__(self, all_items, ui):
                self.all_items = all_items
                self.simple_melee_weapons = self.all_items.simple_melee_weapons
                self.martial_melee_weapons = self.all_items.martial_melee_weapons
                self.simple_ranged_weapons = self.all_items.simple_ranged_weapons
                self.martial_ranged_weapons = self.all_items.martial_ranged_weapons
                self.all_melee_weapons = {**self.simple_melee_weapons, **self.martial_melee_weapons}
                self.all_ranged_weapons = {**self.simple_ranged_weapons, **self.martial_ranged_weapons}
                self.armors = self.all_items.armors
                self.shields = self.all_items.shields
                self.potions = self.all_items.potions
                self.everything = {**self.simple_melee_weapons, **self.martial_melee_weapons, **self.simple_ranged_weapons, **self.martial_ranged_weapons, **self.armors, **self.shields, **self.potions}
                self.shop_list_melee_weapons = []
                self.shop_list_ranged_weapons = []
                self.shop_list_armors = []
                self.shop_list_potions = []
                self.gen_shop_listing()
                self.shop_types = {
                        1: "weaponsmith",
                        2: "bowyer/fletcher",
                        3: "armorer",
                        4: "alchemist"
                        }
        def convert_attributes(self, attr, type):
                attributes_string = ""
                #[cost, dmg die, dmg die cnt, ench, dmg type, weight, light/heavy, finesse, hands, thrown, monk weapon]
                if type == 1:
                        dmg_type = ""
                        if attr[4] == "b":
                                dmg_type = " (bludgeoning)"
                        elif attr[4] == "s":
                                dmg_type = " (slashing)"
                        elif attr[4] == "p":
                                dmg_type = " (piercing)"
                        light_heavy = ""
                        if attr[6] == 1:
                                light_heavy = "light"
                        elif attr[6] == 2:
                                light_heavy = "heavy"
                        finesse = ""
                        if attr[7]:
                                finesse = "finesse"
                        hands = ""
                        if attr[8] == 1:
                                hands = "one-handed"
                        elif attr[8] == 1.5:
                                hands = "versatile"
                        elif attr[8] == 2:
                                hands = "two-handed"
                        monk_weapon = ""
                        if attr[10]:
                                monk_weapon = "monk weapon"
                        properties = hands
                        if light_heavy != "":
                                properties += ", " + light_heavy
                        if finesse != "":
                                properties += ", " + finesse
                        if monk_weapon != "":
                                properties += ", " + monk_weapon
                        attributes_string = "Cost: " + str(attr[0]) + " GP\nWeight: " + str(attr[5]) + " lbs.\n" + \
                                "Damage: " + str(attr[2]) + "d" + str(attr[1]) + "{0:+}".format(attr[3]) + dmg_type + "\n" + \
                                "Properties: " + properties
                #[cost, dmg die, dmg die cnt, ench, dmg type, weight, light/heavy, finesse, hands, load]
                elif type == 2:
                        dmg_type = ""
                        if attr[4] == "b":
                                dmg_type = " (bludgeoning)"
                        elif attr[4] == "s":
                                dmg_type = " (slashing)"
                        elif attr[4] == "p":
                                dmg_type = " (piercing)"
                        light_heavy = ""
                        if attr[6] == 1:
                                light_heavy = "light"
                        elif attr[6] == 2:
                                light_heavy = "heavy"
                        finesse = ""
                        if attr[7]:
                                finesse = "finesse"
                        hands = ""
                        if attr[8] == 1:
                                hands = "one-handed"
                        elif attr[8] == 1.5:
                                hands = "versatile"
                        elif attr[8] == 2:
                                hands = "two-handed"
                        properties = hands
                        if light_heavy != "":
                                properties += ", " + light_heavy
                        if finesse != "":
                                properties += ", " + finesse
                        attributes_string = "Cost: " + str(attr[0]) + " GP\nWeight: " + str(attr[5]) + " lbs.\n" + \
                                "Damage: " + str(attr[2]) + "d" + str(attr[1]) + "{0:+}".format(attr[3]) + dmg_type + "\n" + \
                                "Properties: " + properties
                # name: [cost, ac, ench, str, type, stealth disadv, weight]
                elif type == 3:
                        armor_type = ""
                        if attr[4] == 0:
                                armor_type = "light"
                        elif attr[4] == 1:
                                armor_type = "medium"
                        elif attr[4] == 2:
                                armor_type = "heavy"
                        properties = armor_type
                        restrictions = ""
                        if attr[3] != 0:
                                restrictions = str(attr[3]) + " Strength required" + "\n"
                        if attr[5]:
                                restrictions += "Disadvantage on Stealth checks"
                        if restrictions == "":
                                restrictions = "None"
                        attributes_string = "Cost: " + str(attr[0]) + " GP\nWeight: " + str(attr[6]) + " lbs.\n" + \
                                "Armor: " + str(attr[1]) + "{0:+}".format(attr[2]) + "\n" + \
                                "Properties: " + properties + "\n" + \
                                "Restrictions: \n" + restrictions
                #name: [cost, die, die cnt, mod, weight]
                elif type == 4:
                        attributes_string = "Cost: " + str(attr[0]) + " GP\nWeight: " + str(attr[4]) + " lbs.\n" + \
                                "Heal: " + str(attr[2]) + "d" + str(attr[1]) + "{0:+}".format(attr[3])
                return attributes_string
        def gen_shop_listing(self):
                type = 1
                index = 0
                for _ in range(math.floor(len(self.simple_melee_weapons) / 3)):
                        index += 1
                        random_choice = random.choice(list(self.simple_melee_weapons.keys()))
                        attributes = self.convert_attributes(self.simple_melee_weapons[random_choice], type)
                        self.shop_list_melee_weapons.append([random_choice, index, attributes])
                for _ in range(math.floor(len(self.martial_melee_weapons) / 3)):
                        index += 1
                        random_choice = random.choice(list(self.martial_melee_weapons.keys()))
                        attributes = self.convert_attributes(self.martial_melee_weapons[random_choice], type)
                        self.shop_list_melee_weapons.append([random_choice, index, attributes])
                type = 2
                index = 0
                for _ in range(math.floor(len(self.simple_ranged_weapons) / 2)):
                        index += 1
                        random_choice = random.choice(list(self.simple_ranged_weapons.keys()))
                        attributes = self.convert_attributes(self.simple_ranged_weapons[random_choice], type)
                        self.shop_list_ranged_weapons.append([random_choice, index, attributes])
                for _ in range(math.floor(len(self.martial_ranged_weapons) / 2)):
                        index += 1
                        random_choice = random.choice(list(self.martial_ranged_weapons.keys()))
                        attributes = self.convert_attributes(self.martial_ranged_weapons[random_choice], type)
                        self.shop_list_ranged_weapons.append([random_choice, index, attributes])
                type = 3
                index = 0
                for _ in range(math.floor(len(self.armors) / 2)):
                        index += 1
                        random_choice = random.choice(list(self.armors.keys()))
                        attributes = self.convert_attributes(self.armors[random_choice], type)
                        self.shop_list_armors.append([random_choice, index, attributes])
                for _ in range(math.ceil(len(self.shields) / 2)):
                        index += 1
                        random_choice = random.choice(list(self.shields.keys()))
                        attributes = self.convert_attributes(self.shields[random_choice], type)
                        self.shop_list_armors.append([random_choice, index, attributes])
                type = 4
                index = 0
                for _ in range(len(self.potions)):
                        index += 1
                        random_choice = random.choice(list(self.potions.keys()))
                        attributes = self.convert_attributes(self.potions[random_choice], type)
                        self.shop_list_potions.append([random_choice, index, attributes])
        def shopping_flow(self, char, ui):
                done_shopping = False
                while done_shopping == False:
                        for i in range(4):
                                i += 1
                                exit_shop = False
                                while not exit_shop:
                                        choice = self.shop_purchase(i, char, ui)
                                        if choice != -1:
                                                ui.push_message("Take another look?")
                                                if int(ui.get_binary_input()) == 0:
                                                        exit_shop = True
                                                        ui.push_prompt("Ola Kala, bye.\n")
                                        else:
                                                exit_shop = True
                                                ui.push_prompt("Ola Kala, bye.\n")
                        ui.push_message("Another round?")
                        finished = int(ui.get_binary_input())
                        if finished == 0:
                                done_shopping = True
                                ui.push_prompt(char.name + " has left the marketplace.\n")
        def shop_purchase(self, type, char, ui):
                ui.push_message(self.shop_types[type].capitalize())
                ui.push_message(random.choice(["Looking to protect yourself, or deal some damage?", "Welcome to my shop. Take a look!", "Tabaxi has wares if you have the coin.", "Hail to you champion.", "What's up, boy? We guarantee all items to be in good condition.", "Some may call this junk. Me, I call them treasures.", "Approach and let's trade."]))
                # price and weight positions may need to be adjusted across different types of items (dictionary)
                price_pos = 0
                weight_pos = 0
                # melee weaponsmith
                if type == 1:
                        shop_list = self.shop_list_melee_weapons
                        item_list = {**self.simple_melee_weapons, **self.martial_melee_weapons}
                        weight_pos = 5
                        ui.push_message("What do you need?")
                        purchase_choice = int(ui.get_list_choice_input(shop_list))
                # ranged weaponsmith
                elif type == 2:
                        shop_list = self.shop_list_ranged_weapons
                        item_list = {**self.simple_ranged_weapons, **self.martial_ranged_weapons}
                        weight_pos = 5
                        ui.push_message("What do you need?")
                        purchase_choice = int(ui.get_list_choice_input(shop_list))
                # armorer
                elif type == 3:
                        shop_list = self.shop_list_armors
                        item_list = {**self.armors, **self.shields}
                        weight_pos = 6
                        ui.push_message("What do you need?")
                        purchase_choice = int(ui.get_list_choice_input(shop_list))
                # alchemist
                elif type == 4:
                        shop_list = self.shop_list_potions
                        item_list = self.potions
                        weight_pos = 4
                        ui.push_message("Name your poison!")
                        purchase_choice = int(ui.get_list_choice_input(shop_list))
                if purchase_choice != -1:
                        purchased_item = shop_list[purchase_choice - 1][0]
                        purchased_item_price = item_list[purchased_item][price_pos]
                        purchased_item_weight = item_list[purchased_item][weight_pos]
                        ui.push_message("You sure you want the " + purchased_item + " (" + str(purchased_item_price) + " GP)?")
                        if int(ui.get_binary_input()) == 1:
                                if char.gold >= purchased_item_price:
                                        if char.carry + purchased_item_weight > char.max_carry:
                                                ui.push_prompt("You cannot purchase the " + purchased_item + ". Get rid of something first.")
                                        else:
                                                char.inv.add_item(purchased_item, type)
                                                char.gold -= purchased_item_price
                                                char.gold = round(char.gold, 2)
                                                char.carry += purchased_item_weight
                                                char.carry = round(char.carry, 2)
                                                shop_list[purchase_choice - 1][0] = "sold"
                                                ui.push_prompt("You bought the " + purchased_item + " for " + str(purchased_item_price) + " GP.")
                                                ui.update_status()
                                                if type != 4:
                                                        ui.push_message("Wanna equip the " + purchased_item + "?")
                                                        if int(ui.get_binary_input()) == 1:
                                                                char.equip(1, purchased_item, type, item_list, self.all_items, self.everything, self.all_melee_weapons, self.all_ranged_weapons, ui)
                                else:
                                        ui.push_prompt(random.choice(["Not enough gold.", "You've not enough gold coins."]))
                        else:
                                ui.push_prompt("Ah, you've changed your mind, I see...")
                elif purchase_choice == -1:
                        ui.push_prompt("Oh, not interested, huh?")
                return purchase_choice

'''
AI a.k.a. artificial intelligence for DM gameplay.
IN
  N/A
OUT
- ai (object)
'''
class AI:
        "Artificial intelligence for enemy activities."
        def __init__(self):
                self.diff = -1
                self.diff_lvls = {
                        0: "retargeted",
                        1: "noob",
                        2: "minmaxer"
                        }
        def get_diff_lvls(self):
                return self.diff_lvls
        def set_diff_lvl(self, diff):
                self.diff = diff
        def choose(self, char, choices, type):
                choice = 0
                list_of_choices = list(choices)
                if self.diff == 0:
                        choice = random.choice(list_of_choices)
                elif self.diff == 1:
                        if type == 1:
                                if char.battle_menu_options[1][1] < 1:
                                        choice = 4
                                else:
                                        choice = 1
                        elif type == 2:
                                choice = 1
                        elif type == 0:
                                choice = random.choice(list_of_choices)
                elif self.diff == 2:
                        pass
                return choice

# Utilities
def roll_dice(dice, mod, type, ui):
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
        #ui.push_message("Dice roll: " + str(roll) + " + " + str(mod))
        return roll + mod, crit

def random_str(length):
        chars = string.ascii_lowercase
        return "".join(random.choice(chars) for _ in range(length))

# Combat related
def act(attacker, act_choice, battle, all_items, ui):
        # character is not unconscious = can act on its turn
        if not attacker.conditions["down"]:
                # actions
                if act_choice == 1:
                        attacker.battle_menu_options[1][1] -= 1
                        if not attacker.npc:
                                action = int(ui.get_dict_choice_input(attacker.actions))
                        else:
                                action = ai.choose(attacker, attacker.actions.keys(), 2)
                        # attack action
                        if action in attacker.actions and action == 1:
                                for _ in range(attacker.attacks):
                                        roll_mod = 0
                                        targets = battle.get_targets(attacker)
                                        if len(targets) != 0:
                                                defender = target_selector(attacker, battle, targets, ui)
                                                roll_mod = get_adv_disadv(attacker, defender, ui)
                                                attack(attacker, defender, 1, roll_mod, battle, all_items, ui)
                                        else:
                                                ui.push_prompt("Noone to attack.")
                                if attacker.char_class == 3:
                                        attacker.did_attack = True
                        # dodge action
                        elif action in attacker.actions and action == 2:
                                attacker.conditions["dodge"] = True
                                ui.push_prompt(attacker.name + " is taking a defensive stance.")
                                if attacker.bonus_attack:
                                        attacker.bonus_actions.pop(1)
                        # disengage action
                        elif action in attacker.actions and action == 3:
                                attacker.conditions["flee"] = True
                                ui.push_prompt(attacker.name + " has disengaged and is about to flee from combat.")
                                if attacker.bonus_attack:
                                        attacker.bonus_actions.pop(1)
                        # shove action
                        elif action in attacker.actions and action == 4:
                                targets = battle.get_targets(attacker)
                                if len(targets) != 0:
                                        defender = target_selector(attacker, battle, targets, ui)
                                        for _ in range(attacker.attacks):
                                                shove(attacker, defender, ui)
                                        if attacker.bonus_attack:
                                                attacker.bonus_actions.pop(1)
                                else:
                                        ui.push_prompt("Noone to shove.")
                                if attacker.char_class == 3:
                                        attacker.did_attack = True
                        # grapple action
                        elif action in attacker.actions and action == 5:
                                targets = battle.get_targets(attacker)
                                if len(targets) != 0:
                                        defender = target_selector(attacker, battle, targets, ui)
                                        roll_mod = get_adv_disadv(attacker, defender, ui)
                                        for _ in range(attacker.attacks):
                                                grapple(attacker, defender, roll_mod, all_items, ui)
                                        if attacker.bonus_attack:
                                                attacker.bonus_actions.pop(1)
                                else:
                                        ui.push_prompt("Noone to grapple.")
                                if attacker.char_class == 3:
                                        attacker.did_attack = True
                        # use action to escape a grapple
                        elif action in attacker.actions and action == 6:
                                escape_grapple(attacker, battle, all_items, ui)
                                if attacker.bonus_attack:
                                        attacker.bonus_actions.pop(1)
                                if attacker.char_class == 3:
                                        attacker.did_attack = True
                        # lay on hands (paladin only)
                        elif action in attacker.actions and action == 7:
                                allies = battle.get_allies(attacker, 1)
                                receiver = target_selector(attacker, battle, allies, ui)
                                receiver_max_healable = receiver.max_hp - max(0, receiver.hp)
                                lay_on_hands_heal = amount_selector(attacker.lay_on_hands_pool, receiver_max_healable, ui)
                                actual_heal = receiver.receive_healing(attacker, lay_on_hands_heal, ui)
                                attacker.lay_on_hands_pool -= actual_heal
                                if attacker.lay_on_hands_pool <= 0:
                                        attacker.actions.pop(action)
                                        attacker.lay_on_hands_pool = 0
                        # help action
                        elif action in attacker.actions and action == 8:
                                allies = battle.get_allies(attacker, 0)
                                receiver = target_selector(attacker, battle, allies, ui)
                                receiver.conditions["helped"] = True
                                receiver.help_adv = True
                                attacker.helpee = receiver.player_id
                                if attacker.bonus_attack:
                                        attacker.bonus_actions.pop(1)
                        # use potion action
                        elif action in attacker.actions and action == 9:
                                avail_potions = attacker.inv.get_potions()
                                potions = []
                                potions_for_choice = []
                                for key, value in avail_potions.items():
                                        potions_for_choice.append([value, key, "%sd%s+%s" % (all_items.potions[value][2], all_items.potions[value][1], all_items.potions[value][3])])
                                        potions.append([value, key, all_items.potions[value]])
                                potion_choice = int(ui.get_list_choice_input(potions_for_choice))
                                if potion_choice != -1:
                                        allies = battle.get_allies(attacker, 1)
                                        receiver = target_selector(attacker, battle, allies, ui)
                                        receiver_max_healable = receiver.max_hp - max(0, receiver.hp)
                                        potion_heal = 0
                                        potion_stats = all_items.potions[avail_potions[potion_choice]]
                                        for _ in range(potion_stats[2]):
                                                potion_heal += roll_dice(potion_stats[1], 0, 0, ui)[0]
                                        potion_heal += potion_stats[3]
                                        actual_heal = receiver.receive_healing(attacker, potion_heal, ui)
                                        attacker.inv.remove_item(avail_potions[potion_choice])
                                        attacker.carry -= all_items.potions[value][4]
                                else:
                                        attacker.battle_menu_options[1][1] += 1
                        # back to battle menu
                        elif action in attacker.actions and action == 0:
                                attacker.battle_menu_options[1][1] += 1
                # bonus actions
                elif act_choice == 2:
                        attacker.battle_menu_options[2][1] -= 1
                        if not attacker.npc:
                                bonus_action = int(ui.get_dict_choice_input(attacker.bonus_actions))
                        else:
                                bonus_action = ai.choose(attacker, attacker.bonus_actions.keys(), 3)
                        # attack bonus action
                        if bonus_action in attacker.bonus_actions and bonus_action == 1:
                                if attacker.battle_menu_options[1][1] < 1:
                                        targets = battle.get_targets(attacker)
                                        if len(targets) != 0:
                                                defender = target_selector(attacker, battle, targets, ui)
                                                roll_mod = get_adv_disadv(attacker, defender, ui)
                                                attack(attacker, defender, 2, roll_mod, battle, all_items, ui)
                                        else:
                                                ui.push_prompt("Noone to attack.")
                                        if attacker.char_class == 3:
                                                attacker.did_attack = True
                                else:
                                        ui.push_prompt("Must use an attack action first.")
                                        attacker.battle_menu_options[2][1] += 1
                        # second wind bonus action (fighter only)
                        elif bonus_action in attacker.bonus_actions and bonus_action == 2:
                                current_hp = attacker.hp
                                second_wind_heal = roll_dice(10, attacker.level, 0, ui)[0]
                                attacker.hp = min(attacker.hp + second_wind_heal, attacker.max_hp)
                                if current_hp + second_wind_heal > attacker.max_hp:
                                        actual_heal = second_wind_heal - ((current_hp + second_wind_heal) - attacker.max_hp)
                                else:
                                        actual_heal = second_wind_heal
                                ui.update_status()
                                ui.push_prompt(attacker.name + " healed " + str(actual_heal) + " HP.")
                                attacker.second_wind = False
                                attacker.bonus_actions.pop(bonus_action)
                        # rage bonus action (barbarian only)
                        elif bonus_action in attacker.bonus_actions and bonus_action == 3:
                                if attacker.raging == False:
                                        attacker.rage_on(all_items, ui)
                                else:
                                        attacker.rage_off(all_items, ui)
                        # disengage bonus action (rogue only)
                        elif bonus_action in attacker.bonus_actions and bonus_action == 4:
                                attacker.conditions["flee"] = True
                                ui.push_prompt(attacker.name + " has disengaged and is about to flee from combat.")
                        # back to battle menu
                        elif bonus_action in attacker.bonus_actions and bonus_action == 0:
                                attacker.battle_menu_options[2][1] += 1
                # specials
                elif act_choice == 3:
                        if not attacker.npc:
                                special = int(ui.get_dict_choice_input(attacker.specials))
                        else:
                                special = ai.choose(attacker, attacker.specials.keys(), 4)
                        if special in attacker.specials and special == 1:
                                pass
                        # back to main menu
                        elif special in attacker.specials and special == 0:
                                pass
                # end turn
                elif act_choice == 4:
                        attacker.turn_done = True
                        ui.clear_message()
        # character is unconscious = death saving throw or stabilized (incapacitated)
        elif attacker.conditions["down"] and not attacker.conditions["dead"] and attacker.death_st_success < 3:
                attacker.deaths_door(ui)
                attacker.turn_done = True
        elif attacker.conditions["down"] and attacker.conditions["dead"]:
                ui.push_prompt(attacker.name + " is dead.")
                attacker.turn_done = True
        elif attacker.conditions["down"] and not attacker.conditions["dead"] and attacker.death_st_success == 3:
                ui.push_prompt(attacker.name + " is taking a rest.")
                attacker.turn_done = True

def get_adv_disadv(source, target, ui):
        roll_mod = 0
        if target.conditions["prone"] and not source.ranged:
                roll_mod += 1
        if target.conditions["prone"] and source.ranged:
                roll_mod -= 1
        elif target.conditions["dodge"]:
                roll_mod -= 1
        if source.help_adv:
                roll_mod += 1
                stop_help(source.player_id)
        if source.attack_adv:
                roll_mod += 1
        elif source.attack_disadv:
                roll_mod -= 1
        if roll_mod < -1:
                roll_mod = -1
        elif roll_mod > 1:
                roll_mod = 1
        if roll_mod == 1:
                ui.push_message("Rolling with advantage.")
        elif roll_mod == -1:
                ui.push_message("Rolling with disadvantage.")
        elif roll_mod == 0:
                ui.push_message("Straight roll.")
        return roll_mod

def target_selector(source, battle, targets, ui):
        if not source.npc:
                ui.push_message("Choose a target.")
        if not source.npc:
                target_choice = int(ui.get_dict_choice_input(targets))
        else:
                target_choice = ai.choose(source, targets.keys(), 0)
        if target_choice != -1:
                return battle.get_target_by_name(targets[target_choice])
        else:
                return None

def amount_selector(pool, max_avail, ui):
        ui.push_message("Heal for how much?")
        amount = int(ui.get_amount(pool, max_avail))
        return amount

def attack(source, target, type, adv_disadv, battle, all_items, ui):
        str_att_mod = 0
        dex_att_mod = 0
        str_dmg_mod = 0
        dex_dmg_mod = 0
        ench = 0
        # main hand attack
        if type == 1:
                ui.push_message(source.name + " attacks " + target.name + " with " + source.eq_weapon_main + ".")
                str_att_mod = source.main_str_att_mod
                dex_att_mod = source.main_dex_att_mod
                str_dmg_mod = source.main_str_dmg_mod
                dex_dmg_mod = source.main_dex_dmg_mod
                ench = source.ench_main
        # off-hand attack
        elif type == 2:
                ui.push_message(source.name + " attacks " + target.name + " with " + source.eq_weapon_offhand + ".")
                str_att_mod = source.off_str_att_mod
                dex_att_mod = source.off_dex_att_mod
                str_dmg_mod = source.off_str_dmg_mod
                dex_dmg_mod = source.off_dex_dmg_mod
                ench = source.ench_off
        # attack and damage modifier definition
        # ranged weapons use DEX
        if source.ranged:
                att_mod = dex_att_mod + ench
                dmg_mod = dex_dmg_mod + ench
        # monk weapons, monk unarmed strikes and finesse weapons use either STR or DEX (whichever is higher)
        elif type == 1 and source.eq_weapon_main_finesse:
                att_mod = max(dex_att_mod, str_att_mod) + ench
                dmg_mod = max(dex_dmg_mod, str_dmg_mod) + ench
        elif type == 2 and source.eq_weapon_offhand_finesse:
                att_mod = max(dex_att_mod, str_att_mod) + ench
                dmg_mod = max(dex_dmg_mod, str_dmg_mod) + ench
        # melee weapons and non-monk unarmed strikes use STR
        else:
                att_mod = str_att_mod + ench
                dmg_mod = str_dmg_mod + ench
        # monks and martial classes with two weapon fighting style add the damage modifier to their bonus attack, everyone else does not, unless it's negative
        if type == 2 and source.offhand_dmg_mod:
                dmg_mod = min(0, max(dex_dmg_mod, str_dmg_mod)) + ench
        # to hit calculation
        to_hit = roll_dice(20, att_mod, adv_disadv, ui)
        crit = to_hit[1]
        if crit == 1:
                to_hit_conf = roll_dice(20, att_mod, adv_disadv, ui)
                to_hit_conf_flag = False
                if to_hit_conf[0] < target.ac and to_hit_conf[1] != 1:
                        crit = 0
                else:
                        to_hit_conf_flag = True
        # hit -> calculate damage
        dmg = 0
        if to_hit[0] >= target.ac or crit == 1:
                # sneak attack
                # rogue only extra dmg once per round if certain conditions are met (adv on attack with finesse or ranged weapon or target is distracted by ally and no disadv on attack roll)
                if source.char_class == 4:
                        allies = battle.get_allies(attacker, 1)
                        # check for sneak attack conditions
                        distraction = False
                        if len(allies) > 1:
                                for value in allies.values():
                                        if not battle.participants[value].conditions["down"]:
                                                distraction = True
                        if (attacker.attack_adv or attacker.help_adv or (distraction and not attacker.attack_disadv)) and ((type == 1 and attacker.eq_weapon_main_finesse) or (type == 2 and attacker.eq_weapon_offhand_finesse) or attacker.ranged):
                                ui.push_message("Apply sneak attack?")
                                if int(ui.get_binary_input()) == 1:
                                        attacker.sneak_attack = True
                dmg_result = calc_dmg(source, crit, dmg_mod, type, all_items, ui)
                dmg = dmg_result[0]
                dmg_type = dmg_result[1]
                if dmg_type == "b":
                        dmg_type = "bludgeoning"
                elif dmg_type == "p":
                        dmg_type = "piercing"
                elif dmg_type == "s":
                        dmg_type = "slashing"
                elif dmg_type == "mb":
                        dmg_type = "magical bludgeoning"
                elif dmg_type == "mp":
                        dmg_type = "magical piercing"
                elif dmg_type == "ms":
                        dmg_type = "magical slashing"
                # critical threat and confirmation for critical damage (double damage dice) (D&D 3.5 style)
                if crit == 0:
                        ui.push_message("Hit: " + str(to_hit[0]) + " vs AC " + str(target.ac) + " \nDamage: " + str(dmg) + " (" + dmg_type + ")\n")
                elif crit == 1:
                        ui.push_message("Critical hit: " + str(to_hit[0]) + " vs AC " + str(target.ac))
                        ui.push_message("Critical hit confirmation: " + str(to_hit_conf[0]) + " vs AC " + str(target.ac))
                        if not to_hit_conf_flag:
                                ui.push_message("Damage: " + str(dmg) + " (" + dmg_type + ")\n")
                        else:
                                ui.push_message("2x dice damage: " + str(dmg) + " (" + dmg_type + ")\n")
                if target.char_class == 3:
                        target.got_attacked = True
                        if target.raging and dmg_type in ["piercing", "bludgeoning", "slashing", "magical piercing", "magical bludgeoning", "magical slashing"]:
                                dmg = math.floor(dmg / 2)
                                ui.push_message(target.name + " didn't take as much damage as expected.")
                target.hp -= dmg
                ui.update_status()
        # miss
        elif to_hit[0] < target.ac or crit == -1:
                if crit == 0:
                        ui.push_message("Miss: " + str(to_hit[0]) + " vs AC " + str(target.ac) + "\n")
                elif crit == -1:
                        ui.push_message("Critical miss\n")
        # check if target got downed
        if target.hp <= 0:
                target.conditions["down"] = True
                ui.push_message(target.name + " is down.")
                if target.grappling != "":
                        release_grapple(target, battle, all_items)
                if target.char_class == 3:
                        if target.raging == True:
                                target.got_attacked = True
                if target.max_hp * -1 >= target.hp:
                        ui.push_message("Death blow! " + target.name + " falls dead. RIP")
                        target.conditions["dead"] = True
        ui.push_prompt("")

def stop_help(target_id):
        helpee = battle.get_char_by_id(target_id)
        helpee.conditions["helped"] = False
        helpee.help_adv = False

def shove(source, target, ui):
        att_check = roll_dice(20, source.skills["athletics"][0] + source.skills["athletics"][1], 0, ui)[0]
        def_check = roll_dice(20, max(target.skills["athletics"][0] + target.skills["athletics"][1], target.skills["acrobatics"][0] + target.skills["acrobatics"][1]), 0, ui)[0]
        ui.push_message("Contested check: " + str(att_check) + " vs " + str(def_check))
        if att_check > def_check:
                target.conditions["prone"] = True
                if target.char_class in [1, 4, 5, 6] or (target.char_class == 2 and target.level < 2) or (target.char_class == 3 and target.level < 5):
                        target.actions.pop(3)
                ui.push_prompt(target.name + " was knocked prone.")
        else:
                ui.push_prompt("Shove attempt failed.")

def grapple(source, target, adv_disadv, all_items, ui):
        att_mod = max(source.off_dex_att_mod, source.off_str_att_mod)
        to_hit = roll_dice(20, att_mod, adv_disadv, ui)
        ui.push_message("Hit: " + str(to_hit[0]) + " vs AC " + str(target.ac) + "\n")
        if to_hit[0] > target.ac:
                target.conditions["grappled"] = True
                target.grappled_by = source.player_id
                source.grappling = target.player_id
                target.actions.pop(3)
                target.actions[6] = "escape grapple"
                ui.push_prompt(target.name + " is grappled by " + source.name + ".")
                if source.eq_weapon_main != "unarmed strike":
                        if all_items.all_melee_weapons[source.eq_weapon_main][8] == 2:
                                source.actions.pop(1)
                        elif all_items.all_melee_weapons[source.eq_weapon_main][8] == 1.5:
                                source.dmg_die_main -= 2
        else:
                ui.push_prompt(source.name + " failed to grapple " + target.name + ".")

def release_grapple(grappler, battle, all_items):
        grapplee = battle.get_char_by_id(grappler.grappling)
        grapplee.grappled_by = ""
        grapplee.conditions["grappled"] = False
        grappler.grappling = ""
        grapplee.actions[3] = "disengage"
        grapplee.actions.pop(6)
        if all_items[grappler.eq_weapon_main][8] == 2:
                grappler.actions[1] = "attack"
        elif all_items[grappler.eq_weapon_main][8] == 1.5:
                grappler.dmg_die_main += 2

def escape_grapple(grapplee, battle, all_items, ui):
        grappler = battle.get_char_by_id(grapplee.grappled_by)
        att_check = roll_dice(20, max(grapplee.skills["athletics"][0] + grapplee.skills["athletics"][1], grapplee.skills["acrobatics"][0] + grapplee.skills["acrobatics"][1]), 0, ui)[0]
        def_check = roll_dice(20, grappler.skills["athletics"][0] + grappler.skills["athletics"][1], 0, ui)[0]
        ui.push_message("Contested check: " + str(att_check) + " vs " + str(def_check))
        if att_check > def_check:
                grapplee.grappled_by = ""
                grapplee.conditions["grappled"] = False
                grappler.grappling = ""
                grapplee.actions[3] = "disengage"
                grapplee.actions.pop(6)
                if all_items[grappler.eq_weapon_main][8] == 2:
                        grappler.actions[1] = "attack"
                if all_items[grappler.eq_weapon_main][8] == 1.5:
                        grappler.dmg_die_main += 2
                ui.push_prompt(grapplee.name + " has escaped the grapple.")
        else:
                ui.push_prompt("Grapple escape attempt failed.")

def calc_dmg(source, crit, dmg_mod, type, all_items, ui):
        dmg = 0
        die_cnt = 1
        dmg_die = 1
        dmg_type = ""
        # action attack
        if type == 1:
                die_cnt = source.dmg_die_cnt_main
                dmg_die = source.dmg_die_main
                dmg_type = source.dmg_die_type_main
        # bonus action attack
        if type == 2:
                die_cnt = source.dmg_die_cnt_off
                dmg_die = source.dmg_die_off
                dmg_type = source.dmg_die_type_off
        # reaction attack
        if type == 3:
                die_cnt = source.dmg_die_cnt_main
                dmg_die = source.dmg_die_main
                dmg_type = source.dmg_die_type_main
        if crit == 1:
                die_cnt *= 2
        else:
                die_cnt *= 1
        for _ in range(die_cnt):
                dmg_roll = roll_dice(dmg_die, 0, 0, ui)[0]
                dmg_reroll = 0
                if (dmg_roll == 1 or dmg_roll == 2) and source.reroll_dmg:
                        dmg_reroll = roll_dice(dmg_die, 0, 0, ui)[0]
                dmg += max(dmg_roll, dmg_reroll)
        dmg += dmg_mod
        # sneak attack damage
        if source.char_class == 4:
                die_cnt = source.sneak_damage[1]
                if crit == 1:
                        die_cnt *= 2
                else:
                        die_cnt *= 1
                if source.sneak_attack:
                        for _ in range(die_cnt):
                                dmg += roll_dice(source.sneak_damage[0], 0, 0, ui)[0]
                        source.sneak_attack = False
        # the minimum damage one can deal is 0
        if dmg < 0:
                dmg = 0
        return dmg, dmg_type

# Character initialization
def gen_stats(ui):
        stre = 0
        dex = 0
        con = 0
        inte = 0
        wis = 0
        cha = 0
        roll = 0
        min = 6
        for _ in range(4):
                roll = roll_dice(6, 0, 0, ui)[0]
                if roll < min:
                        min = roll
                stre += roll
        stre -= min
        min = 6
        for _ in range(4):
                roll = roll_dice(6, 0, 0, ui)[0]
                if roll < min:
                        min = roll
                dex += roll
        dex -= min
        min = 6
        for _ in range(4):
                roll = roll_dice(6, 0, 0, ui)[0]
                if roll < min:
                        min = roll
                con += roll
        con -= min
        min = 6
        for _ in range(4):
                roll = roll_dice(6, 0, 0, ui)[0]
                if roll < min:
                        min = roll
                inte += roll
        inte -= min
        min = 6
        for _ in range(4):
                roll = roll_dice(6, 0, 0, ui)[0]
                if roll < min:
                        min = roll
                wis += roll
        wis -= min
        min = 6
        for _ in range(4):
                roll = roll_dice(6, 0, 0, ui)[0]
                if roll < min:
                        min = roll
                cha += roll
        cha -= min
        ui.push_message("============")
        ui.push_message("Rolled stats\n" + "Strength: " + str(stre) + "\n" + "Dexterity: " + str(dex) + "\n" + "Constitution: " + str(con) + "\n" + "Intelligence: " + str(inte) + "\n" + "Wisdom: " + str(wis) + "\n" + "Charisma: " + str(cha) + "\n")
        return stre, dex, con, inte, wis, cha

def gen_race(stats, ui):
        str_stat = stats[0]
        dex_stat = stats[1]
        con_stat = stats[2]
        int_stat = stats[3]
        wis_stat = stats[4]
        cha_stat = stats[5]
        races = {
                1: "human",
                2: "halfling",
                3: "dwarf",
                4: "gnome",
                5: "elf",
                6: "half-orc"
                }
        ui.push_message("Choose your race.")
        race_choice = int(ui.get_dict_choice_input_racial(races))
        if race_choice == 1:
                str_stat += 1
                dex_stat += 1
                con_stat += 1
                int_stat += 1
                wis_stat += 1
                cha_stat += 1
        elif race_choice == 2:
                dex_stat += 2
        elif race_choice == 3:
                con_stat += 2
        elif race_choice == 4:
                int_stat += 2
        elif race_choice == 5:
                dex_stat += 2
        elif race_choice == 6:
                str_stat += 2
                con_stat += 1
        ui.push_message("============")
        ui.push_message("Stats with racial traits\n" + "Strength: " + str(str_stat) + "\n" + "Dexterity: " + str(dex_stat) + "\n" + "Constitution: " + str(con_stat) + "\n" + "Intelligence: " + \
                str(int_stat) + "\n" + "Wisdom: " + str(wis_stat) + "\n" + "Charisma: " + str(cha_stat) + "\n")
        subraces = {
                11: "vanilla",
                21: "lightfoot",
                22: "stout",
                23: "ghostwise",
                31: "hill",
                32: "mountain",
                33: "duergar",
                41: "forest",
                42: "rock",
                43: "svirfneblin",
                51: "high",
                52: "wood",
                53: "drow",
                61: "vanilla"
                }
        for sr in subraces.copy():
                if race_choice != math.floor(sr / 10):
                        subraces.pop(sr)
        ui.push_message("Choose your subrace.")
        subrace_choice = int(ui.get_dict_choice_input_racial(subraces))
        if subrace_choice == 11:
                pass
        elif subrace_choice == 21:
                cha_stat += 1
        elif subrace_choice == 22:
                con_stat += 1
        elif subrace_choice == 23:
                wis_stat += 1
        elif subrace_choice == 31:
                wis_stat += 1
        elif subrace_choice == 32:
                str_stat += 2
        elif subrace_choice == 33:
                str_stat += 1
        elif subrace_choice == 41:
                dex_stat += 1
        elif subrace_choice == 42:
                con_stat += 1
        elif subrace_choice == 43:
                dex_stat += 1
        elif subrace_choice == 51:
                int_stat += 1
        elif subrace_choice == 52:
                wis_stat += 1
        elif subrace_choice == 53:
                cha_stat += 1
        elif subrace_choice == 61:
                pass
        ui.push_message("============")
        ui.push_message("Stats with subracial traits\n" + "Strength: " + str(str_stat) + "\n" + "Dexterity: " + str(dex_stat) + "\n" + "Constitution: " + str(con_stat) + "\n" + "Intelligence: " + \
                str(int_stat) + "\n" + "Wisdom: " + str(wis_stat) + "\n" + "Charisma: " + str(cha_stat) + "\n")
        return race_choice, subrace_choice, [str_stat, dex_stat, con_stat, int_stat, wis_stat, cha_stat]

def gen_char(name, starting_level, all_items, npc, ui):
        need_stat_reroll = True
        while need_stat_reroll:
                classes = {
                        1: "fighter",
                        2: "monk",
                        3: "barbarian",
                        4: "rogue",
                        5: "paladin",
                        6: "ranger"
                        }
                stats = gen_stats(ui)
                stats_post_race = gen_race(stats, ui)
                str_stat = stats_post_race[2][0]
                dex_stat = stats_post_race[2][1]
                con_stat = stats_post_race[2][2]
                int_stat = stats_post_race[2][3]
                wis_stat = stats_post_race[2][4]
                cha_stat = stats_post_race[2][5]
                race = stats_post_race[0]
                subrace = stats_post_race[1]
                # stat restrictions
                # fighter
                if str_stat < 13 and dex_stat < 13:
                        classes.pop(1)
                # monk
                if dex_stat < 13 or wis_stat < 13:
                        classes.pop(2)
                # barbarian
                if str_stat < 13:
                        classes.pop(3)
                # rogue
                if dex_stat < 13:
                        classes.pop(4)
                # paladin
                if str_stat < 13 or cha_stat < 13:
                        classes.pop(5)
                # ranger
                if dex_stat < 13 or wis_stat < 13:
                        classes.pop(6)
                if classes:
                        need_stat_reroll = False
                elif not classes:
                        need_stat_reroll = True
                        ui.clear_message()
                        ui.push_message("Rerolling stats.")
        ui.push_message("Choose your class.")
        class_choice = int(ui.get_dict_choice_input(classes))
        if class_choice == 1:
                char = Fighter(name, str_stat, dex_stat, con_stat, int_stat, wis_stat, cha_stat, starting_level, race, subrace, npc, ui)
        if class_choice == 2:
                char = Monk(name, str_stat, dex_stat, con_stat, int_stat, wis_stat, cha_stat, starting_level, race, subrace, npc, ui)
        if class_choice == 3:
                char = Barbarian(name, str_stat, dex_stat, con_stat, int_stat, wis_stat, cha_stat, starting_level, race, subrace, npc, ui)
        if class_choice == 4:
                char = Rogue(name, str_stat, dex_stat, con_stat, int_stat, wis_stat, cha_stat, starting_level, race, subrace, npc, ui)
        if class_choice == 5:
                char = Paladin(name, str_stat, dex_stat, con_stat, int_stat, wis_stat, cha_stat, starting_level, race, subrace, npc, ui)
        if class_choice == 6:
                char = Ranger(name, str_stat, dex_stat, con_stat, int_stat, wis_stat, cha_stat, starting_level, race, subrace, npc, ui)
        ui.create_status(char)
        char.gen_starting_gold(char.char_class, ui)
        char.gen_class(char.char_class, ui)
        char.gen_starting_equipment(all_items, ui)
        char.action_economy()
        return char

def gen_mon(monster, all_items, ui):
        mon = Monster(monster, ui)
        #ui.create_mon_status(mon)
        #mon.gen_loot(all_items)
        mon.action_economy()
        return mon

'''
Initialize PCs (player characters)
IN
- all_items (object)
- ui (object)
OUT
- allies (array)
'''
def init_chars(all_items, ui):
        starting_level = 1
        ui.push_message("Name your hero:")
        name = ui.get_text_input()
        npc = False
        if name == "":
                name = "Rick"
        ui.push_message(name)
        p1_char = gen_char(name, starting_level, all_items, npc, ui)
        
        name = "Rei"
        npc = False
        ui.push_message(name)
        p2_char = gen_char(name, starting_level, all_items, npc, ui)
        
        name = "Benny"
        npc = False
        ui.push_message(name)
        p3_char = gen_char(name, starting_level, all_items, npc, ui)
        
        name = "Alf"
        npc = False
        ui.push_message(name)
        p4_char = gen_char(name, starting_level, all_items, npc, ui)
        
        allies = [p1_char, p2_char, p3_char, p4_char]
        return allies

'''
Initialize NPCs (non-player characters)
IN
- all_items (object)
- ui (object)
OUT
- enemy_list (list of objects)
'''
def init_enemies(all_items, all_monsters, dungeon, enemy_cnt):
        enemy_counter = {}
        enemy_list = []
        for _ in range(enemy_cnt):
                enemy = gen_mon(all_monsters.monsters[random.choice(dungeon.avail_monsters)], all_items, ui)
                if enemy.name not in enemy_counter:
                        enemy_counter[enemy.name] = 1
                else:
                        enemy_counter[enemy.name] += 1
                enemy.name = "%s #%s" % (enemy.name, enemy_counter[enemy.name])
                enemy_list.append(enemy)
        return enemy_list

main_window = tk.Tk()
ui = gui.GUI(main_window)
all_items = AllItems()
all_monsters = MonsterManual()
ai = AI()
ui.push_prompt("Welcome to Shining in the Dungeon (5e Duel)")
ui.push_message("Choose the difficulty.")
ai.set_diff_lvl(ui.get_dict_choice_input(ai.get_diff_lvls()))
chars = init_chars(all_items, ui)
allies = chars
encounters = 10
monsters = [1, 2]
dungeon = Dungeon(encounters, allies, monsters, ui)
enemy_cnt = math.ceil(len(allies) * 1.5)
enemies = init_enemies(all_items, all_monsters, dungeon, enemy_cnt)
for enc in range(dungeon.enc_cnt):
        battle = dungeon.start_battle(enc, allies, enemies, ui)
        battle.initiative(ui)
        attacker = battle.get_first_init(ui)
        battle_end = False
        while not battle_end:
                battle.get_hp_init_board(ui)
                attacker = battle.get_current_init(ui)
                attacker.reset_until_start_of_next_turn(ui)
                attacker.turn_done = False
                while not attacker.turn_done:
                        act_choice = attacker.battle_menu(ui)
                        act(attacker, act_choice, battle, all_items, ui)
                attacker.reset_until_end_of_current_turn(all_items, ui)
                if battle.check_end():
                        battle.get_hp_init_board(ui)
                        battle_end = battle.end(ui)
                else:
                        battle.set_next_init(ui)
                        battle.check_round_end()
        if battle.pcs_won or battle.pcs_fled or battle.foes_fled:
                dungeon.get_respite_options(ui)
        else:
                break
dungeon.end_dungeon(ui)
main_window.mainloop()

#TODO: fix rests
#TODO: back option for menus
#TODO: level up, proficiency up, asi choice (unequip-equip flow to recalc stats)
#TODO: after every 2nd battle pcs level up, get loot from opposing team
#TODO: 4-lane battle formation/2-lane marching order, net restrain, whip pull, push/pull, move mechanic