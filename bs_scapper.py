from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd



driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")

def get_soup(url):
	driver.get(url)
	content = driver.page_source
	soup = BeautifulSoup(content, "lxml")
	return soup

def pd_df(columns):
	df = pd.DataFrame(columns=columns)
	return df

def write_to_csv(df, file_name):
	df.to_csv(file_name)




def radhe():
	
	url = "https://shop.radheonline.com.au/"
	columns = ["category", "product_link", "image_link", "product_name", "price", "unit"]
	df = pd_df(columns)
	
	soup = get_soup(url)
	results = soup.findAll("a", class_="Menu__Item")
	links = []
	for l in results:
		links.append((l.get("href")))




	count = 0
	for link in links:
		soup = get_soup(f'{url[0:-1]}{link}')
		results = soup.findAll("div", class_="talker talker--row")

		for res in results:
			l = f'{url[0:-1]}{res.find("a").get("href")}'
			im = res.find("img").get("src")
			prod = res.find("div", class_="talker__name talker__section").get("title")
			price = res.find("strong",  class_="price__sell").text
			unit = res.find("span", class_="price__units weak").text

			df.loc[count] = [link.split("/")[2], l, im, prod, price, unit]
			count +=1

	
	write_to_csv(df, 'radhe.csv')



def ozkirana():
	url = "https://ozkirana.com.au/"
	columns = ["category", "product_link", "image_link", "product_name", "price", "vendor"]
	df = pd_df(columns)
	
	soup = get_soup(url)
	results = soup.find("nav", class_="site-navigation").findAll("a")
	count = 0
	for res in results:
		link = res.get("href")
		if "collections" in link:
			soup = get_soup(f'{url[0:-1]}{link}')
			category = link.split("/")[2]
			prods = soup.findAll("div", class_="productitem")
			for p in prods:
				l = f'{url[0:-1]}{p.find("a", class_="productitem--image-link").get("href")}'
				print(l)
				img = f'https:{p.find("img").get("src")}'
				price = p.find("span", class_="money").text
				name = p.find("h2", class_="productitem--title").find("a").text
				product_vendor = p.find("h3", class_="productitem--vendor").text


				df.loc[count] = [category,  l, img, name, price, product_vendor]
				count+=1

	write_to_csv(df, 'ozkirana.csv')

		

ozkirana()