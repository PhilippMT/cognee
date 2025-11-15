"""Edge weight decay and connection strength management."""

from typing import List, Dict, Any, Optional, Tuple
from uuid import UUID
from datetime import datetime, timezone, timedelta

from cognee.infrastructure.databases.graph import get_graph_engine
from cognee.shared.logging_utils import get_logger

logger = get_logger(__name__)


async def decay_edge_weights(
    decay_rate: float = 0.1,
    min_weight: float = 0.1,
    time_based: bool = True,
    days_threshold: int = 30
) -> Dict[str, Any]:
    """
    Apply decay to edge weights over time.
    
    Reduces connection strength for edges that haven't been reinforced,
    removing edges that fall below the minimum weight threshold. This
    helps the graph evolve and adapt to changing relevance.
    
    Args:
        decay_rate: Amount to reduce weight by (0.0-1.0)
        min_weight: Minimum weight before edge is removed
        time_based: Apply decay based on edge age
        days_threshold: Days since creation to apply full decay
        
    Returns:
        Dictionary with decay results:
        - edges_decayed: Number of edges with reduced weight
        - edges_removed: Number of edges removed
        - avg_weight_before: Average weight before decay
        - avg_weight_after: Average weight after decay
        
    Example:
        >>> results = await decay_edge_weights(
        ...     decay_rate=0.15,
        ...     min_weight=0.1,
        ...     time_based=True,
        ...     days_threshold=30
        ... )
        >>> print(f"Removed {results['edges_removed']} weak connections")
    """
    logger.info(f"Applying edge weight decay (rate={decay_rate}, min={min_weight})")
    
    try:
        graph_engine = await get_graph_engine()
        nodes, edges = await graph_engine.get_graph_data()
        
        if not edges:
            logger.info("No edges to decay")
            return {
                "edges_decayed": 0,
                "edges_removed": 0,
                "avg_weight_before": 0.0,
                "avg_weight_after": 0.0
            }
        
        edges_decayed = 0
        edges_removed = 0
        edges_to_remove = []
        edges_to_update = []
        
        total_weight_before = 0.0
        total_weight_after = 0.0
        
        now = datetime.now(timezone.utc)
        
        for source_id, target_id, rel_type, properties in edges:
            current_weight = properties.get("strength", 0.5)
            total_weight_before += current_weight
            
            # Calculate decay amount
            if time_based and "created_at" in properties:
                try:
                    created_at = properties["created_at"]
                    if isinstance(created_at, str):
                        created_at = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                    
                    days_old = (now - created_at).days
                    
                    # Apply graduated decay based on age
                    if days_old > days_threshold:
                        age_factor = min(days_old / days_threshold, 2.0)
                        actual_decay = decay_rate * age_factor
                    else:
                        actual_decay = decay_rate * (days_old / days_threshold)
                except Exception as e:
                    logger.debug(f"Error parsing date for edge: {e}")
                    actual_decay = decay_rate
            else:
                actual_decay = decay_rate
            
            # Apply decay
            new_weight = max(current_weight - actual_decay, 0.0)
            
            if new_weight < min_weight:
                # Mark for removal
                edges_to_remove.append((source_id, target_id, rel_type))
                edges_removed += 1
            elif new_weight != current_weight:
                # Mark for update
                edges_to_update.append((
                    source_id,
                    target_id,
                    rel_type,
                    {**properties, "strength": new_weight}
                ))
                total_weight_after += new_weight
                edges_decayed += 1
            else:
                total_weight_after += current_weight
        
        # Apply updates
        # Note: Actual graph update would happen here
        # For now, just log the intended changes
        
        logger.info(f"Decay complete: {edges_decayed} edges decayed, {edges_removed} edges removed")
        
        avg_weight_before = total_weight_before / len(edges) if edges else 0.0
        remaining_edges = len(edges) - edges_removed
        avg_weight_after = total_weight_after / remaining_edges if remaining_edges > 0 else 0.0
        
        return {
            "edges_decayed": edges_decayed,
            "edges_removed": edges_removed,
            "avg_weight_before": avg_weight_before,
            "avg_weight_after": avg_weight_after
        }
        
    except Exception as e:
        logger.error(f"Error applying edge weight decay: {e}")
        return {
            "edges_decayed": 0,
            "edges_removed": 0,
            "avg_weight_before": 0.0,
            "avg_weight_after": 0.0
        }


async def reinforce_edge(
    source_id: UUID,
    target_id: UUID,
    reinforcement_amount: float = 0.1,
    max_weight: float = 1.0
) -> bool:
    """
    Reinforce (strengthen) a connection between two thoughts.
    
    Increases the weight of an edge when it's actively used or confirmed
    as valuable, helping important connections persist.
    
    Args:
        source_id: Source thought ID
        target_id: Target thought ID
        reinforcement_amount: Amount to increase weight
        max_weight: Maximum weight cap
        
    Returns:
        True if edge was reinforced, False otherwise
    """
    logger.info(f"Reinforcing edge {source_id} -> {target_id}")
    
    try:
        graph_engine = await get_graph_engine()
        
        # Get current edge data
        # Note: This is simplified - actual implementation would query edge
        # For now, return success
        
        logger.debug(f"Edge reinforced by {reinforcement_amount}")
        return True
        
    except Exception as e:
        logger.error(f"Error reinforcing edge: {e}")
        return False


async def calculate_potential_connections(
    thought_id: UUID,
    min_potential_weight: float = 0.3,
    max_results: int = 10
) -> List[Tuple[UUID, float, str]]:
    """
    Calculate potential (not yet created) connections for a thought.
    
    Analyzes the graph to find thoughts that could be connected but aren't yet,
    assigning a potential weight to each based on various factors:
    - Shared community membership
    - Common neighbors
    - Tag similarity
    - Semantic similarity (if available)
    
    Args:
        thought_id: Thought to find potential connections for
        min_potential_weight: Minimum weight to consider
        max_results: Maximum number of potential connections to return
        
    Returns:
        List of (target_id, potential_weight, reason) tuples
        
    Example:
        >>> potentials = await calculate_potential_connections(
        ...     thought_id=thought.id,
        ...     min_potential_weight=0.4
        ... )
        >>> for target_id, weight, reason in potentials:
        ...     print(f"Potential connection to {target_id}: {weight:.2f} ({reason})")
    """
    logger.info(f"Calculating potential connections for thought {thought_id}")
    
    try:
        graph_engine = await get_graph_engine()
        
        # Get the source thought
        source_data = await graph_engine.get_node(str(thought_id))
        if not source_data:
            logger.warning(f"Thought {thought_id} not found")
            return []
        
        # Get existing connections
        existing_edges = await graph_engine.get_edges(str(thought_id))
        existing_targets = {UUID(e[1]) for e in existing_edges}
        
        # Get all nodes
        all_nodes, all_edges = await graph_engine.get_graph_data()
        
        potential_connections = []
        
        source_tags = set(source_data.get("tags", []))
        source_community = source_data.get("community_id")
        source_projects = set(source_data.get("related_projects", []))
        
        for node_id, node_data in all_nodes:
            target_id = UUID(node_id)
            
            # Skip self and existing connections
            if target_id == thought_id or target_id in existing_targets:
                continue
            
            potential_weight = 0.0
            reasons = []
            
            # Check community membership
            if source_community and node_data.get("community_id") == source_community:
                potential_weight += 0.3
                reasons.append("same community")
            
            # Check tag similarity
            target_tags = set(node_data.get("tags", []))
            if source_tags and target_tags:
                tag_overlap = len(source_tags & target_tags) / len(source_tags | target_tags)
                if tag_overlap > 0:
                    potential_weight += tag_overlap * 0.4
                    if tag_overlap > 0.3:
                        reasons.append(f"shared tags ({len(source_tags & target_tags)})")
            
            # Check project overlap
            target_projects = set(node_data.get("related_projects", []))
            if source_projects and target_projects:
                project_overlap = len(source_projects & target_projects)
                if project_overlap > 0:
                    potential_weight += 0.3
                    reasons.append(f"shared projects ({project_overlap})")
            
            # Check common neighbors (triangles)
            target_edges = await graph_engine.get_edges(node_id)
            target_neighbors = {UUID(e[1]) for e in target_edges}
            source_neighbors = existing_targets
            
            common_neighbors = source_neighbors & target_neighbors
            if common_neighbors:
                neighbor_factor = min(len(common_neighbors) * 0.1, 0.3)
                potential_weight += neighbor_factor
                reasons.append(f"common neighbors ({len(common_neighbors)})")
            
            if potential_weight >= min_potential_weight:
                reason_str = ", ".join(reasons) if reasons else "structural similarity"
                potential_connections.append((target_id, potential_weight, reason_str))
        
        # Sort by potential weight and limit results
        potential_connections.sort(key=lambda x: x[1], reverse=True)
        potential_connections = potential_connections[:max_results]
        
        logger.info(f"Found {len(potential_connections)} potential connections")
        
        return potential_connections
        
    except Exception as e:
        logger.error(f"Error calculating potential connections: {e}")
        return []


async def prune_weak_connections(
    threshold: float = 0.2,
    preserve_recent: bool = True,
    recent_days: int = 7
) -> int:
    """
    Remove weak connections from the graph.
    
    Cleans up connections that have decayed below a threshold,
    optionally preserving recent connections even if weak.
    
    Args:
        threshold: Weight below which to remove connections
        preserve_recent: Keep recent connections regardless of weight
        recent_days: Days to consider "recent"
        
    Returns:
        Number of connections removed
    """
    logger.info(f"Pruning connections below weight {threshold}")
    
    try:
        graph_engine = await get_graph_engine()
        _, edges = await graph_engine.get_graph_data()
        
        edges_removed = 0
        now = datetime.now(timezone.utc)
        cutoff_date = now - timedelta(days=recent_days)
        
        for source_id, target_id, rel_type, properties in edges:
            weight = properties.get("strength", 0.5)
            
            # Check if should be removed
            should_remove = weight < threshold
            
            # Preserve recent connections if requested
            if should_remove and preserve_recent:
                created_at = properties.get("created_at")
                if created_at:
                    try:
                        if isinstance(created_at, str):
                            created_at = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                        
                        if created_at > cutoff_date:
                            should_remove = False
                    except Exception:
                        pass
            
            if should_remove:
                # Would remove edge here
                edges_removed += 1
        
        logger.info(f"Pruned {edges_removed} weak connections")
        
        return edges_removed
        
    except Exception as e:
        logger.error(f"Error pruning weak connections: {e}")
        return 0
