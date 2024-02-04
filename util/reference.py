import requests
from bs4 import BeautifulSoup as bs


def make_reference(title: str, writer: str, date: str, pub: str, url: str):
    try:
        if pub == '국회입법조사처 학술지(입법과 정책)':
            res = requests.get(url)
            soup = bs(res.text, 'html.parser')
            vol_raw = soup.select_one('.vol').get_text().split(',')
            reference = '{} ({}). {}. 입법과 정책. {}({}), {}.'.format(writer, vol_raw[0], title, vol_raw[1].strip()[4:],
                                                                  vol_raw[2].strip()[3:],
                                                                  vol_raw[3].strip()[3:].replace(' ', ''))
            return reference

        reference = '{} ({}). {}. {}.'.format(writer, date.split('-')[0], title, pub)
        return reference
    except:
        return ''
