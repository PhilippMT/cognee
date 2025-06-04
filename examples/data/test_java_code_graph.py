import asyncio
from cognee.tasks.repo_processor.get_local_dependencies_java import get_local_java_dependencies

# Example Java file for testing
JAVA_TEST_FILE = "examples/data/HelloWorld.java"
REPO_PATH = "examples/data"

def print_graph(graph):
    print(f"Graph ID: {graph.id}")
    print(f"Graph Name: {graph.name}")
    print(f"Language: {graph.language}")
    print("Nodes:")
    for node in graph.nodes:
        print(f"  - {type(node).__name__}: {getattr(node, 'name', None)}")

async def main():
    graph = await get_local_java_dependencies(REPO_PATH, JAVA_TEST_FILE, detailed_extraction=True)
    print_graph(graph)

if __name__ == "__main__":
    asyncio.run(main())
