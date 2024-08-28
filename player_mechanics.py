import random

class Player:
    def __init__(self):
        self.gold = 200
        self.inventory = {'apples': 0}
        self.equipment = {'weapon': None, 'armor': None}
        self.hp = 100
        self.speed = random.randint(1, 11)
        self.intelligence = random.randint(1, 11)
        self.strength = random.randint(1, 11)
        self.dexterity = random.randint(1, 11)
        self.level = 1
        self.experience = 0
        self.skill_points = 0

    def __str__(self):
        return (f"Player Stats:\n"
                f"HP: {self.hp}, Speed: {self.speed}, Intelligence: {self.intelligence}, "
                f"Strength: {self.strength}, Dexterity: {self.dexterity}, Level: {self.level}, "
                f"Experience: {self.experience}, Skill Points: {self.skill_points}")

    def buy_item(self, item, price):
        if self.gold >= price:
            self.gold -= price
            self.inventory[item['name']] = self.inventory.get(item['name'], 0) + 1
            print(f"You bought {item['name']}. Remaining gold: {self.gold}")
            if 'weapon' in item['type']:
                self.equipment['weapon'] = item
            elif 'armor' in item['type']:
                self.equipment['armor'] = item
            self.apply_item_stats(item)
        else:
            print("You don't have enough gold.")

    def apply_item_stats(self, item):
        if 'weapon' in item['type']:
            self.strength += int(item['Strength'])
            self.dexterity += int(item['Dexterity'])
            self.speed += int(item['Speed'])
            print(f"Equipped {item['name']}. Strength: {self.strength}, Dexterity: {self.dexterity}, Speed: {self.speed}.")
        elif 'armor' in item['type']:
            self.hp += int(item['Defense'])
            self.intelligence += int(item['Intelligence'])
            print(f"Equipped {item['name']}. HP: {self.hp}, Intelligence: {self.intelligence}.")

    def unequip_item(self, item_name):
        if self.equipment['weapon'] and self.equipment['weapon']['name'] == item_name:
            self.strength -= int(self.equipment['weapon']['Strength'])
            self.dexterity -= int(self.equipment['weapon']['Dexterity'])
            self.speed -= int(self.equipment['weapon']['Speed'])
            self.equipment['weapon'] = None
            print(f"Unequipped {item_name}.")
        elif self.equipment['armor'] and self.equipment['armor']['name'] == item_name:
            self.hp -= int(self.equipment['armor']['Defense'])
            self.intelligence -= int(self.equipment['armor']['Intelligence'])
            self.equipment['armor'] = None
            print(f"Unequipped {item_name}.")

    def add_apples(self, count):
        self.inventory['apples'] += count
        print(f"You found {count} apples. Total apples: {self.inventory['apples']}")

    def gain_experience(self, amount):
        self.experience += amount
        print(f"You gained {amount} experience points. Total experience: {self.experience}")
        if self.experience >= self.level * 100:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.skill_points += 5
        self.experience = 0
        print(f"Congratulations! You leveled up to level {self.level}. You have {self.skill_points} skill points to spend.")

    def spend_skill_points(self, hp=0, speed=0, intelligence=0, strength=0, dexterity=0):
        total_points = hp + speed + intelligence + strength + dexterity
        if total_points <= self.skill_points:
            self.hp += hp
            self.speed += speed
            self.intelligence += intelligence
            self.strength += strength
            self.dexterity += dexterity
            self.skill_points -= total_points
            print(f"Skill points spent. New stats - HP: {self.hp}, Speed: {self.speed}, Intelligence: {self.intelligence}, Strength: {self.strength}, Dexterity: {self.dexterity}")
        else:
            print("You don't have enough skill points.")

    def show_status(self):
        print("\nStatus Window")
        print(self)
