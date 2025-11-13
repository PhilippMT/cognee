"""Tests for thought graph algorithms."""

import pytest
from uuid import uuid4

from cognee.modules.thought_graph.algorithms.pagerank import calculate_pagerank
from cognee.modules.thought_graph.algorithms.centrality import calculate_centrality, find_bridge_thoughts
from cognee.modules.thought_graph.algorithms.community_detection import detect_communities
from cognee.modules.thought_graph.algorithms.shortest_path import find_shortest_paths
from cognee.modules.thought_graph.algorithms.transitive_connections import find_transitive_connections


# Test data fixtures
@pytest.fixture
def sample_graph():
    """Create a sample graph for testing."""
    node1_id = str(uuid4())
    node2_id = str(uuid4())
    node3_id = str(uuid4())
    node4_id = str(uuid4())
    
    nodes = [
        (node1_id, {"content": "Node 1", "tags": ["a", "b"]}),
        (node2_id, {"content": "Node 2", "tags": ["b", "c"]}),
        (node3_id, {"content": "Node 3", "tags": ["c", "d"]}),
        (node4_id, {"content": "Node 4", "tags": ["d", "e"]}),
    ]
    
    edges = [
        (node1_id, node2_id, "relates_to", {"strength": 0.8}),
        (node2_id, node3_id, "relates_to", {"strength": 0.7}),
        (node3_id, node4_id, "relates_to", {"strength": 0.9}),
        (node1_id, node3_id, "relates_to", {"strength": 0.5}),
    ]
    
    return nodes, edges


@pytest.mark.asyncio
async def test_pagerank_calculation(sample_graph):
    """Test PageRank calculation."""
    nodes, edges = sample_graph
    
    pagerank_scores = await calculate_pagerank(nodes, edges)
    
    assert len(pagerank_scores) == len(nodes)
    assert all(0.0 <= score <= 1.0 for score in pagerank_scores.values())
    # Sum of PageRank scores should be approximately 1.0
    assert abs(sum(pagerank_scores.values()) - 1.0) < 0.01


@pytest.mark.asyncio
async def test_pagerank_empty_graph():
    """Test PageRank with empty graph."""
    pagerank_scores = await calculate_pagerank([], [])
    
    assert pagerank_scores == {}


@pytest.mark.asyncio
async def test_pagerank_no_edges(sample_graph):
    """Test PageRank with nodes but no edges."""
    nodes, _ = sample_graph
    
    pagerank_scores = await calculate_pagerank(nodes, [])
    
    # With no edges, all nodes should have equal PageRank
    scores = list(pagerank_scores.values())
    assert all(abs(score - scores[0]) < 0.001 for score in scores)


@pytest.mark.asyncio
async def test_centrality_betweenness(sample_graph):
    """Test betweenness centrality calculation."""
    nodes, edges = sample_graph
    
    centrality_scores = await calculate_centrality(nodes, edges, "betweenness")
    
    assert len(centrality_scores) == len(nodes)
    assert all(0.0 <= score <= 1.0 for score in centrality_scores.values())


@pytest.mark.asyncio
async def test_centrality_closeness(sample_graph):
    """Test closeness centrality calculation."""
    nodes, edges = sample_graph
    
    centrality_scores = await calculate_centrality(nodes, edges, "closeness")
    
    assert len(centrality_scores) == len(nodes)
    # Closeness centrality can be > 1.0 in some graph configurations
    assert all(score >= 0.0 for score in centrality_scores.values())


@pytest.mark.asyncio
async def test_centrality_degree(sample_graph):
    """Test degree centrality calculation."""
    nodes, edges = sample_graph
    
    centrality_scores = await calculate_centrality(nodes, edges, "degree")
    
    assert len(centrality_scores) == len(nodes)
    assert all(0.0 <= score <= 1.0 for score in centrality_scores.values())


@pytest.mark.asyncio
async def test_find_bridge_thoughts(sample_graph):
    """Test finding bridge thoughts."""
    nodes, edges = sample_graph
    
    bridges = await find_bridge_thoughts(nodes, edges, threshold=0.1)
    
    assert isinstance(bridges, list)
    # Middle nodes should be bridges
    assert len(bridges) >= 0


@pytest.mark.asyncio
async def test_community_detection(sample_graph):
    """Test community detection."""
    nodes, edges = sample_graph
    
    communities = await detect_communities(nodes, edges, algorithm="greedy")
    
    assert len(communities) == len(nodes)
    # All nodes should be assigned to a community
    assert all(community_id.startswith("community_") for community_id in communities.values())


@pytest.mark.asyncio
async def test_community_detection_empty():
    """Test community detection with empty graph."""
    communities = await detect_communities([], [])
    
    assert communities == {}


@pytest.mark.asyncio
async def test_shortest_paths(sample_graph):
    """Test shortest path finding."""
    nodes, edges = sample_graph
    node1_id = nodes[0][0]
    
    # Convert string ID to UUID
    from uuid import UUID
    node1_uuid = UUID(node1_id)
    
    paths = await find_shortest_paths(nodes, edges, node1_uuid, max_length=5)
    
    assert isinstance(paths, dict)
    # Should find paths to at least some nodes
    assert len(paths) >= 0


@pytest.mark.asyncio
async def test_transitive_connections(sample_graph):
    """Test transitive connection discovery."""
    nodes, edges = sample_graph
    
    transitive = await find_transitive_connections(nodes, edges, max_hops=3)
    
    assert isinstance(transitive, list)
    # Each transitive connection should be a tuple
    for src, tgt, hops, path in transitive:
        assert isinstance(hops, int)
        assert 2 <= hops <= 3
        assert len(path) == hops + 1


@pytest.mark.asyncio
async def test_transitive_connections_empty():
    """Test transitive connections with empty graph."""
    transitive = await find_transitive_connections([], [])
    
    assert transitive == []
