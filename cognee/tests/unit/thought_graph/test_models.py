"""Tests for thought graph models."""

import pytest
from uuid import uuid4
from datetime import datetime, timezone

from cognee.modules.thought_graph.models.thought_node import ThoughtNode
from cognee.modules.thought_graph.models.connection import Connection
from cognee.modules.thought_graph.models.surprise_score import SurpriseScore


def test_thought_node_creation():
    """Test creating a ThoughtNode."""
    thought = ThoughtNode(
        id=uuid4(),
        content="Test thought about ADHD management",
        title="ADHD Test",
        tags=["adhd", "test"],
        importance_score=7
    )
    
    assert thought.content == "Test thought about ADHD management"
    assert thought.title == "ADHD Test"
    assert "adhd" in thought.tags
    assert thought.importance_score == 7
    assert thought.connection_count == 0


def test_thought_node_defaults():
    """Test ThoughtNode default values."""
    thought = ThoughtNode(
        id=uuid4(),
        content="Minimal thought"
    )
    
    assert thought.tags == []
    assert thought.related_projects == []
    assert thought.connection_count == 0
    assert thought.centrality_score is None
    assert thought.pagerank_score is None
    assert thought.community_id is None


def test_thought_node_to_dict():
    """Test converting ThoughtNode to dictionary."""
    thought = ThoughtNode(
        id=uuid4(),
        content="Test content",
        title="Test",
        tags=["test"]
    )
    
    thought_dict = thought.to_dict()
    
    assert "id" in thought_dict
    assert thought_dict["content"] == "Test content"
    assert thought_dict["title"] == "Test"
    assert thought_dict["tags"] == ["test"]


def test_connection_creation():
    """Test creating a Connection."""
    source_id = uuid4()
    target_id = uuid4()
    
    connection = Connection(
        source_id=source_id,
        target_id=target_id,
        relationship_type="relates_to",
        strength=0.8,
        discovery_method="semantic_similarity"
    )
    
    assert connection.source_id == source_id
    assert connection.target_id == target_id
    assert connection.relationship_type == "relates_to"
    assert connection.strength == 0.8
    assert connection.bidirectional is True


def test_connection_with_path():
    """Test Connection with path information."""
    intermediate_id = uuid4()
    
    connection = Connection(
        source_id=uuid4(),
        target_id=uuid4(),
        relationship_type="transitive",
        path_length=2,
        intermediate_nodes=[intermediate_id]
    )
    
    assert connection.path_length == 2
    assert len(connection.intermediate_nodes) == 1
    assert connection.intermediate_nodes[0] == intermediate_id


def test_surprise_score_creation():
    """Test creating a SurpriseScore."""
    surprise = SurpriseScore(
        source_id=uuid4(),
        target_id=uuid4(),
        overall_score=0.7,
        semantic_distance=0.8,
        temporal_distance=0.6,
        structural_distance=0.7,
        domain_distance=0.9,
        explanation="Very different topics",
        confidence=0.8
    )
    
    assert surprise.overall_score == 0.7
    assert surprise.semantic_distance == 0.8
    assert surprise.explanation == "Very different topics"
    assert surprise.confidence == 0.8


def test_surprise_score_validation():
    """Test SurpriseScore validation of scores."""
    # Test valid scores
    surprise = SurpriseScore(
        source_id=uuid4(),
        target_id=uuid4(),
        overall_score=0.5
    )
    assert 0.0 <= surprise.overall_score <= 1.0
    
    # Test invalid scores (should raise validation error)
    with pytest.raises(Exception):  # Pydantic validation error
        SurpriseScore(
            source_id=uuid4(),
            target_id=uuid4(),
            overall_score=1.5  # Invalid: > 1.0
        )
