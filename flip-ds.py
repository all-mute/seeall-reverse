import json

# Путь к входному и выходному файлам
input_file = "dataset-X.jsonl"
output_file = "dataset-X-flipped.jsonl"

def flip_request_response(line):
    """
    Меняет местами текст запроса пользователя и ответ в одной строке датасета
    """
    data = json.loads(line)
    
    # Получаем текст пользователя из request
    user_text = next(msg["text"] for msg in data["request"] if msg["role"] == "user")
    
    # Получаем оригинальный ответ
    original_response = data["response"]
    
    # Создаем новый request, где текст пользователя заменен на оригинальный ответ
    new_request = [
        {"role": "system", "text": next(msg["text"] for msg in data["request"] if msg["role"] == "system")},
        {"role": "user", "text": original_response}
    ]
    
    # Создаем новую структуру данных
    flipped_data = {
        "request": new_request,
        "response": user_text
    }
    
    return json.dumps(flipped_data, ensure_ascii=False)

# Читаем входной файл и записываем измененные данные в выходной
with open(input_file, 'r', encoding='utf-8') as infile, \
     open(output_file, 'w', encoding='utf-8') as outfile:
    
    for line in infile:
        flipped_line = flip_request_response(line.strip())
        outfile.write(flipped_line + '\n')

print("Готово! Данные сохранены в", output_file)
