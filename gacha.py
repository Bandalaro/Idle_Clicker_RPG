import pandas as pd
import random

# Load the generated weapon entries
def load_generated_entries(file_path):
    df = pd.read_csv(file_path)
    return df

# Function to simulate gacha and fetch a random weapon entry
def run_gacha(file_path):
    df = load_generated_entries(file_path)
    num_entries = len(df)
    if num_entries == 0:
        return None
    random_index = random.randint(0, num_entries - 1)
    weapon_entry = df.iloc[random_index].to_dict()
    return weapon_entry

# Function to print the weapon entry in a formatted manner
def print_weapon_entry(weapon_entry):
    if weapon_entry:
        print("Congratulations! You received the following weapon:")
        for key, value in weapon_entry.items():
            print(f"{key}: {value}")
    else:
        print("No generated weapon entries available.")

# Example usage
if __name__ == "__main__":
    generated_file = 'generated_weapon_entries.csv'
    weapon_entry = run_gacha(generated_file)
    print_weapon_entry(weapon_entry)
