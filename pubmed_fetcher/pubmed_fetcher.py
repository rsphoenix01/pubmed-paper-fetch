import requests
import xml.etree.ElementTree as ET
import re
from typing import List, Dict, Optional

def search_pubmed(query: str, debug: bool = False) -> List[str]:
    """
    Use PubMed ESearch API to return a list of PubMed IDs for the given query.
    """
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": "100"  # adjust max number of results as needed
    }
    if debug:
        print("Searching PubMed with query:", query)
    response = requests.get(base_url, params=params)
    if response.status_code != 200:
        raise Exception(f"Error fetching data from PubMed: {response.status_code}")
    data = response.json()
    id_list = data.get("esearchresult", {}).get("idlist", [])
    if debug:
        print("Found IDs:", id_list)
    return id_list

def fetch_details(pubmed_ids: List[str], debug: bool = False) -> List[ET.Element]:
    """
    Use PubMed EFetch API to fetch paper details in XML for a list of PubMed IDs.
    """
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {
        "db": "pubmed",
        "id": ",".join(pubmed_ids),
        "retmode": "xml"
    }
    if debug:
        print("Fetching details for IDs:", pubmed_ids)
    response = requests.get(base_url, params=params)
    if response.status_code != 200:
        raise Exception(f"Error fetching details from PubMed: {response.status_code}")
    root = ET.fromstring(response.content)
    return list(root.findall("PubmedArticle"))

def is_company_affiliation(affiliation: str) -> bool:
    """
    Returns True if the affiliation text appears to be from a pharmaceutical/biotech company.
    """
    keywords = ["pharma", "pharmaceutical", "biotech", "biotechnology"]
    return any(keyword in affiliation.lower() for keyword in keywords)

def is_academic_affiliation(affiliation: str) -> bool:
    """
    Returns True if the affiliation text indicates an academic institution.
    """
    academic_keywords = ["university", "college", "institute", "hospital", "academy", "school"]
    return any(keyword in affiliation.lower() for keyword in academic_keywords)

def extract_email(text: str) -> Optional[str]:
    """
    Extracts the first email address found in the given text.
    """
    matches = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    return matches[0] if matches else None

def parse_pubmed_article(article: ET.Element, debug: bool = False) -> Optional[Dict[str, str]]:
    """
    Parses one PubMedArticle XML element and returns a dictionary with required fields.
    Only returns a result if there is at least one company affiliation.
    """
    try:
        medline = article.find("MedlineCitation")
        if medline is None:
            return None
        pmid_elem = medline.find("PMID")
        pubmed_id = pmid_elem.text if pmid_elem is not None else "N/A"

        article_elem = medline.find("Article")
        if article_elem is None:
            return None

        title_elem = article_elem.find("ArticleTitle")
        title = title_elem.text if title_elem is not None else "N/A"

        # Extract publication date from Journal Issue (may vary in structure)
        journal = article_elem.find("Journal")
        pub_date = "N/A"
        if journal is not None:
            journal_issue = journal.find("JournalIssue")
            if journal_issue is not None:
                pub_date_elem = journal_issue.find("PubDate")
                if pub_date_elem is not None:
                    year_elem = pub_date_elem.find("Year")
                    medline_date_elem = pub_date_elem.find("MedlineDate")
                    if year_elem is not None:
                        pub_date = year_elem.text
                    elif medline_date_elem is not None:
                        pub_date = medline_date_elem.text

        # Process authors and affiliations
        author_list_elem = article_elem.find("AuthorList")
        non_academic_authors = []
        company_affiliations = set()
        corresponding_email = None
        if author_list_elem is not None:
            for author in author_list_elem.findall("Author"):
                # Skip if author names are missing (could be collective names)
                last_name_elem = author.find("LastName")
                fore_name_elem = author.find("ForeName")
                if last_name_elem is None or fore_name_elem is None:
                    continue
                full_name = f"{fore_name_elem.text} {last_name_elem.text}"
                # Examine each affiliation provided for the author
                aff_infos = author.findall("AffiliationInfo")
                for aff in aff_infos:
                    affiliation_elem = aff.find("Affiliation")
                    if affiliation_elem is not None and affiliation_elem.text:
                        affiliation_text = affiliation_elem.text.strip()
                        # If affiliation does not indicate an academic institution, add the author
                        if not is_academic_affiliation(affiliation_text):
                            non_academic_authors.append(full_name)
                        # If affiliation is a company affiliation, record it
                        if is_company_affiliation(affiliation_text):
                            company_affiliations.add(affiliation_text)
                        # Attempt to extract a corresponding email if not already found
                        if corresponding_email is None:
                            email = extract_email(affiliation_text)
                            if email:
                                corresponding_email = email
        # Only include this paper if there's at least one company affiliation.
        if not company_affiliations:
            return None

        return {
            "PubmedID": pubmed_id,
            "Title": title,
            "Publication Date": pub_date,
            "Non-academic Author(s)": "; ".join(non_academic_authors),
            "Company Affiliation(s)": "; ".join(company_affiliations),
            "Corresponding Author Email": corresponding_email if corresponding_email else ""
        }
    except Exception as e:
        if debug:
            print(f"Error parsing article: {e}")
        return None

def get_papers(query: str, debug: bool = False) -> List[Dict[str, str]]:
    """
    Given a PubMed query, fetches papers and returns a list of dictionaries with required fields.
    Only papers with at least one author affiliated with a pharmaceutical/biotech company are included.
    """
    try:
        id_list = search_pubmed(query, debug=debug)
        if not id_list:
            if debug:
                print("No articles found for query.")
            return []
        articles = fetch_details(id_list, debug=debug)
        papers = []
        for article in articles:
            parsed = parse_pubmed_article(article, debug=debug)
            if parsed:
                papers.append(parsed)
        return papers
    except Exception as e:
        if debug:
            print(f"Error in get_papers: {e}")
        return []
