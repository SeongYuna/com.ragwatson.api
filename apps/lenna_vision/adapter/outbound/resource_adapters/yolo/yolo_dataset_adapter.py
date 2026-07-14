"""resources/yolo_train 디렉토리를 YOLO 데이터셋으로 연결하는 어댑터.

resources/yolo_train/
  train/   ← 학습 이미지 (.jpg)
  val/     ← 검증 이미지 (.jpg)

라벨이 없는 얼굴 이미지이므로 auto-annotation 방식(YOLO 내장 face detector)으로
바운딩박스를 생성한 뒤 data.yaml을 작성한다.
"""
from __future__ import annotations

import logging
from pathlib import Path

import cv2
from ultralytics import YOLO

from lenna_vision.app.ports.output.yolo_dataset_port import YoloDatasetPort

logger = logging.getLogger(__name__)

_FACE_DETECTOR_MODEL = "yolov8n.pt"
_YAML_FILENAME = "data.yaml"


class YoloDatasetAdapter(YoloDatasetPort):
    """로컬 resources/yolo_train 이미지를 YOLO 학습 포맷으로 변환한다."""

    def __init__(self, resources_root: str | None = None) -> None:
        if resources_root is None:
            resources_root = str(Path(__file__).resolve().parents[6] / "resources" / "yolo_train")
        self._root = Path(resources_root)
        self._train_dir = self._root / "train"
        self._val_dir = self._root / "val"
        self._label_train_dir = self._root / "labels" / "train"
        self._label_val_dir = self._root / "labels" / "val"
        self._yaml_path = self._root / _YAML_FILENAME

    def get_dataset_yaml_path(self) -> str:
        self._validate_image_dirs()
        self._ensure_labels()
        self._write_yaml()
        return str(self._yaml_path)

    def _validate_image_dirs(self) -> None:
        for d in (self._train_dir, self._val_dir):
            if not d.exists():
                raise FileNotFoundError(f"데이터셋 디렉토리 없음: {d}")
            images = list(d.glob("*.jpg")) + list(d.glob("*.png"))
            if not images:
                raise FileNotFoundError(f"이미지 파일이 없음: {d}")
            logger.info("[Dataset] %s — 이미지 %d장", d.name, len(images))

    def _ensure_labels(self) -> None:
        self._label_train_dir.mkdir(parents=True, exist_ok=True)
        self._label_val_dir.mkdir(parents=True, exist_ok=True)

        pairs = [
            (self._train_dir, self._label_train_dir),
            (self._val_dir, self._label_val_dir),
        ]
        detector = None
        for img_dir, lbl_dir in pairs:
            images = list(img_dir.glob("*.jpg")) + list(img_dir.glob("*.png"))
            missing = [img for img in images if not (lbl_dir / (img.stem + ".txt")).exists()]
            if not missing:
                logger.info("[Dataset] %s 라벨 이미 존재 (%d장)", img_dir.name, len(images))
                continue

            logger.info("[Dataset] %s — 라벨 자동 생성 시작 (%d장)", img_dir.name, len(missing))
            if detector is None:
                detector = YOLO(_FACE_DETECTOR_MODEL)

            for img_path in missing:
                self._auto_label(detector, img_path, lbl_dir)

    def _auto_label(self, detector: YOLO, img_path: Path, lbl_dir: Path) -> None:
        img = cv2.imread(str(img_path))
        if img is None:
            logger.warning("[Dataset] 이미지 읽기 실패: %s", img_path.name)
            return

        results = detector(img, verbose=False)
        boxes = results[0].boxes
        lbl_path = lbl_dir / (img_path.stem + ".txt")
        lines: list[str] = []
        for box in boxes:
            x_c, y_c, bw, bh = box.xywhn[0].tolist()
            lines.append(f"0 {x_c:.6f} {y_c:.6f} {bw:.6f} {bh:.6f}")
        lbl_path.write_text("\n".join(lines))

    def _write_yaml(self) -> None:
        yaml_content = f"""path: {self._root.as_posix()}
train: train
val: val

nc: 1
names:
  0: face
"""
        self._yaml_path.write_text(yaml_content, encoding="utf-8")
        logger.info("[Dataset] data.yaml 작성 완료: %s", self._yaml_path)
