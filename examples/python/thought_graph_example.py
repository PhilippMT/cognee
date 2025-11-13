"""
Example demonstrating the ADHD-optimized thought graph system.

This example shows how to:
1. Quickly capture scattered thoughts
2. Automatically discover connections between them
3. Enrich the graph with insights (PageRank, communities, etc.)
4. Find surprise connections
5. Visualize the thought network

Perfect for managing ADHD brainfog and brainchaos!
"""

import asyncio
import os
from pathlib import Path

import cognee
from cognee.modules.thought_graph.operations.add_thought import add_thought, add_thoughts_batch
from cognee.modules.thought_graph.operations.enrich_thought_graph import enrich_thought_graph
from cognee.modules.thought_graph.operations.find_surprise_connections import find_surprise_connections
from cognee.modules.thought_graph.operations.get_thought_communities import get_thought_communities
from cognee.shared.logging_utils import setup_logging, INFO


async def main():
    """Run the thought graph example."""
    print("=" * 80)
    print("ADHD Thought Graph Example")
    print("Managing brainfog and brainchaos with automatic connection discovery")
    print("=" * 80)
    print()
    
    # Setup
    print("Setting up cognee...")
    await cognee.prune.prune_data()
    await cognee.prune.prune_system(metadata=True)
    print("✓ Clean slate ready\n")
    
    # =========================================================================
    # PHASE 1: Rapid Thought Capture
    # =========================================================================
    print("=" * 80)
    print("PHASE 1: Rapid Thought Capture (ADHD-friendly quick capture)")
    print("=" * 80)
    print()
    
    # Simulate a brainstorming session with scattered ADHD thoughts
    thoughts_data = [
        {
            "content": "Build a knowledge graph system for managing scattered thoughts and ideas",
            "title": "Knowledge Graph System",
            "tags": ["project", "ai", "productivity"],
            "importance_score": 9,
            "energy_level": 8,
        },
        {
            "content": "ADHD brains work differently - non-linear, associative thinking patterns",
            "title": "ADHD Brain Patterns",
            "tags": ["adhd", "neuroscience", "learning"],
            "importance_score": 8,
        },
        {
            "content": "Need a better way to capture ideas when they suddenly appear",
            "title": "Quick Capture Tool",
            "tags": ["productivity", "adhd", "tools"],
            "importance_score": 7,
            "context": "Thought appeared while driving",
        },
        {
            "content": "Graph databases are perfect for representing non-hierarchical relationships",
            "title": "Graph Database Benefits",
            "tags": ["database", "technology", "graphs"],
            "importance_score": 6,
        },
        {
            "content": "Obsidian and Roam Research use bidirectional links - but could be smarter",
            "title": "PKM Tool Inspiration",
            "tags": ["tools", "productivity", "notes"],
            "importance_score": 7,
        },
        {
            "content": "PageRank algorithm could identify the most important thoughts in my network",
            "title": "Using PageRank",
            "tags": ["algorithms", "ai", "graphs"],
            "importance_score": 6,
        },
        {
            "content": "Community detection might reveal thematic clusters in my scattered ideas",
            "title": "Community Detection",
            "tags": ["algorithms", "ai", "organization"],
            "importance_score": 6,
        },
        {
            "content": "Sometimes the best ideas come from unexpected connections between topics",
            "title": "Serendipitous Discovery",
            "tags": ["creativity", "learning", "innovation"],
            "importance_score": 8,
        },
        {
            "content": "Working memory issues make it hard to hold multiple ideas at once",
            "title": "Working Memory Challenges",
            "tags": ["adhd", "neuroscience", "challenges"],
            "importance_score": 7,
        },
        {
            "content": "External brain systems compensate for ADHD working memory limitations",
            "title": "External Brain Concept",
            "tags": ["adhd", "productivity", "tools"],
            "importance_score": 9,
        },
    ]
    
    print(f"Capturing {len(thoughts_data)} thoughts from a brainstorming session...\n")
    
    # Add thoughts in batch (fast!)
    thoughts = await add_thoughts_batch(thoughts_data, auto_connect=True)
    
    print(f"✓ Captured {len(thoughts)} thoughts")
    print(f"✓ Auto-discovered initial connections\n")
    
    # Show some captured thoughts
    print("Sample captured thoughts:")
    for i, thought in enumerate(thoughts[:3], 1):
        print(f"{i}. {thought.title}")
        print(f"   Tags: {', '.join(thought.tags)}")
        print(f"   Importance: {thought.importance_score}/10")
        print()
    
    # =========================================================================
    # PHASE 2: Graph Enrichment
    # =========================================================================
    print("=" * 80)
    print("PHASE 2: Graph Enrichment (Discovering hidden patterns)")
    print("=" * 80)
    print()
    
    print("Running enrichment algorithms...")
    print("- Computing PageRank (influential thoughts)")
    print("- Computing Centrality (bridge ideas)")
    print("- Detecting Communities (thematic clusters)")
    print("- Finding Transitive Connections (hidden links)")
    print()
    
    enrichment_results = await enrich_thought_graph(
        compute_pagerank=True,
        compute_centrality=True,
        detect_communities_flag=True,
        find_transitive=True,
        auto_add_transitive_links=True,
        transitive_strength_threshold=0.3
    )
    
    print("✓ Enrichment complete!")
    print(f"  - Enriched {enrichment_results['nodes_enriched']} thought nodes")
    print(f"  - Detected {enrichment_results['communities_detected']} thematic communities")
    print(f"  - Found {enrichment_results['transitive_found']} transitive connections")
    print(f"  - Added {enrichment_results['transitive_added']} new connection links")
    print()
    
    # =========================================================================
    # PHASE 3: Community Analysis
    # =========================================================================
    print("=" * 80)
    print("PHASE 3: Community Analysis (Organizing the chaos)")
    print("=" * 80)
    print()
    
    communities = await get_thought_communities(include_summary=True)
    
    print(f"Your thoughts organized into {communities['total_communities']} communities:\n")
    
    for community_id, summary in communities["summaries"].items():
        print(f"Community: {community_id}")
        print(f"  Size: {summary['size']} thoughts")
        if summary['top_tags']:
            print(f"  Main topics: {', '.join(summary['top_tags'])}")
        if summary['avg_importance']:
            print(f"  Avg importance: {summary['avg_importance']:.1f}/10")
        print()
    
    # =========================================================================
    # PHASE 4: Surprise Connections
    # =========================================================================
    print("=" * 80)
    print("PHASE 4: Surprise Connections (Serendipitous discoveries)")
    print("=" * 80)
    print()
    
    print("Finding unexpected connections between your thoughts...\n")
    
    surprises = await find_surprise_connections(
        min_surprise_score=0.4,
        max_results=10,
        include_explanation=True
    )
    
    if surprises:
        print(f"Found {len(surprises)} surprising connections:\n")
        
        for i, surprise in enumerate(surprises[:5], 1):
            print(f"{i}. {surprise.explanation}")
            print(f"   Surprise score: {surprise.overall_score:.2f}/1.0")
            print(f"   Semantic distance: {surprise.semantic_distance:.2f}")
            print(f"   Domain distance: {surprise.domain_distance:.2f}")
            print()
    else:
        print("No surprise connections found yet. Add more diverse thoughts!")
        print()
    
    # =========================================================================
    # PHASE 5: Insights and Recommendations
    # =========================================================================
    print("=" * 80)
    print("PHASE 5: Insights & Recommendations")
    print("=" * 80)
    print()
    
    print("💡 Key Insights:")
    print()
    print("1. Your thought graph is now enriched with:")
    print("   - Importance scores (PageRank) showing which ideas are most central")
    print("   - Community structure revealing thematic organization")
    print("   - Hidden connections you might not have noticed consciously")
    print()
    
    print("2. Next steps:")
    print("   - Review surprise connections to spark new ideas")
    print("   - Develop thoughts with high PageRank scores")
    print("   - Explore isolated communities that might need more connections")
    print()
    
    print("3. ADHD-friendly features:")
    print("   ✓ Quick capture without breaking flow")
    print("   ✓ Automatic connection discovery")
    print("   ✓ Non-hierarchical organization")
    print("   ✓ Serendipitous discovery of hidden patterns")
    print("   ✓ Visual graph representation (coming soon)")
    print()
    
    # =========================================================================
    # Summary
    # =========================================================================
    print("=" * 80)
    print("Example Complete!")
    print("=" * 80)
    print()
    print("This thought graph system helps manage ADHD brainfog by:")
    print("- Capturing thoughts instantly without organizational overhead")
    print("- Automatically discovering connections you might have missed")
    print("- Revealing patterns through graph algorithms")
    print("- Highlighting surprising connections for creative insights")
    print()
    print("Keep adding thoughts and running enrichment to build your")
    print("personal knowledge graph that grows smarter over time!")
    print()


if __name__ == "__main__":
    # Setup logging
    logger = setup_logging(log_level=INFO)
    
    # Run the example
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(main())
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
