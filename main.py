import os
import argparse
from bs4 import BeautifulSoup
data_folder = "data"

def get_page_url(id):
    idStr : str = "{:05d}".format(id)
    return f"https://vietlott.vn/vi/trung-thuong/ket-qua-trung-thuong/645?id={idStr}&nocatche=1"

def crawl(url):
    from bs4 import BeautifulSoup
    import cloudscraper

    scraper = cloudscraper.create_scraper()
    response = scraper.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        return soup
    else:
        print(f"Failed to bypass Cloudflare, status code: {response.status_code}")
        return None
    
def get_path(filename):
    if not os.path.exists(f"{os.path.curdir}/{data_folder}"):
        os.makedirs(f"{os.path.curdir}/{data_folder}")
    return f"{os.path.curdir}/{data_folder}/{filename}"

def write_to_file(filename, data):
    with open(get_path(filename), "w", encoding="utf-8") as f:
        f.write(data)

def read_from_file(filename):
    with open(get_path(filename), "r", encoding="utf-8") as f:
        return f.read()
    
def append_line_to_file(filename, data):

    isExist : bool = False

    # check if data line is existed in file
    if(os.path.exists(f"{os.path.curdir}/{filename}")):
        with open(f"{os.path.curdir}/{filename}", "r", encoding="utf-8") as f:
            if data in f.read():
                isExist = True

    # print(f"Data is existed: {isExist}")

    if isExist == False:
        with open(f"{os.path.curdir}/{filename}", "a", encoding="utf-8") as f:
            f.write(data)

def remove_file(filename):
    if(os.path.exists(get_path(filename))):
        os.remove(get_path(filename))

def crawl_vietlott(id : int):

    # id : int = 2

    html_file = f"{id}.html"

    soup = None

    if(os.path.exists(get_path(html_file))):
        soup = BeautifulSoup(read_from_file(f"{id}.html"), "html.parser")
    else:
        soup = crawl(get_page_url(id))
        write_to_file(html_file, soup.prettify())

    if(soup == None):
        raise Exception("Failed to crawl")
    else:
        numbers = soup.find_all("span", class_="bong_tron")

        if(len(numbers) == 0):
            if(os.path.exists(get_path(html_file))):
                remove_file(html_file)
            raise Exception("No data found")
            #return

        line = f"{id},"

        for number in numbers:
            line += f"{number.text.strip()},"

        line = line[:-1]

        append_line_to_file("result.csv", line + "\n")

def main_range(start_id, end_id):
    for i in range(start_id, end_id + 1):
        crawl_vietlott(i)

def main_single(id):
    crawl_vietlott(id)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Crawl Vietlott data")
    subparsers = parser.add_subparsers(dest="command")

    range_parser = subparsers.add_parser("range", help="Crawl a range of IDs")
    range_parser.add_argument("--start_id", type=int, required=True, help="Starting ID for crawling")
    range_parser.add_argument("--end_id", type=int, required=True, help="Ending ID for crawling")

    single_parser = subparsers.add_parser("single", help="Crawl a single ID")
    single_parser.add_argument("--id", type=int, required=True, help="ID for crawling")


    all_parser = subparsers.add_parser("all", help="Crawl all IDs, until no more data")

    args = parser.parse_args()

    if args.command == "range":
        main_range(args.start_id, args.end_id)
    elif args.command == "single":
        main_single(args.id)
    elif args.command == "all":
        id = 1
        while True:
            try:
                crawl_vietlott(id)
                id += 1
            except Exception as e:
                print("No more data to crawl")
                break
    else:
        parser.print_help()