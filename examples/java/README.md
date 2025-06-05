# Java Code Graph Example

This directory contains a comprehensive Java code graph example that demonstrates how to use cognee to process Java repositories and extract code dependencies.

## Files Structure

```
examples/java/
├── java_code_graph_example.py          # Main example script
├── sample_java_app/                    # Sample Java application
│   └── src/main/java/com/example/
│       ├── Processable.java            # Interface with generics and default methods
│       ├── ProcessingStatus.java       # Enum with methods and fields
│       ├── BaseProcessor.java          # Abstract class with inheritance
│       ├── TextProcessor.java          # Concrete implementation
│       └── ProcessingApplication.java  # Main application with supporting classes
└── README.md                           # This file
```

## Java Application Features

The sample Java application demonstrates various ontology elements that the code graph can extract:

### 1. **Processable.java** - Interface
- Generic interface (`Processable<T>`)
- Functional interface annotation
- Default methods
- Static methods
- Javadoc comments
- Exception declarations

### 2. **ProcessingStatus.java** - Enum
- Enum with fields and constructors
- Instance methods
- Static utility methods
- Method overriding (`toString`)
- Pattern matching (switch expressions)

### 3. **BaseProcessor.java** - Abstract Class
- Abstract class with generics
- Interface implementation
- Static fields and methods
- Protected and public methods
- Template method pattern
- Composition relationships
- Synchronization primitives

### 4. **TextProcessor.java** - Concrete Implementation
- Class inheritance
- Method overriding
- Regular expressions
- Private utility methods
- Constructor overloading
- Annotations (`@Override`, `@SuppressWarnings`)

### 5. **ProcessingApplication.java** - Main Application
- Main method and application entry point
- Multiple inner classes
- Exception handling
- Async programming with CompletableFuture
- Collections and streams
- Static factory methods

## Ontology Elements Covered

The Java application includes examples of:

- **Classes**: Abstract classes, concrete classes, inner classes
- **Interfaces**: Functional interfaces, generic interfaces
- **Methods**: Static methods, instance methods, abstract methods, default methods
- **Fields**: Static fields, instance fields, final fields
- **Constructors**: Default constructors, parameterized constructors
- **Enums**: Enums with fields and methods
- **Annotations**: Built-in annotations like `@Override`, `@SuppressWarnings`
- **Inheritance**: Class inheritance, interface implementation
- **Generics**: Generic classes, generic methods, bounded types
- **Exceptions**: Custom exceptions, exception handling
- **Collections**: Lists, Maps, Streams
- **Concurrency**: CompletableFuture, synchronization
- **Design Patterns**: Template method, Factory method, Strategy pattern

## Running the Example

### Prerequisites

1. Make sure you have the cognee Python environment set up
2. Ensure Java code graph dependencies are installed

### Basic Usage

```bash
# Run the Java code graph example
cd /workspaces/cognee
python examples/java/java_code_graph_example.py --repo_path examples/java/sample_java_app

# Run with additional options
python examples/java/java_code_graph_example.py \
    --repo_path examples/java/sample_java_app \
    --include_docs true \
    --time true
```

### Expected Output

The script will:

1. Process all Java files in the sample application
2. Extract code graph entities (classes, methods, interfaces, etc.)
3. Store the relationships in cognee's knowledge graph
4. Perform searches for Java-specific terms:
   - Classes
   - Methods
   - Interfaces
5. Display processing time and results

### Sample Output

```
============================================================
Java Code Graph Example
============================================================
Repository Path: examples/java/sample_java_app
Include Documentation: True
Time Execution: True
============================================================

[Processing logs...]

Java Class Search Results:
- Class: Processable (Interface)
- Class: ProcessingStatus (Enum)
- Class: BaseProcessor (Abstract Class)
- Class: TextProcessor (Concrete Class)
- Class: ProcessingApplication (Main Class)

Java Method Search Results:
- Method: process (Interface method)
- Method: doProcess (Abstract method)
- Method: main (Static method)
[... more methods ...]

Java Interface Search Results:
- Interface: Processable
[... implementation details ...]

============================================================
Java Code Graph Pipeline Execution Time: X.XX seconds
Pipeline Status: SUCCESS
============================================================
```

## Testing the Sample Application

You can also run the sample Java application directly to see it in action:

```bash
cd examples/java/sample_java_app/src/main/java
javac com/example/*.java
java com.example.ProcessingApplication
```

This will demonstrate all the implemented features and design patterns.

## Integration with Cognee

The Java code graph example integrates with cognee's broader ecosystem:

1. **Code Search**: Search for Java classes, methods, and interfaces
2. **Dependency Analysis**: Understand relationships between Java components
3. **Documentation**: Link code with documentation and comments
4. **Cross-Language**: Combine with Python code graphs for polyglot projects

## Advanced Features

The example demonstrates several advanced Java 21 features:

- **Pattern Matching**: Switch expressions with pattern matching
- **Text Blocks**: Multi-line string literals (in comments)
- **Records**: (Can be extended to include record classes)
- **Sealed Classes**: (Can be extended to include sealed hierarchies)
- **Virtual Threads**: (Can be extended for modern concurrency)

## Extending the Example

To extend this example:

1. Add more Java files with different patterns
2. Include Java 21+ features like records and sealed classes
3. Add Spring Framework or other enterprise patterns
4. Include build files (Maven/Gradle) for dependency management
5. Add unit tests to demonstrate test code analysis
