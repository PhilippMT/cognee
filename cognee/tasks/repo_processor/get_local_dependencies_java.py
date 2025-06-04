import tree_sitter_java as tsjava
from tree_sitter import Language, Node, Parser, Tree
from cognee.shared.logging_utils import get_logger
from cognee.low_level import DataPoint
from cognee.shared.SourceCodeGraph import (
    Class, Function, Variable, Operator, ClassInstance, FunctionCall, Expression, SourceCodeGraph
)
from uuid import NAMESPACE_OID, uuid5
from typing import AsyncGenerator, Optional
import aiofiles

logger = get_logger()

class JavaFileParser:
    def __init__(self):
        self.parsed_files = {}
        JAVA_LANGUAGE = Language(tsjava.language())
        self.source_code_parser = Parser()
        self.source_code_parser.set_language(JAVA_LANGUAGE)

    async def parse_file(self, file_path: str) -> tuple[str, Tree]:
        if file_path not in self.parsed_files:
            source_code = await get_source_code(file_path)
            source_code_tree = self.source_code_parser.parse(bytes(source_code, "utf-8"))
            self.parsed_files[file_path] = (source_code, source_code_tree)
        return self.parsed_files[file_path]

async def get_source_code(file_path: str):
    try:
        async with aiofiles.open(file_path, "r", encoding="utf-8") as f:
            source_code = await f.read()
            return source_code
    except Exception as error:
        logger.error(f"Error reading file {file_path}: {str(error)}")
        return None

async def extract_java_code_parts(tree_root: Node, script_path: str, existing_nodes: dict = None) -> AsyncGenerator[DataPoint, None]:
    if existing_nodes is None:
        existing_nodes = {}
    for child_node in tree_root.children:
        # Class extraction
        if child_node.type == "class_declaration":
            class_name_node = next((c for c in child_node.children if c.type == "identifier"), None)
            if class_name_node:
                class_name = class_name_node.text.decode()
                if class_name not in existing_nodes:
                    class_node = Class(
                        id=uuid5(NAMESPACE_OID, f"{script_path}:{class_name}"),
                        name=class_name,
                        description="",  # TODO: Extract Javadoc if present
                        constructor_parameters=[],
                        extended_from_class=None,  # TODO: Extract extends info
                        has_methods=[],
                    )
                    existing_nodes[class_name] = class_node
                yield existing_nodes[class_name]
        # Method extraction
        if child_node.type == "method_declaration":
            method_name_node = next((c for c in child_node.children if c.type == "identifier"), None)
            if method_name_node:
                method_name = method_name_node.text.decode()
                if method_name not in existing_nodes:
                    method_node = Function(
                        id=uuid5(NAMESPACE_OID, f"{script_path}:{method_name}"),
                        name=method_name,
                        description="",  # TODO: Extract Javadoc if present
                        parameters=[],  # TODO: Extract parameters
                        return_type="",  # TODO: Extract return type
                        is_static=False,  # TODO: Detect static
                    )
                    existing_nodes[method_name] = method_node
                yield existing_nodes[method_name]
        # TODO: Add extraction for imports, variables, interfaces, enums, annotations, etc.

async def get_local_java_dependencies(repo_path: str, script_path: str, detailed_extraction: bool = False) -> SourceCodeGraph:
    java_parser = JavaFileParser()
    source_code, source_code_tree = await java_parser.parse_file(script_path)
    file_path_relative_to_repo = script_path[len(repo_path) + 1 :]
    nodes = []
    async for part in extract_java_code_parts(source_code_tree.root_node, script_path=script_path):
        nodes.append(part)
    graph = SourceCodeGraph(
        id=uuid5(NAMESPACE_OID, script_path),
        name=file_path_relative_to_repo,
        description="Java 21 code graph",
        language="java",
        nodes=nodes,
    )
    return graph
