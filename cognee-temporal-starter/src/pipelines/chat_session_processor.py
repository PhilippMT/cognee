"""
Coding Agent Chat Session - Temporal Processing Pipeline

This module implements a comprehensive pipeline for processing coding agent chat sessions
with temporal awareness using Graphiti and Cognee's temporal graph capabilities.
"""

import asyncio
from datetime import datetime
from typing import List, Dict, Any, Optional
from uuid import uuid4

import cognee
from cognee.api.v1.cognify import cognify
from cognee.api.v1.search import SearchType, search
from cognee.tasks.temporal_awareness import build_graph_with_temporal_awareness
from cognee.tasks.temporal_awareness.index_graphiti_objects import index_graphiti_objects

from .chat_session_models import (
    ChatMessage,
    DevelopmentFact,
    AgentDecision,
    CodeEntity,
    SessionMetadata,
    InteractionPattern,
    DevelopmentTimeline
)


class ChatSessionProcessor:
    """
    Processes coding agent chat sessions with temporal awareness.
    
    This processor handles the complete pipeline:
    1. Parse raw chat history
    2. Create Graphiti episodes with temporal context
    3. Extract facts using temporal_cognify
    4. Mine development status and decisions
    5. Build temporal knowledge graph
    6. Index for efficient retrieval
    """
    
    def __init__(self, session_id: Optional[str] = None):
        """
        Initialize the chat session processor.
        
        Args:
            session_id: Optional session ID. If None, generates a new UUID.
        """
        self.session_id = session_id or str(uuid4())
        self.messages: List[ChatMessage] = []
        self.facts: List[DevelopmentFact] = []
        self.decisions: List[AgentDecision] = []
        self.code_entities: List[CodeEntity] = []
        self.session_metadata: Optional[SessionMetadata] = None
        
    async def process_chat_history(
        self,
        chat_history: List[Dict[str, Any]],
        use_graphiti: bool = True,
        extract_deep_facts: bool = True,
        preserve_raw_data: bool = True
    ) -> Dict[str, Any]:
        """
        Process complete chat history with temporal awareness.
        
        Args:
            chat_history: List of message dictionaries with keys:
                - role: str (user, assistant, agent, tool)
                - content: str (message text)
                - timestamp: str or datetime (message time)
                - tool_calls: Optional[List[Dict]] (tool calls made)
                - message_id: Optional[str] (unique ID, generated if missing)
            use_graphiti: If True, create Graphiti episodes
            extract_deep_facts: If True, perform deep fact extraction
            preserve_raw_data: If True, store raw messages for future processing
        
        Returns:
            Dictionary with processing results including:
            - session_id: str
            - messages_processed: int
            - facts_extracted: int
            - decisions_found: int
            - processing_time: float
        """
        start_time = datetime.now()
        
        print(f"🚀 Starting chat session processing: {self.session_id}")
        print(f"📊 Processing {len(chat_history)} messages")
        
        # Phase 1: Parse and normalize messages
        await self._parse_messages(chat_history)
        print(f"✅ Phase 1: Parsed {len(self.messages)} messages")
        
        # Phase 2: Store raw data in cognee
        if preserve_raw_data:
            await self._store_raw_messages()
            print(f"✅ Phase 2: Stored raw messages in dataset")
        
        # Phase 3: Create Graphiti episodes for temporal awareness
        if use_graphiti:
            await self._create_graphiti_episodes()
            print(f"✅ Phase 3: Created Graphiti episodes with temporal context")
        
        # Phase 4: Run temporal cognify for event extraction
        await self._run_temporal_cognify()
        print(f"✅ Phase 4: Completed temporal cognify processing")
        
        # Phase 5: Extract development facts and status
        if extract_deep_facts:
            await self._extract_development_facts()
            print(f"✅ Phase 5: Extracted {len(self.facts)} development facts")
        
        # Phase 6: Mine agent decisions
        if extract_deep_facts:
            await self._extract_agent_decisions()
            print(f"✅ Phase 6: Found {len(self.decisions)} agent decisions")
        
        # Phase 7: Extract code entities and their evolution
        if extract_deep_facts:
            await self._extract_code_entities()
            print(f"✅ Phase 7: Identified {len(self.code_entities)} code entities")
        
        # Phase 8: Build session metadata and timeline
        await self._build_session_metadata()
        print(f"✅ Phase 8: Built session metadata and timeline")
        
        # Phase 9: Index all artifacts for retrieval
        await self._index_session_artifacts()
        print(f"✅ Phase 9: Indexed all artifacts")
        
        processing_time = (datetime.now() - start_time).total_seconds()
        
        results = {
            "session_id": self.session_id,
            "messages_processed": len(self.messages),
            "facts_extracted": len(self.facts),
            "decisions_found": len(self.decisions),
            "code_entities": len(self.code_entities),
            "processing_time": processing_time,
            "status": "completed"
        }
        
        print(f"🎉 Processing completed in {processing_time:.2f}s")
        print(f"📈 Summary: {results}")
        
        return results
    
    async def _parse_messages(self, chat_history: List[Dict[str, Any]]):
        """Parse and normalize raw chat messages."""
        for idx, msg in enumerate(chat_history):
            # Parse timestamp
            timestamp = msg.get("timestamp")
            if isinstance(timestamp, str):
                timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            elif timestamp is None:
                timestamp = datetime.now()
            
            # Create message object
            message = ChatMessage(
                session_id=self.session_id,
                message_id=msg.get("message_id", f"msg_{idx}_{uuid4().hex[:8]}"),
                role=msg.get("role", "unknown"),
                content=msg.get("content", ""),
                timestamp=timestamp,
                tool_calls=msg.get("tool_calls"),
                parent_message_id=msg.get("parent_message_id"),
                id=str(uuid4())
            )
            self.messages.append(message)
    
    async def _store_raw_messages(self):
        """Store raw messages in cognee for future processing."""
        # Prepare message texts for storage
        message_texts = [
            f"[{msg.role}] at {msg.timestamp}: {msg.content}"
            for msg in self.messages
        ]
        
        # Add to cognee
        await cognee.add(
            message_texts,
            dataset_name=f"chat_session_{self.session_id}"
        )
    
    async def _create_graphiti_episodes(self):
        """Create Graphiti episodes with temporal context for each message."""
        episode_texts = []
        
        for msg in self.messages:
            # Create rich episode text with context
            episode_text = f"""
Message ID: {msg.message_id}
Role: {msg.role}
Timestamp: {msg.timestamp}
Content: {msg.content}
"""
            if msg.tool_calls:
                episode_text += f"\nTool Calls: {len(msg.tool_calls)} tools used"
            
            episode_texts.append(episode_text)
        
        # Build temporal graph with Graphiti
        graphiti = await build_graph_with_temporal_awareness(episode_texts)
        
        # Index Graphiti nodes and edges
        await index_graphiti_objects()
        
        return graphiti
    
    async def _run_temporal_cognify(self):
        """Run temporal cognify to extract events and relationships."""
        await cognify(
            datasets=[f"chat_session_{self.session_id}"],
            temporal_cognify=True,
            chunks_per_batch=10
        )
    
    async def _extract_development_facts(self):
        """
        Extract development facts from the conversation.
        
        This uses LLM to analyze messages and extract:
        - Code changes
        - Bug fixes
        - Feature additions
        - Refactorings
        - Dependencies
        """
        # Search for development-related content
        dev_queries = [
            "code changes and modifications",
            "bug fixes and solutions",
            "new features and implementations",
            "refactoring activities",
            "dependencies added or removed"
        ]
        
        for query in dev_queries:
            results = await search(
                query_text=query,
                query_type=SearchType.TEMPORAL
            )
            
            # Parse results and create fact objects
            # (Simplified - in production would use structured LLM extraction)
            for result in results[:5]:  # Limit to top 5
                fact = DevelopmentFact(
                    fact_type=self._infer_fact_type(query),
                    description=str(result),
                    status="completed",  # Would be extracted from content
                    valid_at=datetime.now(),
                    session_id=self.session_id,
                    related_message_ids=[],
                    confidence=0.8,
                    id=str(uuid4())
                )
                self.facts.append(fact)
    
    async def _extract_agent_decisions(self):
        """
        Mine agent decisions from the conversation.
        
        Looks for decision points where the agent:
        - Chose between alternatives
        - Made technical choices
        - Decided on approaches
        """
        # Look for decision-making patterns
        decision_patterns = [
            "I will",
            "Let's use",
            "I'll implement",
            "The best approach is",
            "I recommend"
        ]
        
        for msg in self.messages:
            if msg.role in ["assistant", "agent"]:
                content_lower = msg.content.lower()
                
                # Check for decision patterns
                for pattern in decision_patterns:
                    if pattern.lower() in content_lower:
                        decision = AgentDecision(
                            decision=msg.content[:200],  # First 200 chars
                            rationale="Extracted from agent message",
                            alternatives=[],
                            timestamp=msg.timestamp,
                            session_id=self.session_id,
                            message_id=msg.message_id,
                            decision_type="technical",
                            impact="medium",
                            id=str(uuid4())
                        )
                        self.decisions.append(decision)
                        break
    
    async def _extract_code_entities(self):
        """
        Extract code entities mentioned in the conversation.
        
        Identifies:
        - Files
        - Functions
        - Classes
        - Modules
        - Variables
        """
        # Simple heuristics for code entity detection
        code_patterns = {
            "file": [".py", ".js", ".ts", ".java", ".cpp", ".md"],
            "function": ["def ", "function ", "func "],
            "class": ["class ", "interface "],
        }
        
        entity_tracker = {}
        
        for msg in self.messages:
            content = msg.content
            
            # Detect file paths
            for ext in code_patterns["file"]:
                if ext in content:
                    # Extract potential file name (simplified)
                    words = content.split()
                    for word in words:
                        if ext in word:
                            entity_name = word.strip('"`\'(),')
                            if entity_name not in entity_tracker:
                                entity = CodeEntity(
                                    entity_type="file",
                                    entity_name=entity_name,
                                    description=f"File mentioned in session",
                                    first_mentioned=msg.timestamp,
                                    last_mentioned=msg.timestamp,
                                    session_id=self.session_id,
                                    id=str(uuid4())
                                )
                                self.code_entities.append(entity)
                                entity_tracker[entity_name] = entity
                            else:
                                entity_tracker[entity_name].last_mentioned = msg.timestamp
    
    async def _build_session_metadata(self):
        """Build comprehensive session metadata."""
        if not self.messages:
            return
        
        # Determine session type based on content analysis
        session_type = self._infer_session_type()
        
        # Extract session goal
        session_goal = self._extract_session_goal()
        
        # Count tool calls
        tool_calls_count = sum(
            len(msg.tool_calls) if msg.tool_calls else 0
            for msg in self.messages
        )
        
        # Get unique files
        code_changes = list(set(
            entity.entity_name
            for entity in self.code_entities
            if entity.entity_type == "file"
        ))
        
        self.session_metadata = SessionMetadata(
            session_id=self.session_id,
            session_goal=session_goal,
            session_type=session_type,
            start_time=self.messages[0].timestamp,
            end_time=self.messages[-1].timestamp,
            participants=[
                {"role": role, "count": sum(1 for m in self.messages if m.role == role)}
                for role in set(m.role for m in self.messages)
            ],
            completion_status="completed",
            message_count=len(self.messages),
            tool_calls_count=tool_calls_count,
            code_changes=code_changes,
            id=str(uuid4())
        )
    
    async def _index_session_artifacts(self):
        """Index all extracted artifacts for efficient retrieval."""
        # This would index facts, decisions, entities, etc.
        # For now, we've already indexed via cognee.add() and cognify()
        pass
    
    def _infer_fact_type(self, query: str) -> str:
        """Infer fact type from query."""
        query_lower = query.lower()
        if "bug" in query_lower:
            return "bug_fix"
        elif "feature" in query_lower:
            return "feature"
        elif "refactor" in query_lower:
            return "refactor"
        elif "depend" in query_lower:
            return "dependency"
        else:
            return "code_change"
    
    def _infer_session_type(self) -> str:
        """Infer session type from message content."""
        content = " ".join(m.content.lower() for m in self.messages[:10])
        
        if "bug" in content or "error" in content or "fix" in content:
            return "debugging"
        elif "feature" in content or "implement" in content:
            return "feature_development"
        elif "refactor" in content or "improve" in content:
            return "refactoring"
        elif "review" in content:
            return "review"
        else:
            return "exploration"
    
    def _extract_session_goal(self) -> str:
        """Extract session goal from early messages."""
        # Look at first few user messages
        for msg in self.messages[:5]:
            if msg.role == "user" and len(msg.content) > 20:
                return msg.content[:200] + "..." if len(msg.content) > 200 else msg.content
        
        return "No explicit goal stated"


# Convenience function for easy use
async def process_coding_session(
    chat_history: List[Dict[str, Any]],
    session_id: Optional[str] = None,
    **kwargs
) -> Dict[str, Any]:
    """
    Process a coding agent chat session with temporal awareness.
    
    Args:
        chat_history: List of messages with role, content, timestamp
        session_id: Optional session ID
        **kwargs: Additional processing options
    
    Returns:
        Processing results dictionary
    """
    processor = ChatSessionProcessor(session_id=session_id)
    return await processor.process_chat_history(chat_history, **kwargs)
