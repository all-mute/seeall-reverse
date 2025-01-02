import json
import tiktoken

tokenizer = tiktoken.get_encoding("cl100k_base")
THRESHOLD = 4000

def load_messages(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    assert isinstance(data, list)
    return data

def inspect_messages(messages):
    print(len(messages))
    print(len([item for item in messages if len(tokenizer.encode(item)) > THRESHOLD]))
    print([item for item in messages if len(tokenizer.encode(item)) > THRESHOLD])
    print([len(tokenizer.encode(item)) for item in messages if len(tokenizer.encode(item)) > THRESHOLD])
    
if __name__ == "__main__":
    messages = load_messages("combined_messages.json")
    inspect_messages(messages)

