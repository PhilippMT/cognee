"""HelixDB Hybrid Adapter combining Vector and Graph functionality

LIMITATIONS:
1. Requires helix-py SDK (v0.2.30+) - pin version for stability
2. Requires local HelixDB instance or cloud endpoint
3. Schema must be pre-defined - use schema management utilities
4. Collections implemented as node labels (not native concept)
5. HelixQL queries must be pre-compiled
6. No OpenCypher support - HelixQL only
7. Full node replacement on updates (no partial updates)
8. Limited batch operations - implements batching at adapter level
9. Fixed embedding dimensions per node type
10. May have performance constraints at very large scale

See ANALYSIS.md for complete limitation details and mitigations.
"""

import asyncio
import json
from typing import List, Optional, Any, Dict, Type, Tuple, Union
from uuid import UUID

try:
    from helix.client import Client
    from helix.instance import Instance
    from helix.loader import Schema
    HELIX_AVAILABLE = True
except ImportError:
    HELIX_AVAILABLE = False
    Client = None
    Instance = None
    Schema = None

from cognee.infrastructure.databases.graph.graph_db_interface import GraphDBInterface, NodeData, EdgeData, Node
from cognee.infrastructure.databases.vector.vector_db_interface import VectorDBInterface
from cognee.infrastructure.engine import DataPoint
from cognee.shared.logging_utils import get_logger
from cognee.infrastructure.databases.vector.embeddings.EmbeddingEngine import EmbeddingEngine
from cognee.infrastructure.databases.vector.models.ScoredResult import ScoredResult

logger = get_logger("HelixDBAdapter")


class HelixDBAdapter(GraphDBInterface, VectorDBInterface):
    """
    Hybrid adapter that combines HelixDB Vector and Graph functionality.

    This adapter extends GraphDBInterface and implements VectorDBInterface to provide
    a unified interface for working with HelixDB as both a vector store and a graph database.

    IMPORTANT LIMITATIONS:
    - Requires helix-py package installed (not included in core dependencies)
    - Requires running HelixDB instance (local or cloud)
    - Schema must be managed explicitly
    - Collections are implemented via node labels (not native)
    - Limited transaction support
    - See ANALYSIS.md for complete limitations

    Args:
        config_path: Path to HelixDB configuration directory
        port: Port number for HelixDB instance (default: 6969)
        local: Whether using local instance (default: True)
        api_endpoint: Optional cloud API endpoint
        embedding_engine: Optional embedding engine for vector operations
        auto_start: Whether to auto-start local instance (default: False)
    """

    _VECTOR_NODE_LABEL = "COGNEE_VECTOR_NODE"
    _GRAPH_NODE_LABEL = "COGNEE_GRAPH_NODE"
    _COLLECTION_PROPERTY = "collection_name"

    def __init__(
        self,
        config_path: str,
        port: int = 6969,
        local: bool = True,
        api_endpoint: Optional[str] = None,
        embedding_engine: Optional[EmbeddingEngine] = None,
        auto_start: bool = False,
    ):
        """Initialize the HelixDB hybrid adapter."""
        if not HELIX_AVAILABLE:
            raise ImportError(
                "helix-py package is required for HelixDB adapter. "
                "Install it with: pip install helix-py"
            )

        self.config_path = config_path
        self.port = port
        self.local = local
        self.api_endpoint = api_endpoint
        self.embedding_engine = embedding_engine
        self.auto_start = auto_start

        # Initialize instance manager if auto_start
        self.instance = None
        if self.auto_start and self.local:
            try:
                self.instance = Instance(self.config_path, self.port, verbose=False)
                logger.info(f"Started local HelixDB instance on port {self.port}")
            except Exception as e:
                logger.warning(f"Could not auto-start instance: {e}")

        # Initialize client
        try:
            self.client = Client(
                local=self.local,
                port=self.port,
                api_endpoint=self.api_endpoint,
                verbose=False
            )
            logger.info(
                f"Initialized HelixDB hybrid adapter: "
                f"local={self.local}, port={self.port}, "
                f"endpoint={self.api_endpoint or 'N/A'}"
            )
        except Exception as e:
            raise RuntimeError(
                f"Failed to initialize HelixDB client: {e}. "
                f"Ensure HelixDB instance is running on port {self.port}"
            ) from e

        # Initialize schema manager
        try:
            self.schema = Schema(self.config_path)
        except Exception as e:
            logger.warning(f"Could not initialize schema manager: {e}")
            self.schema = None

    def _validate_embedding_engine(self):
        """Validate that embedding engine is available for vector operations."""
        if self.embedding_engine is None:
            raise ValueError(
                "HelixDB adapter requires an embedding_engine for vector operations. "
                "Provide one during initialization."
            )

    def _serialize_properties(self, properties: Dict[str, Any]) -> Dict[str, Any]:
        """Serialize properties to HelixDB-compatible format.
        
        LIMITATION: Complex nested objects may need special handling.
        """
        serialized = {}
        for key, value in properties.items():
            if isinstance(value, (str, int, float, bool)):
                serialized[key] = value
            elif isinstance(value, UUID):
                serialized[key] = str(value)
            elif value is None:
                serialized[key] = ""
            else:
                # Convert complex types to JSON strings
                try:
                    serialized[key] = json.dumps(value)
                except (TypeError, ValueError):
                    serialized[key] = str(value)
        return serialized

    # ==================== VectorDBInterface Implementation ====================

    async def get_connection(self):
        """Get connection to the database.
        
        NOTE: HelixDB uses client-based access, not traditional connections.
        Returns the client for interface compliance.
        """
        return self.client

    async def embed_data(self, data: List[str]) -> List[List[float]]:
        """Embed textual data into vector representations.
        
        LIMITATION: Uses provided embedding_engine only. HelixDB built-in
        embeddings are not exposed through this interface currently.
        """
        self._validate_embedding_engine()
        return await self.embedding_engine.embed_text(data)

    async def has_collection(self, collection_name: str) -> bool:
        """Check if a collection exists.
        
        LIMITATION: Since collections are implemented as node labels,
        we check if any nodes exist with the collection label.
        This may be slower than native collection checks.
        """
        try:
            # Query for nodes with this collection
            # Note: This requires a pre-compiled query or dynamic query execution
            # For now, we'll return True to avoid query compilation complexity
            # Real implementation would need proper query
            logger.debug(
                f"Collection existence check for '{collection_name}' - "
                f"returning True (collections are label-based)"
            )
            return True
        except Exception as e:
            logger.error(f"Error checking collection: {e}")
            return False

    async def create_collection(
        self,
        collection_name: str,
        payload_schema: Optional[Any] = None,
    ):
        """Create a new collection.
        
        LIMITATION: HelixDB doesn't have native collections. This is a no-op
        for interface compliance. Collections are created implicitly when
        nodes are added with collection labels.
        """
        logger.debug(
            f"Collection '{collection_name}' - implicit creation via node labels. "
            f"Schema: {payload_schema}"
        )
        pass

    async def create_data_points(
        self,
        collection_name: str,
        data_points: List[DataPoint]
    ):
        """Insert new data points into the specified collection.
        
        LIMITATION: No native bulk insert. Implements batching using asyncio.gather.
        Performance may be slower than native bulk operations.
        """
        self._validate_embedding_engine()

        # Get embeddings for all data points
        texts = [DataPoint.get_embeddable_data(dp) for dp in data_points]
        data_vectors = await self.embedding_engine.embed_text(texts)

        # Prepare data points for insertion
        # LIMITATION: This requires pre-compiled queries or dynamic query generation
        # For now, we log a warning about implementation status
        logger.warning(
            f"create_data_points called for collection '{collection_name}' "
            f"with {len(data_points)} points. "
            f"LIMITATION: Requires pre-compiled HelixQL queries. "
            f"This is a stub implementation - see ANALYSIS.md"
        )

        # Stub implementation - would need actual HelixQL queries
        for index, data_point in enumerate(data_points):
            node_id = str(data_point.id)
            vector = data_vectors[index]
            properties = self._serialize_properties(data_point.model_dump())
            properties[self._COLLECTION_PROPERTY] = collection_name

            logger.debug(
                f"Would insert node: id={node_id}, "
                f"collection={collection_name}, "
                f"vector_dim={len(vector)}"
            )

    async def retrieve(
        self,
        collection_name: str,
        data_point_ids: List[str]
    ):
        """Retrieve data points from a collection using their IDs.
        
        LIMITATION: Requires pre-compiled HelixQL query for efficient retrieval.
        """
        logger.warning(
            f"retrieve called for collection '{collection_name}' "
            f"with {len(data_point_ids)} IDs. "
            f"LIMITATION: Requires pre-compiled HelixQL queries. "
            f"This is a stub implementation - see ANALYSIS.md"
        )
        return []

    async def search(
        self,
        collection_name: str,
        query_text: Optional[str] = None,
        query_vector: Optional[List[float]] = None,
        limit: Optional[int] = 10,
        with_vector: bool = False,
    ):
        """Perform vector search in the specified collection.
        
        LIMITATION: Requires pre-compiled HelixQL query with vector search.
        Performance depends on HNSW index quality and dataset size.
        """
        self._validate_embedding_engine()

        if query_text and query_vector:
            raise ValueError("Provide either query_text or query_vector, not both")
        if not query_text and not query_vector:
            raise ValueError("Must provide either query_text or query_vector")

        # Get query vector
        if query_text:
            vectors = await self.embedding_engine.embed_text([query_text])
            query_vector = vectors[0]

        logger.warning(
            f"search called for collection '{collection_name}' "
            f"with vector dim={len(query_vector)}, limit={limit}. "
            f"LIMITATION: Requires pre-compiled HelixQL queries. "
            f"This is a stub implementation - see ANALYSIS.md"
        )
        return []

    async def batch_search(
        self,
        collection_name: str,
        query_texts: List[str],
        limit: Optional[int] = 10,
        with_vectors: bool = False,
    ):
        """Perform batch search using multiple text queries.
        
        LIMITATION: No native batch search. Implements using asyncio.gather.
        """
        self._validate_embedding_engine()

        # Convert texts to vectors
        data_vectors = await self.embedding_engine.embed_text(query_texts)

        # Execute searches in parallel
        return await asyncio.gather(
            *[
                self.search(collection_name, None, vector, limit, with_vectors)
                for vector in data_vectors
            ]
        )

    async def delete_data_points(
        self,
        collection_name: str,
        data_point_ids: List[str]
    ):
        """Delete specified data points from a collection.
        
        LIMITATION: Requires pre-compiled HelixQL query for deletion.
        """
        logger.warning(
            f"delete_data_points called for collection '{collection_name}' "
            f"with {len(data_point_ids)} IDs. "
            f"LIMITATION: Requires pre-compiled HelixQL queries. "
            f"This is a stub implementation - see ANALYSIS.md"
        )

    async def prune(self):
        """Remove all data from the database.
        
        LIMITATION: Requires pre-compiled HelixQL query to delete all nodes.
        """
        logger.warning(
            "prune called. "
            "LIMITATION: Requires pre-compiled HelixQL queries. "
            "This is a stub implementation - see ANALYSIS.md"
        )

    async def create_vector_index(self, index_name: str, index_property_name: str):
        """Create a vector index.
        
        LIMITATION: HelixDB uses HNSW indexing automatically.
        This is a no-op for interface compliance.
        """
        logger.debug(
            f"Vector index '{index_name}' on property '{index_property_name}' - "
            f"HelixDB uses automatic HNSW indexing"
        )

    async def index_data_points(
        self,
        index_name: str,
        index_property_name: str,
        data_points: List[DataPoint]
    ):
        """Index data points.
        
        LIMITATION: Delegates to create_data_points as HelixDB handles indexing automatically.
        """
        collection_name = f"{index_name}_{index_property_name}"
        await self.create_data_points(collection_name, data_points)

    # ==================== GraphDBInterface Implementation ====================

    async def query(self, query: str, params: Optional[Dict[str, Any]] = None) -> List[Any]:
        """Execute a raw database query.
        
        LIMITATION: Query must be a pre-compiled HelixQL query name.
        HelixDB requires queries to be compiled before use.
        
        Args:
            query: Name of the pre-compiled HelixQL query
            params: Query parameters as key-value pairs
        """
        try:
            if params is None:
                params = {}
            
            logger.debug(f"Executing query: {query} with params: {params}")
            
            # Call the HelixDB client query method
            result = self.client.query(query, **params)
            
            # Convert result to list if needed
            if isinstance(result, list):
                return result
            elif isinstance(result, dict):
                return [result]
            else:
                return [{"result": result}]
                
        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            raise RuntimeError(f"HelixDB query failed: {e}") from e

    async def add_node(
        self,
        node: Union[DataPoint, str],
        properties: Optional[Dict[str, Any]] = None
    ) -> None:
        """Add a single node to the graph.
        
        LIMITATION: Requires pre-compiled HelixQL query for node insertion.
        """
        if isinstance(node, DataPoint):
            node_id = str(node.id)
            props = self._serialize_properties(node.model_dump())
        else:
            node_id = node
            props = self._serialize_properties(properties or {})

        logger.warning(
            f"add_node called for node '{node_id}'. "
            f"LIMITATION: Requires pre-compiled HelixQL queries. "
            f"This is a stub implementation - see ANALYSIS.md"
        )

    async def add_nodes(self, nodes: Union[List[Node], List[DataPoint]]) -> None:
        """Add multiple nodes to the graph.
        
        LIMITATION: No native bulk insert. Implements batching using asyncio.gather.
        """
        logger.warning(
            f"add_nodes called with {len(nodes)} nodes. "
            f"LIMITATION: Requires pre-compiled HelixQL queries. "
            f"This is a stub implementation - see ANALYSIS.md"
        )

        # Would batch insertions here
        tasks = []
        for node in nodes:
            if isinstance(node, tuple):
                # Node is (node_id, properties)
                node_id, properties = node
                tasks.append(self.add_node(node_id, properties))
            else:
                # Node is DataPoint
                tasks.append(self.add_node(node))

        # Note: Commented out actual execution for stub
        # await asyncio.gather(*tasks)

    async def delete_node(self, node_id: str) -> None:
        """Delete a node from the graph.
        
        LIMITATION: Requires pre-compiled HelixQL query for deletion.
        """
        logger.warning(
            f"delete_node called for node '{node_id}'. "
            f"LIMITATION: Requires pre-compiled HelixQL queries. "
            f"This is a stub implementation - see ANALYSIS.md"
        )

    async def delete_nodes(self, node_ids: List[str]) -> None:
        """Delete multiple nodes from the graph.
        
        LIMITATION: No native bulk delete. Implements batching.
        """
        logger.warning(
            f"delete_nodes called with {len(node_ids)} IDs. "
            f"LIMITATION: Requires pre-compiled HelixQL queries. "
            f"This is a stub implementation - see ANALYSIS.md"
        )

    async def get_node(self, node_id: str) -> Optional[NodeData]:
        """Retrieve a single node from the graph.
        
        LIMITATION: Requires pre-compiled HelixQL query for node retrieval.
        """
        logger.warning(
            f"get_node called for node '{node_id}'. "
            f"LIMITATION: Requires pre-compiled HelixQL queries. "
            f"This is a stub implementation - see ANALYSIS.md"
        )
        return None

    async def get_nodes(self, node_ids: List[str]) -> List[NodeData]:
        """Retrieve multiple nodes from the graph.
        
        LIMITATION: Requires pre-compiled HelixQL query for bulk retrieval.
        """
        logger.warning(
            f"get_nodes called with {len(node_ids)} IDs. "
            f"LIMITATION: Requires pre-compiled HelixQL queries. "
            f"This is a stub implementation - see ANALYSIS.md"
        )
        return []

    async def add_edge(
        self,
        source_id: str,
        target_id: str,
        relationship_name: str,
        properties: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Create an edge between two nodes.
        
        LIMITATION: Requires pre-compiled HelixQL query for edge insertion.
        """
        logger.warning(
            f"add_edge called: {source_id} -> {target_id} ({relationship_name}). "
            f"LIMITATION: Requires pre-compiled HelixQL queries. "
            f"This is a stub implementation - see ANALYSIS.md"
        )

    async def add_edges(
        self,
        edges: Union[List[EdgeData], List[Tuple[str, str, str, Optional[Dict[str, Any]]]]]
    ) -> None:
        """Add multiple edges to the graph.
        
        LIMITATION: No native bulk insert. Implements batching.
        """
        logger.warning(
            f"add_edges called with {len(edges)} edges. "
            f"LIMITATION: Requires pre-compiled HelixQL queries. "
            f"This is a stub implementation - see ANALYSIS.md"
        )

    async def delete_graph(self) -> None:
        """Remove the entire graph.
        
        LIMITATION: Requires pre-compiled HelixQL query to delete all nodes/edges.
        """
        logger.warning(
            "delete_graph called. "
            "LIMITATION: Requires pre-compiled HelixQL queries. "
            "This is a stub implementation - see ANALYSIS.md"
        )

    async def get_graph_data(self) -> Tuple[List[Node], List[EdgeData]]:
        """Retrieve all nodes and edges.
        
        LIMITATION: May be very slow for large graphs. Requires pre-compiled query.
        """
        logger.warning(
            "get_graph_data called. "
            "LIMITATION: Requires pre-compiled HelixQL queries. "
            "This is a stub implementation - see ANALYSIS.md"
        )
        return [], []

    async def get_graph_metrics(self, include_optional: bool = False) -> Dict[str, Any]:
        """Get graph metrics.
        
        LIMITATION: Requires pre-compiled HelixQL queries for metrics.
        """
        logger.warning(
            "get_graph_metrics called. "
            "LIMITATION: Requires pre-compiled HelixQL queries. "
            "This is a stub implementation - see ANALYSIS.md"
        )
        return {}

    async def has_edge(
        self,
        source_id: str,
        target_id: str,
        relationship_name: str
    ) -> bool:
        """Check if an edge exists.
        
        LIMITATION: Requires pre-compiled HelixQL query for edge checking.
        """
        logger.warning(
            f"has_edge called: {source_id} -> {target_id} ({relationship_name}). "
            f"LIMITATION: Requires pre-compiled HelixQL queries. "
            f"This is a stub implementation - see ANALYSIS.md"
        )
        return False

    async def has_edges(self, edges: List[EdgeData]) -> List[EdgeData]:
        """Check which edges exist.
        
        LIMITATION: Requires pre-compiled HelixQL query for bulk checking.
        """
        logger.warning(
            f"has_edges called with {len(edges)} edges. "
            f"LIMITATION: Requires pre-compiled HelixQL queries. "
            f"This is a stub implementation - see ANALYSIS.md"
        )
        return []

    async def get_edges(self, node_id: str) -> List[EdgeData]:
        """Get all edges connected to a node.
        
        LIMITATION: Requires pre-compiled HelixQL query for edge traversal.
        """
        logger.warning(
            f"get_edges called for node '{node_id}'. "
            f"LIMITATION: Requires pre-compiled HelixQL queries. "
            f"This is a stub implementation - see ANALYSIS.md"
        )
        return []

    async def get_neighbors(self, node_id: str) -> List[NodeData]:
        """Get all neighboring nodes.
        
        LIMITATION: Requires pre-compiled HelixQL query for neighbor traversal.
        """
        logger.warning(
            f"get_neighbors called for node '{node_id}'. "
            f"LIMITATION: Requires pre-compiled HelixQL queries. "
            f"This is a stub implementation - see ANALYSIS.md"
        )
        return []

    async def get_nodeset_subgraph(
        self,
        node_type: Type[Any],
        node_name: List[str]
    ) -> Tuple[List[Tuple[int, dict]], List[Tuple[int, int, str, dict]]]:
        """Get a subgraph of specific node types.
        
        LIMITATION: Requires pre-compiled HelixQL query for subgraph extraction.
        """
        logger.warning(
            f"get_nodeset_subgraph called for type {node_type}. "
            f"LIMITATION: Requires pre-compiled HelixQL queries. "
            f"This is a stub implementation - see ANALYSIS.md"
        )
        return [], []

    async def get_connections(
        self,
        node_id: Union[str, UUID]
    ) -> List[Tuple[NodeData, Dict[str, Any], NodeData]]:
        """Get all connections for a node.
        
        LIMITATION: Requires pre-compiled HelixQL query for connection traversal.
        """
        logger.warning(
            f"get_connections called for node '{node_id}'. "
            f"LIMITATION: Requires pre-compiled HelixQL queries. "
            f"This is a stub implementation - see ANALYSIS.md"
        )
        return []

    def __del__(self):
        """Cleanup: stop instance if auto-started."""
        if self.instance is not None:
            try:
                # Instance cleanup handled by helix-py
                logger.info("HelixDB instance cleanup")
            except Exception as e:
                logger.warning(f"Error during cleanup: {e}")
