import random
import item_dict
import enemy_data
from termcolor import colored, cprint
import os

class Item:
    def __init__(self, name, type, damage, defense):
        self.name = name
        self.type = type
        self.damage = damage
        self.defense = defense

class Player:
    def __init__(self):
        self.equiped_items = []
        self.health = 20
        self.defense = 3
        self.damage = 7
        self.luck = 1
        self.level = 1
        self.room = None
        self.inventory = []
        self.crit_chance = 100 / 10
        if random.randint(0, self.crit_chance) == 0:
            self.damage = self.damage * 2
    
    def update_stats(self):
        self.damage = self.damage + self.equiped_items.get('damage')
        self.defense = self.defense + self.equiped_items.get('defense')

    def getDamage(self, damage):
        if damage > self.defense:
            self.health -= int(damage - self.defense)
        else:
            self.health -= int(damage)
        if self.health < 0:
            self.health == 0

    def check_gameOver(self):
        if self.health <= 0:
            cprint('You have been defeated!', 'red', attrs=['bold'])
            return True
        else:
            return False

class Enemy:
    def __init__(self, player_level, room_type):
        self.enemy_data = {}
        for key, values in enemy_data.types.items():
            for i in range(values.get('Location') == room_type):
                self.chance = random.randint(1, int(100*(1/values.get('Rarity'))))
                if self.chance == 1:
                    self.enemy_data = values
        self.name = self.enemy_data.get('Name')
        if player_level > 5:
            self.level = player_level - random.randint(0, 3)
        else:
            self.level = player_level
        self.health = self.enemy_data.get('Health')
        self.damage = self.enemy_data.get('Damage')
        self.defense = self.enemy_data.get('Defense')
        self.attack_chance = 100 / random.randint(70, 100)
        self.loot = {}
        for key, values in item_dict.items.items():
            if (values.get('type') == 'drop') and (values.get('enemy') == self.name):
                if random.randint(1, int(100*(1/values.get('drop_chance')))) == 1:
                    self.loot[i+1] = Item(values.get('name'), values.get('type'), values.get('damage'), values.get('defense'))

    def getDamage(self, damage):
        self.damage_taken = int(damage - self.defense)
        if self.damage_taken <= 0:
            self.damage_taken = 0
        self.health -= self.damage_taken
        if self.health < 0:
            self.health == 0

    def check_gameOver(self):
        if self.health <= 0:
            cprint('Enemy dead!', 'red', attrs=['bold'])
            return True
        else:
            return False
    
    def print_stats(self):
        print(self.enemy_data)
        print(f'\n    name: {self.name}\n    level: {self.level}\n    health: {self.health}\n    damage: {self.damage}\n    defense: {self.defense}\n    loot: {self.loot}')

class Shop:
    def __init__(self):
        asd = 'asd'

def get_item(item, player):
    player.inventory.append(item)

def equip_item(item, player):
    for i in range(len(player.equiped_items)):
        if item.name != i.get('name'):
            player.equiped_items.append(item)
            print(f'{item.name} was equipped!')
        else:
            print('This items is already equipped')

def gen_new_room():
    room_type_list = ('jungle', 'moss', 'cobblestone', 'golden')
    room_data = {
        'room_type': random.choice(room_type_list), 
        'enemies': {}, 
        'loot': {}
        }
    for i in range(3):
        newEnemy = Enemy(player.level, room_data.get('room_type'))
        if random.randint(1, int(100*(1/newEnemy.chance))) == 1:
            room_data['enemies'][(i + 1)] = newEnemy
    print(room_data.get('room_type'))
    print(room_data.get('enemies'))
    return room_data

def collection(player_inventory, items):
    if items != 0:
        total_percentage = 100/(player_inventory/items)
    else:
        total_percentage = 0
    return int(total_percentage)

def battle(b_enemy):
    your_turn = True
    enemy_turn = False
    battle = True
    while battle:
        if enemy_turn == True:
            if random.randint(0, int(b_enemy.attack_chance)) == 0:
                player.getDamage(b_enemy.damage)
                if player.check_gameOver() == False:
                    enemy_turn = False
                    your_turn = True
                else:
                    battle = False
        elif your_turn == True:
            print(colored('  Your turn!\n', 'cyan'))
            print(f'Enemy health: {b_enemy.health}\nEnemy attack: {b_enemy.damage}\n\nYour health: {player.health}\nYour attack: {player.damage}\n--------------------\n')
            player_input_battle = input('Battle >>  ')
            player_input_battle = player_input_battle.split(' ')
            if player_input_battle[0] == 'attack':
                b_enemy.getDamage(player.damage)
                if b_enemy.check_gameOver() == False:
                    your_turn = False
                    enemy_turn = True
                else:
                    battle = False
                    for key, values in item_dict.items.items():
                        if (values.get('type') == 'drop') and (values.get('enemy') == b_enemy.name):
                            get_item(b_enemy.loot.get(random.randint(1, len(b_enemy.loot))), player)
            elif player_input_battle[0] == 'enemy_stats':
                b_enemy.print_stats()
            elif player_input_battle[0] == 'check_stats':
                print(f'Your defense: {player.defense}\nWeapon on hand: {player.equiped_items}')

player = Player()
player.room = gen_new_room()

running = True

cprint('InfiniDungeon (InDev)\n', 'yellow', attrs=['bold'])

while running:
    player_input = input('>>  ')
    player_input = player_input.split(' ')
    os.system('cls' if os.name == 'nt' else 'clear')

    if player_input[0] == 'quit':
        print('>> Funcion de guardado aun no implementada <<')
        running = False
    
    elif player_input[0] == 'equip':
        for i in range(len(player.inventory)):
            if player.inventory[i].get('name') != player.inventory.get(player_input[1]):
                equip_item(player.inventory.get(player_input[1]), player)
            else:
                print('This item is already equipped')

    elif player_input[0] == 'inventory':
        c_total = len(item_dict.items)
        for i in range(len(player.inventory)):
            print('\n--->  Inventory  <---')
            print(f'      ({c_total}/{len(player.inventory)}) {100*(len(player.inventory)/c_total)}')
            print('    >>  ' + player.inventory[i].name)

    elif player_input[0] == 'gen_enemy':
        newEnemy = None
        newEnemy = Enemy(player.level, player.room.get('room_type'))
        newEnemy.print_stats()

    elif player_input[0] == 'force_encounter':
        battle(newEnemy)

    elif player_input[0] == 'gen_room':
        player.room.clear()
        player.room = gen_new_room()

    elif player_input[0] == 'collection':
        print(collection(len(item_dict.items), len(player.inventory)))

    elif player_input[0] == 'enemy_loot':
        print(newEnemy.loot[int(player_input[1])].name)
