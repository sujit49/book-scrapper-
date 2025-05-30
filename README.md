
# Book Scraper

This project is a Python web scraper that extracts book details from the website [Books to Scrape](http://books.toscrape.com). It collects information such as book title, price, stock status, and rating across multiple pages and saves the data into a CSV file.

## Features

- **Web Scraping:**
  - Scrapes multiple pages of the website dynamically.
  - Extracts key book details:
    - Title
    - Price
    - Stock Availability
    - Rating
- **Robustness:**
  - Handles HTTP request failures gracefully with logging warnings and errors.
  - Uses a User-Agent header to mimic browser requests.
- **Progress Monitoring:**
  - Displays a progress bar using `tqdm` to track scraping status.
- **Data Persistence:**
  - Saves the scraped data into a CSV file inside a dedicated folder (`scraper_output`).
- **Configurable:**
  - Accepts command-line arguments for the base URL and output file name.

## Prerequisites

- Python 3.x
- Required Python packages:
  - `requests`
  - `beautifulsoup4`
  - `tqdm`

## Installation

1. Clone this repository or download the script file.

2. Install the required libraries by running:
    ```bash
    pip install requests beautifulsoup4 tqdm
    ```

## Usage

Run the scraper script with optional command-line arguments:

```bash
python scraper.py --base_url "http://books.toscrape.com/catalogue/page-{}.html" --output "books_data.csv"
```

- `--base_url`: The base URL with a placeholder `{}` for the page number. Defaults to `http://books.toscrape.com/catalogue/page-{}.html`.
- `--output`: The output CSV file name. Defaults to `books_data.csv`.

Example without arguments (uses defaults):

```bash
python scraper.py
```

### Output

- Scraped book data will be saved in the `scraper_output` directory inside the specified CSV file.
- The console will display logs and a progress bar during scraping.

## File Structure

- `scraper.py`: Main Python script that performs web scraping and saves the data.
- `scraper_output/`: Directory where the output CSV file is saved.

## How It Works

1. The script first determines the total number of pages available by inspecting the pagination element on the first page.
2. It iterates through each page, scraping book information using BeautifulSoup.
3. Each book's title, price, stock status, and rating are extracted.
4. All the data is accumulated in a list.
5. After scraping, the data is saved to a CSV file in the `scraper_output` folder.
6. Logging messages provide real-time status updates and error handling.

## Potential Enhancements

- Add retries with exponential backoff for failed HTTP requests.
- Support scraping additional book details like product description or category.
- Implement multi-threading or asynchronous scraping for faster execution.
- Build a simple GUI or web interface to configure and run the scraper easily.
- Export data in other formats such as JSON or Excel.

---

Feel free to customize or extend this scraper for your own use cases!

---

*Created with Python, Requests, BeautifulSoup, and tqdm.*
