# Vietlott Crawler

This project is a web crawler for Vietlott lottery results. It fetches the lottery results from the Vietlott website and stores them in a CSV file.

## Project Structure

```
data/
    # Contains the HTML files fetched from the Vietlott website
main.py
readme.md
result.csv
run_single.sh
env_vars.sh
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

To run the crawler, execute the `main.py` script with the desired parameters:

For a range of IDs:
```sh
python main.py range --start_id 1 --end_id 1315
```

For a single ID:
```sh
python main.py single --id 1
```

## Running with Cron Job

To run the crawler automatically every Wednesday, Friday, and Sunday at 7 PM, you can set up a cron job.

1. Create a shell script `run_single.sh` to run the `main.py` script with the `single` command.
2. Make the shell script executable:
    ```sh
    chmod +x /f:/WorkSpace/vietlott/run_single.sh
    ```
3. Edit the crontab file to add the cron job:
    ```sh
    crontab -e
    ```
4. Add the following line to the crontab file to schedule the job for every Wednesday, Friday, and Sunday at 7 PM:
    ```sh
    0 19 * * 3,5,7 /f:/WorkSpace/vietlott/run_single.sh
    ```

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
