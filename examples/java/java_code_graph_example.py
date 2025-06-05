import argparse
import asyncio
import cognee
from cognee import SearchType
from cognee.shared.logging_utils import get_logger, ERROR

from cognee.api.v1.cognify.code_graph_pipeline import run_code_graph_pipeline


async def main(repo_path, include_docs):
    run_status = False
    async for run_status in run_code_graph_pipeline(repo_path, include_docs=include_docs):
        run_status = run_status

    # Test CODE search for Java-specific terms
    search_results = await cognee.search(query_type=SearchType.CODE, query_text="class")
    assert len(search_results) != 0, "The search results list is empty."
    print("\n\nJava Class Search Results:\n")
    for result in search_results:
        print(f"{result}\n")

    # Search for method declarations
    method_results = await cognee.search(query_type=SearchType.CODE, query_text="method")
    print("\n\nJava Method Search Results:\n")
    for result in method_results:
        print(f"{result}\n")

    # Search for interface implementations
    interface_results = await cognee.search(query_type=SearchType.CODE, query_text="interface")
    print("\n\nJava Interface Search Results:\n")
    for result in interface_results:
        print(f"{result}\n")

    return run_status


def parse_args():
    parser = argparse.ArgumentParser(description="Java Code Graph Example - Process Java repositories with cognee")
    parser.add_argument("--repo_path", type=str, required=True, help="Path to the Java repository")
    parser.add_argument(
        "--include_docs",
        type=lambda x: x.lower() in ("true", "1"),
        default=True,
        help="Whether or not to process non-code files (documentation, README, etc.)",
    )
    parser.add_argument(
        "--time",
        type=lambda x: x.lower() in ("true", "1"),
        default=True,
        help="Whether or not to time the pipeline run",
    )
    return parser.parse_args()


if __name__ == "__main__":
    logger = get_logger(level=ERROR)

    args = parse_args()

    print("=" * 60)
    print("Java Code Graph Example")
    print("=" * 60)
    print(f"Repository Path: {args.repo_path}")
    print(f"Include Documentation: {args.include_docs}")
    print(f"Time Execution: {args.time}")
    print("=" * 60)

    if args.time:
        import time

        start_time = time.time()
        result = asyncio.run(main(args.repo_path, args.include_docs))
        end_time = time.time()
        print("\n" + "=" * 60)
        print(f"Java Code Graph Pipeline Execution Time: {end_time - start_time:.2f} seconds")
        print(f"Pipeline Status: {'SUCCESS' if result else 'FAILED'}")
        print("=" * 60 + "\n")
    else:
        result = asyncio.run(main(args.repo_path, args.include_docs))
        print(f"\nPipeline Status: {'SUCCESS' if result else 'FAILED'}")
