import random

class Enemy:
    def __init__(self, player):
        self.name = random.choice(["Slime", "Goblin", "Skeleton"])
        self.hp = random.randint(10, player.hp)
        self.speed = random.randint(1, player.speed)
        self.intelligence = random.randint(1, player.intelligence)
        self.strength = random.randint(1, player.strength)
        self.dexterity = random.randint(1, player.dexterity)
        self.exp_reward = random.randint(5, 20)

def attack(attacker, defender):
    hit_chance = (attacker.dexterity / (attacker.dexterity + defender.dexterity)) * 100
    if random.randint(1, 100) <= hit_chance:
        damage = max(attacker.strength - defender.strength // 2, 1)
        defender.hp -= damage
        print(f"{attacker.__class__.__name__} attacked and dealt {damage} damage!")
    else:
        print(f"{attacker.__class__.__name__} missed the attack!")

def try_weapon(player):
    enemy = Enemy(player)
    print(f"A wild {enemy.name} appeared!")

    while player.hp > 0 and enemy.hp > 0:
        print(f"\nPlayer HP: {player.hp}, Enemy HP: {enemy.hp}")
        action = input("Choose an action: 1. Attack 2. Flee\n")

        if action == '1':
            if player.speed >= enemy.speed:
                attack(player, enemy)
                if enemy.hp > 0:
                    attack(enemy, player)
            else:
                attack(enemy, player)
                if player.hp > 0:
                    attack(player, enemy)
        elif action == '2':
            print("You fled from the battle!")
            return

        if player.hp <= 0:
            print("You were defeated by the enemy...")
            return
        elif enemy.hp <= 0:
            print(f"You defeated the {enemy.name}!")
            player.gain_experience(enemy.exp_reward)
            return

if __name__ == "__main__":
    from player_mechanics import Player
    player = Player()
    try_weapon(player)
