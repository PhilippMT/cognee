from typing import List, Optional
from cognee.low_level import DataPoint


class Repository(DataPoint):
    path: str


class ImportStatement(DataPoint):
    name: str
    module: str
    start_point: tuple
    end_point: tuple
    source_code: str
    file_path: Optional[str] = None


class MethodDefinition(DataPoint):
    name: str
    start_point: tuple
    end_point: tuple
    source_code: str
    file_path: Optional[str] = None
    metadata: dict = {"index_fields": ["source_code"]}


class ClassDefinition(DataPoint):
    name: str
    start_point: tuple
    end_point: tuple
    source_code: str
    file_path: Optional[str] = None
    metadata: dict = {"index_fields": ["source_code"]}


class InterfaceDefinition(DataPoint):
    name: str
    start_point: tuple
    end_point: tuple
    source_code: str
    file_path: Optional[str] = None
    metadata: dict = {"index_fields": ["source_code"]}


class EnumDefinition(DataPoint):
    name: str
    start_point: tuple
    end_point: tuple
    source_code: str
    file_path: Optional[str] = None
    metadata: dict = {"index_fields": ["source_code"]}


class AnnotationDefinition(DataPoint):
    name: str
    start_point: tuple
    end_point: tuple
    source_code: str
    file_path: Optional[str] = None
    metadata: dict = {"index_fields": ["source_code"]}


class FieldDefinition(DataPoint):
    name: str
    start_point: tuple
    end_point: tuple
    source_code: str
    file_path: Optional[str] = None
    metadata: dict = {"index_fields": ["source_code"]}


class ConstructorDefinition(DataPoint):
    name: str
    start_point: tuple
    end_point: tuple
    source_code: str
    file_path: Optional[str] = None
    metadata: dict = {"index_fields": ["source_code"]}


class JavaFile(DataPoint):
    name: str
    file_path: str
    source_code: Optional[str] = None
    part_of: Optional[Repository] = None
    depends_on: Optional[List["ImportStatement"]] = []
    provides_class_definition: Optional[List["ClassDefinition"]] = []
    provides_interface_definition: Optional[List["InterfaceDefinition"]] = []
    provides_enum_definition: Optional[List["EnumDefinition"]] = []
    provides_annotation_definition: Optional[List["AnnotationDefinition"]] = []
    provides_method_definition: Optional[List["MethodDefinition"]] = []
    provides_field_definition: Optional[List["FieldDefinition"]] = []
    provides_constructor_definition: Optional[List["ConstructorDefinition"]] = []
    metadata: dict = {"index_fields": ["name"]}


class JavaPart(DataPoint):
    file_path: str
    source_code: Optional[str] = None
    metadata: dict = {"index_fields": []}


class JavaSourceCodeChunk(DataPoint):
    code_chunk_of: Optional[JavaPart] = None
    source_code: Optional[str] = None
    previous_chunk: Optional["JavaSourceCodeChunk"] = None
    metadata: dict = {"index_fields": ["source_code"]}


JavaFile.model_rebuild()
JavaSourceCodeChunk.model_rebuild()