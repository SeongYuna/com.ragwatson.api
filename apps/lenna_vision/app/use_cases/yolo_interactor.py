from __future__ import annotations

import logging

from lenna_vision.app.dtos.yolo_train_dto import YoloTrainCommand, YoloTrainResult
from lenna_vision.app.ports.input.yolo_train_use_case import YoloTrainUseCase
from lenna_vision.app.ports.output.yolo_dataset_port import YoloDatasetPort
from lenna_vision.app.ports.output.yolo_port import YoloTrainerPort

logger = logging.getLogger(__name__)


class YoloInteractor(YoloTrainUseCase):
    """데이터셋 준비(YoloDatasetPort)와 모델 훈련(YoloTrainerPort)을 조합하는 오케스트레이터."""

    def __init__(self, dataset_port: YoloDatasetPort, trainer_port: YoloTrainerPort) -> None:
        self._dataset_port = dataset_port
        self._trainer_port = trainer_port

    def train(self, command: YoloTrainCommand) -> YoloTrainResult:
        logger.info("[YoloInteractor] 훈련 시작 — epochs=%d batch=%d device=%s",
                    command.epochs, command.batch, command.device)

        yaml_path = self._dataset_port.get_dataset_yaml_path()
        logger.info("[YoloInteractor] data.yaml 준비 완료: %s", yaml_path)

        result = self._trainer_port.train(yaml_path=yaml_path, command=command)
        logger.info("[YoloInteractor] 훈련 완료 — best=%s", result.best_model_path)

        return result
