import argparse
import csv
import sys
from typing import List, Dict
from pubmed_fetcher.pubmed_fetcher import get_papers

def main() -> None:
    """
    Command-line interface to fetch papers based on a query and output as CSV.
    """
    parser = argparse.ArgumentParser(
        description="Fetch research papers from PubMed with non-academic authors from pharma/biotech companies."
    )
    parser.add_argument("query", type=str, help="PubMed query to search for papers.")
    parser.add_argument("-d", "--debug", action="store_true", help="Print debug information during execution.")
    parser.add_argument("-f", "--file", type=str, help="Filename to save the results as CSV. If not provided, output prints to console.")
    
    args = parser.parse_args()
    
    papers: List[Dict[str, str]] = get_papers(args.query, debug=args.debug)
    
    if args.debug:
        print(f"Total papers found with company affiliation: {len(papers)}")
    
    if not papers:
        print("No papers found matching the criteria.")
        sys.exit(0)
    
    headers = [
        "PubmedID",
        "Title",
        "Publication Date",
        "Non-academic Author(s)",
        "Company Affiliation(s)",
        "Corresponding Author Email"
    ]
    
    # Output CSV either to file or to the console
    if args.file:
        try:
            with open(args.file, mode="w", newline='', encoding="utf-8") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=headers)
                writer.writeheader()
                for paper in papers:
                    writer.writerow(paper)
            print(f"Results saved to {args.file}")
        except Exception as e:
            print(f"Error writing to file: {e}")
    else:
        writer = csv.DictWriter(sys.stdout, fieldnames=headers)
        writer.writeheader()
        for paper in papers:
            writer.writerow(paper)

if __name__ == "__main__":
    main()
