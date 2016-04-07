from bs4 import BeautifulSoup
import requests, urlparse, re, sys

def main():
	to_crawl = []
	
	try:
		headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' }
		r = requests.get("http://www.lyricsfreak.com/b/bob+marley/", headers=headers)
	except requests.exceptions.RequestException as e:
		print e

	soup = BeautifulSoup(r.text, "html.parser")

	for a_tag in soup.find_all("a"):
		try:
			link = a_tag.get("href")
			link = link.strip()
			link = urlparse.urljoin("http://www.lyricsfreak.com/b/bob+marley/", link)
			if link.startswith("http://www.lyricsfreak.com/b/bob+marley/"):
				to_crawl.append(link)
		except:
			continue
	'''

	filename = sys.argv[1]
	infile = open(filename)
	seed_list = [line.rstrip('\n') for line in open(filename)]
	for seed in seed_list:
		to_crawl.append(seed)
	'''
	for link in to_crawl:
		try:
			try:
				headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' }
				r = requests.get(link, headers=headers)
			except requests.exceptions.RequestException as e:
				print link, e


			soup = BeautifulSoup(r.text, "html.parser")

			title = soup.title.string.split("Lyrics")[0].strip()
			title = re.sub(" ", "_", title)
			title = re.sub("/", "_", title)
			print title
			div = soup.find("div", attrs={"class": "dn"})
			f = open("BobMarleyLyrics/" + title, "w")
			f.write(title + "\n")
			f.write("\n")
			f.write(div.text)
			f.close()
		except:
			continue


main()