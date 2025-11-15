"""
Enhanced thought graph example demonstrating web enrichment, project matching,
edge weight management, and the full memify pipeline.
"""

import asyncio
import cognee
from cognee.modules.thought_graph.operations import (
    add_thoughts_batch,
    memify_thoughts,
    enrich_with_web_search,
    match_to_projects,
    decay_edge_weights,
    calculate_potential_connections
)
from cognee.shared.logging_utils import setup_logging, INFO


async def main():
    """Run enhanced thought graph example with all new features."""
    print("=" * 80)
    print("Enhanced ADHD Thought Graph Example")
    print("Web Enrichment • Project Matching • Edge Weight Decay • Memify")
    print("=" * 80)
    print()
    
    # Setup
    print("Setting up cognee...")
    await cognee.prune.prune_data()
    await cognee.prune.prune_system(metadata=True)
    print("✓ Clean slate ready\n")
    
    # =========================================================================
    # PHASE 1: Capture Thoughts with Project Context
    # =========================================================================
    print("=" * 80)
    print("PHASE 1: Capturing thoughts with project context")
    print("=" * 80)
    print()
    
    thoughts_data = [
        {
            "content": "Need to implement web search enrichment for cognee thought graphs",
            "title": "Web Search Feature",
            "tags": ["cognee", "feature", "web-search"],
            "related_projects": ["cognee"],
            "importance_score": 9
        },
        {
            "content": "Edge weights should decay over time if not reinforced",
            "title": "Edge Weight Decay",
            "tags": ["cognee", "graph-algorithms", "maintenance"],
            "related_projects": ["cognee"],
            "importance_score": 8
        },
        {
            "content": "Match thoughts to GitHub repositories automatically",
            "title": "Repository Matching",
            "tags": ["github", "automation", "integration"],
            "related_projects": ["cognee", "github-integration"],
            "importance_score": 7
        },
        {
            "content": "ADHD brains need automatic connection discovery",
            "title": "ADHD Auto-Discovery",
            "tags": ["adhd", "productivity", "automation"],
            "importance_score": 9
        },
        {
            "content": "Tavily API can be used for deep web research",
            "title": "Tavily Integration",
            "tags": ["tavily", "web-search", "api"],
            "related_projects": ["cognee"],
            "importance_score": 6
        }
    ]
    
    thoughts = await add_thoughts_batch(thoughts_data, auto_connect=True)
    print(f"✓ Captured {len(thoughts)} thoughts")
    print(f"✓ Auto-discovered initial connections\n")
    
    # =========================================================================
    # PHASE 2: Web Enrichment (Single Thought Example)
    # =========================================================================
    print("=" * 80)
    print("PHASE 2: Web Enrichment Example")
    print("=" * 80)
    print()
    
    if thoughts:
        print("Enriching first thought with web search...")
        print(f"Thought: '{thoughts[0].title}'")
        print()
        
        # Note: This requires TAVILY_API_KEY environment variable
        web_results = await enrich_with_web_search(
            thought_id=thoughts[0].id,
            max_results=3,
            search_depth="basic"
        )
        
        print(f"✓ Found {len(web_results['search_results'])} web resources")
        print(f"✓ Created {web_results['connections_created']} connections")
        print(f"✓ Added {web_results['content_added']} characters of content\n")
    
    # =========================================================================
    # PHASE 3: Project Matching
    # =========================================================================
    print("=" * 80)
    print("PHASE 3: Project Matching")
    print("=" * 80)
    print()
    
    print("Matching thoughts to projects...")
    
    project_patterns = {
        "cognee": ["cognee", "knowledge graph", "thought graph", "memory"],
        "github-integration": ["github", "repository", "repo"],
        "web-enrichment": ["tavily", "web search", "scraping"],
        "adhd-tools": ["adhd", "productivity", "brainfog"]
    }
    
    match_results = await match_to_projects(
        auto_detect=True,
        project_patterns=project_patterns
    )
    
    print(f"✓ Matched {match_results['thoughts_matched']} thoughts")
    print(f"✓ Found {len(match_results['projects_found'])} projects:")
    for project in sorted(match_results['projects_found']):
        thought_count = sum(1 for m in match_results['matches'] if m[1] == project)
        print(f"  - {project}: {thought_count} thoughts")
    print()
    
    # =========================================================================
    # PHASE 4: Edge Weight Management
    # =========================================================================
    print("=" * 80)
    print("PHASE 4: Edge Weight Decay & Management")
    print("=" * 80)
    print()
    
    print("Applying edge weight decay...")
    
    decay_results = await decay_edge_weights(
        decay_rate=0.1,
        min_weight=0.15,
        time_based=True,
        days_threshold=30
    )
    
    print(f"✓ Decayed {decay_results['edges_decayed']} edges")
    print(f"✓ Removed {decay_results['edges_removed']} weak connections")
    print(f"✓ Avg weight before: {decay_results['avg_weight_before']:.3f}")
    print(f"✓ Avg weight after: {decay_results['avg_weight_after']:.3f}\n")
    
    # Calculate potential connections
    if thoughts:
        print("Calculating potential connections...")
        
        potentials = await calculate_potential_connections(
            thought_id=thoughts[0].id,
            min_potential_weight=0.3,
            max_results=5
        )
        
        print(f"✓ Found {len(potentials)} potential connections:")
        for target_id, weight, reason in potentials[:3]:
            print(f"  - Weight {weight:.2f}: {reason}")
        print()
    
    # =========================================================================
    # PHASE 5: Full Memify Pipeline
    # =========================================================================
    print("=" * 80)
    print("PHASE 5: Enhanced Memify Pipeline")
    print("=" * 80)
    print()
    
    print("Running full memify enrichment...")
    print("(This includes graph algorithms, web enrichment, project matching,")
    print(" edge decay, and potential connection discovery)")
    print()
    
    memify_results = await memify_thoughts(
        thought_ids=[t.id for t in thoughts] if thoughts else None,
        enable_web_enrichment=False,  # Set to True with TAVILY_API_KEY
        enable_project_matching=True,
        enable_edge_decay=True,
        enable_potential_connections=True,
        project_patterns=project_patterns,
        decay_rate=0.05,
        min_edge_weight=0.1
    )
    
    print("✓ Memify complete!\n")
    
    # Display results
    print("Graph Enrichment:")
    graph_enrich = memify_results.get("graph_enrichment", {})
    print(f"  - Nodes enriched: {graph_enrich.get('nodes_enriched', 0)}")
    print(f"  - PageRank computed: {graph_enrich.get('pagerank_computed', False)}")
    print(f"  - Communities detected: {graph_enrich.get('communities_detected', 0)}")
    print(f"  - Transitive connections: {graph_enrich.get('transitive_found', 0)}")
    print()
    
    print("Project Matching:")
    project_match = memify_results.get("project_matching", {})
    print(f"  - Thoughts matched: {project_match.get('thoughts_matched', 0)}")
    print(f"  - Projects found: {len(project_match.get('projects_found', set()))}")
    print()
    
    print("Edge Management:")
    edge_mgmt = memify_results.get("edge_management", {})
    print(f"  - Edges decayed: {edge_mgmt.get('edges_decayed', 0)}")
    print(f"  - Edges removed: {edge_mgmt.get('edges_removed', 0)}")
    print()
    
    print("Potential Connections:")
    print(f"  - Found: {memify_results.get('potential_connections', 0)}")
    print()
    
    # =========================================================================
    # PHASE 6: Use Cases Summary
    # =========================================================================
    print("=" * 80)
    print("PHASE 6: Use Cases & Capabilities")
    print("=" * 80)
    print()
    
    print("This enhanced thought graph system supports:")
    print()
    
    print("1. WEB ENRICHMENT")
    print("   - Automatically search for related web content")
    print("   - Deep research using Tavily API")
    print("   - Scrape specific URLs for context")
    print("   - Link thoughts to external knowledge")
    print()
    
    print("2. PROJECT MATCHING")
    print("   - Auto-detect project/repository mentions")
    print("   - Match thoughts to GitHub/GitLab repos")
    print("   - Group thoughts by project affiliation")
    print("   - Track project-related ideas")
    print()
    
    print("3. EDGE WEIGHT MANAGEMENT")
    print("   - Time-based weight decay")
    print("   - Remove weak/stale connections")
    print("   - Reinforce important connections")
    print("   - Keep graph fresh and relevant")
    print()
    
    print("4. POTENTIAL CONNECTIONS")
    print("   - Discover missing links")
    print("   - Calculate connection likelihood")
    print("   - Suggest new relationships")
    print("   - Strengthen graph connectivity")
    print()
    
    print("5. INTEGRATED MEMIFY")
    print("   - One command for full enrichment")
    print("   - Combines all enrichment methods")
    print("   - Periodic maintenance automation")
    print("   - ADHD-optimized workflow")
    print()
    
    # =========================================================================
    # Summary
    # =========================================================================
    print("=" * 80)
    print("Summary")
    print("=" * 80)
    print()
    
    print("The enhanced thought graph system now includes:")
    print()
    print("✓ Web enrichment with search & scraping")
    print("✓ Automatic project/repository matching")
    print("✓ Edge weight decay and reinforcement")
    print("✓ Potential connection discovery")
    print("✓ Integrated memify pipeline")
    print()
    
    print("Use Cases:")
    print("- Research assistance: Enrich ideas with web knowledge")
    print("- Project management: Track thoughts by project")
    print("- Graph maintenance: Keep connections relevant")
    print("- Knowledge discovery: Find hidden connections")
    print("- ADHD support: Automatic organization & enrichment")
    print()
    
    print("Next Steps:")
    print("1. Set TAVILY_API_KEY for web enrichment")
    print("2. Run memify_thoughts() periodically")
    print("3. Review potential connections")
    print("4. Reinforce valuable connections")
    print("5. Let weak connections decay naturally")
    print()


if __name__ == "__main__":
    logger = setup_logging(log_level=INFO)
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(main())
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
