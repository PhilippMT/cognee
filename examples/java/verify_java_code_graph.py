#!/usr/bin/env python3
"""
Verification script for Java code graph processing.
Tests the Java code graph extraction on our sample Java application.
"""

import asyncio
import sys
import os

# Add the cognee module to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from cognee.tasks.repo_processor.get_local_dependencies_java import get_local_java_dependencies

REPO_PATH = "examples/java/sample_java_app"
JAVA_FILES = [
    "examples/java/sample_java_app/src/main/java/com/example/Processable.java",
    "examples/java/sample_java_app/src/main/java/com/example/ProcessingStatus.java", 
    "examples/java/sample_java_app/src/main/java/com/example/BaseProcessor.java",
    "examples/java/sample_java_app/src/main/java/com/example/TextProcessor.java",
    "examples/java/sample_java_app/src/main/java/com/example/ProcessingApplication.java"
]

async def test_java_code_graph():
    """Test Java code graph extraction on all sample files"""
    print("🔍 Testing Java Code Graph Processing")
    print("=" * 50)
    
    for java_file in JAVA_FILES:
        if not os.path.exists(java_file):
            print(f"❌ File not found: {java_file}")
            continue
            
        print(f"\n📁 Processing: {os.path.basename(java_file)}")
        try:
            graph = await get_local_java_dependencies(REPO_PATH, java_file, detailed_extraction=True)
            
            print(f"✅ Graph ID: {graph.id}")
            print(f"📄 File: {graph.name}")
            print(f"🏷️  Language: {graph.language}")
            print(f"📊 Node count: {len(graph.nodes)}")
            
            if graph.nodes:
                print("📋 Extracted elements:")
                for node in graph.nodes:
                    node_type = type(node).__name__
                    node_name = getattr(node, 'name', 'Unknown')
                    print(f"   - {node_type}: {node_name}")
            else:
                print("   ⚠️  No nodes extracted")
                
        except Exception as e:
            print(f"❌ Error processing {java_file}: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Java Code Graph verification complete!")

if __name__ == "__main__":
    asyncio.run(test_java_code_graph())
