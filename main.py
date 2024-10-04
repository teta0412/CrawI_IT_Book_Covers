##pip install lxml
##pip install requests
##pip install beautifulsoup4
##pip install langdetect
##pip install pandas
##pip install XlsxWriter

import requests
from bs4 import BeautifulSoup
from langdetect import detect
import csv
import os
import pandas as pd
import xlsxwriter


def crawl_giaotrinhpdf_site():
    data = []
    for page in range (1,2):
        site_url = 'https://giaotrinhpdf.com/tags/cong-nghe-thong-tin/trang-'+ str(page) +'.html#google_vignette'
        res = requests.get(site_url)
        soup = BeautifulSoup(res.text,'lxml')
        html = soup.find('div',class_='tab-content')
        img_urls = html.find_all('img')
        for url in img_urls:
            tmp = 'https://giaotrinhpdf.com/'
            img_url = {'url': tmp + url['data-src']}
            data.append(img_url)
    print(data)
def crawl_nhasachlt_site():
    data = []
    for page in range(1,19):
        site_url = 'https://nhasachlaptrinh.com/sach-cong-nghe-thong-tin-pc218844.html?page='+str(page)
        res = requests.get(site_url)
        soup = BeautifulSoup(res.text, 'lxml')
        html = soup.find('ul', class_='product-list')
        img_urls = html.find_all('img', class_='lazyload')
        for url in img_urls:
            if detect(url['alt']) == 'vi' and 'Combo' not in url['alt']:
                img_url = {'image_url': url['data-src']}
                data.append(img_url)
    with open('IT_Book_datasets.csv', 'w', newline='') as csvfile:
        fieldnames = ['image_url']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


def download_image(url, folder):
    try:
        response = requests.get(url, timeout=100)
        if response.status_code == 200:
            filename = os.path.join(folder, url.split('/')[-1])
            with open(filename, 'wb') as f:
                f.write(response.content)
            return True
    except Exception as e:
        print(f"Error downloading {url}: {str(e)}")
    return False


# crawl_site()
# df = pd.read_csv('IT_Book_datasets.csv')
#
# # Create a folder to store the images
# output_folder = '/Users/anhducnguyen/PycharmProjects/CrawI_IT_Books/images'
# os.makedirs(output_folder, exist_ok=True)
#
# for url in df['image_url']:
#     download_image(url, output_folder)
#
# print("Download completed!")

crawl_giaotrinhpdf_site()


