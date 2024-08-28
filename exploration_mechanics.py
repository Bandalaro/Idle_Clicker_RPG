import random

def search_resources(player):
    resources = {
        'apples': random.randint(1, 5),
        'gold': random.randint(10, 50),
        'herbs': random.randint(1, 3)
    }

    events = [
        "You found a hidden stash of gold!",
        "You encountered a wandering merchant and traded some herbs.",
        "You discovered a rare herb with healing properties."
    ]

    found_resources = []
    for resource, amount in resources.items():
        if amount > 0:
            player.inventory[resource] = player.inventory.get(resource, 0) + amount
            found_resources.append(f"{amount} {resource}")

    event = random.choice(events)

    print(f"Exploration Result: You found {', '.join(found_resources)}. {event}")

    if "rare herb" in event:
        player.inventory['rare herb'] = player.inventory.get('rare herb', 0) + 1

def special_event(player):
    event_chance = random.random()
    if event_chance < 0.3:
        print("You encountered a mysterious figure who offers to enhance your weapon.")
        choice = input("Do you accept the offer? (yes/no): ")
        if choice.lower() == 'yes':
            if player.equipment['weapon']:
                player.equipment['weapon']['Strength'] += random.randint(1, 5)
                print(f"Your weapon's strength increased! New strength: {player.equipment['weapon']['Strength']}")
            else:
                print("You don't have a weapon to enhance.")
        else:
            print("You decided to decline the offer.")
    elif event_chance < 0.6:
        print("You found an ancient relic that grants you a temporary boost in strength.")
        player.strength += 10
        print(f"Temporary boost: Your strength is now {player.strength}.")
    else:
        print("You found nothing of interest.")

def explore(player):
    print("You are exploring the surroundings...")
    search_resources(player)
    special_event(player)
