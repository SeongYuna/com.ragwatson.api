from __future__ import annotations

from core.lol.t1_mid_faker_orchestrator import faker_orchestrator
from starcraft_hub.app.ports.input.command_port import CommandPort
from starcraft_hub.app.use_cases.command_interactor import CommandInteractor
from starcraft_hub.dependencies.crawler_provider import get_crawler_use_case
from starcraft_hub.dependencies.scrapper_provider import get_scrapper_use_case


def get_command_use_case() -> CommandPort:
    return CommandInteractor(
        orchestrator=faker_orchestrator,
        crawler=get_crawler_use_case(),
        scrapper=get_scrapper_use_case(),
    )
