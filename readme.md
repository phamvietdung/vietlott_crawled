

# Vietlott Crawler


This project is a web crawler for Vietlott lottery results. It fetches the lottery results from the Vietlott website and stores them in a CSV file.

## Project Structure

```
data/
    # Contains the HTML files fetched from the Vietlott website
main.py
readme.md
result.csv
suggested/
    # Additional suggested files or scripts
```

## Requirements

- Python 3.x
- `beautifulsoup4` library
- `cloudscraper` library

You can install the required libraries using pip:

```sh
pip install beautifulsoup4 cloudscraper
```

## Usage

To run the crawler, execute the main.py script:

```sh
python main.py
```

The script will fetch the lottery results for IDs ranging from 1 to 1315 and store the results in result.csv.

## Functions

- `get_page_url(id)`: Generates the URL for the given lottery ID.
- `crawl(url)`: Fetches the HTML content from the given URL.
- `get_path(filename)`: Returns the file path for the given filename in the data folder.
- `write_to_file(filename, data)`: Writes data to a file.
- `read_from_file(filename)`: Reads data from a file.
- `append_line_to_file(filename, data)`: Appends a line of data to a file.
- `crawl_vietlott(id)`: Crawls the Vietlott website for the given lottery ID and stores the results in result.csv.

## License

This project is licensed under the MIT License.

phamvietdung: @GitHubCopilot 
