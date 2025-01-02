from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
import asyncio
from langchain_core.messages import HumanMessage, SystemMessage

YANDEX_API_KEY = os.getenv("UE_YANDEX_API_KEY")
FOLDER_ID = os.getenv("UE_FOLDER_ID")
api_key = f"{FOLDER_ID}@{YANDEX_API_KEY}"
base_url = f"https://latest.o2y.ai-cookbook.ru/v1/"

file_name = 'seeall0'
with open(f'r/in/{file_name}.txt', 'r') as file:
    test_text = file.read()

llm = ChatOpenAI(
    api_key=api_key,
    base_url=base_url,
    model="gpt://b1glma7ae7cm9j2908sk/yandexgpt-lite/latest@tamr1hh1ss1kiotep4bd0",
    #model="yandexgpt-lite/latest",
    temperature=0,
    max_tokens=4094,
)

messages = [
    SystemMessage(content="Ты - полезный ассистент, который переписывает текст в более интересный и приятный читателю формат, для блога в телеграмм. "),
    HumanMessage(content=test_text),
]

if __name__ == "__main__":
    response = llm.invoke(messages)
    print("LLM response:")
    print(response.content)
    
    with open(f'r/out/{file_name}.txt', 'w') as file:
        file.write(response.content)
