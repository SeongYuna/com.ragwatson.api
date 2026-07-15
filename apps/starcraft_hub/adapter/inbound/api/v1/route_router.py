from __future__ import annotations

from fastapi import APIRouter, Depends

from starcraft_hub.adapter.inbound.api.schemas.route_schema import (
    RouteRequest,
    RouteResponse,
)
from starcraft_hub.app.dtos.route_dto import RouteQueryCommand
from starcraft_hub.app.ports.input.route_port import RoutePort
from starcraft_hub.dependencies.route_provider import get_route_use_case

router = APIRouter(prefix="/starcraft/router", tags=["starcraft"])


@router.post("/semantic", response_model=RouteResponse)
async def route_query(
    body: RouteRequest,
    use_case: RoutePort = Depends(get_route_use_case),
) -> RouteResponse:
    command = RouteQueryCommand(question=body.question)
    result = await use_case.route(command)
    return RouteResponse(
        destination=result.destination.value,
        entities=result.entities,
    )
