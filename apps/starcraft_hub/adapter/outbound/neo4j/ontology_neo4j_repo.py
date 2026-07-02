from __future__ import annotations

from neo4j import AsyncDriver

from starcraft_hub.app.ports.output.ontology_repo_port import OntologyRepoPort
from starcraft_hub.domain.entities.ontology_node import NodeType, OntologyNode


class OntologyNeo4jRepo(OntologyRepoPort):
    def __init__(self, driver: AsyncDriver) -> None:
        self._driver = driver

    async def get_spam_categories(self) -> list[OntologyNode]:
        query = "MATCH (n:SpamCategory) RETURN n.id AS id, n.label AS label"
        async with self._driver.session() as session:
            result = await session.run(query)
            records = await result.data()
        return [
            OntologyNode(id=r["id"], node_type=NodeType.SPAM_CATEGORY, label=r["label"])
            for r in records
        ]

    async def get_keywords_for_category(self, category: str) -> list[str]:
        query = (
            "MATCH (:SpamCategory {label: $category})-[:indicatedBy]->(k:Keyword) "
            "RETURN k.value AS keyword"
        )
        async with self._driver.session() as session:
            result = await session.run(query, category=category)
            records = await result.data()
        return [r["keyword"] for r in records]

    async def save_classification(
        self,
        email_id: str,
        category: str,
        score: float,
    ) -> None:
        query = (
            "MERGE (e:Email {id: $email_id}) "
            "MERGE (c:SpamCategory {label: $category}) "
            "MERGE (e)-[r:hasCategory]->(c) "
            "SET r.score = $score, r.classified_at = datetime()"
        )
        async with self._driver.session() as session:
            await session.run(query, email_id=email_id, category=category, score=score)
