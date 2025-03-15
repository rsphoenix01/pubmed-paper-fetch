PubMed Paper Fetcher Project Report
Introduction
This project was designed to meet the assignment requirements for a Python-based command-line tool that fetches research papers from PubMed based on a user-specified query. The tool filters the results to include only papers with at least one author affiliated with a pharmaceutical or biotech company. The filtered data is then output as a CSV file. The project was developed with a focus on clean code, modular design, proper dependency management using Poetry, and continuous integration through GitHub Actions.

Approach & Methodology
1. Requirements Analysis
Data Source: PubMed API using ESearch and EFetch endpoints.
Filtering Criteria: Include only those papers that have at least one author with a non-academic (pharmaceutical/biotech) affiliation.
Output: CSV file containing:
PubmedID
Title
Publication Date
Non-academic Author(s)
Company Affiliation(s)
Corresponding Author Email
Command-line Interface: Accept query parameters and options for debug output and output file location.
Development Practices:
Typed Python code
Modular design (splitting core functionality and CLI)
Unit testing with pytest
Version control with Git and hosted on GitHub
Continuous integration (CI) using GitHub Actions
Dependency management with Poetry
2. Implementation Details
a. Module Development (pubmed_fetcher)
API Interaction:
Used PubMed’s ESearch API to retrieve a list of PubMed IDs matching the user query.
Utilized PubMed’s EFetch API to obtain detailed XML data for each paper.
XML Parsing & Filtering:
Employed Python’s xml.etree.ElementTree for parsing XML responses.
Implemented functions to extract key details (e.g., title, publication date, author affiliations).
Developed helper functions to identify non-academic and company affiliations using keyword-based heuristics.
Extracted corresponding author emails using regular expressions.
b. Command-line Interface (cli.py)
Argument Parsing:
Used the argparse module to support command-line arguments:
Query string for the search.
Debug flag (-d/--debug) for verbose output.
File flag (-f/--file) to specify CSV output destination.
Integration:
The CLI invokes the core functions from the pubmed_fetcher module and either prints the CSV output to the console or writes it to a file.
Entry Point:
Configured the CLI as an executable command (get-papers-list) via Poetry's [tool.poetry.scripts].
c. Dependency Management & Packaging
Poetry:
Managed project dependencies and packaging using Poetry.
Defined project metadata and dependencies in pyproject.toml.
Declared the package directory to ensure the module is recognized and installed correctly.
d. Testing & Continuous Integration
Unit Testing:
Created tests using pytest for key functions (e.g., affiliation detection, email extraction, XML parsing).
Tests ensure that filtering logic works as expected.
GitHub Actions:
Configured a CI workflow (.github/workflows/python-app.yml) to automatically run tests on every push or pull request.
The workflow sets up Python, installs Poetry, installs dependencies, and runs the test suite.
Results
Functionality:
The CLI successfully fetches papers from PubMed and filters results according to the specified criteria.
The CSV output contains all required columns and accurately represents the filtered data.
Testing:
Unit tests have been implemented and are executed automatically through GitHub Actions.
The CI pipeline passes successfully, ensuring code quality and robustness.
Packaging:
The project is properly packaged with Poetry and can be installed locally. An executable command (get-papers-list) is available for use.
Documentation:
The repository includes comprehensive documentation (README.md) detailing installation, usage, and contribution guidelines.
Future Considerations:
Optionally, the module can be published to Test PyPI for broader distribution.
Further refinements to affiliation detection and error handling can be added based on user feedback.
Conclusion
The PubMed Paper Fetcher project meets the assignment specifications by:

Fetching and filtering research papers from PubMed.
Providing a robust command-line interface.
Utilizing modern development practices, including dependency management with Poetry, version control, unit testing, and CI via GitHub Actions.
This project not only fulfills the core requirements but also lays the groundwork for further enhancements and potential distribution to a wider audience.
