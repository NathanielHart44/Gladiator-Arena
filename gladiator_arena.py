import random
from sys import exit
import glad_global_info as info
import glad_classes as classes
import glad_items as items
import glad_inventory as inventory
global opponent

def explain(info):
    print(info)
    input("Please press 'enter' to continue.")

def fight_explain():
    explain("\tWelcome to the fighting pits! Your goal is to reduce your opponents' health to 0. Contestants, including yourself, start with 10 health points, so don't worry if your opponent hits you every so often. This is a game of survival, not (necessarily) who hits first!")
    explain("\n\tThere are a couple of other stats that will be important to remember...")
    explain("\n\nSkill: The chance one of your attacks hits your opponent. Also helps you dodge your opponent's attacks.")
    explain("\nSpeed: Decides who gets to attack first. Also helps you dodge your opponent's attacks.")
    explain("\nStrength: How hard one of your attacks hits, once it connects with your opponent.")
    explain("\n\n\tThat being said, your equipment has an impact on your stats as well. Choose a cumbersome weapon, and your Speed will go down. Attack with something small, and your Strength doesn't do much good.\n\n\t\t\t\t\tGood luck!\n\n")
    explain("\n\n\n\n\n")

def weapon_pick():
    print("Here are the weapons you can choose from:")
    for weapon in info.weapon_ls:
        print(weapon.name)
    print(f"Out of these {len(info.weapon_ls)} options, you can only pick one.")
    for weapon in info.weapon_ls:
        weapon_select = input(f"Would you like to use a {weapon.name}?\n> ")
        if weapon_select.lower() == 'yes':
            info.player.weapon = weapon
            print(f"You've chosen to fight with a {weapon.name}.")
            break

def armor_pick():
    print("Here are the armor options you can choose from:")
    for armor in info.armor_ls:
        print(armor.name)
    print(f"Out of these {len(info.armor_ls)} options, you can only pick one.")
    for armor in info.armor_ls:
        armor_select = input(f"Would you like to use {armor.name}?\n> ")
        if armor_select.lower() == 'yes':
            info.player.armor = armor
            print(f"You've chosen to fight with {armor.name}.")
            break

def arena_enter():
    explain("\nYou're ready to fight! There are several other contestants.")
    for count,contestant in enumerate(info.contestants_ls,1):
        print(f"Contestant {count} is: " + contestant.name)

    def opponent_input_check():
        opponent_input = input("Please type the number of the contestant you would like to duel.\n> ")
        if opponent_input.isnumeric() != True or int(opponent_input) > count or int(opponent_input) <= 0:
            print("It looks like you haven't typed in a valid number. Please try again.\n")
            opponent_input_check()
        else:
            info.valid_opponent_input = int(opponent_input)

    opponent_input_check()
    info.opponent = info.contestants_ls[info.valid_opponent_input - 1]
    info.opponent.weapon = random.choice(info.weapon_ls)
    info.opponent.armor = random.choice(info.armor_ls)
    explain(f"\n{info.opponent.name} will be fighting you with a {info.opponent.weapon.name}, which is a {info.opponent.weapon.w_type} weapon. They are also equipped with {info.opponent.armor.name}. Good luck!\n")

def combat_stats():
    print(f"\n{info.opponent.name}'s skill: {info.opponent.skill}, speed: {info.opponent.speed}, strength: {info.opponent.strength}.\n")
    explain(f"{info.player.name}'s skill: {info.player.skill}, speed: {info.player.speed}, strength: {info.player.strength}.\n")
    print("\nHere's how the weapons and armor of you and your opponent impacted your stats...\n")
    print(f"\n{info.opponent.name}'s skill: {info.opponent.skill}, speed: {info.opponent.getSpeed()}, potential damage: {info.opponent.getDamage()}, potential defense: {info.opponent.getDefense()}.\n")
    explain(f"{info.player.name}'s skill: {info.player.skill}, speed: {info.player.getSpeed()}, potential damage: {info.player.getDamage()}, potential defense: {info.player.getDefense()}.\n")


def attack_init():
    if info.player.getSpeed() > info.opponent.getSpeed():
        explain("\nYou are faster than your opponent. You attack first.\n")
    elif info.player.getSpeed() < info.opponent.getSpeed():
        explain("\nYour opponent is faster than you. They attack first.\n")
        info.turnCount += 1
    else:
        chance = random.randrange(0, 2)
        if chance == 0:
            explain("\nNeither you nor your opponent is faster, but your opponent gains the upper hand.\n")
            info.turnCount += 1
        else:
            explain("\nNeither you nor your opponent is faster, but you gain the upper hand.\n")
    attack()


def attack():
    chance = random.randrange(0, info.hit_chance)
    if info.turnCount % 2 == 0:
        b = "Your"
        source = info.player
        target = info.opponent
    else:
        b = "Their"
        source = info.opponent
        target = info.player
    if source.skill + chance >= info.hit_chance:
        explain(f"{b} attack hits!\n")
        damage_done = round(source.getDamage() - (((target.skill + target.speed) * info.attack_evade_mod) + target.getDefense()))

        if damage_done >= 0:
            print(f"{b} damage done was {damage_done}. {target.name}'s {target.armor.name} blocked {round(target.getDefense())} damage.")
            target.takeDamage(damage_done)
        else:
            print(f"1 damage was done.")
            target.takeDamage(1)
        explain(f"{target.name} has {target.health} health left.\n")
    else:
        explain(f"{b} attack misses.\n")
    win_condition()
    info.turnCount += 1
    attack()

def win_condition():
    if info.opponent.health <= 0 and (len(info.contestants_ls) - 1) > 0:
        c = info.contestants_ls.index(info.opponent)
        info.contestants_ls.pop(c)
        explain(f"\nYou beat {info.opponent.name}!\n")
        play_again()
        quit()
    elif info.opponent.health <= 0 and (len(info.contestants_ls) - 1) == 0:
        print(f"\n\n\t\t\t\t\tYou beat {info.opponent.name}!")
        print("\n\n\t\t\t\t\tYou win!\n\n\n\n\n")
        quit()
    elif info.player.health <= 0:
        print("\n\n\n\t\t\t\t\tYou lose.\n\n\n\n\n")
        r = input("Would you like to play again?\n> ")
        if r.lower() == "yes" or r.lower() == "y":
            info.player.health = info.start_health
            info.opponent.health = info.start_health
            classes.get_player_name()
            weapon_pick()
            armor_pick()
            arena_enter()
            combat_stats()
            attack_init()
        else:
            quit()

def play_again():
    r = input("\nWould you like to play again?\n> ")
    if r.lower() == "yes" or r.lower() == "y":
        info.player.health = info.start_health
        arena_enter()
        combat_stats()
        attack_init()
    else:
        q = input("Are you sure? Type 'q' to quit.\n> ")
        if q.lower() == "q":
            quit()
        else:
            play_again()

def explanation():
    check_explain = input("Would you like an explanation of how this works?\n> ")
    if check_explain.lower() == "yes":
        fight_explain()


explanation()
classes.get_player_name()
weapon_pick()
armor_pick()
arena_enter()
combat_stats()
attack_init()
