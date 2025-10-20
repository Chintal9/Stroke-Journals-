import requests
import json
import xml.etree.ElementTree as ET
from datetime import datetime

def get_config():
    with open("config.json") as f:
        return json.load(f)

def fetch_pubmed_ids(query, max_results):
    esearch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": max_results,
        "sort": "pub+date",
        "retmode": "json"
    }
    r = requests.get(esearch_url, params=params)
    r.raise_for_status()
    data = r.json()
    return data["esearchresult"].get("idlist", [])

def fetch_pubmed_details(ids):
    efetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {
        "db": "pubmed",
        "id": ",".join(ids),
        "retmode": "xml"
    }
    r = requests.get(efetch_url, params=params)
    r.raise_for_status()
    return r.text

def parse_pubmed_articles(xml_data):
    root = ET.fromstring(xml_data)
    articles = []
    for article in root.findall(".//PubmedArticle"):
        medline = article.find("MedlineCitation")
        pmid = medline.find("PMID").text
        article_info = medline.find("Article")
        title = article_info.find("ArticleTitle").text if article_info.find("ArticleTitle") is not None else "No Title"
        abstract = article_info.find("Abstract/AbstractText")
        abstract_text = abstract.text if abstract is not None else ""
        authors = []
        for author in article_info.findall("AuthorList/Author"):
            lastname = author.find("LastName")
            firstname = author.find("ForeName")
            if lastname is not None and firstname is not None:
                authors.append(f"{firstname.text} {lastname.text}")
        authors_str = ", ".join(authors)
        journal = article_info.find("Journal/Title")
        journal_str = journal.text if journal is not None else ""
        pub_date = article_info.find("Journal/JournalIssue/PubDate/Year")
        pub_year = pub_date.text if pub_date is not None else ""
        url = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
        # TLDR: first 40 words of abstract or "No TLDR available"
        tldr = " ".join(abstract_text.split()[:40]) + ("..." if len(abstract_text.split()) > 40 else "") if abstract_text else "No TLDR available."
        articles.append({
            "title": title,
            "link": url,
            "pubDate": pub_year,
            "journal": journal_str,
            "authors": authors_str,
            "abstract": abstract_text,
            "tldr": tldr
        })
    return articles

def build_rss(feed_config, articles):
    rss = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss, "channel")
    ET.SubElement(channel, "title").text = feed_config["title"]
    ET.SubElement(channel, "link").text = feed_config["link"]
    ET.SubElement(channel, "description").text = feed_config["description"]
    ET.SubElement(channel, "lastBuildDate").text = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
    for art in articles:
        item = ET.SubElement(channel, "item")
        ET.SubElement(item, "title").text = art["title"]
        ET.SubElement(item, "link").text = art["link"]
        ET.SubElement(item, "description").text = f"""
        <b>Journal:</b> {art['journal']}<br>
        <b>Authors:</b> {art['authors']}<br>
        <b>TLDR:</b> {art['tldr']}<br>
        <b>Abstract:</b> {art['abstract']}
        """
        ET.SubElement(item, "pubDate").text = art["pubDate"]
    tree = ET.ElementTree(rss)
    tree.write("docs/feed.xml", encoding="utf-8", xml_declaration=True)

def main():
    config = get_config()
    ids = fetch_pubmed_ids(config["query"], config["max_results"])
    if not ids:
        print("No articles found for query.")
        return
    xml_data = fetch_pubmed_details(ids)
    articles = parse_pubmed_articles(xml_data)
    build_rss(config, articles)

if __name__ == "__main__":
    main()