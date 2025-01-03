#!/usr/bin/env python3

from __future__ import annotations
import pathlib
import uuid
from yandex_cloud_ml_sdk import YCloudML
import os
from yandex_cloud_ml_sdk.tuning import optimizers as to
from yandex_cloud_ml_sdk.tuning import schedulers as ts
from yandex_cloud_ml_sdk.tuning import types as tt

YANDEX_API_KEY = os.getenv("UE_YANDEX_API_KEY")
FOLDER_ID = os.getenv("UE_FOLDER_ID")


def local_path(path: str) -> pathlib.Path:
    return pathlib.Path(__file__).parent / path

def main() -> None:
    sdk = YCloudML(folder_id=FOLDER_ID, auth=YANDEX_API_KEY)
    train_dataset = sdk.datasets.get("")
    base_model = sdk.models.completions('yandexgpt-lite')

    tuning_task = base_model.tune_deferred(
        train_dataset,
        #validation_datasets=validation_dataset,
        name=str(uuid.uuid4()),
        description="cool tuning",
        #labels={'good': 'yes'},
        seed=322,
        lr=5e-4, # 0.0005 instead of 0.0001
        #n_samples=100,
        tuning_type=tt.TuningTypeLora(),
        scheduler=ts.SchedulerLinear(),
        optimizer=to.OptimizerAdamw()
    )
    print(f'new {tuning_task=}')

    try:
        new_model = tuning_task.wait()
        print(f'tuning result: {new_model}')
        print(f'new model url: {new_model.uri}')
    except BaseException:
        tuning_task.cancel()
        raise
    
if __name__ == "__main__":
    main()
