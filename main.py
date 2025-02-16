import os
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
    with open(f"{os.path.curdir}/{filename}", "a", encoding="utf-8") as f:
        f.write(data)
    

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

        line = f"{id},"

        for number in numbers:
            line += f"{number.text.strip()},"

        line = line[:-1]

        append_line_to_file("result.csv", line + "\n")

for i in range(1, 1316):
    crawl_vietlott(i)