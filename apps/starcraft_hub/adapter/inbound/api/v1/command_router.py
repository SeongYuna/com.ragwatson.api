from __future__ import annotations

from fastapi import APIRouter, Depends

from starcraft_hub.adapter.inbound.api.schemas.command_schema import (
    CommandRequest,
    CommandResponse,
)
from starcraft_hub.app.dtos.command_dto import ExecuteCommandCommand
from starcraft_hub.app.ports.input.command_port import CommandPort
from starcraft_hub.dependencies.command_provider import get_command_use_case

router = APIRouter(prefix="/starcraft/command", tags=["starcraft"])


@router.post("/run", response_model=CommandResponse)
async def run_command(
    body: CommandRequest,
    use_case: CommandPort = Depends(get_command_use_case),
) -> CommandResponse:
    result = await use_case.execute(ExecuteCommandCommand(text=body.text))
    return CommandResponse(
        action=result.action,
        websites=result.websites,
        keywords=result.keywords,
        count=result.count,
        saved_files=result.saved_files,
    )
