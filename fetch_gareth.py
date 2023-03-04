import requests
from bs4 import BeautifulSoup # w/ lxml
from urllib.parse import urljoin


def fetch_gareth_papers():
    url = "https://tartarus.org/gareth/maths/tripos/"
    resp = requests.get(url)
    html = resp.content.decode()
    # print(dpmms_html)
    parsed_html = BeautifulSoup(html, features="lxml")
    papers = []
    # first line is list of titles
    parsed_table = parsed_html.find_all("table")[0].find_all("tr")
    # print(parsed_table)
    part = ""
    for yearrow in parsed_table:
        if len(yearrow.find_all("td")) == 3:
            box = yearrow.find_all("td")[0]
            if str(box.a["href"]).startswith("http") or str(box.a["href"]).startswith("https") or str(box.a["href"]).startswith("www"):
                papers.append([str(box.a["href"]), box.get_text().lower()+" all"])
            else:
                papers.append([urljoin(url,str(box.a["href"])), box.get_text()+" collated",part])
        else:
            part=yearrow.find_all("td")[0].get_text().strip("Part ")
    return papers


if __name__=="__main__":
    print(fetch_gareth_papers())