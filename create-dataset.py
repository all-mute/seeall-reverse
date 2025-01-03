import asyncio
import json
from tqdm import tqdm
from utils import llm, eliza
from langchain_core.messages import SystemMessage, HumanMessage
import random

SYSTEM_MESSAGE = "Ты - полезный ассистент. Перепиши текст пользователя в очень-очень скучный, формальный, унылый, строгий формат, который тяжело и неинтересно читать. Сохраняй размер и детали, но можешь нарушать форматирование."
FROZEN = "В интернете есть много сайтов с информацией на эту тему. [Посмотрите, что нашлось в поиске](https://ya.ru)"
FROZEN_OAI = ("Извините,", "I'm sorry,")
SYSTEM_FOR_DATASET = "Ты - полезный ассистент, который переписывает текст в более интересный и приятный читателю формат, для блога в телеграмм. "

def load_messages(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    assert isinstance(data, list)
    return data[:]

async def ainvoke_llm(message) -> str:
    #1. try eliza
    response = await eliza.ainvoke([
        SystemMessage(content=SYSTEM_MESSAGE),
        HumanMessage(content=message)
    ])
    if response.content.startswith(FROZEN_OAI):
        ...
    else:
        return response.content
    
    #2. try llm
    response = await llm.ainvoke([
        SystemMessage(content=SYSTEM_MESSAGE),
        HumanMessage(content=message)
    ])    
    if response.content == FROZEN:
        return None
    else:
        return response.content

async def process_message(message):
    response = await ainvoke_llm(message)
    if response is None:
        return None
    
    if random.random() < 0.5:
        response = await ainvoke_llm(response)
        if response is None:
            return None
    
    return {
        "request": [
            {
                "role": "system",
                "text": SYSTEM_FOR_DATASET
            },
            {
                "role": "user", 
                "text": response
            }
        ],
        "response": message
    }

async def main():
    messages = load_messages("combined_messages.json")
    
    # Create semaphore to limit concurrent tasks
    semaphore = asyncio.Semaphore(9)
    
    async def bounded_process_message(msg):
        async with semaphore:
            return await process_message(msg)
    
    # Create tasks with semaphore
    tasks = [asyncio.create_task(bounded_process_message(msg)) for msg in messages]
    
    results = []
    
    for task in tqdm(asyncio.as_completed(tasks), total=len(tasks)):
        try:
            result = await task
            results.append(result)
        except Exception as e:
            print(f"Ошибка при обработке сообщения: {e}")
            
    with open("dataset-X.jsonl", "w", encoding="utf-8") as f:
        i = 0
        for result in results:
            if result is not None:
                f.write(json.dumps(result, ensure_ascii=False) + "\n")
                i += 1
        print(f"Обработано {i} сообщений")

if __name__ == "__main__":
    asyncio.run(main())
    
    
    