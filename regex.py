import requests
import json
import re


url = "http://www.juzimi.com/article/%E6%83%85%E4%B9%A6"
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

    sentences = re.findall(r'\"xlistju\">(.+?)</a>', html)
    loveds = re.findall(r"(喜欢\(\d*?\))", html)
    comments = re.findall(r">(评论\(?\d*?\)?)</a>", html)

    with open("love_letter.txt", "a", encoding="utf-8") as ob:
        for i in range(len(sentences)):
            data["sentence"] = sentences[i]
            data["loved"] = loveds[i]
            data["comment"] = comments[i]

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