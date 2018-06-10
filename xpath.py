import requests
from lxml import etree
import json


startUrl = "http://www.juzimi.com/"
url = "http://www.juzimi.com/search/node/%E5%82%B2%E6%85%A2%E4%B8%8E%E5%81%8F%E8%A7%81%20type%3Asentence"
headers = {
    # "Accept-Language": "zh-CN,zh;q=0.9",
    # "Cache-Control": "max-age=0",
    # "Connection": "keep-alive",
    # "Host": "www.juzimi.com",
    # "Upgrade-Insecure-Requests": "1",
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
    selector = etree.HTML(html)
    print(selector)
    ruler = '//div[@class="view-content"]/div[contains(@class, "views-row")]'
    roots = selector.xpath(ruler)

    with open("s.txt", "a", encoding="utf-8") as ob:
        for root in roots:
            try:
                data["sentence"] = root.xpath('./div/div[1]/a/text()')[0]
                data["loved"] = root.xpath('./div/div[3]/a/text()')[0]
                data["comment"] = root.xpath('./div/div[5]/a/text()')[0]
            except IndexError:
                continue

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
