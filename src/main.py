import sys
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
from urllib.parse import urljoin
import re


class WebsiteDataFetcher:
    def __init__(self, base_url):
        self.base_url = base_url

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    def fetch_html(self, timeout=10):
        """Fetches the HTML content of the given URL with a timeout to avoid blocking."""
        try:
            response = requests.get(
                self.base_url, headers=self.headers, timeout=timeout
            )
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Error accessing {self.base_url}: {str(e)}", file=sys.stderr)
            return None


class DataExtractor:
    def __init__(self, html, base_url):
        self.html = html
        self.base_url = base_url
        self.soup = BeautifulSoup(html, "html.parser") if html else None

    def extract_logo(self):
        """Extracts logo by checking various possible locations."""
        if not self.soup:
            return "No logo found"
        logo = (
            self.soup.find("img", {"alt": re.compile(r"logo", re.I)})
            or self.soup.find("img", {"class": re.compile(r"logo", re.I)})
            or self.soup.find("img", src=re.compile(r"logo", re.I))
            or self.soup.find("img", src=re.compile(r"brand", re.I))
        )
        return urljoin(self.base_url, logo["src"]) if logo else "No logo found"

    def extract_phone_numbers(self):
        if not self.soup:
            return []
        phones = {}  # Use a dictionary to map normalized numbers to formatted ones
        phone_pattern = re.compile(
            r"\(?\+?\d{1,3}\)?[\s-]?\d{1,4}[\s-]?\d{1,4}[\s-]?\d{1,4}"
        )

        # Extracting from 'tel:' links
        tel_links = self.soup.find_all("a", href=re.compile(r"^tel:"))
        for link in tel_links:
            tel_number = link["href"].replace("tel:", "").strip()
            norm_number = re.sub(
                r"[^\d]", "", tel_number
            )  # Normalize by removing non-numeric chars
            phones[norm_number] = tel_number  # Store using normalized number as key

        # Search within text nodes for additional numbers
        text_nodes = self.soup.find_all(string=True)
        for node in text_nodes:
            found_numbers = phone_pattern.findall(node)
            for number in found_numbers:
                cleaned_number = re.sub(r"[^\d\+\(\)]", "", number).strip()
                norm_number = re.sub(r"[^\d]", "", cleaned_number)  # Normalize
                if 7 <= len(norm_number) <= 15:  # Check normalized length
                    phones[norm_number] = cleaned_number  # Store original format

        return list(phones.values())  # Return the list of unique, formatted numbers


class WebsiteInfoProcessor:
    def __init__(self, urls):
        self.urls = urls

    def process_websites(self):
        results = []
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = {
                executor.submit(self.fetch_and_extract, url): url for url in self.urls
            }
            for future in as_completed(futures):
                result = future.result()
                if result:
                    results.append(result)
        return results

    def fetch_and_extract(self, url):
        fetcher = WebsiteDataFetcher(url)
        html = fetcher.fetch_html()
        extractor = DataExtractor(html, url)
        logo = extractor.extract_logo()
        phones = extractor.extract_phone_numbers()
        return {"url": url, "logo": logo, "phones": phones}


def main():
    urls = [line.strip() for line in sys.stdin if line.strip()]
    processor = WebsiteInfoProcessor(urls)
    results = processor.process_websites()
    for result in results:
        print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
