from lenna_vision.app.ports.input.yolo_inference_use_case import YoloInferenceUseCase
from lenna_vision.app.use_cases.yolo_inference_interactor import YoloInferenceInteractor


def get_yolo_inference_use_case() -> YoloInferenceUseCase:
    from lenna_vision.adapter.outbound.resource_adapters.yolo.yolo_inference_adapter import YoloInferenceAdapter
    return YoloInferenceInteractor(
        inference_port=YoloInferenceAdapter(),
    )
