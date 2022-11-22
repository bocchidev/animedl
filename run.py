import requests, os, shutil, mimetypes, zippyshare_downloader as ZippyDL
from tqdm.auto import tqdm
from bs4 import BeautifulSoup as bs


def GetZippyURL(query: str) -> list:
    try:
        URLData = []
        data = requests.get(f"https://arzxh.herokuapp.com/api/otakudesu?query={query}")
        episode = data["episode"]
        for eps in episode:
            link = [
                dat for dat in eps["download"]["hd_720p"] if dat["name"] == "Zippy"
            ][0]
            link_data = requests.get(link["url"])
            link_html = bs(link_data.text, "html.parser")
            meta = link_html.find("meta", {"property": "og:url"}).get("content")
            Zippy = f"https:{meta}"
            URLData.append(Zippy)
        return URLData
    except:
        pass


def Download(url: str):
    try:
        data = ZippyDL.get_info(url)
        title = data["name_file"]
        href = data["download_url"]
        with requests.get(href, stream=True) as r:
            total_length = int(r.headers.get("Content-Length"))
            ext = os.path.splitext(title)[1]
            with tqdm.wrapattr(r.raw, "read", total=total_length, desc=title) as raw:
                with open(f"{title}", "wb") as output:
                    shutil.copyfileobj(raw, output)
        return
    except:
        pass


def Main():
    try:
        inp = input("Masukkan judul anime yang ingin diunduh: ")
        data = GetZippyURL(inp)
        if not data:
            print("Anime tidak ditemukan!")
        else:
            os.mkdir(inp)
            os.chdir(inp)
            os.system("clear")
            print("Sedang proses mengunduh, mohon tunggu ...\n")
            for url in data:
                Download(url)
        return
    except:
        pass


if __name__ == "__main__":
    Main()
