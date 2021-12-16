import random
import math
import glad_global_info as info
import glad_classes as classes
import glad_items as items
import glad_inventory as inventory

class Game():
    def __init__(self, num_opponents, game_difficulty, item_quality, stats_quality):
        self.num_opponents = num_opponents
        self.game_difficulty = game_difficulty
        self.item_quality = item_quality
        self.stats_quality = stats_quality


    #: Creates a dictionary from weapon_stats & weapon_names lists.
    #: 2nd dictionary sorts high-low based off of their stats.
    def gen_weapon_containers(self):
        global sorted_weapon_dict
        weapon_stats = []
        weapon_names = []
        b = 0
        for a in enumerate(info.weapon_ls):
            weapon_stats.append((info.weapon_ls[b].speed + info.weapon_ls[b].damage) / 2)
            weapon_names.append(info.weapon_ls[b].name)
            b += 1
        unsorted_weapon_dict = dict((k, v) for k, v in zip(weapon_names, weapon_stats))
        sorted_weapon_dict = sorted(unsorted_weapon_dict.items(), key=lambda x: x[1], reverse=True)

    #: Best weapons and best odds are at the front.
    def generate_weapon(self, mode):
        global weapon_str
        odds = []
        def find_odds():
            r = len(sorted_weapon_dict)
            if mode == "Normal":
                for b in sorted_weapon_dict:
                    odds.append(r * 10)
                    r -= 1
            elif mode == "Easy":
                for b in sorted_weapon_dict:
                    odds.append(r * 10)
                    r += 1
            elif mode == "Hard":
                for b in sorted_weapon_dict:
                    odds.append(math.exp(r) * 10)
                    r -=1
        find_odds()
        opponent_weapon_pick = random.choices(sorted_weapon_dict, odds, k = 1)
        q = (str(opponent_weapon_pick)).split(",")
        weapon_str = q[0].replace("'", "").replace("(", "").replace("[", "")

    #: Find index of picked weapon in info.weapon_ls
    def set_opponent_weapon(self):
        m = 0
        for a in info.weapon_ls:
            if info.weapon_ls[m].name != weapon_str:
                m += 1
            elif info.weapon_ls[m].name == weapon_str:
                info.opponent.weapon = info.weapon_ls[m]


    #: Creates a dictionary from armor_stats & armor_names lists.
    #: 2nd dictionary sorts high-low based off of their stats.
    def gen_armor_containers(self):
        global sorted_armor_dict
        armor_stats = []
        armor_names = []
        b = 0
        for a in enumerate(info.armor_ls):
            armor_stats.append((info.armor_ls[b].defense * 4) - info.armor_ls[b].weight)
            armor_names.append(info.armor_ls[b].name)
            b += 1
        unsorted_armor_dict = dict((k, v) for k, v in zip(armor_names, armor_stats))
        sorted_armor_dict = sorted(unsorted_armor_dict.items(), key=lambda x: x[1], reverse=True)

    #: Best armors and best odds are at the front.
    def generate_armor(self, mode):
        global armor_str
        odds = []
        def find_odds():
            r = len(sorted_armor_dict)
            if mode == "Normal":
                for b in sorted_armor_dict:
                    odds.append(r * 10)
                    r -= 1
            elif mode == "Easy":
                for b in sorted_armor_dict:
                    odds.append(r * 10)
                    r += 1
            elif mode == "Hard":
                for b in sorted_armor_dict:
                    odds.append(math.exp(r) * 10)
                    r -=1
        find_odds()
        opponent_armor_pick = random.choices(sorted_armor_dict, odds, k = 1)
        q = (str(opponent_armor_pick)).split(",")
        armor_str = q[0].replace("'", "").replace("(", "").replace("[", "")

    #: Find index of picked armor in info.armor_ls
    def set_opponent_armor(self):
        m = 0
        for a in info.armor_ls:
            if info.armor_ls[m].name != armor_str:
                m += 1
            elif info.armor_ls[m].name == armor_str:
                info.opponent.armor = info.armor_ls[m]


test_game = Game(3, 0, 0, 0)

def get_weapon():
    a = test_game
    a.gen_weapon_containers()
    a.generate_weapon(info.game_mode)
    a.set_opponent_weapon()

def get_armor():
    a = test_game
    a.gen_armor_containers()
    a.generate_armor(info.game_mode)
    a.set_opponent_armor()
