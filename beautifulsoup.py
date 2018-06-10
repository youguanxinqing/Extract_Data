import requests
from bs4 import BeautifulSoup
import json


url = "http://www.juzimi.com/article/%E7%88%B1%E4%B8%BD%E4%B8%9D%E6%A2%A6%E6%B8%B8%E4%BB%99%E5%A2%83"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36",
    "Referer": "http://www.juzimi.com/search/node/%E5%82%B2%E6%85%A2%E4%B8%8E%E5%81%8F%E8%A7%81%20type%3Asentence",
}


def get_html(params):
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        print(response.url)
        print(response.status_code)
    except Exception as e:
        print(e)
        print("connection error")
        return None

    response.encoding = response.apparent_encoding
    return response.text

def parse_html(html):
    data = {}
    soup  = BeautifulSoup(html, "lxml")
    sentences = soup.find_all("a", {"class":"xlistju"}) #sentences
    loveds = soup.find_all("a", {"class":"flag-action"}) #loved
    comments = soup.find_all("a", {"class":"comment-link"}) #comment

    with open("Alice.txt", "a", encoding="utf-8") as ob:
        for i in range(len(sentences)):
            data["sentence"] = sentences.pop().get_text()
            data["loved"] = loveds.pop().get_text()
            data["comment"] = comments.pop().get_text()

            ob.write(json.dumps(data, ensure_ascii=False))
            ob.write("\n")

def main():
    for i in range(4):
        if i:
            params = {"page":i}
        else:
            params ={}
        html = get_html(params)
        if html:
            parse_html(html)
    print("结束")

if __name__ == "__main__":
    main()