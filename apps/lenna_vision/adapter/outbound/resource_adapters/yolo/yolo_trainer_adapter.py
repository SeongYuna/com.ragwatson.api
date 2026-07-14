"""YOLOv11 Nano 기반 얼굴 인식 파인튜닝 어댑터.

ultralytics 의존성은 이 파일에만 격리된다.
모델: yolo11n.pt (파라미터 2.6M — 최신 초경량 아키텍처)
"""
from __future__ import annotations

import logging
from pathlib import Path

from ultralytics import YOLO

from lenna_vision.app.dtos.yolo_train_dto import YoloTrainCommand, YoloTrainResult
from lenna_vision.app.ports.output.yolo_port import YoloTrainerPort

logger = logging.getLogger(__name__)

_MODEL = "yolo11n.pt"


class YoloTrainerAdapter(YoloTrainerPort):
    def train(self, yaml_path: str, command: YoloTrainCommand) -> YoloTrainResult:
        logger.info("[YoloTrainer] 모델 로드: %s", _MODEL)
        model = YOLO(_MODEL)

        results = model.train(
            data=yaml_path,
            epochs=command.epochs,
            batch=command.batch,
            imgsz=command.imgsz,
            device=command.device,
            task="detect",
        )

        best_path = str(Path(results.save_dir) / "weights" / "best.pt")
        return YoloTrainResult(
            success=True,
            best_model_path=best_path,
            epochs_completed=command.epochs,
            message=f"훈련 완료 ({_MODEL} → face). best: {best_path}",
        )
