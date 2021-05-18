import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np


def read_csv(filename):
    data = pd.read_csv(filename)
    return np.array(data)


def is_contain(soup, domain):
    meta = soup.find("meta", attrs={'name': 'description'})
    title = str(soup.head.title)
    if domain in str(meta) or title == domain or domain in title:
        return True


def processing(soup):
    data = read_csv("domains.csv")

    for line in data:
        domain_only = ' '.join(line.astype(str))
        if is_contain(soup, domain_only):
            return domain_only
    return "(Out of domain list's)" + str(soup.head.title)


def make_response(company_name, description):
    all_info = str(description).replace('xa0', ' ')
    all_info = all_info.replace('\\n', '')
    all_info = all_info.replace('\\t', '')
    all_info = ' '.join(w for w in re.split(r"\W", str(all_info)) if w)
    result = "Company name: " + str(company_name) + "\n" + " | Description: " + all_info
    return result


def search_company(url):
    response = requests.get(url, verify=False)
    soup = BeautifulSoup(response.text, "html.parser")
    return make_response(processing(soup), [s for s in soup.strings])
