"""
Knowledge Graph (§16)
Models multi-relational ontology connecting texts, verses, concepts, commentators,
sampradāyas, and claims. Explicitly designed to hold contradiction and uncertainty.
"""

from enum import Enum
from typing import List, Dict, Optional, Set, Any
from pydantic import BaseModel, Field


class EntityType(str, Enum):
    TEXT = "TEXT"
    VERSE = "VERSE"
    TERM = "TERM"
    CONCEPT = "CONCEPT"
    PERSON = "PERSON"
    COMMENTATOR = "COMMENTATOR"
    SAMPRADAYA = "SAMPRADĀYA"
    TRADITION = "TRADITION"
    EVENT = "EVENT"
    PLACE = "PLACE"
    RITUAL = "RITUAL"
    ART = "ART"
    SOURCE = "SOURCE"
    CLAIM = "CLAIM"
    INTERPRETATION = "INTERPRETATION"
    HISTORICAL_ASSERTION = "HISTORICAL_ASSERTION"
    LANGUAGE = "LANGUAGE"


class RelationType(str, Enum):
    CONTAINS = "contains"
    DISCUSSES = "discusses"
    COMMENTS_ON = "comments_on"
    INTERPRETS = "interprets"
    SUPPORTS = "supports"
    DISPUTES = "disputes"
    TRANSLATES_TO = "translates_to"
    BELONGS_TO = "belongs_to"
    AUTHORED_OR_COMMENTED = "authored/commented_on"
    PARALLELS = "parallels"


class GraphNode(BaseModel):
    node_id: str
    entity_type: EntityType
    label: str
    metadata: Dict[str, Any] = Field(default_factory=dict)


class GraphEdge(BaseModel):
    source_id: str
    target_id: str
    relation: RelationType
    is_disputed: bool = False
    notes: Optional[str] = None


class KnowledgeGraph:
    """Directed graph capable of storing multiple interpretations, contradictions, and parallels."""

    def __init__(self):
        self.nodes: Dict[str, GraphNode] = {}
        self.edges: List[GraphEdge] = []

    def add_node(self, node: GraphNode) -> None:
        self.nodes[node.node_id] = node

    def add_edge(self, edge: GraphEdge) -> None:
        self.edges.append(edge)

    def get_neighbors(self, node_id: str, relation: Optional[RelationType] = None) -> List[GraphNode]:
        target_ids = []
        for edge in self.edges:
            if edge.source_id == node_id:
                if relation is None or edge.relation == relation:
                    target_ids.append(edge.target_id)
        return [self.nodes[t] for t in target_ids if t in self.nodes]

    def traverse_connections(self, start_node_id: str, depth: int = 2) -> Dict[str, Any]:
        """Traverses concepts, parallels, and commentaries from an initial verse/text node."""
        visited: Set[str] = set()
        subgraph: Dict[str, Any] = {"start_node": start_node_id, "nodes": [], "edges": []}

        def _dfs(current_id: str, current_depth: int):
            if current_depth > depth or current_id in visited:
                return
            visited.add(current_id)

            if current_id in self.nodes:
                subgraph["nodes"].append(self.nodes[current_id].model_dump())

            for edge in self.edges:
                if edge.source_id == current_id:
                    subgraph["edges"].append(edge.model_dump())
                    _dfs(edge.target_id, current_depth + 1)
                elif edge.target_id == current_id:
                    subgraph["edges"].append(edge.model_dump())
                    _dfs(edge.source_id, current_depth + 1)

        _dfs(start_node_id, 0)
        return subgraph
