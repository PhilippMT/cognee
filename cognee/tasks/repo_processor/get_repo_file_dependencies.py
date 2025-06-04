import asyncio
import math
import os

# from concurrent.futures import ProcessPoolExecutor
from typing import AsyncGenerator
from uuid import NAMESPACE_OID, uuid5

from cognee.infrastructure.engine import DataPoint
from cognee.shared.CodeGraphEntities import CodeFile, Repository


async def get_source_code_files(repo_path):
    """
    Retrieve Python source code files from the specified repository path.

    This function scans the given repository path for files that have the .py extension
    while excluding test files and files within a virtual environment. It returns a list of
    absolute paths to the source code files that are not empty.

    Parameters:
    -----------

        - repo_path: The file path to the repository to search for Python source files.

    Returns:
    --------

        A list of absolute paths to .py files that contain source code, excluding empty
        files, test files, and files from a virtual environment.
    """
    if not os.path.exists(repo_path):
        return {}

    source_files_paths = []
    excluded_python_dirs = [os.path.join(repo_path, ".venv")]
    excluded_java_dirs = [
        os.path.join(repo_path, "target"),
        os.path.join(repo_path, "build"),
        os.path.join(repo_path, "out"),
        os.path.join(repo_path, ".gradle"),
        os.path.join(repo_path, ".mvn"),
    ]

    for root, _, files in os.walk(repo_path):
        # Python specific directory exclusions
        if any(excluded_dir in root for excluded_dir in excluded_python_dirs):
            continue

        # Java specific directory exclusions
        if any(excluded_dir in root for excluded_dir in excluded_java_dirs):
            continue

        for file in files:
            is_python_file = file.endswith(".py")
            is_java_file = file.endswith(".java")

            if is_python_file:
                if file.startswith("test_") or file.endswith("_test.py"):
                    continue
            elif is_java_file:
                if file.endswith("Test.java") or file.startswith("Test"):
                    continue
            elif not is_python_file and not is_java_file:
                continue

            file_path = os.path.join(root, file)
            file_path = os.path.abspath(file_path)

            if os.path.getsize(file_path) == 0:
                continue

            source_files_paths.append(file_path)

    return list(set(source_files_paths))


def run_coroutine(coroutine_func, *args, **kwargs):
    """
    Run a coroutine function until it completes.

    This function creates a new asyncio event loop, sets it as the current loop, and
    executes the given coroutine function with the provided arguments. Once the coroutine
    completes, the loop is closed. Intended for use in environments where an existing event
    loop is not available or desirable.

    Parameters:
    -----------

        - coroutine_func: The coroutine function to be run.
        - *args: Positional arguments to pass to the coroutine function.
        - **kwargs: Keyword arguments to pass to the coroutine function.

    Returns:
    --------

        The result returned by the coroutine after completion.
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(coroutine_func(*args, **kwargs))
    loop.close()
    return result


async def get_repo_file_dependencies(
    repo_path: str, detailed_extraction: bool = False
) -> AsyncGenerator[DataPoint, None]:
    """
    Generate a dependency graph for Python files in the given repository path.

    Check the validity of the repository path and yield a repository object followed by the
    dependencies of Python files within that repository. Raise a FileNotFoundError if the
    provided path does not exist. The extraction of detailed dependencies can be controlled
    via the `detailed_extraction` argument.

    Parameters:
    -----------

        - repo_path (str): The file path to the repository where Python files are located.
        - detailed_extraction (bool): A flag indicating whether to perform a detailed
          extraction of dependencies (default is False). (default False)
    """

    if not os.path.exists(repo_path):
        raise FileNotFoundError(f"Repository path {repo_path} does not exist.")

    source_code_files = await get_source_code_files(repo_path)

    repo = Repository(
        id=uuid5(NAMESPACE_OID, repo_path),
        path=repo_path,
    )

    yield repo

    chunk_size = 100
    number_of_chunks = math.ceil(len(source_code_files) / chunk_size)
    chunk_ranges = [
        (
            chunk_number * chunk_size,
            min((chunk_number + 1) * chunk_size, len(source_code_files)) - 1,
        )
        for chunk_number in range(number_of_chunks)
    ]

    # Codegraph dependencies are not installed by default, so we import where we use them.
    from cognee.tasks.repo_processor.get_local_dependencies import get_local_script_dependencies

    for start_range, end_range in chunk_ranges:
        # with ProcessPoolExecutor(max_workers=12) as executor:
        tasks = [
            get_local_script_dependencies(repo_path, file_path, detailed_extraction)
            for file_path in source_code_files[start_range : end_range + 1]
        ]

        results: list[CodeFile] = await asyncio.gather(*tasks)

        for source_code_file in results:
            source_code_file.part_of = repo

            yield source_code_file
