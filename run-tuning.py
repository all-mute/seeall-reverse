#!/usr/bin/env python3

from __future__ import annotations
import pathlib
import uuid
from yandex_cloud_ml_sdk import YCloudML
import os

YANDEX_API_KEY = os.getenv("UE_YANDEX_API_KEY")
FOLDER_ID = os.getenv("UE_FOLDER_ID")


def local_path(path: str) -> pathlib.Path:
    return pathlib.Path(__file__).parent / path


def main():
    sdk = YCloudML(
        folder_id=FOLDER_ID,
        auth=YANDEX_API_KEY,
    )

    # Посмотрим список датасетов, прошедших валидацию
    for dataset in sdk.datasets.list(status="READY"):#, name_pattern="completions"):
        print(f"List of existing datasets {dataset=}")
    print("--------------------------------")

    # Зададим датасет для обучения и базовую модель
    train_dataset = sdk.datasets.get("fdsuptf94qs4t5of11rf")
    print(train_dataset)
    base_model = sdk.models.completions("yandexgpt-lite")
    
    for tuning_task in sdk.tuning.list():
        # or you could wait for tasks, instead of canceling
        print(f'found task {tuning_task=}, canceling')
        print(tuning_task.get_task_info())
        print(tuning_task.get_status())
        print(tuning_task.get_metrics_url())
        #tuning_task.cancel()
    
    return

    # Определяем минимальные параметры
    # Используйте base_model.tune_deferred(), чтобы контролировать больше параметров
    tuned_model = base_model.tune(train_dataset, name=(str(uuid.uuid4()) + "-X-flipped"))
    #tuned_model = base_model.tune_deferred(train_dataset, name=str(uuid.uuid4()))
    print(f"Resulting {tuned_model}")

    # Запускаем дообучение
    completion_result = tuned_model.run("hey!")
    print(f"{completion_result=}")

    return

    # Сохраним URI дообученной модели
    tuned_uri = tuned_model.uri
    model = sdk.models.completions(tuned_uri)

    completion_result = model.run("hey!")
    print(f"{completion_result=}")


if __name__ == "__main__":
    main()
