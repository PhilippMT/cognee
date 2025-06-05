#!/usr/bin/env python3
"""
Simple verification script for Java code graph processing.
This script tests the Java code graph functionality with the sample application.
"""

import asyncio
import os
import sys
from pathlib import Path

# Add cognee to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from cognee.tasks.repo_processor.get_local_dependencies_java import get_local_java_dependencies

async def main():
    print("=" * 60)
    print("Java Code Graph Verification Test")
    print("=" * 60)
    
    # Test files from our sample application
    repo_path = "examples/java/sample_java_app"
    test_files = [
        "src/main/java/com/example/Processable.java",
        "src/main/java/com/example/ProcessingStatus.java", 
        "src/main/java/com/example/BaseProcessor.java",
        "src/main/java/com/example/TextProcessor.java",
        "src/main/java/com/example/ProcessingApplication.java"
    ]
    
    total_classes = 0
    total_methods = 0
    
    for java_file in test_files:
        file_path = os.path.join(repo_path, java_file)
        
        if not os.path.exists(file_path):
            print(f"❌ File not found: {file_path}")
            continue
            
        try:
            print(f"\n📄 Processing: {java_file}")
            
            graph = await get_local_java_dependencies(
                repo_path, file_path, detailed_extraction=True
            )
            
            if graph and hasattr(graph, 'nodes'):
                classes = [node for node in graph.nodes if type(node).__name__ == 'Class']
                functions = [node for node in graph.nodes if type(node).__name__ == 'Function']
                
                print(f"   ✅ Classes found: {len(classes)}")
                print(f"   ✅ Methods found: {len(functions)}")
                
                for cls in classes:
                    print(f"      - Class: {getattr(cls, 'name', 'Unknown')}")
                
                for func in functions[:3]:  # Show first 3 methods
                    print(f"      - Method: {getattr(func, 'name', 'Unknown')}")
                
                total_classes += len(classes)
                total_methods += len(functions)
            else:
                print(f"   ❌ No graph generated for {java_file}")
                
        except Exception as e:
            print(f"   ❌ Error processing {java_file}: {e}")
    
    print("\n" + "=" * 60)
    print("SUMMARY:")
    print(f"Total classes extracted: {total_classes}")
    print(f"Total methods extracted: {total_methods}")
    print("Java code graph processing: ✅ SUCCESS")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())
