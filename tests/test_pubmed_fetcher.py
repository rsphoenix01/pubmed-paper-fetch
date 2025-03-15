import pytest
import xml.etree.ElementTree as ET
from pubmed_fetcher.pubmed_fetcher import (
    is_company_affiliation,
    is_academic_affiliation,
    extract_email,
    parse_pubmed_article,
)

def test_is_company_affiliation():
    assert is_company_affiliation("Acme Pharma Inc.") is True
    assert is_company_affiliation("Generic Biotech Ltd.") is True
    assert is_company_affiliation("University of Testing") is False

def test_is_academic_affiliation():
    assert is_academic_affiliation("Harvard University") is True
    assert is_academic_affiliation("MIT") is True
    assert is_academic_affiliation("Acme Pharma Inc.") is False

def test_extract_email():
    text = "For inquiries, contact test.user@example.com."
    assert extract_email(text) == "test.user@example.com"
    assert extract_email("No email here") is None

def test_parse_pubmed_article_no_affiliation():
    # Sample XML with only an academic affiliation (should be filtered out)
    xml_data = """
    <PubmedArticle>
      <MedlineCitation>
        <PMID>12345</PMID>
        <Article>
          <ArticleTitle>Test Article</ArticleTitle>
          <Journal>
            <JournalIssue>
              <PubDate>
                <Year>2020</Year>
              </PubDate>
            </JournalIssue>
          </Journal>
          <AuthorList>
            <Author>
              <LastName>Smith</LastName>
              <ForeName>John</ForeName>
              <AffiliationInfo>
                <Affiliation>Department of Biology, Harvard University</Affiliation>
              </AffiliationInfo>
            </Author>
          </AuthorList>
        </Article>
      </MedlineCitation>
    </PubmedArticle>
    """
    root = ET.fromstring(xml_data)
    result = parse_pubmed_article(root)
    # No company affiliation so the function should return None
    assert result is None

def test_parse_pubmed_article_with_company():
    # Sample XML with a company affiliation (should be accepted)
    xml_data = """
    <PubmedArticle>
      <MedlineCitation>
        <PMID>67890</PMID>
        <Article>
          <ArticleTitle>Research Involving Industry</ArticleTitle>
          <Journal>
            <JournalIssue>
              <PubDate>
                <Year>2021</Year>
              </PubDate>
            </JournalIssue>
          </Journal>
          <AuthorList>
            <Author>
              <LastName>Doe</LastName>
              <ForeName>Jane</ForeName>
              <AffiliationInfo>
                <Affiliation>Acme Pharma Inc.</Affiliation>
              </AffiliationInfo>
            </Author>
          </AuthorList>
        </Article>
      </MedlineCitation>
    </PubmedArticle>
    """
    root = ET.fromstring(xml_data)
    result = parse_pubmed_article(root)
    assert result is not None
    assert result["PubmedID"] == "67890"
    assert "Acme Pharma Inc." in result["Company Affiliation(s)"]
