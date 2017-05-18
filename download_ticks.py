# dowload_exchange_rates.py
from lxml import html

#import urlparse
import urllib.parse
import datetime
import requests
import zipfile
import io
#import io.StringIO
#from io import StringIO
import sys
import os

# download_prices
def download_prices():

    year_str = '2014'
    space_str = '%20'

    #output_folder_base_path = '/Users/P/Documents/Prices/'
    output_folder_base_path = 'C:\\Julian\\Prices\\'

    if os.path.exists(output_folder_base_path) == False:
        os.makedirs(output_folder_base_path)

    base_url_str = 'http://ratedata.gaincapital.com'

    for month in range(1,13):
        
        # doesnt matter what year we just want the names of the months
        month_str = datetime.date(2008, month, 1).strftime('%B')
        month_num_str = str(month).zfill(2)

        page_str = month_num_str + space_str + month_str

        full_url_str_yr = urllib.parse.urljoin(base_url_str, year_str)
        full_url_str = urllib.parse.urljoin(full_url_str_yr + '/', page_str)

        page = requests.get(full_url_str)
        tree = html.fromstring(page.content)

        zip_arefs = tree.xpath('//a/@href')
        zip_files = [x.replace('.\\', '') for x in zip_arefs]

        for zip_file_str in zip_files:
            if ('USD_JPY' not in zip_file_str):
                continue

            zip_url = urllib.parse.urljoin(full_url_str + '/', zip_file_str)
            folder_name = zip_file_str[0:7]

            output_folder_path = os.path.join(output_folder_base_path, year_str, folder_name, month_str)

            if os.path.exists(output_folder_path) == False:
                os.makedirs(output_folder_path)
            
            print(zip_url + ' downloading..')

            f = requests.get(zip_url, stream=True)
            full_path_name = os.path.join(output_folder_path, zip_file_str)
            zip_file = zipfile.ZipFile(io.BytesIO(f.content))
            zip_file.printdir()
            zip_file.extractall(output_folder_path)


download_prices()