import os
import aiofiles
import importlib
from typing import AsyncGenerator, Optional
from uuid import NAMESPACE_OID, uuid5
import tree_sitter_java as tsjava
from tree_sitter import Language, Node, Parser, Tree
from cognee.shared.logging_utils import get_logger

from cognee.low_level import DataPoint
from cognee.shared.JavaCodeGraphEntities import (
    JavaFile,
    ImportStatement,
    MethodDefinition,
    ClassDefinition,
    InterfaceDefinition,
    EnumDefinition,
    AnnotationDefinition,
    FieldDefinition,
    ConstructorDefinition,
)

logger = get_logger()


class JavaFileParser:
    """
    Handles the parsing of Java files into source code and an abstract syntax tree
    representation. Public methods include:

    - parse_file: Parses a file and returns its source code and syntax tree representation.
    """

    def __init__(self):
        self.parsed_files = {}

    async def parse_file(self, file_path: str) -> tuple[str, Tree]:
        """
        Parse a file and return its source code along with its syntax tree representation.

        If the file has already been parsed, retrieve the result from memory instead of reading
        the file again.

        Parameters:
        -----------

            - file_path (str): The path of the file to parse.

        Returns:
        --------

            - tuple[str, Tree]: A tuple containing the source code of the file and its
              corresponding syntax tree representation.
        """
        JAVA_LANGUAGE = Language(tsjava.language())
        source_code_parser = Parser(JAVA_LANGUAGE)

        if file_path not in self.parsed_files:
            source_code = await get_source_code(file_path)
            source_code_tree = source_code_parser.parse(bytes(source_code, "utf-8"))
            self.parsed_files[file_path] = (source_code, source_code_tree)

        return self.parsed_files[file_path]


async def get_source_code(file_path: str):
    """
    Read source code from a file asynchronously.

    This function attempts to open a file specified by the given file path, read its
    contents, and return the source code. In case of any errors during the file reading
    process, it logs an error message and returns None.

    Parameters:
    -----------

        - file_path (str): The path to the file from which to read the source code.

    Returns:
    --------

        Returns the contents of the file as a string if successful, or None if an error
        occurs.
    """
    try:
        async with aiofiles.open(file_path, "r", encoding="utf-8") as f:
            source_code = await f.read()
            return source_code
    except Exception as error:
        logger.error(f"Error reading file {file_path}: {str(error)}")
        return None


async def get_java_local_script_dependencies(
    repo_path: str, script_path: str, detailed_extraction: bool = False
) -> JavaFile:
    """
    Retrieve local Java script dependencies and create a JavaFile object.

    Parameters:
    -----------

        - repo_path (str): The path to the repository that contains the script.
        - script_path (str): The path of the script for which dependencies are being
          extracted.
        - detailed_extraction (bool): A flag indicating whether to perform a detailed
          extraction of code components.

    Returns:
    --------

        - JavaFile: Returns a JavaFile object containing information about the script,
          including its dependencies and definitions.
    """
    code_file_parser = JavaFileParser()
    source_code, source_code_tree = await code_file_parser.parse_file(script_path)

    file_path_relative_to_repo = script_path[len(repo_path) + 1 :]

    if not detailed_extraction:
        java_file_node = JavaFile(
            id=uuid5(NAMESPACE_OID, script_path),
            name=file_path_relative_to_repo,
            source_code=source_code,
            file_path=script_path,
        )
        return java_file_node

    java_file_node = JavaFile(
        id=uuid5(NAMESPACE_OID, script_path),
        name=file_path_relative_to_repo,
        source_code=None,
        file_path=script_path,
    )

    async for part in extract_java_code_parts(source_code_tree.root_node, script_path=script_path):
        part.file_path = script_path

        if isinstance(part, MethodDefinition):
            java_file_node.provides_method_definition.append(part)
        if isinstance(part, ClassDefinition):
            java_file_node.provides_class_definition.append(part)
        if isinstance(part, InterfaceDefinition):
            java_file_node.provides_interface_definition.append(part)
        if isinstance(part, EnumDefinition):
            java_file_node.provides_enum_definition.append(part)
        if isinstance(part, AnnotationDefinition):
            java_file_node.provides_annotation_definition.append(part)
        if isinstance(part, FieldDefinition):
            java_file_node.provides_field_definition.append(part)
        if isinstance(part, ConstructorDefinition):
            java_file_node.provides_constructor_definition.append(part)
        if isinstance(part, ImportStatement):
            java_file_node.depends_on.append(part)

    return java_file_node


def find_node(nodes: list[Node], condition: callable) -> Node:
    """
    Find and return the first node that satisfies the given condition.

    Iterate through the provided list of nodes and return the first node for which the
    condition callable returns True. If no such node is found, return None.

    Parameters:
    -----------

        - nodes (list[Node]): A list of Node objects to search through.
        - condition (callable): A callable that takes a Node and returns a boolean
          indicating if the node meets specified criteria.

    Returns:
    --------

        - Node: The first Node that matches the condition, or None if no such node exists.
    """
    for node in nodes:
        if condition(node):
            return node

    return None


async def extract_java_code_parts(
    tree_root: Node, script_path: str, existing_nodes: dict = None
) -> AsyncGenerator[DataPoint, None]:
    """
    Extract code parts from a given Java AST node tree asynchronously.

    Iteratively yields DataPoint nodes representing import statements, method definitions,
    class definitions, interface definitions, enum definitions, annotation definitions,
    field definitions, and constructor definitions found in the children of the specified tree root.
    The function checks if nodes are already present in the existing_nodes dictionary to prevent duplicates.
    This function has to be used in an asynchronous context, and it requires a valid tree_root
    and proper initialization of existing_nodes.

    Parameters:
    -----------

        - tree_root (Node): The root node of the AST tree containing code parts to extract.
        - script_path (str): The file path of the script from which the AST was generated.
        - existing_nodes (dict): A dictionary that holds already extracted DataPoint nodes
          to avoid duplicates. (default None)

    Returns:
    --------

        Yields DataPoint nodes representing imported modules, methods, classes, interfaces,
        enums, annotations, fields, and constructors.
    """
    if existing_nodes is None:
        existing_nodes = {}

    # Process imports
    import_declarations = tree_root.children_by_field_name("import_declaration")
    if import_declarations:
        for import_node in import_declarations:
            import_text = import_node.text.decode("utf-8")
            parts = import_text.split()
            
            if parts[0] == "import":
                module_name = parts[1].rstrip(';')
                
                if ".*" in module_name:
                    # Wildcard import
                    module_name = module_name.replace(".*", "")
                
                if module_name not in existing_nodes:
                    import_statement_node = ImportStatement(
                        name=module_name,
                        module=module_name,
                        start_point=import_node.start_point,
                        end_point=import_node.end_point,
                        file_path=script_path,
                        source_code=import_node.text,
                    )
                    existing_nodes[module_name] = import_statement_node
                
                yield existing_nodes[module_name]

    # Process class declarations
    for child_node in tree_root.children:
        # Class declarations
        if child_node.type == "class_declaration":
            class_name_node = child_node.child_by_field_name("name")
            if class_name_node:
                class_name = class_name_node.text.decode("utf-8")
                
                if class_name not in existing_nodes:
                    class_definition_node = ClassDefinition(
                        name=class_name,
                        start_point=child_node.start_point,
                        end_point=child_node.end_point,
                        file_path=script_path,
                        source_code=child_node.text,
                    )
                    existing_nodes[class_name] = class_definition_node
                
                yield existing_nodes[class_name]
                
                # Process class body for methods, fields, and constructors
                class_body = child_node.child_by_field_name("body")
                if class_body:
                    async for part in extract_java_code_parts(class_body, script_path, existing_nodes):
                        yield part
        
        # Interface declarations
        elif child_node.type == "interface_declaration":
            interface_name_node = child_node.child_by_field_name("name")
            if interface_name_node:
                interface_name = interface_name_node.text.decode("utf-8")
                
                if interface_name not in existing_nodes:
                    interface_definition_node = InterfaceDefinition(
                        name=interface_name,
                        start_point=child_node.start_point,
                        end_point=child_node.end_point,
                        file_path=script_path,
                        source_code=child_node.text,
                    )
                    existing_nodes[interface_name] = interface_definition_node
                
                yield existing_nodes[interface_name]
                
                # Process interface body for method declarations
                interface_body = child_node.child_by_field_name("body")
                if interface_body:
                    async for part in extract_java_code_parts(interface_body, script_path, existing_nodes):
                        yield part
        
        # Enum declarations
        elif child_node.type == "enum_declaration":
            enum_name_node = child_node.child_by_field_name("name")
            if enum_name_node:
                enum_name = enum_name_node.text.decode("utf-8")
                
                if enum_name not in existing_nodes:
                    enum_definition_node = EnumDefinition(
                        name=enum_name,
                        start_point=child_node.start_point,
                        end_point=child_node.end_point,
                        file_path=script_path,
                        source_code=child_node.text,
                    )
                    existing_nodes[enum_name] = enum_definition_node
                
                yield existing_nodes[enum_name]
                
                # Process enum body
                enum_body = child_node.child_by_field_name("body")
                if enum_body:
                    async for part in extract_java_code_parts(enum_body, script_path, existing_nodes):
                        yield part
        
        # Annotation declarations
        elif child_node.type == "annotation_type_declaration":
            annotation_name_node = child_node.child_by_field_name("name")
            if annotation_name_node:
                annotation_name = annotation_name_node.text.decode("utf-8")
                
                if annotation_name not in existing_nodes:
                    annotation_definition_node = AnnotationDefinition(
                        name=annotation_name,
                        start_point=child_node.start_point,
                        end_point=child_node.end_point,
                        file_path=script_path,
                        source_code=child_node.text,
                    )
                    existing_nodes[annotation_name] = annotation_definition_node
                
                yield existing_nodes[annotation_name]
                
                # Process annotation body
                annotation_body = child_node.child_by_field_name("body")
                if annotation_body:
                    async for part in extract_java_code_parts(annotation_body, script_path, existing_nodes):
                        yield part
        
        # Method declarations
        elif child_node.type == "method_declaration":
            method_name_node = child_node.child_by_field_name("name")
            if method_name_node:
                method_name = method_name_node.text.decode("utf-8")
                method_key = f"method_{method_name}_{child_node.start_point[0]}"
                
                if method_key not in existing_nodes:
                    method_definition_node = MethodDefinition(
                        name=method_name,
                        start_point=child_node.start_point,
                        end_point=child_node.end_point,
                        file_path=script_path,
                        source_code=child_node.text,
                    )
                    existing_nodes[method_key] = method_definition_node
                
                yield existing_nodes[method_key]
        
        # Constructor declarations
        elif child_node.type == "constructor_declaration":
            constructor_name_node = child_node.child_by_field_name("name")
            if constructor_name_node:
                constructor_name = constructor_name_node.text.decode("utf-8")
                constructor_key = f"constructor_{constructor_name}_{child_node.start_point[0]}"
                
                if constructor_key not in existing_nodes:
                    constructor_definition_node = ConstructorDefinition(
                        name=constructor_name,
                        start_point=child_node.start_point,
                        end_point=child_node.end_point,
                        file_path=script_path,
                        source_code=child_node.text,
                    )
                    existing_nodes[constructor_key] = constructor_definition_node
                
                yield existing_nodes[constructor_key]
        
        # Field declarations
        elif child_node.type == "field_declaration":
            declarator = child_node.child_by_field_name("declarator")
            if declarator:
                field_name_node = declarator.child_by_field_name("name")
                if field_name_node:
                    field_name = field_name_node.text.decode("utf-8")
                    field_key = f"field_{field_name}_{child_node.start_point[0]}"
                    
                    if field_key not in existing_nodes:
                        field_definition_node = FieldDefinition(
                            name=field_name,
                            start_point=child_node.start_point,
                            end_point=child_node.end_point,
                            file_path=script_path,
                            source_code=child_node.text,
                        )
                        existing_nodes[field_key] = field_definition_node
                    
                    yield existing_nodes[field_key]