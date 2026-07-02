from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class NodeType(str, Enum):
    EMAIL = "Email"
    SPAM_CATEGORY = "SpamCategory"
    LEGITIMATE_CATEGORY = "LegitimateCategory"
    KEYWORD = "Keyword"
    PATTERN = "Pattern"


class SpamCategory(str, Enum):
    PHISHING = "Phishing"
    ADVERTISING = "Advertising"
    MALWARE = "Malware"
    SCAM = "Scam"
    SOCIAL_ENGINEERING = "SocialEngineering"


class LegitimateCategory(str, Enum):
    TRANSACTIONAL = "Transactional"
    NEWSLETTER = "Newsletter"
    PERSONAL = "Personal"
    WORK = "Work"


@dataclass
class OntologyNode:
    id: str
    node_type: NodeType
    label: str
    properties: dict = field(default_factory=dict)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, OntologyNode):
            return NotImplemented
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)
