from __future__ import annotations

import os

from neo4j import AsyncGraphDatabase

from core.lol.t1_mid_faker_orchestrator import faker_orchestrator
from starcraft_hub.adapter.outbound.neo4j.ontology_neo4j_repo import OntologyNeo4jRepo
from starcraft_hub.app.ports.input.classify_port import ClassifyPort
from starcraft_hub.app.use_cases.classify_spam_interactor import ClassifySpamInteractor

_NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
_NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
_NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "ragwatson")

_driver = AsyncGraphDatabase.driver(_NEO4J_URI, auth=(_NEO4J_USER, _NEO4J_PASSWORD))


def get_classify_use_case() -> ClassifyPort:
    return ClassifySpamInteractor(
        orchestrator=faker_orchestrator,
        ontology_repo=OntologyNeo4jRepo(driver=_driver),
    )
