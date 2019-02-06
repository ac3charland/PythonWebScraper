from bs4 import BeautifulSoup
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
import time
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A'}

def is_good_response(resp):
    """
    Returns true if the response seems to be HTML, false otherwise
    """
    content_type = resp.headers['Content-Type'].lower()
    if resp.status_code != 200:
        print('Error code: {}'.format(resp.status_code))
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)

def log_error(e):
    """
       It is always a good idea to log errors.
       This function just prints them, but you can
       make it do anything.
       """
    print(e)

def simple_get(url):

    try:
        with closing(get(url, headers=headers, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else: 
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
    return None


def get_clinic_count(page_url, html_tag, tag_identifier):
    response = simple_get(page_url)

    if response is not None:
        html = BeautifulSoup(response, 'html.parser')
        clinic_elements = 0
        clinics = html.find_all(html_tag, tag_identifier)

        for clinic in clinics:
            clinic_elements += 1

        if clinic_elements == 0:
            print('No clinics found. Printing html: ')
            time.sleep(2)
            print(response)

        return clinic_elements


count = get_clinic_count('https://www.citymd.com/all-locations', 'a', {'class': 'link-btn'})
print(count)