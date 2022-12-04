##############################################################################
# 
#  Creator: Sandy Pratama (Suaminya Gotou Hitori><)
#  Facebook: https://facebook.com/arzhavz
#  Donation: https://trakteer.id/arzhavz
#  Catatan: Project ini akan terus dikembangkan, soalnya aku juga pake ini hehe.
#           Kedepannya akan ditambahkan banyak fitur lagi tentunya.
#
###############################################################################

import requests, os, shutil, click, zippyshare_downloader as ZippyDL
from tqdm.auto import tqdm
from bs4 import BeautifulSoup as bs
from lib.otakudesu import Otakudesu


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
	except Exception as e:
		raise e

			
@click.command()
@click.option("--tipe", type=str, default="anime", help="Tipe unduhan, saat ini hanya tersedia untuk anime. Example: --tipe=anime")
@click.option("--latest", type=bool, default=False, help="Untuk mengunduh hanya episode terakhir yang rilis. Example: --latest=True")
def Main(tipe, latest):
	if tipe.strip().lower() == "anime":
		title = input("Masukkan judul anime yang ingin kamu unduh: ")
		data = Otakudesu(title)
		if not data:
			print("Anime tidak ditemukan!")
		else:
			try:
				os.mkdir(data.title)
			except:
				pass
			os.chdir(data.title)
			os.system("clear")
			print("Sedang proses mengunduh, mohon tunggu ...\n")
			if not latest:
				for url in data.get_zippy:
					Download(url)
			else:
				Download(data.get_zippy[0])
			print("\nUnduhan selesai!\nJika kamu suka dengan tools ini \nmohon donasi seikhlasnya di https://trakteer.id/arzhavz")
	else:
		print(f"Invalid tipe!\nKetik python run.py --help untuk bantuan!")
	return


if __name__ == "__main__":
	Main()
