import requests
from bs4 import BeautifulSoup
import csv
import logging
import os
from tqdm import tqdm  # For progress bar
import argparse

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# User-Agent header to mimic browser
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}

def fetch_books(base_url, page_number):
    """
    Fetch books from the given page number.
    Returns a list of dictionaries containing book details.
    """
    url = base_url.format(page_number)
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        logging.warning(f"Failed to fetch page {page_number}. HTTP Status Code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    books = []

    for article in soup.find_all('article', class_='product_pod'):
        title = article.h3.a['title']
        price = article.find('p', class_='price_color').text.strip()
        stock_status = article.find('p', class_='instock availability').text.strip()
        rating = article.p['class'][1]  # Extract rating from class

        books.append({
            "Title": title,
            "Price": price,
            "Stock Status": stock_status,
            "Rating": rating
        })

    return books

def save_to_csv(data, filename):
    """
    Save a list of dictionaries to a CSV file.
    """
    os.makedirs("scraper_output", exist_ok=True)
    filepath = os.path.join("scraper_output", filename)
    with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ["Title", "Price", "Stock Status", "Rating"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    logging.info(f"Data saved to {filepath}")

def get_total_pages(base_url):
    """
    Get the total number of pages to scrape.
    """
    response = requests.get(base_url.format(1), headers=HEADERS)
    if response.status_code != 200:
        logging.error("Failed to fetch the first page to determine total pages.")
        return 0

    soup = BeautifulSoup(response.content, 'html.parser')
    try:
        total_pages = int(soup.find('li', class_='current').text.strip().split()[-1])
        return total_pages
    except AttributeError:
        logging.warning("Could not determine total pages. Defaulting to 1 page.")
        return 1

def main():
    """
    Main function to scrape book details and save to a CSV file.
    """
    parser = argparse.ArgumentParser(description="Web scraper for books.")
    parser.add_argument("--base_url", type=str, default="http://books.toscrape.com/catalogue/page-{}.html",
                        help="Base URL of the website to scrape.")
    parser.add_argument("--output", type=str, default="books_data.csv",
                        help="Name of the output CSV file.")
    args = parser.parse_args()

    base_url = args.base_url
    output_file = args.output

    # Determine total pages
    logging.info("Determining total pages...")
    total_pages = get_total_pages(base_url)

    all_books = []

    # Scrape all pages
    logging.info(f"Scraping {total_pages} pages...")
    for page_number in tqdm(range(1, total_pages + 1), desc="Scraping"):
        books = fetch_books(base_url, page_number)
        if not books:
            break
        all_books.extend(books)

    if all_books:
        save_to_csv(all_books, output_file)
    else:
        logging.error("No data scraped. Exiting.")

if __name__ == "__main__":
    main()
