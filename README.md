# Website Information Extractor

## Overview

The Website Information Extractor is a Python-based command-line tool that processes a list of URLs to extract and display website logos and phone numbers. The tool supports concurrent processing of multiple URLs to enhance performance and efficiency.

This application is designed to be run both as a standalone Python module or within a Docker container, depending on the user's environment and requirements.

## Libraries Used

### Requests

**Why**: The `requests` library is used for making HTTP requests to fetch web pages. It is chosen for its ease of use, community support, and ability to handle various types of HTTP requests efficiently.

**Benefits**:

- Simplifies HTTP request management.
- Supports session handling, which can be used for maintaining persistent connections.
- Robust error handling capabilities.

### BeautifulSoup4

**Why**: `beautifulsoup4` is utilized for parsing HTML documents and extracting necessary data (e.g., logos and phone numbers). It is preferred for its flexibility and effectiveness in navigating and searching the parse tree.

**Benefits**:

- Parses malformed HTML and XML documents gracefully.
- Provides simple methods and Pythonic idioms for navigating, searching, and modifying the parse tree.
- Compatible with multiple parsers like `lxml` and `html5lib`, giving flexibility depending on the required level of parsing.

### Concurrent.futures

**Why**: The `concurrent.futures` module is used to provide a high-level interface for asynchronously executing callables. It is integral to the tool's ability to process multiple URLs in parallel, significantly improving performance.

**Benefits**:

- Simplifies thread and process management.
- Provides a future-based interface for result management.
- Enhances overall responsiveness and throughput of the application when dealing with I/O-bound tasks.

## Best Practices

### Error Handling

- Comprehensive error handling strategies are implemented to manage exceptions and unexpected outcomes during HTTP requests and data parsing processes.
- Errors are logged to STDERR, maintaining clean output streams for result data.

### Code Modularity

- The application is structured into classes and functions that handle specific tasks, improving modularity and readability.
- Separate functions for fetching data, parsing content, and executing concurrent tasks make the codebase easier to maintain and extend.

### Concurrency

- Utilizing `ThreadPoolExecutor` for managing a pool of threads, which handle tasks concurrently rather than sequentially, optimizing resource use and execution time.
- Proper management of thread pools to prevent resource leakage and ensure that all processes are completed gracefully.

### Docker Integration

- Docker is used to encapsulate the project's environment, ensuring consistency across different development and production setups.
- The Dockerfile is optimized for Python environments, ensuring lightweight containers and straightforward deployments.

### Input and Output Handling

- The application is designed to read URLs from standard input and output results in JSON format to standard output. This design supports flexible integration with other tools and systems in a pipeline.

### Extensibility

- The project is structured to allow easy updates and modifications, particularly in the areas of regex patterns and HTML parsing criteria to accommodate changes in web standards or project requirements.

## Usage Guidelines

- The tool is designed to be intuitive and easy to use from the command line, catering both to development and production needs.
- Detailed usage instructions provided in the README ensure that users can effectively operate the tool without prior in-depth knowledge of its internal workings.

## Setup

### Prerequisites

- Python 3.9 or higher
- Docker (for Docker-based execution)

### Installation

1. **Clone the repository:**

```bash
git clone https://website_info_extractor.git
cd website_info_extractor
```

## Running the script

### As a Standalone Python Module

1. Install the Python package(Is recommended to use virtual environment):

```bash
pip install -r requirements.txt
```

2. Acces the src/ folder

```bash
cd src/
```

3. Run the script with input from a file:

```bash
cat websites.txt | python3 -m main
```

If Windows:

```bash
type websites.txt | python3 -m main
```

### Using Docker

1. Build the Docker image, on the root folder:

```bash
docker build -t website-info-extractor .
```

2. Run the Docker container with input from a file:

```bash
docker run -i website-info-extractor
```

## Running Tests

Testing is an essential part of ensuring the reliability and correctness of the application. Below are the instructions for running the tests in both a standalone environment and within a Docker container.

### Running Tests in a Standalone Environment

To run the tests on your local machine without Docker, follow these steps:

1. **Navigate to the src/ folder**:

2. **Install the required dependencies** (if not already installed):
   ```bash
   pip install -r requirements.txt
   ```
3. Run the tests using Python’s pytest framework:

```bash
python3 test_info_extractor.py
```

If Windows:

```bash
python test_info_extractor.py
```
