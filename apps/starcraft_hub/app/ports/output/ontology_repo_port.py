from __future__ import annotations

from abc import ABC, abstractmethod

from starcraft_hub.domain.entities.ontology_node import OntologyNode


class OntologyRepoPort(ABC):
    @abstractmethod
    async def get_spam_categories(self) -> list[OntologyNode]:
        ...

    @abstractmethod
    async def get_keywords_for_category(self, category: str) -> list[str]:
        ...

    @abstractmethod
    async def save_classification(
        self,
        email_id: str,
        category: str,
        score: float,
    ) -> None:
        ...
