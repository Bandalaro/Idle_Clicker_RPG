import pandas as pd
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer, Trainer, TrainingArguments, TextDataset, DataCollatorForLanguageModeling
import os

# Load the new dataset
df = pd.read_csv('Weapon_New - Sheet1.csv')

# Concatenate all rows into a single text string with each row separated by a newline
# Adjust the format to match the new columns
text_data = df.apply(lambda row: '\t'.join(row.astype(str)), axis=1).str.cat(sep='\n')

# Save to a text file
with open('weapon_data.txt', 'w') as f:
    f.write(text_data)

# Load pre-trained GPT-2 model and tokenizer
model_name = 'gpt2'
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)

# Function to load the dataset
def load_dataset(file_path, tokenizer, block_size=128):
    return TextDataset(
        tokenizer=tokenizer,
        file_path=file_path,
        block_size=block_size
    )

# Function to create data collator
def create_data_collator(tokenizer):
    return DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False,
    )

# Load dataset
train_dataset = load_dataset('weapon_data.txt', tokenizer)
data_collator = create_data_collator(tokenizer)

# Define training arguments
training_args = TrainingArguments(
    output_dir='./results',
    overwrite_output_dir=True,
    num_train_epochs=3,
    per_device_train_batch_size=2,
    save_steps=10_000,
    save_total_limit=2,
)

# Initialize Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    data_collator=data_collator,
    train_dataset=train_dataset,
)

# Fine-tune the model
trainer.train()

# Save the fine-tuned model
model.save_pretrained('./fine_tuned_gpt2')
tokenizer.save_pretrained('./fine_tuned_gpt2')

# Load the fine-tuned model and tokenizer
tokenizer = GPT2Tokenizer.from_pretrained('./fine_tuned_gpt2')
model = GPT2LMHeadModel.from_pretrained('./fine_tuned_gpt2')

# Define a function to generate weapon entries
def generate_weapon_entry(prompt, max_length=200):
    inputs = tokenizer.encode(prompt, return_tensors='pt')
    outputs = model.generate(inputs, max_length=max_length, num_return_sequences=1, pad_token_id=tokenizer.eos_token_id)
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return generated_text

# Function to parse the generated output into a structured format
def parse_generated_output(generated_output):
    columns = ["Name", "Weapon Type", "Strength", "Defense", "Speed", "Dexterity", "Intelligence", "Ability Name", "Ability Description", "Total Stats", "Rank"]
    attributes = generated_output.split('\t')
    weapon_entry = dict(zip(columns, attributes))
    return weapon_entry

# Function to save the structured data to a file
def save_weapon_entry(weapon_entry, filename='generated_weapon_entries.csv'):
    if os.path.exists(filename):
        weapon_df = pd.read_csv(filename)
        weapon_df = weapon_df.append(weapon_entry, ignore_index=True)
    else:
        weapon_df = pd.DataFrame([weapon_entry])
    weapon_df.to_csv(filename, index=False)

# Example usage
if __name__ == "__main__":
    prompt = (
        "Generate a detailed weapon entry with the following columns:\n"
        "Name, Weapon Type, Strength, Defense, Speed, Dexterity, Intelligence, Ability Name, Ability Description, Total Stats, Rank\n\n"
    )
    generated_output = generate_weapon_entry(prompt)
    print(f"Generated Output: {generated_output}")

    weapon_entry = parse_generated_output(generated_output)
    print(f"Parsed Weapon Entry: {weapon_entry}")

    save_weapon_entry(weapon_entry)
    print(f"Weapon entry saved to 'generated_weapon_entries.csv'")
