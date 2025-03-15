# PubMed Paper Fetcher

This project provides a Python module and command-line interface to fetch research papers from PubMed based on a user-specified query. The program filters results to include only papers with at least one author affiliated with a pharmaceutical or biotech company. The CSV output contains the following columns:

- **PubmedID**: Unique identifier for the paper.
- **Title**: Title of the paper.
- **Publication Date**: Date the paper was published.
- **Non-academic Author(s)**: Names of authors affiliated with non-academic institutions.
- **Company Affiliation(s)**: Names of pharmaceutical/biotech companies.
- **Corresponding Author Email**: Email address of the corresponding author.

## Project Structure

- `pubmed_fetcher.py`: Contains functions to interact with the PubMed API, parse XML responses, and filter papers.
- `cli.py`: Command-line interface that accepts a query and options (debug mode and output file) and prints or saves the CSV.
- `pyproject.toml`: Poetry configuration for dependency management and packaging.
- `README.md`: Documentation and usage instructions.

## Installation

1. **Prerequisites:**  
   - Python 3.8 or later  
   - [Poetry](https://python-poetry.org/docs/#installation)

2. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/pubmed-paper-fetcher.git
   cd pubmed-paper-fetcher
