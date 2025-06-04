import os
import aiofiles
import importlib
from typing import AsyncGenerator, Optional
from uuid import NAMESPACE_OID, uuid5
import tree_sitter_python as tspython
import tree_sitter_java as tsjava
from tree_sitter import Language, Node, Parser, Tree
from cognee.shared.logging_utils import get_logger

from cognee.low_level import DataPoint
from cognee.shared.CodeGraphEntities import (
    CodeFile,
    ImportStatement,
    FunctionDefinition,
    ClassDefinition,
    PackageStatement,
    InterfaceDefinition,
    EnumDefinition,
    MethodDefinition,
    FieldDefinition,
)

logger = get_logger()

PY_LANGUAGE = Language(tspython.language())
JAVA_LANGUAGE = Language(tsjava.language())


class FileParser:
    """
    Handles the parsing of files into source code and an abstract syntax tree
    representation. Public methods include:

    - parse_file: Parses a file and returns its source code and syntax tree representation.
    """

    def __init__(self):
        self.parsed_files = {}
        self.source_code_parser = Parser()

    async def parse_file(self, file_path: str) -> Optional[tuple[str, Tree]]:
        """
        Parse a file and return its source code along with its syntax tree representation.

        If the file has already been parsed, retrieve the result from memory instead of reading
        the file again.

        Parameters:
        -----------

            - file_path (str): The path of the file to parse.

        Returns:
        --------

            - Optional[tuple[str, Tree]]: A tuple containing the source code of the file and its
              corresponding syntax tree representation, or None if parsing is not supported or fails.
        """
        if file_path.endswith(".py"):
            self.source_code_parser.set_language(PY_LANGUAGE)
        elif file_path.endswith(".java"):
            self.source_code_parser.set_language(JAVA_LANGUAGE)
        else:
            logger.warning(f"Unsupported file type for parsing: {file_path}. Skipping.")
            return None, None # Or handle as per specific requirements

        if file_path not in self.parsed_files:
            source_code = await get_source_code(file_path)
            if source_code is None: # Handle case where file reading failed
                return None, None
            source_code_tree = self.source_code_parser.parse(bytes(source_code, "utf-8"))
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


def resolve_module_path(module_name):
    """
    Find the file path of a module.

    Return the file path of the specified module if found, or return None if the module does
    not exist or cannot be located.

    Parameters:
    -----------

        - module_name: The name of the module whose file path is to be resolved.

    Returns:
    --------

        The file path of the module as a string or None if the module is not found.
    """
    try:
        spec = importlib.util.find_spec(module_name)
        if spec and spec.origin:
            return spec.origin
    except ModuleNotFoundError:
        return None
    return None


def find_function_location(
    module_path: str, function_name: str, parser: FileParser
) -> Optional[tuple[str, str]]:
    """
    Find the location of a function definition in a specified module.

    Parameters:
    -----------

        - module_path (str): The path to the module where the function is defined.
        - function_name (str): The name of the function whose location is to be found.
        - parser (FileParser): An instance of FileParser used to parse the module's source
          code.

    Returns:
    --------

        - Optional[tuple[str, str]]: Returns a tuple containing the module path and the
          start point of the function if found; otherwise, returns None.
    """
    if not module_path or not os.path.exists(module_path):
        return None

    source_code, tree = parser.parse_file(module_path)
    root_node: Node = tree.root_node

    for node in root_node.children:
        if node.type == "function_definition":
            func_name_node = node.child_by_field_name("name")

            if func_name_node and func_name_node.text.decode() == function_name:
                return (module_path, node.start_point)  # (line, column)

    return None


async def get_local_script_dependencies(
    repo_path: str, script_path: str, detailed_extraction: bool = False
) -> CodeFile:
    """
    Retrieve local script dependencies and create a CodeFile object.

    Parameters:
    -----------

        - repo_path (str): The path to the repository that contains the script.
        - script_path (str): The path of the script for which dependencies are being
          extracted.
        - detailed_extraction (bool): A flag indicating whether to perform a detailed
          extraction of code components.

    Returns:
    --------

        - CodeFile: Returns a CodeFile object containing information about the script,
          including its dependencies and definitions.
    """
    code_file_parser = FileParser()
    parsed_data = await code_file_parser.parse_file(script_path)

    if parsed_data is None or parsed_data[0] is None or parsed_data[1] is None:
        # This case handles unsupported file types or files that couldn't be read/parsed.
        # Create a simple CodeFile node without source code or further analysis.
        file_path_relative_to_repo = script_path[len(repo_path) + 1 :]
        return CodeFile(
            id=uuid5(NAMESPACE_OID, script_path),
            name=file_path_relative_to_repo,
            file_path=script_path,
        )

    source_code, source_code_tree = parsed_data
    file_path_relative_to_repo = script_path[len(repo_path) + 1 :]

    if not detailed_extraction:
        code_file_node = CodeFile(
            id=uuid5(NAMESPACE_OID, script_path),
            name=file_path_relative_to_repo,
            source_code=source_code,
            file_path=script_path,
        )
        return code_file_node

    code_file_node = CodeFile(
        id=uuid5(NAMESPACE_OID, script_path),
        name=file_path_relative_to_repo,
        source_code=None,
        file_path=script_path,
    )

    async for part in extract_code_parts(source_code_tree.root_node, script_path=script_path):
        part.file_path = script_path

        if isinstance(part, FunctionDefinition):
            code_file_node.provides_function_definition.append(part)
        if isinstance(part, ClassDefinition):
            code_file_node.provides_class_definition.append(part)
        if isinstance(part, ImportStatement):
            code_file_node.depends_on.append(part)

    return code_file_node


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


def get_node_text(node: Node) -> str:
    return node.text.decode("utf-8")

def get_preceding_javadoc(node: Node) -> Optional[str]:
    """
    Attempts to find a Javadoc comment (block_comment starting with /**)
    that immediately precedes the given node.
    """
    previous_sibling = node.prev_named_sibling
    if previous_sibling and previous_sibling.type == 'block_comment':
        comment_text = get_node_text(previous_sibling)
        if comment_text.startswith("/**"):
            return comment_text
    return None

async def _extract_python_code_parts(
    tree_root: Node, script_path: str, existing_nodes: dict
) -> AsyncGenerator[DataPoint, None]:
    for child_node in tree_root.children:
        node_type = child_node.type
        node_text_bytes = child_node.text

        if node_type == "import_statement" or node_type == "import_from_statement":
            parts = get_node_text(child_node).split()
            module_name = ""
            function_name = None

            if parts[0] == "import":
                module_name = parts[1]
            elif parts[0] == "from":
                module_name = parts[1]
                if len(parts) > 3:
                    function_name = parts[3]
                    if " as " in function_name:
                        function_name = function_name.split(" as ")[0]

            if " as " in module_name:
                module_name = module_name.split(" as ")[0]

            # Yield imported function/member if applicable
            if function_name:
                key = f"import:{function_name}:{module_name}:{child_node.start_point[0]}"
                if key not in existing_nodes:
                    import_node = ImportStatement(
                        name=function_name,
                        module=module_name,
                        start_point=child_node.start_point,
                        end_point=child_node.end_point,
                        file_path=script_path,
                        source_code=node_text_bytes,
                    )
                    existing_nodes[key] = import_node
                    yield import_node

            # Yield imported module
            key = f"module_import:{module_name}:{child_node.start_point[0]}"
            if key not in existing_nodes:
                import_node = ImportStatement(
                    name=module_name, # For module import, name and module can be the same
                    module=module_name,
                    start_point=child_node.start_point,
                    end_point=child_node.end_point,
                    file_path=script_path,
                    source_code=node_text_bytes,
                )
                existing_nodes[key] = import_node
                yield import_node

        elif node_type == "function_definition":
            name_node = child_node.child_by_field_name("name")
            if name_node:
                func_name = get_node_text(name_node)
                key = f"function:{func_name}:{child_node.start_point[0]}"
                if key not in existing_nodes:
                    func_def_node = FunctionDefinition(
                        name=func_name,
                        start_point=child_node.start_point,
                        end_point=child_node.end_point,
                        file_path=script_path,
                        source_code=node_text_bytes,
                        # TODO: Add parameters, docstring if possible
                    )
                    existing_nodes[key] = func_def_node
                    yield func_def_node

        elif node_type == "class_definition":
            name_node = child_node.child_by_field_name("name")
            if name_node:
                class_name = get_node_text(name_node)
                key = f"class:{class_name}:{child_node.start_point[0]}"
                if key not in existing_nodes:
                    class_def_node = ClassDefinition(
                        name=class_name,
                        start_point=child_node.start_point,
                        end_point=child_node.end_point,
                        file_path=script_path,
                        source_code=node_text_bytes,
                        # TODO: Add docstring if possible
                    )
                    existing_nodes[key] = class_def_node
                    yield class_def_node

                # Recursively parse body of the class for nested definitions
                body_node = child_node.child_by_field_name("body")
                if body_node:
                    async for item in _extract_python_code_parts(body_node, script_path, existing_nodes):
                        yield item

async def _extract_java_code_parts(
    tree_root: Node, script_path: str, existing_nodes: dict
) -> AsyncGenerator[DataPoint, None]:
    for child_node in tree_root.named_children: # Use named_children for efficiency
        node_type = child_node.type
        node_text_bytes = child_node.text
        javadoc = get_preceding_javadoc(child_node)

        if node_type == "package_declaration":
            name_node = find_node(child_node.children, lambda n: n.type in ['identifier', 'scoped_identifier'])
            if name_node:
                package_name = get_node_text(name_node)
                key = f"package:{package_name}:{child_node.start_point[0]}"
                if key not in existing_nodes:
                    package_stmt_node = PackageStatement(
                        name=package_name,
                        start_point=child_node.start_point,
                        end_point=child_node.end_point,
                        file_path=script_path,
                        source_code=node_text_bytes,
                        comment=javadoc, # Though Javadoc on package is rare via package-info.java
                    )
                    existing_nodes[key] = package_stmt_node
                    yield package_stmt_node

        elif node_type == "import_declaration":
            name_node = find_node(child_node.children, lambda n: n.type in ['identifier', 'scoped_identifier', 'asterisk', 'type_identifier']) # Added type_identifier for some static imports
            if name_node:
                import_name = get_node_text(name_node)
                # For Java, module can be tricky, often it's part of the import_name itself
                # For simplicity, using the full import string or a part of it as module
                module_name = import_name if child_node.child_by_field_name('asterisk') else '.'.join(import_name.split('.')[:-1])
                if not module_name and import_name != '*': # handle default package import like "import SomeClass"
                    module_name = "default"


                key = f"import:{import_name}:{child_node.start_point[0]}"
                if key not in existing_nodes:
                    import_stmt_node = ImportStatement(
                        name=import_name,
                        module=module_name if module_name else import_name,
                        start_point=child_node.start_point,
                        end_point=child_node.end_point,
                        file_path=script_path,
                        source_code=node_text_bytes,
                        comment=javadoc,
                    )
                    existing_nodes[key] = import_stmt_node
                    yield import_stmt_node

        elif node_type in ["class_declaration", "interface_declaration", "enum_declaration"]:
            name_node = child_node.child_by_field_name("name")
            if name_node:
                type_name = get_node_text(name_node)
                body_node = child_node.child_by_field_name("body") # e.g., class_body, interface_body, enum_body
                body_text = get_node_text(body_node) if body_node else None
                body_bytes = body_text.encode('utf-8') if body_text else None

                key = f"{node_type}:{type_name}:{child_node.start_point[0]}"
                if key not in existing_nodes:
                    if node_type == "class_declaration":
                        instance = ClassDefinition(
                            name=type_name,
                            start_point=child_node.start_point,
                            end_point=child_node.end_point,
                            file_path=script_path,
                            source_code=node_text_bytes,
                            comment=javadoc,
                            body=body_bytes,
                        )
                    elif node_type == "interface_declaration":
                        instance = InterfaceDefinition(
                            name=type_name,
                            start_point=child_node.start_point,
                            end_point=child_node.end_point,
                            file_path=script_path,
                            source_code=node_text_bytes,
                            comment=javadoc,
                            body=body_bytes,
                        )
                    elif node_type == "enum_declaration":
                        instance = EnumDefinition(
                            name=type_name,
                            start_point=child_node.start_point,
                            end_point=child_node.end_point,
                            file_path=script_path,
                            source_code=node_text_bytes,
                            comment=javadoc,
                            body=body_bytes,
                        )
                    else: # Should not happen based on the if condition
                        continue

                    existing_nodes[key] = instance
                    yield instance

                if body_node:
                    async for item in _extract_java_code_parts(body_node, script_path, existing_nodes):
                        yield item

        elif node_type == "method_declaration":
            name_node = child_node.child_by_field_name("name")
            if name_node:
                method_name = get_node_text(name_node)

                return_type_node = child_node.child_by_field_name("type") # tree-sitter-java uses 'type' for return type
                return_type_text = get_node_text(return_type_node) if return_type_node else None

                parameters_node = child_node.child_by_field_name("parameters")
                params_list = []
                if parameters_node:
                    for param_node in parameters_node.children_by_field_name("formal_parameter"): # Or 'spread_parameter'
                        param_type_node = param_node.child_by_field_name("type")
                        param_name_node = param_node.child_by_field_name("name")
                        if param_type_node and param_name_node:
                            params_list.append({
                                "name": get_node_text(param_name_node),
                                "type": get_node_text(param_type_node),
                            })

                body_node = child_node.child_by_field_name("body")
                body_text = get_node_text(body_node) if body_node else None
                body_bytes = body_text.encode('utf-8') if body_text else None

                key = f"method:{method_name}:{child_node.start_point[0]}"
                if key not in existing_nodes:
                    method_def_node = MethodDefinition(
                        name=method_name,
                        start_point=child_node.start_point,
                        end_point=child_node.end_point,
                        file_path=script_path,
                        source_code=node_text_bytes,
                        comment=javadoc,
                        parameters=params_list,
                        return_type=return_type_text,
                        body=body_bytes,
                    )
                    existing_nodes[key] = method_def_node
                    yield method_def_node

                if body_node:
                    async for item in _extract_java_code_parts(body_node, script_path, existing_nodes):
                        yield item

        elif node_type == "field_declaration":
            field_type_node = child_node.child_by_field_name("type")
            field_type_text = get_node_text(field_type_node) if field_type_node else None

            # A field declaration can declare multiple variables, e.g., int x, y;
            for var_declarator in child_node.children_by_field_name("declarator"):
                name_node = var_declarator.child_by_field_name("name")
                if name_node:
                    field_name = get_node_text(name_node)
                    # The javadoc for a field declaration applies to all variables in it.
                    # The source_code for FieldDefinition will be the specific variable declarator.
                    var_declarator_text_bytes = var_declarator.text

                    key = f"field:{field_name}:{var_declarator.start_point[0]}"
                    if key not in existing_nodes:
                        field_def_node = FieldDefinition(
                            name=field_name,
                            field_type=field_type_text,
                            start_point=var_declarator.start_point,
                            end_point=var_declarator.end_point,
                            file_path=script_path,
                            source_code=var_declarator_text_bytes,
                            comment=javadoc,
                        )
                        existing_nodes[key] = field_def_node
                        yield field_def_node


async def extract_code_parts(
    tree_root: Node, script_path: str, existing_nodes: Optional[dict] = None
) -> AsyncGenerator[DataPoint, None]:
    """
    Extract code parts from a given AST node tree asynchronously.
    Supports both Python and Java.

    Iteratively yields DataPoint nodes representing import statements, function definitions,
    class definitions, etc. found in the children of the specified tree root.
    The function checks if nodes are already present in the existing_nodes dictionary
    to prevent duplicates.

    Parameters:
    -----------
        tree_root (Node): The root node of the AST tree.
        script_path (str): The file path of the script.
        existing_nodes (Optional[dict]): A dictionary to store already extracted nodes
                                         to avoid duplicates. Defaults to None,
                                         which initializes an empty dict.
    Returns:
    --------
        AsyncGenerator[DataPoint, None]: Yields DataPoint nodes.
    """
    if existing_nodes is None:
        existing_nodes = {}

    if script_path.endswith(".py"):
        async for item in _extract_python_code_parts(tree_root, script_path, existing_nodes):
            yield item
    elif script_path.endswith(".java"):
        async for item in _extract_java_code_parts(tree_root, script_path, existing_nodes):
            yield item
    else:
        logger.warning(f"Unsupported file type for code part extraction: {script_path}")
        return
