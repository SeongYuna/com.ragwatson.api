from __future__ import annotations

from fastapi import APIRouter, Depends

from starcraft_hub.adapter.inbound.api.schemas.classify_schema import (
    ClassifyRequest,
    ClassifyResponse,
)
from starcraft_hub.app.dtos.classify_dto import ClassifyEmailCommand
from starcraft_hub.app.ports.input.classify_port import ClassifyPort
from starcraft_hub.dependencies.classify_provider import get_classify_use_case

router = APIRouter(prefix="/starcraft/ontology", tags=["starcraft"])


@router.post("/classify", response_model=ClassifyResponse)
async def classify_email(
    body: ClassifyRequest,
    use_case: ClassifyPort = Depends(get_classify_use_case),
) -> ClassifyResponse:
    command = ClassifyEmailCommand(
        subject=body.subject,
        body=body.body,
        sender=body.sender,
    )
    result = await use_case.classify(command)
    return ClassifyResponse(
        is_spam=result.is_spam,
        category=result.category,
        confidence=result.confidence,
        score=result.score,
        reasoning=result.reasoning,
    )
