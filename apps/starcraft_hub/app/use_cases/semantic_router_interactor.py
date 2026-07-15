from __future__ import annotations

import json
import re

from core.lol.orchestrator_port import (
    OrchestratorMessage,
    OrchestratorPort,
    OrchestratorRequest,
)
from starcraft_hub.app.dtos.route_dto import RouteQueryCommand, RouteQueryResult
from starcraft_hub.app.ports.input.route_port import RoutePort
from starcraft_hub.domain.value_objects.route_destination import RouteDestination

_SYSTEM_PROMPT = """너는 입력된 질문의 의도를 파악하는 똑똑한 분류 비서야.
아래 지정된 JSON 형식으로만 응답해줘. 다른 친절한 설명이나 텍스트는 절대 붙이지 마.

출력 JSON 스키마:
{"destination": "crud" | "exaone_rag" | "gemini", "entities": ["질문 속 핵심 단어나 고유명사"]}

[분류 기준]
- 사용자가 데이터 생성, 수정, 삭제를 명확히 요구할 때: "crud"
- 스타 토폴로지 내 노드 관계, 사내 전문 도메인 지식 질문: "exaone_rag"
- 일상 대화, 인사, 일반 상식 등 사내 정보가 필요 없는 질문: "gemini"

[예시]
질문: "회사 인프라 서버 사양이 어떻게 돼?"
답변: {"destination": "exaone_rag", "entities": ["인프라 서버", "사양"]}"""


class SemanticRouterInteractor(RoutePort):
    def __init__(self, orchestrator: OrchestratorPort) -> None:
        self._orchestrator = orchestrator

    async def route(self, command: RouteQueryCommand) -> RouteQueryResult:
        request = OrchestratorRequest(
            messages=[
                OrchestratorMessage(role="system", content=_SYSTEM_PROMPT),
                OrchestratorMessage(role="user", content=command.question),
            ]
        )
        response = await self._orchestrator.chat(request)
        return self._parse(response.content)

    @staticmethod
    def _parse(content: str) -> RouteQueryResult:
        match = re.search(r"\{.*\}", content, re.DOTALL)
        if match:
            try:
                decision = json.loads(match.group())
                return RouteQueryResult(
                    destination=RouteDestination(decision["destination"]),
                    entities=decision.get("entities", []),
                )
            except (json.JSONDecodeError, KeyError, ValueError):
                pass

        return RouteQueryResult(destination=RouteDestination.EXAONE_RAG, entities=[])
