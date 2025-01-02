from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
import asyncio
from langchain_core.messages import HumanMessage

YANDEX_API_KEY = os.getenv("UE_YANDEX_API_KEY")
FOLDER_ID = os.getenv("UE_FOLDER_ID")
api_key = f"{FOLDER_ID}@{YANDEX_API_KEY}"
base_url = f"https://latest.o2y.ai-cookbook.ru/v1/"

print(api_key)

llm = ChatOpenAI(
    api_key=api_key,
    base_url=base_url,
    model="yandexgpt/latest",
    #default_headers={'Raw-Answer':'True'},
    temperature=0.5,
    max_tokens=4094,
)

async def make_call(message: str) -> str:
    response = await llm.ainvoke([HumanMessage(content=message)])
    return response.content

async def run_parallel_calls():
    messages = ["Write small story about a cat" for _ in range(10)]
    tasks = [make_call(msg) for msg in messages]
    results = await asyncio.gather(*tasks)
    return results

if __name__ == "__main__":
    results = asyncio.run(run_parallel_calls())
    for i, result in enumerate(results, 1):
        print(f"Response {i}: {result}")
