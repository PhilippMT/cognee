import os
import asyncio
import tempfile
from uuid import uuid4

from cognee.tasks.repo_processor.get_java_file_dependencies import get_java_repo_file_dependencies
from cognee.shared.JavaCodeGraphEntities import JavaFile, ClassDefinition, MethodDefinition


def test_java_code_graph():
    # Create a temporary Java file for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        java_file_path = os.path.join(temp_dir, "TestClass.java")
        
        # Simple Java class with methods
        java_content = """
package com.example;

import java.util.List;
import java.util.ArrayList;

/**
 * This is a test class for Java code graph
 */
public class TestClass {
    private String name;
    private int count;
    
    public TestClass(String name) {
        this.name = name;
        this.count = 0;
    }
    
    public void incrementCount() {
        this.count++;
    }
    
    public int getCount() {
        return this.count;
    }
    
    public String getName() {
        return this.name;
    }
}
"""
        
        with open(java_file_path, "w") as f:
            f.write(java_content)
        
        # Run the Java code graph extraction
        results = []
        
        async def collect_results():
            async for result in get_java_repo_file_dependencies(temp_dir, detailed_extraction=True):
                results.append(result)
        
        asyncio.run(collect_results())
        
        # Verify the results
        assert len(results) > 0, "No results were returned"
        
        # First result should be the Repository
        assert results[0].path == temp_dir
        
        # Second result should be the JavaFile
        java_file = next((r for r in results if isinstance(r, JavaFile)), None)
        assert java_file is not None, "JavaFile not found in results"
        assert java_file.name.endswith("TestClass.java")
        
        # Check that we have class definitions
        assert len(java_file.provides_class_definition) > 0, "No class definitions found"
        class_def = java_file.provides_class_definition[0]
        assert class_def.name == "TestClass"
        
        # Check that we have method definitions
        assert len(java_file.provides_method_definition) > 0, "No method definitions found"
        
        # Check that we have imports
        assert len(java_file.depends_on) > 0, "No imports found"
        
        # Check that we have field definitions
        assert len(java_file.provides_field_definition) > 0, "No field definitions found"
        
        # Check that we have constructor definitions
        assert len(java_file.provides_constructor_definition) > 0, "No constructor definitions found"