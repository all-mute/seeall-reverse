import json

def convert_format(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f_in, \
         open(output_file, 'w', encoding='utf-8') as f_out:
        
        for line in f_in:
            # Read input JSON
            data = json.loads(line)
            
            # Create new message format
            messages = []
            
            # Convert request items to messages
            for item in data['request']:
                messages.append({
                    "role": item['role'],
                    "content": item['text']
                })
            
            # Add assistant's response
            messages.append({
                "role": "assistant",
                "content": data['response']
            })
            
            # Create new format
            new_format = {
                "messages": messages
            }
            
            # Write to output file
            f_out.write(json.dumps(new_format, ensure_ascii=False) + '\n')

# Example usage
input_file = 'dataset-2-flipped.jsonl'
output_file = 'dataset-openai-format.jsonl'
convert_format(input_file, output_file)
