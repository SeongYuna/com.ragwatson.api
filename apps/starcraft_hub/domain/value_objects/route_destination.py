from __future__ import annotations

from enum import Enum


class RouteDestination(str, Enum):
    CRUD = "crud"
    EXAONE_RAG = "exaone_rag"
    GEMINI = "gemini"
