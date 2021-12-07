import numpy as np
import pandas as pd

import requests as rq

from bs4 import BeautifulSoup
import re

url = 'https://pt.stardewvalleywiki.com/Esta%C3%A7%C3%B5es'
response = rq.get(url)
html_page = BeautifulSoup(response.text, 'html.parser')

print(html_page.find('table'))

