# HelixDB Adapter Limitations

**🚨 IMPORTANT**: This document lists ALL known limitations of the HelixDB hybrid adapter implementation. Review these carefully before using in production.

## Overview

The HelixDB adapter is a **stub/skeleton implementation** that provides the interface structure but requires significant user configuration to become fully operational. This design is due to HelixDB's architecture requiring pre-compiled HelixQL queries.

## Critical Limitations (Must Understand)

### 1. Pre-compiled Queries Required ⛔
**Impact**: High  
**Severity**: Critical

- **Problem**: All database operations require HelixQL queries to be pre-compiled in `.hx` files before use
- **Impact**: Cannot dynamically generate queries at runtime; adapter methods are stubs that log warnings
- **Workaround**: 
  1. Define all needed queries in `.hx` files
  2. Compile with `helix check`
  3. Deploy with `helix deploy`
  4. Update adapter methods to call your queries
- **Example**:
  ```helix
  # In queries.hx
  QUERY addNode(id: String, properties: String) =>
      node <- AddN<MyNode({id: id, props: properties})>
      RETURN node
  ```

### 2. No Native Collections ⚠️
**Impact**: Medium  
**Severity**: High

- **Problem**: HelixDB doesn't have native collection concept like other vector databases
- **Impact**: Collections implemented via node labels; less efficient than native collections
- **Workaround**: Use consistent labeling strategy; filter by collection property
- **Performance**: May be slower for large-scale collection operations

### 3. Schema Must Be Pre-defined 📋
**Impact**: High  
**Severity**: High

- **Problem**: Schema must be defined in `.hx` files before data can be inserted
- **Impact**: Cannot dynamically create node/edge types; requires redeployment for schema changes
- **Workaround**: Plan schema carefully upfront; version control `.hx` files
- **Migration**: Schema changes require data migration (no built-in tools)

### 4. No Partial Node Updates 🔄
**Impact**: Medium  
**Severity**: Medium

- **Problem**: Updating a node requires replacing entire node, not just changed properties
- **Impact**: Higher bandwidth usage; more complex update logic
- **Workaround**: Read-modify-write pattern; cache frequently accessed nodes
- **Example**:
  ```python
  # Cannot do: node.update({"age": 25})
  # Must do: recreate entire node with new age value
  ```

### 5. Fixed Vector Dimensions 📏
**Impact**: Medium  
**Severity**: High

- **Problem**: Vector embedding dimensions set at schema creation time
- **Impact**: Cannot change dimensions without schema recreation
- **Workaround**: Choose embedding model carefully; use consistent model
- **Compatibility**: Different node types can have different dimensions

## Architecture Limitations

### 6. Instance Management Required 🖥️
**Severity**: Medium

- Requires running HelixDB instance (local or cloud)
- No serverless option like Neptune Analytics
- Must manage instance lifecycle yourself
- Auto-start available but limited to local development

### 7. LMDB Storage Engine 💾
**Severity**: Low

- Single-machine storage (not distributed)
- Disk space usage can be significant
- Performance tied to disk I/O
- Limited horizontal scaling

### 8. CLI Dependency 🔧
**Severity**: Medium

- Requires HelixDB CLI installed for query compilation
- Schema deployment must use CLI
- Cannot deploy from Python code alone
- Installation: `curl -fsSL "https://install.helix-db.com" | bash`

### 9. helix-py SDK Maturity 📦
**Severity**: Medium

- SDK version 0.2.30 (relatively new)
- Potential for breaking changes
- Limited community support
- Documentation gaps in some areas
- **Mitigation**: Pin specific version in requirements

### 10. No OpenCypher Support ❌
**Severity**: High (for Neo4j/Neptune users)

- Only HelixQL query language supported
- No Cypher compatibility
- Different syntax from industry standard
- Requires learning new query language
- Migration from Cypher databases is manual

## Vector Operations Limitations

### 11. HNSW Algorithm Only 🔍
**Severity**: Low

- Fixed to HNSW (Hierarchical Navigable Small World)
- Cannot choose alternative algorithms (IVF, LSH, etc.)
- Performance characteristics are HNSW-specific
- Good for most use cases but not optimal for all

### 12. On-Disk Vector Storage 💿
**Severity**: Low

- Vectors stored on disk, not fully in-memory
- Slightly slower than pure in-memory solutions
- Better for large datasets that don't fit in RAM
- Good balance for most applications

### 13. No Native Batch Insert 📦
**Severity**: Medium

- No bulk insert API
- Adapter implements batching via `asyncio.gather`
- Performance: ~1000 inserts/sec (estimated)
- Slower than databases with native bulk operations

### 14. Limited Metadata Filtering 🔎
**Severity**: Medium

- Metadata filtering requires custom query logic
- No built-in WHERE clauses on metadata
- Must implement in HelixQL queries
- More complex than databases like Pinecone

### 15. No Hybrid Search Built-in 🔀
**Severity**: Medium

- No native keyword + vector hybrid search
- Must implement manually in queries
- Separate keyword and vector indexes
- More complex than specialized hybrid search databases

## Graph Operations Limitations

### 16. Complex Query Complexity 🧩
**Severity**: Medium

- Complex graph traversals need custom HelixQL
- No graph algorithm library exposed
- PageRank, shortest path, etc. must be implemented
- Less rich than Neo4j's algorithms library

### 17. Limited Aggregations 📊
**Severity**: Medium

- Some aggregations need client-side processing
- GROUP BY, HAVING may be limited
- COUNT, SUM available but constrained
- More complex queries may need multiple round trips

### 18. Node ID Format Constraints 🆔
**Severity**: Low

- May have restrictions on ID format/length
- UUID conversion to string needed
- Validate IDs before insertion
- Document ID rules for your schema

### 19. Relationship Property Limits 🔗
**Severity**: Low

- May have size limits on edge properties
- Complex nested objects may need serialization
- Large property values should be avoided
- Store large data as separate nodes

### 20. No Bidirectional Traversal Syntax ↔️
**Severity**: Low

- May need separate queries for IN/OUT edges
- Less convenient than Cypher's `-[]-` syntax
- Document edge direction in schema
- Plan queries with direction in mind

## Performance Limitations

### 21. Vector Search Performance 🚀
**Expected**: Sub-millisecond to milliseconds  
**Limitation**: Dataset size dependent

- Small datasets (<100K): Sub-millisecond
- Medium datasets (100K-1M): 1-10ms
- Large datasets (>1M): 10-100ms+
- Depends on HNSW parameters and index quality

### 22. Graph Traversal Performance 🔄
**Expected**: Milliseconds  
**Limitation**: Query complexity dependent

- Simple patterns (1-2 hops): 1-5ms
- Medium patterns (3-5 hops): 5-50ms
- Complex patterns (>5 hops): 50ms+
- Lazy evaluation helps with large result sets

### 23. Bulk Insert Performance 📥
**Expected**: ~1000 records/second  
**Limitation**: No native bulk API

- Single inserts: ~100/sec
- Batched (10s): ~500/sec
- Batched (100s): ~1000/sec
- Limited by network round trips

### 24. Update Performance 🔄
**Expected**: Milliseconds  
**Limitation**: Full node replacement

- Simple updates: 1-5ms
- Large nodes: 5-50ms
- Updates more expensive than pure KV stores
- Plan for read-heavy workloads

### 25. Index Building Time ⏱️
**Expected**: Seconds to minutes  
**Limitation**: Initial HNSW construction

- Small datasets (<10K): Seconds
- Medium datasets (10K-100K): Minutes
- Large datasets (>100K): 10+ minutes
- Re-indexing on schema changes is costly

## Integration Limitations

### 26. Transaction Support 🔒
**Severity**: High (for some use cases)

- Limited transaction semantics
- No full ACID guarantees
- Best-effort consistency
- Plan for eventual consistency patterns

### 27. Concurrent Access 🔀
**Severity**: Medium

- May have locking constraints
- Write contention possible
- Connection pooling not built-in
- Test under concurrent load

### 28. Error Messages 💬
**Severity**: Low

- Errors may be cryptic
- SDK error wrapping minimal
- Implement error translation layer
- Log full context for debugging

### 29. Backup/Restore 💾
**Severity**: High

- No native backup tools
- Manual file system backup needed
- No point-in-time recovery
- Plan backup strategy carefully

### 30. Monitoring/Observability 📈
**Severity**: Medium

- Limited built-in metrics
- No native APM integration
- Implement custom monitoring
- Log query performance manually

## Operational Limitations

### 31. Local Development Setup 💻
**Complexity**: Medium

- Requires local instance installation
- CLI tools needed
- Schema setup before coding
- Docker support limited

### 32. Deployment Complexity 🚀
**Complexity**: Medium

- Manual instance management
- No managed service (except paid cloud)
- Manual scaling
- Operations burden higher than managed services

### 33. Resource Usage 📊
**Consideration**: High

- LMDB disk space usage can be large
- Memory usage depends on workload
- CPU usage for vector search
- Monitor and plan capacity

### 34. Version Compatibility 🔄
**Risk**: Medium

- SDK version 0.2.30 is relatively new
- Potential breaking changes in updates
- Pin versions in production
- Test upgrades thoroughly

### 35. Multi-tenancy 👥
**Support**: Limited

- No built-in tenant isolation
- Implement at application layer
- Single database per instance
- Consider multiple instances for tenants

## Security Limitations

### 36. Query Injection Risk 💉
**Severity**: High  
**Mitigation**: Required

- Dynamic query generation risky
- Parameterize all queries
- Validate all inputs
- Use pre-compiled queries only

### 37. Access Control 🔐
**Severity**: High

- No fine-grained permissions
- All-or-nothing access model
- Implement authorization in application
- Use network security

### 38. Encryption at Rest 🔒
**Severity**: Medium

- No native encryption
- Use OS/disk-level encryption
- Encrypt backups separately
- Consider data sensitivity

### 39. Network Security 🌐
**Severity**: Medium

- HTTP endpoints not encrypted by default
- Use HTTPS in production
- Implement auth layer
- VPN/firewall recommendations

### 40. Audit Logging 📝
**Severity**: Medium

- Limited built-in audit features
- Implement at adapter layer
- Log all sensitive operations
- Retention policy needed

## Data Model Limitations

### 41. Property Type Constraints 📝
**Severity**: Medium

- Schema defines strict types
- Type validation required
- No automatic type conversion
- Plan data types carefully

### 42. Nested Object Handling 🗂️
**Severity**: Low

- Complex nested objects may need JSON serialization
- Not as natural as document databases
- Serialize to strings for storage
- Parse on retrieval

### 43. Reserved Word Conflicts ⚠️
**Severity**: Low

- HelixQL has reserved keywords
- Property names may conflict
- Escape or rename conflicting names
- Document reserved words

### 44. Array/List Support 📋
**Severity**: Low

- Array handling may be limited
- Serialize complex arrays
- Consider separate nodes for lists
- Document array limitations

### 45. Null Value Handling ❓
**Severity**: Low

- Null handling may vary
- Explicit null checks needed
- Use empty strings or defaults
- Document null semantics

## Feature Gaps vs Other Databases

### vs Neptune Analytics

| Feature | Neptune Analytics | HelixDB |
|---------|-------------------|---------|
| Managed Service | ✅ Yes | ❌ Self-hosted |
| OpenCypher | ✅ Yes | ❌ HelixQL only |
| AWS Integration | ✅ Native | ❌ Manual |
| Serverless | ✅ Yes | ❌ Always-on |
| VPC Integration | ✅ Native | ⚠️ Manual |
| Enterprise Support | ✅ AWS | ⚠️ Community |

### vs Neo4j

| Feature | Neo4j | HelixDB |
|---------|-------|---------|
| Cypher | ✅ Yes | ❌ HelixQL only |
| Graph Algorithms | ✅ Rich library | ⚠️ Limited |
| Enterprise Edition | ✅ Yes | ⚠️ Limited |
| Clustering | ✅ Yes | ❌ No |
| ACID Transactions | ✅ Full | ⚠️ Limited |

### vs Pinecone

| Feature | Pinecone | HelixDB |
|---------|----------|---------|
| Managed Service | ✅ Yes | ❌ Self-hosted |
| Metadata Filtering | ✅ Rich | ⚠️ Custom queries |
| Hybrid Search | ✅ Native | ⚠️ Manual |
| Multi-tenancy | ✅ Built-in | ❌ Manual |

### vs Weaviate

| Feature | Weaviate | HelixDB |
|---------|----------|---------|
| Vector + Schema | ✅ Yes | ✅ Yes |
| GraphQL API | ✅ Yes | ❌ No |
| Modules System | ✅ Rich | ⚠️ Limited |
| Multi-modal | ✅ Yes | ⚠️ Manual |

## Documentation Limitations

### 46. SDK Documentation 📚
**Status**: Incomplete

- helix-py docs are limited
- Some features undocumented
- Rely on examples
- Community support growing

### 47. HelixQL Documentation 📖
**Status**: Basic

- Core features documented
- Advanced features sparse
- Learning curve exists
- Community examples limited

### 48. Best Practices 💡
**Status**: Emerging

- Database is relatively new
- Few production patterns documented
- Community best practices evolving
- Experimentation may be needed

### 49. Migration Guides 🔄
**Status**: Limited

- No official migration tools
- Manual migration from other DBs
- Document your migrations
- Share learnings with community

### 50. Troubleshooting 🔧
**Status**: Basic

- Limited troubleshooting docs
- Error messages may be unclear
- Community support essential
- Document your solutions

## Compatibility Limitations

### 51. Python Version 🐍
**Requirement**: Python 3.7+

- Tested with Python 3.10-3.12
- Older versions not guaranteed
- Check helix-py compatibility

### 52. Operating System 💻
**Support**: Linux, macOS, Windows

- Best support: Linux
- macOS: Good support
- Windows: May have issues
- Use Docker if problems

### 53. Dependency Conflicts 📦
**Risk**: Low-Medium

- helix-py dependencies may conflict
- Test in virtual environment
- Pin all dependencies
- Document requirements

## Scaling Limitations

### 54. Vertical Scaling 📈
**Limitation**: Single machine

- Scale up, not out
- Hardware limits apply
- Plan for growth
- Monitor capacity

### 55. Horizontal Scaling ↔️
**Limitation**: Not supported

- No native clustering
- No sharding
- Single instance architecture
- Consider multiple instances

### 56. Data Volume 💾
**Practical Limit**: Depends on hardware

- Test with your dataset size
- Monitor disk usage
- Plan for growth
- Benchmark performance

## Known Bugs/Issues

### 57. SDK Stability 🐛
**Status**: Generally stable, but...

- New SDK (v0.2.30)
- Report issues to GitHub
- Check known issues list
- Pin stable versions

### 58. Memory Leaks 💧
**Status**: Unknown

- No known issues currently
- Monitor memory usage
- Report if found
- Restart instances if needed

### 59. Connection Pooling 🏊
**Status**: Not implemented

- One connection per client
- May need manual pooling
- Test under load
- Monitor connection count

### 60. Batch Operation Deadlocks 🔒
**Risk**: Unknown

- Test concurrent operations
- Implement retry logic
- Monitor for deadlocks
- Report to maintainers

## Future Limitations (Roadmap Items)

### 61. Native Bulk Operations 📦
**Status**: Planned

- Currently no native bulk API
- Future versions may add
- Check roadmap for updates

### 62. Graph Algorithms Library 🧮
**Status**: Planned

- Limited algorithms currently
- Future expansion expected
- Community contributions welcome

### 63. Enhanced Monitoring 📊
**Status**: Planned

- Native metrics coming
- APM integration future
- Check roadmap

### 64. Migration Tools 🔄
**Status**: Planned

- No tools currently
- Future support expected
- Community tools emerging

### 65. Managed Service Availability ☁️
**Status**: Limited beta

- Paid managed service exists
- Limited availability
- Contact for access
- Self-hosted alternative

## Mitigation Strategies

For each limitation, we recommend:

1. **Document**: Keep detailed notes on workarounds
2. **Test**: Thoroughly test in your specific use case
3. **Monitor**: Track performance and issues
4. **Plan**: Account for limitations in architecture
5. **Contribute**: Help improve docs and tools
6. **Fallback**: Have alternative approaches ready

## Getting Help

When you encounter issues:

1. Check this document first
2. Review README.md for examples
3. Check ANALYSIS.md for design decisions
4. Search GitHub issues
5. Ask in HelixDB Discord
6. Report bugs with full context

## Conclusion

This adapter is designed as a **foundation** for HelixDB integration. It provides the interface structure but requires significant user configuration to become fully functional. 

**Key Takeaway**: Plan for the limitations, implement required queries, and test thoroughly with your specific use case.

**Not Recommended For**:
- Production without query implementation
- Dynamic query generation needs
- Fully managed service requirements
- Need for OpenCypher compatibility

**Recommended For**:
- Learning HelixDB architecture
- Prototype development
- Custom query implementation
- Understanding limitations before full implementation

---

**Document Version**: 1.0  
**Last Updated**: 2025-10-11  
**Adapter Version**: Initial stub implementation  
**HelixDB Version**: Compatible with latest  
**helix-py Version**: 0.2.30+
