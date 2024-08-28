class Shop:
    def __init__(self):
        self.items_for_sale = [
            {'name': 'Basic Sword', 'type': 'weapon', 'price': 30, 'Strength': 5, 'Dexterity': 2, 'Speed': 1},
            {'name': 'Basic Armor', 'type': 'armor', 'price': 35, 'Defense': 5, 'Intelligence': 2},
            {'name': 'Healing Potion', 'type': 'potion', 'price': 10, 'hp_restore': 20},
        ]

    def display_items(self):
        print("\nShopkeeper: Welcome to my humble shop! Take a look at what I have for sale:")
        for item in self.items_for_sale:
            print(f"- {item['name']} ({item['type'].capitalize()}): {item['price']} gold")

    def buy_item(self, player, item_name):
        for item in self.items_for_sale:
            if item['name'].lower() == item_name.lower():
                if player.gold >= item['price']:
                    player.buy_item(item, item['price'])
                    print(f"Shopkeeper: Thank you for your purchase! You bought {item['name']}.")
                else:
                    print("Shopkeeper: You don't have enough gold for that item.")
                return
        print("Shopkeeper: Sorry, we don't have that item in stock.")

    def sell_item(self, player, item_name):
        if item_name in player.inventory:
            if item_name in player.equipment['weapon'] or item_name in player.equipment['armor']:
                player.unequip_item(item_name)

            sell_price = player.inventory[item_name] * 0.5  # Selling items for half their buying price
            player.gold += sell_price
            del player.inventory[item_name]
            print(f"Shopkeeper: I have bought {item_name} from you for {sell_price} gold.")
        else:
            print("Shopkeeper: You don't have that item to sell.")

    def interact(self, player):
        print("Shopkeeper: How can I assist you today?")
        while True:
            choice = input("Choose an action: 1. Buy 2. Sell 3. Exit\n")
            if choice == '1':
                self.display_items()
                item_name = input("Enter the name of the item you want to buy: ")
                self.buy_item(player, item_name)
            elif choice == '2':
                print(f"Your inventory: {player.inventory.keys()}")
                item_name = input("Enter the name of the item you want to sell: ")
                self.sell_item(player, item_name)
            elif choice == '3':
                print("Shopkeeper: Come again soon!")
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    from player_mechanics import Player
    player = Player()
    shop = Shop()
    shop.interact(player)
