from lenna_vision.adapter.outbound.resource_adapters.yolo.yolo_dataset_adapter import YoloDatasetAdapter
from lenna_vision.adapter.outbound.resource_adapters.yolo.yolo_trainer_adapter import YoloTrainerAdapter
from lenna_vision.app.ports.input.yolo_train_use_case import YoloTrainUseCase
from lenna_vision.app.use_cases.yolo_interactor import YoloInteractor


def get_yolo_train_use_case() -> YoloTrainUseCase:
    return YoloInteractor(
        dataset_port=YoloDatasetAdapter(),
        trainer_port=YoloTrainerAdapter(),
    )
