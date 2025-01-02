#!/usr/bin/env python3

from __future__ import annotations
import asyncio
import pathlib
from yandex_cloud_ml_sdk import AsyncYCloudML
from yandex_cloud_ml_sdk.auth import YandexCloudCLIAuth
import os
FOLDER_ID = os.getenv("UE_FOLDER_ID")
YANDEX_API_KEY = os.getenv("UE_YANDEX_API_KEY")

def local_path(path: str) -> pathlib.Path:
    return pathlib.Path(__file__).parent / path


async def main():

    sdk = AsyncYCloudML(
        folder_id=FOLDER_ID,
        auth=YANDEX_API_KEY,
    )

    datasets = sdk.datasets.list()
    async for dataset in datasets:
        print(dataset.id, dataset.name)
        #await dataset.delete()

if __name__ == "__main__":
    asyncio.run(main())
