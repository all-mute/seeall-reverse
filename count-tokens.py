import json
import tiktoken

def count_tokens_in_dataset(file_path):
    # Initialize tokenizer
    encoding = tiktoken.get_encoding("cl100k_base")  # GPT-4 tokenizer
    
    total_tokens = 0
    conversation_count = 0
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            conversation_count += 1
            data = json.loads(line)
            
            # Count tokens in each message
            for message in data['messages']:
                message_tokens = len(encoding.encode(message['content']))
                total_tokens += message_tokens
    
    return total_tokens, conversation_count

# Example usage
file_path = 'dataset-openai-format.jsonl'
total_tokens, conv_count = count_tokens_in_dataset(file_path)

print(f"Всего токенов в датасете: {total_tokens}")
print(f"Количество диалогов: {conv_count}")
print(f"Среднее количество токенов на диалог: {total_tokens / conv_count:.2f}") 