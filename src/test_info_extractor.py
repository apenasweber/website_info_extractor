import unittest
from unittest.mock import patch
from requests.exceptions import HTTPError
from main import WebsiteInfoProcessor, WebsiteDataFetcher, DataExtractor


class TestWebsiteInfoExtractor(unittest.TestCase):
    def test_fetch_website_data_success(self):
        with patch("requests.get") as mocked_get:
            mocked_get.return_value.status_code = 200
            mocked_get.return_value.text = "Success"
            processor = WebsiteInfoProcessor(["http://example.com"])
            result = processor.process_websites()[0]
            self.assertEqual(result["url"], "http://example.com")
            self.assertEqual(result["logo"], "No logo found")
            self.assertEqual(result["phones"], [])

    def test_fetch_website_data_failure(self):
        with patch("requests.get") as mocked_get:
            mocked_response = mocked_get.return_value
            mocked_response.raise_for_status.side_effect = HTTPError(
                "Failed to connect"
            )
            fetcher = WebsiteDataFetcher("http://example.com")
            response = fetcher.fetch_html()
            self.assertIsNone(response)

    def test_extract_logo_and_phone_found(self):
        html = """
        <html>
            <head><title>Test</title></head>
            <body>
                <img src="http://example.com/logo.png" alt="company logo">
                <p>Call us at +1234567890</p>
            </body>
        </html>
        """
        base_url = "http://example.com"
        extractor = DataExtractor(html, base_url)
        logo = extractor.extract_logo()
        phones = extractor.extract_phone_numbers()
        result = {"logo": logo, "phones": phones}
        self.assertEqual(result["logo"], "http://example.com/logo.png")
        self.assertIn("+1234567890", result["phones"])

    def test_extract_logo_and_phone_none_found(self):
        html = """
        <html>
            <head><title>Test</title></head>
            <body><p>No contact info here.</p></body>
        </html>
        """
        base_url = "http://example.com"
        extractor = DataExtractor(html, base_url)
        logo = extractor.extract_logo()
        phones = extractor.extract_phone_numbers()
        result = {"logo": logo, "phones": phones}
        self.assertEqual(result["logo"], "No logo found")
        self.assertEqual(len(result["phones"]), 0)


if __name__ == "__main__":
    unittest.main()
