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

__all__ = [
    "discover_connections",
    "find_surprise_connections",
    "get_thought_neighbors",
    "enrich_thought_graph",
]
