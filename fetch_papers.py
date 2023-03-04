import requests
from bs4 import BeautifulSoup # w/ lxml
from urllib.parse import urljoin
# probably less resilient than dampt as pdfs in weird places

def fetch_papers_from_link(url:str, year:str, part:str): # url, year, IA/IB/II no part III
    resp = requests.get(url)
    html = resp.content.decode()
    parsed_html = BeautifulSoup(html, features="lxml")
    parsed_main = parsed_html.find_all("tbody")[0]
    # print(parsed_main)
    papers = []
    # assuming well-ordered sheets pls be true
    for i, entry in enumerate(parsed_main.find_all("tr")):
        # try:
            if str(entry.td.a["href"]).startswith("http") or str(entry.td.a["href"]).startswith("https") or str(entry.td.a["href"]).startswith("www"):
                papers.append([str(entry.td.a["href"]),year,part,entry.th.get_text().strip("Paper ")]) # [link,year,part,number/type]
            # else:
            #     sheets.append([urljoin(url,str(entry.a["href"])), coursename.strip(), i + 1])
        # except:
        #     pass
    return papers


def fetch_papers():
    url = "https://www.maths.cam.ac.uk/undergrad/pastpapers/past-ia-ib-and-ii-examination-papers"
    resp = requests.get(url)
    html = resp.content.decode()
    # print(dpmms_html)
    parsed_html = BeautifulSoup(html, features="lxml")
    papers = []
    # first line is list of titles
    parsed_table = parsed_html.find_all("table",{"class":"facultyleftlists"})[0].find_all("tr")[1::]
    # print(parsed_table)
    for yearrow in parsed_table:
        for entry in yearrow.find_all("td"):
            papers+=fetch_papers_from_link(entry.a["href"],yearrow.th.get_text(), entry.a.contents[0].strip("Part "))
    return papers


if __name__=="__main__":
    print(fetch_papers())