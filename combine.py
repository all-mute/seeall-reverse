import json

# Time difference in seconds (10 minutes)
TIME_DIFF = 7 * 60  # 7 minutes

def load_messages(file_path):
    """
    Load messages from the specified JSON file.
    
    :param file_path: Path to the JSON file containing messages.
    :return: List of message objects.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data.get('messages', [])

def combine_messages(messages):
    """
    Combine messages that are posted within TIME_DIFF seconds of each other.
    
    :param messages: List of message objects.
    :return: List of combined message texts.
    """
    # Sort messages by date in ascending order
    sorted_messages = sorted(messages, key=lambda x: x.get('date', 0))
    combined = []
    current_group = []
    previous_date = None

    for message in sorted_messages:
        msg_date = message.get('date')
        msg_text = message.get('message', '').strip()

        if not msg_text:
            continue  # Skip messages without text

        if previous_date is None:
            current_group.append(msg_text)
        else:
            if msg_date - previous_date < TIME_DIFF:
                current_group.append(msg_text)
            else:
                # Combine the current group into a single string separated by "\n---\n"
                combined.append('\n---\n'.join(current_group))
                current_group = [msg_text]
        previous_date = msg_date

    # Add the last group if it exists
    if current_group:
        combined.append('\n---\n'.join(current_group))

    return combined

def save_combined_messages(combined_messages, output_path):
    """
    Save the combined messages to a JSON file.
    
    :param combined_messages: List of combined message texts.
    :param output_path: Path to the output JSON file.
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(combined_messages, f, ensure_ascii=False, indent=4)

def main():
    """
    Main function to execute the script.
    """
    input_file = 'seeall-channel.json'
    output_file = 'combined_messages.json'

    # Load messages from the input file
    messages = load_messages(input_file)

    # Combine messages based on the time difference
    combined = combine_messages(messages)

    # Save the combined messages to the output file
    save_combined_messages(combined, output_file)
    print(f"Combined messages have been saved to {output_file}")

if __name__ == "__main__":
    main()
