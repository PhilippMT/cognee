"""
Thought Graph Module for ADHD-optimized idea management.

This module provides functionality for managing interconnected ideas and thoughts,
with a focus on discovering hidden connections, transitive relationships, and
surprising associations that are especially valuable for ADHD thought patterns.
"""

from .operations.discover_connections import discover_connections
from .operations.find_surprise_connections import find_surprise_connections
from .operations.get_thought_neighbors import get_thought_neighbors
from .operations.enrich_thought_graph import enrich_thought_graph
from .operations.add_thought import add_thought, add_thoughts_batch
from .operations.enrich_with_web import enrich_with_web_search, enrich_with_scraped_content
from .operations.match_projects import match_to_projects, create_project_connections
from .operations.edge_weight_management import decay_edge_weights, calculate_potential_connections
from .operations.memify_thoughts import memify_thoughts, cognify_and_memify_thoughts

__all__ = [
    "discover_connections",
    "find_surprise_connections",
    "get_thought_neighbors",
    "enrich_thought_graph",
    "add_thought",
    "add_thoughts_batch",
    "enrich_with_web_search",
    "enrich_with_scraped_content",
    "match_to_projects",
    "create_project_connections",
    "decay_edge_weights",
    "calculate_potential_connections",
    "memify_thoughts",
    "cognify_and_memify_thoughts",
]
