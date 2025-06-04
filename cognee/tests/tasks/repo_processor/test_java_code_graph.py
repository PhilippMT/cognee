import asyncio
import os
from uuid import uuid5, NAMESPACE_OID # For potential ID checks if necessary
import pytest # Pytest will be the test runner

from cognee.tasks.repo_processor.get_local_dependencies import get_local_script_dependencies
from cognee.shared.CodeGraphEntities import (
    CodeFile,
    PackageStatement,
    ImportStatement,
    ClassDefinition,
    InterfaceDefinition,
    EnumDefinition,
    MethodDefinition,
    FieldDefinition,
)

# Helper to run the async generator and get the CodeFile node
async def parse_java_file(repo_path_str: str, file_path_str: str) -> CodeFile:
    code_file_node = None
    # The function get_local_script_dependencies yields Repository first, then CodeFile
    # For these tests, we are interested in the CodeFile that is yielded.
    # If the function yields more than one CodeFile, this helper will need adjustment.
    async for node in get_local_script_dependencies(repo_path_str, file_path_str, detailed_extraction=True):
        if isinstance(node, CodeFile):
            code_file_node = node
            break # Assuming one CodeFile per script_path for these tests
    return code_file_node

@pytest.mark.asyncio
async def test_parse_simple_java_class(tmp_path):
    repo_dir = tmp_path / "repo"
    repo_dir.mkdir()
    sample_file_dir = repo_dir / "com" / "example" / "simple"
    sample_file_dir.mkdir(parents=True, exist_ok=True)

    java_code = """package com.example.simple;

/**
 * This is a Javadoc for SampleClass.
 * It demonstrates basic class structure.
 */
public class SampleClass {

    /**
     * Javadoc for stringField.
     */
    private String stringField;

    /**
     * Javadoc for intField.
     */
    protected int intField = 42;

    double doubleField; // No Javadoc for this field

    /**
     * Constructor Javadoc.
     * @param initialStringValue The initial value for stringField.
     */
    public SampleClass(String initialStringValue) {
        this.stringField = initialStringValue;
    }

    /**
     * Javadoc for getStringField.
     * @return The current value of stringField.
     */
    public String getStringField() {
        return stringField;
    }

    /**
     * Javadoc for setStringField.
     * @param stringField The new value for stringField.
     */
    public void setStringField(String stringField) {
        this.stringField = stringField;
    }

    /**
     * Javadoc for processData.
     * @param count The number of times to process.
     * @param data The data to process.
     * @return A processed string.
     * @throws IllegalArgumentException if count is negative.
     */
    protected String processData(int count, final String data) throws IllegalArgumentException {
        if (count < 0) {
            throw new IllegalArgumentException("Count cannot be negative");
        }
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < count; i++) {
            sb.append(data);
        }
        return sb.toString();
    }

    void utilityMethod() {
        // Do something
    }

    private static class NestedClass {
        private int nestedField;
        public void nestedMethod() {}
    }
}
"""
    java_file_path = sample_file_dir / "SampleClass.java"
    java_file_path.write_text(java_code)

    code_file_node = await parse_java_file(str(repo_dir), str(java_file_path))

    assert code_file_node is not None
    assert code_file_node.name == os.path.join("com", "example", "simple", "SampleClass.java")

    # Package
    assert len(code_file_node.provides_package_statement) == 1
    package_stmt = code_file_node.provides_package_statement[0]
    assert package_stmt.name == "com.example.simple"
    assert package_stmt.source_code == b"package com.example.simple;"

    # Class assertions - Should be 2 classes: SampleClass and NestedClass
    assert len(code_file_node.provides_class_definition) == 2

    outer_class_def = next(c for c in code_file_node.provides_class_definition if c.name == "SampleClass")
    assert outer_class_def.comment == "/**\n * This is a Javadoc for SampleClass.\n * It demonstrates basic class structure.\n */"
    assert outer_class_def.source_code.startswith(b"public class SampleClass")

    nested_class_def = next(c for c in code_file_node.provides_class_definition if c.name == "NestedClass")
    assert nested_class_def is not None
    assert nested_class_def.source_code.startswith(b"private static class NestedClass")

    # Fields
    # Expected fields: stringField, intField, doubleField (from SampleClass) + nestedField (from NestedClass)
    assert len(code_file_node.provides_field_definition) == 4

    string_field = next(f for f in code_file_node.provides_field_definition if f.name == "stringField")
    assert string_field.field_type == "String"
    assert string_field.comment == "/**\n     * Javadoc for stringField.\n     */"
    assert string_field.source_code == b"stringField"

    int_field = next(f for f in code_file_node.provides_field_definition if f.name == "intField")
    assert int_field.field_type == "int"
    assert int_field.comment == "/**\n     * Javadoc for intField.\n     */"
    assert int_field.source_code == b"intField = 42"

    double_field = next(f for f in code_file_node.provides_field_definition if f.name == "doubleField")
    assert double_field.field_type == "double"
    assert double_field.comment is None
    assert double_field.source_code == b"doubleField"

    nested_field = next(f for f in code_file_node.provides_field_definition if f.name == "nestedField")
    assert nested_field.field_type == "int" # Assuming type is inferred or defined for nestedField
    assert nested_field.comment is None # No Javadoc for nestedField in sample
    assert nested_field.source_code == b"nestedField"

    # Methods
    # Expected methods: SampleClass (constructor), getStringField, setStringField, processData, utilityMethod (from SampleClass)
    # + nestedMethod (from NestedClass)
    # Total methods = 5 (outer) + 1 (nested) = 6
    assert len(code_file_node.provides_method_definition) == 6

    constructor = next(m for m in code_file_node.provides_method_definition if m.name == "SampleClass")
    assert constructor.return_type is None
    assert len(constructor.parameters) == 1
    assert constructor.parameters[0] == {"name": "initialStringValue", "type": "String"}
    assert constructor.comment == "/**\n     * Constructor Javadoc.\n     * @param initialStringValue The initial value for stringField.\n     */"

    get_string_method = next(m for m in code_file_node.provides_method_definition if m.name == "getStringField")
    assert get_string_method.return_type == "String"
    assert len(get_string_method.parameters) == 0
    assert get_string_method.comment == "/**\n     * Javadoc for getStringField.\n     * @return The current value of stringField.\n     */"

    set_string_method = next(m for m in code_file_node.provides_method_definition if m.name == "setStringField")
    assert set_string_method.return_type == "void"
    assert len(set_string_method.parameters) == 1
    assert set_string_method.parameters[0] == {"name": "stringField", "type": "String"}
    assert set_string_method.comment == "/**\n     * Javadoc for setStringField.\n     * @param stringField The new value for stringField.\n     */"

    process_data_method = next(m for m in code_file_node.provides_method_definition if m.name == "processData")
    assert process_data_method.return_type == "String"
    assert len(process_data_method.parameters) == 2
    assert process_data_method.parameters[0] == {"name": "count", "type": "int"}
    assert process_data_method.parameters[1] == {"name": "data", "type": "String"}
    assert process_data_method.comment.startswith("/**\n     * Javadoc for processData.")

    utility_method = next(m for m in code_file_node.provides_method_definition if m.name == "utilityMethod")
    assert utility_method.return_type == "void"
    assert utility_method.comment is None

    nested_method = next(m for m in code_file_node.provides_method_definition if m.name == "nestedMethod")
    assert nested_method.return_type == "void" # Assuming void from sample
    assert len(nested_method.parameters) == 0
    assert nested_method.comment is None


@pytest.mark.asyncio
async def test_parse_java_package_and_imports(tmp_path):
    repo_dir = tmp_path / "repo"
    repo_dir.mkdir()
    sample_file_dir = repo_dir / "com" / "example" / "imports"
    sample_file_dir.mkdir(parents=True, exist_ok=True)
    java_code = """package com.example.imports;

import java.util.List; // Single type import
import java.util.Map.*; // On-demand import (inner class)
import java.io.*; // On-demand import (whole package)
import static com.example.simple.SampleClass.NestedClass;

/**
 * This class is just for testing package and import statements.
 */
public class PackageAndImports {
    private List<String> items;
}
"""
    java_file_path = sample_file_dir / "PackageAndImports.java"
    java_file_path.write_text(java_code)

    code_file_node = await parse_java_file(str(repo_dir), str(java_file_path))

    assert code_file_node is not None

    # Package
    assert len(code_file_node.provides_package_statement) == 1
    package_stmt = code_file_node.provides_package_statement[0]
    assert package_stmt.name == "com.example.imports"

    # Imports
    assert len(code_file_node.depends_on) == 4
    imports_found = {imp.name: imp for imp in code_file_node.depends_on}

    assert "List" in imports_found
    assert imports_found["List"].module == "java.util.List" # or java.util based on extraction

    assert "*" in imports_found # For Map.*
    assert imports_found["*"].module == "java.util.Map" # Assuming module is the part before .*

    assert "java.io.*" in imports_found or "*" in imports_found and imports_found["*"].module == "java.io"
    # The name might be "*" and module "java.io", or name "java.io.*"

    assert "NestedClass" in imports_found
    assert imports_found["NestedClass"].module == "com.example.simple.SampleClass" # For static import
    assert imports_found["NestedClass"].source_code == b"import static com.example.simple.SampleClass.NestedClass;"

@pytest.mark.asyncio
async def test_parse_java_interface(tmp_path):
    repo_dir = tmp_path / "repo"
    repo_dir.mkdir()
    sample_file_dir = repo_dir / "com" / "example" / "interfaces"
    sample_file_dir.mkdir(parents=True, exist_ok=True)
    java_code = """package com.example.interfaces;

/**
 * Javadoc for SampleInterface.
 * This interface defines a contract for something.
 */
public interface SampleInterface {

    /**
     * Javadoc for performAction.
     * @param actionName The name of the action.
     * @param level The intensity level.
     */
    void performAction(String actionName, int level);

    /**
     * Javadoc for checkStatus.
     * @return True if status is okay, false otherwise.
     */
    boolean checkStatus();

    /**
     * Javadoc for defaultMethod.
     */
    default void defaultMethod() {
        System.out.println("Default implementation");
    }
}
"""
    java_file_path = sample_file_dir / "SampleInterface.java"
    java_file_path.write_text(java_code)

    code_file_node = await parse_java_file(str(repo_dir), str(java_file_path))

    assert code_file_node is not None
    assert len(code_file_node.provides_interface_definition) == 1
    interface_def = code_file_node.provides_interface_definition[0]

    assert interface_def.name == "SampleInterface"
    assert interface_def.comment == "/**\n * Javadoc for SampleInterface.\n * This interface defines a contract for something.\n */"

    assert len(code_file_node.provides_method_definition) == 3 # performAction, checkStatus, defaultMethod

    perform_action = next(m for m in code_file_node.provides_method_definition if m.name == "performAction")
    assert perform_action.return_type == "void"
    assert len(perform_action.parameters) == 2
    assert perform_action.parameters[0] == {"name": "actionName", "type": "String"}
    assert perform_action.parameters[1] == {"name": "level", "type": "int"}
    assert perform_action.comment.startswith("/**\n     * Javadoc for performAction.")
    assert perform_action.body is None # Abstract method

    check_status = next(m for m in code_file_node.provides_method_definition if m.name == "checkStatus")
    assert check_status.return_type == "boolean"
    assert len(check_status.parameters) == 0
    assert check_status.comment.startswith("/**\n     * Javadoc for checkStatus.")
    assert check_status.body is None # Abstract method

    default_method = next(m for m in code_file_node.provides_method_definition if m.name == "defaultMethod")
    assert default_method.return_type == "void"
    assert len(default_method.parameters) == 0
    assert default_method.comment.startswith("/**\n     * Javadoc for defaultMethod.")
    assert default_method.body is not None
    assert b"System.out.println" in default_method.body

@pytest.mark.asyncio
async def test_parse_java_enum(tmp_path):
    repo_dir = tmp_path / "repo"
    repo_dir.mkdir()
    sample_file_dir = repo_dir / "com" / "example" / "enums"
    sample_file_dir.mkdir(parents=True, exist_ok=True)
    java_code = """package com.example.enums;

/**
 * Javadoc for SampleEnum.
 * Represents different states.
 */
public enum SampleEnum {
    /** Javadoc for STATE_ONE. */
    STATE_ONE(10) {
        @Override
        public String customBehavior() {
            return "Behavior for STATE_ONE";
        }
    },
    /** Javadoc for STATE_TWO. */
    STATE_TWO(20),
    STATE_THREE(30);

    /** Javadoc for internalValue. */
    private final int internalValue;

    SampleEnum(int value) { // Constructor
        this.internalValue = value;
    }

    public int getInternalValue() {
        return internalValue;
    }

    public String customBehavior() {
        return "Default behavior";
    }
}
"""
    java_file_path = sample_file_dir / "SampleEnum.java"
    java_file_path.write_text(java_code)

    code_file_node = await parse_java_file(str(repo_dir), str(java_file_path))

    assert code_file_node is not None
    assert len(code_file_node.provides_enum_definition) == 1
    enum_def = code_file_node.provides_enum_definition[0]

    assert enum_def.name == "SampleEnum"
    assert enum_def.comment == "/**\n * Javadoc for SampleEnum.\n * Represents different states.\n */"

    # Enum constants are often parsed as fields.
    # Expected constants/fields: STATE_ONE, STATE_TWO, STATE_THREE, internalValue
    assert len(code_file_node.provides_field_definition) == 4

    state_one = next(f for f in code_file_node.provides_field_definition if f.name == "STATE_ONE")
    assert state_one.comment == "/** Javadoc for STATE_ONE. */"
    # Type for enum constant might be the enum itself or not explicitly typed by tree-sitter in a simple way for fields.

    state_two = next(f for f in code_file_node.provides_field_definition if f.name == "STATE_TWO")
    assert state_two.comment == "/** Javadoc for STATE_TWO. */"

    state_three = next(f for f in code_file_node.provides_field_definition if f.name == "STATE_THREE")
    assert state_three.comment is None

    internal_value_field = next(f for f in code_file_node.provides_field_definition if f.name == "internalValue")
    assert internal_value_field.field_type == "int"
    assert internal_value_field.comment == "/** Javadoc for internalValue. */"

    # Methods: SampleEnum (constructor), getInternalValue, customBehavior (plus one overridden customBehavior in STATE_ONE)
    # Tree-sitter might parse the overridden method as a separate method within an anonymous class for the enum constant.
    # For simplicity, we'll check for the main methods.
    # The constructor `SampleEnum(int value)`
    # `getInternalValue()`
    # `customBehavior()` - the general one
    # `customBehavior()` - the one inside STATE_ONE (This might be harder to isolate without more structure)

    # Check for methods defined in the enum body directly.
    # The overridden method in STATE_ONE might be part of the EnumConstant's own body if the parser handles it that way.
    # Current parser likely flattens methods.

    constructor = next(m for m in code_file_node.provides_method_definition if m.name == "SampleEnum")
    assert constructor.return_type is None # Enum constructors also have no 'type' for return
    assert len(constructor.parameters) == 1
    assert constructor.parameters[0] == {"name": "value", "type": "int"}

    get_internal_value_method = next(m for m in code_file_node.provides_method_definition if m.name == "getInternalValue")
    assert get_internal_value_method.return_type == "int"

    # There will be two customBehavior methods if the overridden one is also captured.
    custom_behavior_methods = [m for m in code_file_node.provides_method_definition if m.name == "customBehavior"]
    assert len(custom_behavior_methods) >= 1 # At least the main one
    # The one inside STATE_ONE might be harder to assert directly without knowing how tree-sitter structures enum constant bodies with methods

    # Check the main customBehavior method
    main_custom_behavior = next(m for m in custom_behavior_methods if b"Default behavior" in m.source_code)
    assert main_custom_behavior is not None

    # If the overridden one is parsed, its body would be different
    overridden_custom_behavior = next((m for m in custom_behavior_methods if b"Behavior for STATE_ONE" in m.source_code), None)
    assert overridden_custom_behavior is not None # This asserts the overridden one is also found

```
