from datetime import timedelta, datetime

from db import SessionLocal

import json

import requests
from urllib import parse

from bs4 import BeautifulSoup  # parser


default_headers = {
    'Accept': '*/*',
    'Accept-Language': 'ko,ko-KR;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://underwood1.yonsei.ac.kr',
    'Referer': 'https://underwood1.yonsei.ac.kr/com/lgin/SsoCtr/initExtPageWork.do?link=shuttle',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"'
}


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


if __name__ == "__main__":
    pass
