from typing import List, Optional, Tuple, Dict
from pydantic import Field
from cognee.low_level import DataPoint


class Repository(DataPoint):
    path: str


class ImportStatement(DataPoint):
    name: str
    module: str
    start_point: tuple
    end_point: tuple
    source_code: bytes # Changed to bytes as per recent plan for new entities, keeping consistent for now
    file_path: Optional[str] = None
    comment: Optional[str] = None # Added field


class FunctionDefinition(DataPoint):
    name: str
    start_point: Tuple[int, int]
    end_point: Tuple[int, int]
    source_code: bytes # Changed to bytes
    file_path: Optional[str] = None
    comment: Optional[str] = None # Added field for docstrings/javadoc
    parameters: Optional[List[Dict[str, str]]] = None # e.g., [{'name': 'param_name', 'type': 'param_type'}]
    return_type: Optional[str] = None
    metadata: dict = {"index_fields": ["source_code"]}


class ClassDefinition(DataPoint):
    name: str
    start_point: Tuple[int, int]
    end_point: Tuple[int, int]
    source_code: bytes # Changed to bytes
    file_path: Optional[str] = None
    comment: Optional[str] = None # Added field for docstrings/javadoc
    body: Optional[bytes] = None # Source code of the body
    # Consider fields for extended classes, implemented interfaces
    metadata: dict = {"index_fields": ["name", "source_code"]}


# New Java-specific entities

class PackageStatement(DataPoint):
    name: str
    start_point: Tuple[int, int]
    end_point: Tuple[int, int]
    file_path: str # Making this non-optional as it's essential
    source_code: bytes
    comment: Optional[str] = None # For any package-level comments (rare for Javadoc)

class InterfaceDefinition(DataPoint):
    name: str
    start_point: Tuple[int, int]
    end_point: Tuple[int, int]
    file_path: str
    source_code: bytes
    comment: Optional[str] = None # For Javadoc
    body: Optional[bytes] = None # Source code of the body
    # Consider fields for extended interfaces: extends_interfaces: Optional[List[str]] = Field(default_factory=list)
    metadata: dict = {"index_fields": ["name", "source_code"]}

class EnumDefinition(DataPoint):
    name: str
    start_point: Tuple[int, int]
    end_point: Tuple[int, int]
    file_path: str
    source_code: bytes
    comment: Optional[str] = None # For Javadoc
    body: Optional[bytes] = None # Source code of the body
    # Consider fields for implemented interfaces and enum constants
    # implements_interfaces: Optional[List[str]] = Field(default_factory=list)
    # constants: Optional[List[str]] = Field(default_factory=list)
    metadata: dict = {"index_fields": ["name", "source_code"]}

class MethodDefinition(DataPoint):
    name: str
    start_point: Tuple[int, int]
    end_point: Tuple[int, int]
    file_path: str
    source_code: bytes
    parameters: Optional[List[Dict[str, str]]] = Field(default_factory=list) # e.g., [{'name': 'param_name', 'type': 'param_type'}]
    return_type: Optional[str] = None
    comment: Optional[str] = None # For Javadoc
    body: Optional[bytes] = None # Source code of the method body
    metadata: dict = {"index_fields": ["name", "source_code"]}

class FieldDefinition(DataPoint):
    name: str
    field_type: Optional[str] = None # Changed from type to field_type to avoid Pydantic conflict
    start_point: Tuple[int, int]
    end_point: Tuple[int, int]
    file_path: str
    source_code: bytes
    comment: Optional[str] = None # For Javadoc
    metadata: dict = {"index_fields": ["name"]}


class CodeFile(DataPoint):
    name: str
    file_path: str
    source_code: Optional[bytes] = None # Changed to bytes
    part_of: Optional[Repository] = None
    depends_on: List[ImportStatement] = Field(default_factory=list) # Ensure list
    provides_function_definition: List[FunctionDefinition] = Field(default_factory=list) # Ensure list
    provides_class_definition: List[ClassDefinition] = Field(default_factory=list) # Ensure list
    # Adding new fields for Java entities
    provides_package_statement: List[PackageStatement] = Field(default_factory=list)
    provides_interface_definition: List[InterfaceDefinition] = Field(default_factory=list)
    provides_enum_definition: List[EnumDefinition] = Field(default_factory=list)
    provides_method_definition: List[MethodDefinition] = Field(default_factory=list)
    provides_field_definition: List[FieldDefinition] = Field(default_factory=list)
    metadata: dict = {"index_fields": ["name"]}


class CodePart(DataPoint):
    file_path: str
    source_code: Optional[bytes] = None # Changed to bytes
    metadata: dict = {"index_fields": []}


class SourceCodeChunk(DataPoint):
    code_chunk_of: Optional[CodePart] = None
    source_code: Optional[bytes] = None # Changed to bytes
    previous_chunk: Optional["SourceCodeChunk"] = None
    metadata: dict = {"index_fields": ["source_code"]}


CodeFile.model_rebuild()
SourceCodeChunk.model_rebuild()
