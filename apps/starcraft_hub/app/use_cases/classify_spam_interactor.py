from __future__ import annotations

from core.lol.orchestrator_port import (
    OrchestratorMessage,
    OrchestratorPort,
    OrchestratorRequest,
)
from starcraft_hub.app.dtos.classify_dto import ClassifyEmailCommand, ClassifyEmailResult
from starcraft_hub.app.ports.input.classify_port import ClassifyPort
from starcraft_hub.app.ports.output.ontology_repo_port import OntologyRepoPort
from starcraft_hub.domain.value_objects.classification_result import Confidence

_SYSTEM_PROMPT = """당신은 이메일 스팸 분류 전문가입니다.
아래 카테고리 중 하나로 분류하고 반드시 JSON으로만 응답하세요:

스팸: Phishing, Advertising, Malware, Scam, SocialEngineering
정상: Transactional, Newsletter, Personal, Work

응답 형식:
{"is_spam": true/false, "category": "<카테고리>", "score": 0.0~1.0, "reasoning": "<근거>"}"""


class ClassifySpamInteractor(ClassifyPort):
    def __init__(
        self,
        orchestrator: OrchestratorPort,
        ontology_repo: OntologyRepoPort,
    ) -> None:
        self._orchestrator = orchestrator
        self._ontology_repo = ontology_repo

    async def classify(self, command: ClassifyEmailCommand) -> ClassifyEmailResult:
        categories = await self._ontology_repo.get_spam_categories()
        category_labels = [n.label for n in categories]

        request = OrchestratorRequest(
            messages=[
                OrchestratorMessage(role="system", content=_SYSTEM_PROMPT),
                OrchestratorMessage(
                    role="user",
                    content=(
                        f"발신자: {command.sender}\n"
                        f"제목: {command.subject}\n"
                        f"본문: {command.body[:1000]}\n"
                        f"가능한 카테고리: {category_labels}"
                    ),
                ),
            ]
        )
        response = await self._orchestrator.chat(request)
        parsed = self._parse(response.content)

        await self._ontology_repo.save_classification(
            email_id=f"{command.sender}:{command.subject}",
            category=parsed["category"],
            score=parsed["score"],
        )

        return ClassifyEmailResult(
            is_spam=parsed["is_spam"],
            category=parsed["category"],
            confidence=Confidence.from_score(parsed["score"]).value,
            score=parsed["score"],
            reasoning=parsed["reasoning"],
        )

    @staticmethod
    def _parse(content: str) -> dict:
        import json
        import re

        match = re.search(r"\{.*\}", content, re.DOTALL)
        if match:
            return json.loads(match.group())
        return {
            "is_spam": False,
            "category": "Unknown",
            "score": 0.0,
            "reasoning": content,
        }
