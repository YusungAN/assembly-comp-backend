import time
from datetime import datetime

import openai
from fastapi import APIRouter, FastAPI, HTTPException
from matplotlib import pyplot as plt
import seaborn as sns

import requests
import json
from pydantic import BaseModel
import pandas as pd
from fastapi import FastAPI, Response, status
from fastapi.responses import FileResponse
import os

router = APIRouter(
    responses={404: {"description": "Not found"}},
)
df = None


@router.get("/stat/list")
async def stats_list():
    # data = {"Sttsapitbl":[{"head":[{"list_total_count":539},{"RESULT":{"CODE":"INFO-000","MESSAGE":"정상 처리되었습니다."}}]},{"row":[{"CATE_FULLNM":"재정통계","STATBL_ID":"T186213000251988","STATBL_NM":"특별회계현황","DTACYCLE_NM":"년","TOP_ORG_NM":"국회예산정책처","ORG_NM":None,"USR_NM":"관리자","LOAD_DATE":"2023-08-09","OPEN_DATE":"2021-07-01","DATA_START_YY":"2017","DATA_END_YY":"2023","STATBL_CMMT":"자료: 국회예산정책처, ｢2023 대한민국 재정｣, 2023.3.","SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T186213000251988.do"},{"CATE_FULLNM":"지방재정","STATBL_ID":"T192943006111034","STATBL_NM":"통합재정기준 연도별 재정사용액","DTACYCLE_NM":"년","TOP_ORG_NM":"국회예산정책처","ORG_NM":None,"USR_NM":"관리자","LOAD_DATE":"2023-07-30","OPEN_DATE":"2019-06-28","DATA_START_YY":"2013","DATA_END_YY":"2023","STATBL_CMMT":"자료: 행정안전부, 「지방자치단체 통합재정개요」\r\n주: 2013년부터 통합재정기준으로 통계작성\r\n","SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T192943006111034.do"},{"CATE_FULLNM":"지방재정","STATBL_ID":"T188183000824584","STATBL_NM":"지방자치단체 평균 통합재정자립도","DTACYCLE_NM":"년","TOP_ORG_NM":"행정안전부","ORG_NM":None,"USR_NM":"국회예산정책처","LOAD_DATE":"2024-01-27","OPEN_DATE":"2020-07-23","DATA_START_YY":"1997","DATA_END_YY":"2023","STATBL_CMMT":"주: 1. 전국평균은 순계, 자치단체별 평균은 총계 기준\r\n    2. 통합재정자립도 = (경상수입 + 자본수입 + 융자회수) / 통합재정수입 × 100 \r\n자료: 행정안전부, 「2023년도 지방자치단체 통합재정 개요」, 2023. 5.","SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T188183000824584.do"},{"CATE_FULLNM":"지방재정","STATBL_ID":"T187533005825286","STATBL_NM":"지방자치단체 평균 통합재정자주도","DTACYCLE_NM":"년","TOP_ORG_NM":"행정안전부","ORG_NM":None,"USR_NM":"국회예산정책처","LOAD_DATE":"2024-01-27","OPEN_DATE":"2020-07-23","DATA_START_YY":"2007","DATA_END_YY":"2023","STATBL_CMMT":"    주: 1. 전국평균은 순계, 자치단체별 평균은 총계 기준\r\n        2. 통합재정자주도 = (경상수입 + 자본수입 + 융자회수 + 이전수입(보조금 제외)) / 통합재정수입 × 100 \r\n자료: 행정안전부, 「2023년도 지방자치단체 통합재정 개요」, 2023. 5.","SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T187533005825286.do"},{"CATE_FULLNM":"지방재정","STATBL_ID":"T195123006342415","STATBL_NM":"시도별 세목별 지방세징수액","DTACYCLE_NM":"년","TOP_ORG_NM":"국회예산정책처","ORG_NM":None,"USR_NM":"관리자","LOAD_DATE":"2023-08-04","OPEN_DATE":"2019-09-05","DATA_START_YY":"2010","DATA_END_YY":"2021","STATBL_CMMT":"1) 2010년 세목개정(소득할주민세→지방소득세)으로 세입은 지방소득세로 표기하고 환급금발생은 주민세에서 차감(서울시)\t\t\t\t\t\t\t\t\t\t\t\t\t\t\r\n2) 지역개발세와 공동시설세를 묶어 지역자원시설세로 통합\t\r\n3) 2022년도 자료는 2023년 10월 공표예정\t\t\t\t\t\t\t\t\t\t\t\t\t","SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T195123006342415.do"},{"CATE_FULLNM":"지방재정","STATBL_ID":"T189813000811224","STATBL_NM":"중앙정부의 지방이전재원","DTACYCLE_NM":"년","TOP_ORG_NM":"기획재정부","ORG_NM":None,"USR_NM":"국회예산정책처","LOAD_DATE":"2024-01-24","OPEN_DATE":"2018-07-02","DATA_START_YY":"2016","DATA_END_YY":"2024","STATBL_CMMT":"각 연도 본예산 기준임 \r\n자료: 기획재정부 「2023년 대한민국 예산」","SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T189813000811224.do"},{"CATE_FULLNM":"지방재정","STATBL_ID":"T181213004058042","STATBL_NM":"연도별 국고보조금 및 지방비부담 현황","DTACYCLE_NM":"년","TOP_ORG_NM":"행정안전부","ORG_NM":None,"USR_NM":"국회예산정책처","LOAD_DATE":"2023-07-30","OPEN_DATE":"2018-07-26","DATA_START_YY":"2013","DATA_END_YY":"2023","STATBL_CMMT":"주: 지방자치단체에서 당초예산에 편성한 금액\r\n자료: 행정안전부, 「2023년도 지방자치단체 통합재정 개요」","SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T181213004058042.do"},{"CATE_FULLNM":"지방재정","STATBL_ID":"T182023000806307","STATBL_NM":"지방세 징수액","DTACYCLE_NM":"년","TOP_ORG_NM":"행정안전부","ORG_NM":None,"USR_NM":"국회예산정책처","LOAD_DATE":"2024-01-27","OPEN_DATE":"2020-07-23","DATA_START_YY":"1991","DATA_END_YY":"2022","STATBL_CMMT":"주: 1) 각 연도말 결산액 기준임\r\n     2) 해당연도 징수액은 차년도 11월 공표(2022년 지방세 징수액은 2023년 11월 공표예정)\r\n자료: 행정안전부, 지방세 통계연감, 각 연도.","SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T182023000806307.do"},{"CATE_FULLNM":"지방재정","STATBL_ID":"T198483006334231","STATBL_NM":"지방세 수입 구조","DTACYCLE_NM":"년","TOP_ORG_NM":"행정안전부","ORG_NM":None,"USR_NM":"국회예산정책처","LOAD_DATE":"2023-08-04","OPEN_DATE":"2019-09-05","DATA_START_YY":"2011","DATA_END_YY":"2021","STATBL_CMMT":"주: 2022년 자료는 2023년 10월 공표예정","SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T198483006334231.do"},{"CATE_FULLNM":"지방재정","STATBL_ID":"T182983000791894","STATBL_NM":"지역별 통합재정 수지","DTACYCLE_NM":"년","TOP_ORG_NM":"행정안전부","ORG_NM":None,"USR_NM":"국회예산정책처","LOAD_DATE":"2023-07-30","OPEN_DATE":"2018-06-30","DATA_START_YY":"2017","DATA_END_YY":"2023","STATBL_CMMT":" 1. 시·도는 시·도 본청 + 시·군·구 \r\n 2. 순세계잉여금이 제외된 수치임 \r\n 3. (통합재정수지) 당해연도의 순수한 수입에서 순수한 지출을 차감한 수치로서 재정 활동의 적자 또는 흑자 등 재정운영수지를 측정하는 지표\r\n    * 통합재정수지 = 세입 - 세출 및 순융자(융자지출 - 융자회수)\r\n 자료: 행정안전부, 2023년도 지방자치단체 통합재정개요, 2023.5.\r\n","SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T182983000791894.do"},{"CATE_FULLNM":"지방재정","STATBL_ID":"T181803000845561","STATBL_NM":"지방자치단체 지방채 현황","DTACYCLE_NM":"년","TOP_ORG_NM":"행정안전부","ORG_NM":None,"USR_NM":"국회예산정책처","LOAD_DATE":"2023-07-30","OPEN_DATE":"2018-07-02","DATA_START_YY":"2015","DATA_END_YY":"2021","STATBL_CMMT":"주: 지방채 현황은 해당연도의 현황이 차년도 말에 공표됨.\r\n자료: 행정안전부(2023.6), 지방자치단체 통합재정개요","SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T181803000845561.do"},{"CATE_FULLNM":"지방재정","STATBL_ID":"T181413001906103","STATBL_NM":"일반자치단체 통합재정 수입·지출","DTACYCLE_NM":"년","TOP_ORG_NM":"국회예산정책처","ORG_NM":None,"USR_NM":"관리자","LOAD_DATE":None,"OPEN_DATE":"2018-07-10","DATA_START_YY":None,"DATA_END_YY":None,"STATBL_CMMT":None,"SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T181413001906103.do"},{"CATE_FULLNM":"지방재정","STATBL_ID":"T181543001385928","STATBL_NM":"중앙-지방간 재원배분: 통합재정 사용액 비교","DTACYCLE_NM":"년","TOP_ORG_NM":"국회예산정책처","ORG_NM":None,"USR_NM":"관리자","LOAD_DATE":None,"OPEN_DATE":"2018-07-09","DATA_START_YY":None,"DATA_END_YY":None,"STATBL_CMMT":None,"SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T181543001385928.do"},{"CATE_FULLNM":"지방재정","STATBL_ID":"T186073001435430","STATBL_NM":"지방교부세","DTACYCLE_NM":"년","TOP_ORG_NM":"국회예산정책처","ORG_NM":None,"USR_NM":"관리자","LOAD_DATE":None,"OPEN_DATE":"2018-07-09","DATA_START_YY":None,"DATA_END_YY":None,"STATBL_CMMT":None,"SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T186073001435430.do"},{"CATE_FULLNM":"국제통계","STATBL_ID":"T203893006904525","STATBL_NM":"OECD 국가의 일반정부 부채","DTACYCLE_NM":"년,분기","TOP_ORG_NM":"국회예산정책처","ORG_NM":None,"USR_NM":"관리자","LOAD_DATE":"2022-01-21","OPEN_DATE":"2020-08-13","DATA_START_YY":"2014","DATA_END_YY":"2020","STATBL_CMMT":"자료: OECD Public Sector Debt, consolidated, nominal value","SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T203893006904525.do"},{"CATE_FULLNM":"국제통계","STATBL_ID":"T182273002916379","STATBL_NM":"OECD 국가별 신재생에너지 공급","DTACYCLE_NM":"년","TOP_ORG_NM":"국회예산정책처","ORG_NM":None,"USR_NM":"관리자","LOAD_DATE":"2023-08-10","OPEN_DATE":"2018-07-15","DATA_START_YY":"2014","DATA_END_YY":"2021","STATBL_CMMT":"자료: 산업통상자원부·에너지경제연구원(2021),「2021 에너지통계연보」; IEA(2021),「Extended World Energy Balance 2021」","SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T182273002916379.do"},{"CATE_FULLNM":"국제통계","STATBL_ID":"T186573002492239","STATBL_NM":"주요국 국방비 비교","DTACYCLE_NM":"년","TOP_ORG_NM":"국회예산정책처","ORG_NM":None,"USR_NM":"관리자","LOAD_DATE":"2023-07-26","OPEN_DATE":"2018-07-11","DATA_START_YY":"2017","DATA_END_YY":"2022","STATBL_CMMT":"주: 러시아, 중국은 예산외자금(extra-budgetary funds) 미포함\r\n자료: 영국 국제전략문제연구소(IISS)「The Military Balance」 2023. 2.","SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T186573002492239.do"},{"CATE_FULLNM":"국제통계","STATBL_ID":"T186533002897124","STATBL_NM":"OECD 국가별 최종에너지 소비","DTACYCLE_NM":"년","TOP_ORG_NM":"국회예산정책처","ORG_NM":None,"USR_NM":"관리자","LOAD_DATE":"2023-08-09","OPEN_DATE":"2018-07-15","DATA_START_YY":"2016","DATA_END_YY":"2020","STATBL_CMMT":"자료: 산업통상자원부·에너지경제연구원(2020),「2020 에너지통계연보」; IEA(2020),「World Energy Balance 2020」","SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T186533002897124.do"},{"CATE_FULLNM":"국제통계","STATBL_ID":"T187153001764738","STATBL_NM":"교사 1인당 학급당 학생수·수업시간 (OECD 평균비교)","DTACYCLE_NM":"년","TOP_ORG_NM":"국회예산정책처","ORG_NM":None,"USR_NM":"관리자","LOAD_DATE":"2023-08-10","OPEN_DATE":"2018-07-10","DATA_START_YY":"2000","DATA_END_YY":"2020","STATBL_CMMT":"주: 1. 전기중등은 중학교 과정, 후기중등은 고등학교 과정에 해당함 \r\n2. 순수업 시간의 '후기 중등'은 '후기 중등(일반계)'에 해당하며, 2017년 부터 '후기 중등(직업계)' 항목이 추가됨","SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T187153001764738.do"},{"CATE_FULLNM":"위원회별 통계>위원회별 예산","STATBL_ID":"T182223003754662","STATBL_NM":"법제사법위원회 재정규모","DTACYCLE_NM":"년","TOP_ORG_NM":"국회예산정책처","ORG_NM":None,"USR_NM":"관리자","LOAD_DATE":None,"OPEN_DATE":"2018-07-23","DATA_START_YY":None,"DATA_END_YY":None,"STATBL_CMMT":None,"SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T182223003754662.do"},{"CATE_FULLNM":"위원회별 통계>위원회별 예산","STATBL_ID":"T183103003745729","STATBL_NM":"국회운영위원회 재정규모","DTACYCLE_NM":"년","TOP_ORG_NM":"국회예산정책처","ORG_NM":None,"USR_NM":"관리자","LOAD_DATE":None,"OPEN_DATE":"2018-07-23","DATA_START_YY":None,"DATA_END_YY":None,"STATBL_CMMT":None,"SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T183103003745729.do"},{"CATE_FULLNM":"위원회별 통계>위원회별 예산","STATBL_ID":"T188663003766933","STATBL_NM":"정무위원회 재정규모","DTACYCLE_NM":"년","TOP_ORG_NM":"국회예산정책처","ORG_NM":None,"USR_NM":"관리자","LOAD_DATE":None,"OPEN_DATE":"2018-07-23","DATA_START_YY":None,"DATA_END_YY":None,"STATBL_CMMT":None,"SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T188663003766933.do"},{"CATE_FULLNM":"위원회별 통계>위원회별 예산","STATBL_ID":"T189573003773650","STATBL_NM":"기획재정위원회 재정규모","DTACYCLE_NM":"년","TOP_ORG_NM":"국회예산정책처","ORG_NM":None,"USR_NM":"관리자","LOAD_DATE":None,"OPEN_DATE":"2018-07-23","DATA_START_YY":None,"DATA_END_YY":None,"STATBL_CMMT":None,"SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T189573003773650.do"},{"CATE_FULLNM":"위원회별 통계>위원회별 예산","STATBL_ID":"T184483001591318","STATBL_NM":"과학기술정보방송통신위원회 재정규모","DTACYCLE_NM":"년","TOP_ORG_NM":"국회예산정책처","ORG_NM":None,"USR_NM":"관리자","LOAD_DATE":None,"OPEN_DATE":"2018-07-09","DATA_START_YY":None,"DATA_END_YY":None,"STATBL_CMMT":None,"SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T184483001591318.do"},{"CATE_FULLNM":"위원회별 통계>위원회별 예산","STATBL_ID":"T185013001819929","STATBL_NM":"교육위원회 재정규모","DTACYCLE_NM":"년","TOP_ORG_NM":"국회예산정책처","ORG_NM":None,"USR_NM":"관리자","LOAD_DATE":None,"OPEN_DATE":"2018-07-10","DATA_START_YY":None,"DATA_END_YY":None,"STATBL_CMMT":None,"SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T185013001819929.do"},{"CATE_FULLNM":"위원회별 통계>위원회별 예산","STATBL_ID":"T199263006041980","STATBL_NM":"문화체육관광위원회 소관 부처 재정규모","DTACYCLE_NM":"년","TOP_ORG_NM":"국회예산정책처","ORG_NM":None,"USR_NM":"관리자","LOAD_DATE":"2019-04-24","OPEN_DATE":"2019-04-24","DATA_START_YY":None,"DATA_END_YY":None,"STATBL_CMMT":None,"SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T199263006041980.do"},{"CATE_FULLNM":"위원회별 통계>위원회별 예산","STATBL_ID":"T189143001982421","STATBL_NM":"외교통일위원회 재정규모","DTACYCLE_NM":"년","TOP_ORG_NM":"국회예산정책처","ORG_NM":None,"USR_NM":"관리자","LOAD_DATE":None,"OPEN_DATE":"2018-07-10","DATA_START_YY":None,"DATA_END_YY":None,"STATBL_CMMT":None,"SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T189143001982421.do"},{"CATE_FULLNM":"위원회별 통계>위원회별 예산","STATBL_ID":"T183923001938596","STATBL_NM":"국방위원회 재정규모","DTACYCLE_NM":"년","TOP_ORG_NM":"국회예산정책처","ORG_NM":None,"USR_NM":"관리자","LOAD_DATE":None,"OPEN_DATE":"2018-07-10","DATA_START_YY":None,"DATA_END_YY":None,"STATBL_CMMT":None,"SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T183923001938596.do"},{"CATE_FULLNM":"위원회별 통계>위원회별 예산","STATBL_ID":"T184123001163879","STATBL_NM":"행정안전위원회재정규모","DTACYCLE_NM":"년","TOP_ORG_NM":"국회예산정책처","ORG_NM":None,"USR_NM":"관리자","LOAD_DATE":None,"OPEN_DATE":"2018-07-05","DATA_START_YY":None,"DATA_END_YY":None,"STATBL_CMMT":None,"SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T184123001163879.do"},{"CATE_FULLNM":"위원회별 통계>위원회별 예산","STATBL_ID":"T181923001992799","STATBL_NM":"보건복지위원회 재정규모","DTACYCLE_NM":"년","TOP_ORG_NM":"국회예산정책처","ORG_NM":None,"USR_NM":"관리자","LOAD_DATE":None,"OPEN_DATE":"2018-07-10","DATA_START_YY":None,"DATA_END_YY":None,"STATBL_CMMT":None,"SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T181923001992799.do"},{"CATE_FULLNM":"위원회별 통계>위원회별 예산","STATBL_ID":"T185793001151282","STATBL_NM":"환경노동위원회 재정규모","DTACYCLE_NM":"년","TOP_ORG_NM":"국회예산정책처","ORG_NM":None,"USR_NM":"관리자","LOAD_DATE":None,"OPEN_DATE":"2018-07-05","DATA_START_YY":None,"DATA_END_YY":None,"STATBL_CMMT":None,"SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T185793001151282.do"},{"CATE_FULLNM":"위원회별 통계>위원회별 예산","STATBL_ID":"T189533002241966","STATBL_NM":"농림축산식품해양수산위원회 재정규모","DTACYCLE_NM":"년","TOP_ORG_NM":"국회예산정책처","ORG_NM":None,"USR_NM":"관리자","LOAD_DATE":None,"OPEN_DATE":"2018-07-11","DATA_START_YY":None,"DATA_END_YY":None,"STATBL_CMMT":None,"SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T189533002241966.do"},{"CATE_FULLNM":"위원회별 통계>위원회별 예산","STATBL_ID":"T186363002221105","STATBL_NM":"산업통상자원중소벤처기업위원회 재정규모","DTACYCLE_NM":"년","TOP_ORG_NM":"국회예산정책처","ORG_NM":None,"USR_NM":"관리자","LOAD_DATE":None,"OPEN_DATE":"2018-07-11","DATA_START_YY":None,"DATA_END_YY":None,"STATBL_CMMT":None,"SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T186363002221105.do"},{"CATE_FULLNM":"위원회별 통계>위원회별 예산","STATBL_ID":"T184173002075170","STATBL_NM":"국토교통위원회 재정규모","DTACYCLE_NM":"년","TOP_ORG_NM":"국회예산정책처","ORG_NM":None,"USR_NM":"관리자","LOAD_DATE":None,"OPEN_DATE":"2018-07-10","DATA_START_YY":None,"DATA_END_YY":None,"STATBL_CMMT":None,"SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T184173002075170.do"},{"CATE_FULLNM":"위원회별 통계>위원회별 예산","STATBL_ID":"T186403002018717","STATBL_NM":"여성가족위원회 재정규모","DTACYCLE_NM":"년","TOP_ORG_NM":"국회예산정책처","ORG_NM":None,"USR_NM":"관리자","LOAD_DATE":None,"OPEN_DATE":"2018-07-10","DATA_START_YY":None,"DATA_END_YY":None,"STATBL_CMMT":"자료: 여성가족부","SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T186403002018717.do"},{"CATE_FULLNM":"국제통계>주요 경제지표","STATBL_ID":"T222723007076919","STATBL_NM":"OECD 소비자물가지수","DTACYCLE_NM":"분기","TOP_ORG_NM":"국회예산정책처","ORG_NM":None,"USR_NM":"관리자","LOAD_DATE":"2024-01-14","OPEN_DATE":"2022-04-27","DATA_START_YY":"1914","DATA_END_YY":"2023","STATBL_CMMT":"출처: OECD 통계 「http://stats.oecd.org」","SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T222723007076919.do"},{"CATE_FULLNM":"국제통계>주요 경제지표","STATBL_ID":"T224243007024812","STATBL_NM":"OECD 국내총생산(GDP)(당해년 가격)","DTACYCLE_NM":"분기","TOP_ORG_NM":"국회예산정책처","ORG_NM":None,"USR_NM":"관리자","LOAD_DATE":"2023-09-24","OPEN_DATE":"2022-04-27","DATA_START_YY":"1955","DATA_END_YY":"2023","STATBL_CMMT":"출처: OECD 통계 「http://stats.oecd.org」","SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T224243007024812.do"},{"CATE_FULLNM":"국제통계>주요 경제지표","STATBL_ID":"T226003007036606","STATBL_NM":"OECD  고용비용지수","DTACYCLE_NM":"분기","TOP_ORG_NM":"국회예산정책처","ORG_NM":None,"USR_NM":"관리자","LOAD_DATE":"2024-01-14","OPEN_DATE":"2022-04-27","DATA_START_YY":"1975","DATA_END_YY":"2023","STATBL_CMMT":"출처: OECD 통계 「http://stats.oecd.org」","SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T226003007036606.do"},{"CATE_FULLNM":"국제통계>주요 경제지표","STATBL_ID":"T223643007051928","STATBL_NM":"OECD 생산자물가지수","DTACYCLE_NM":"분기","TOP_ORG_NM":"국회예산정책처","ORG_NM":None,"USR_NM":"관리자","LOAD_DATE":"2023-10-08","OPEN_DATE":"2022-04-27","DATA_START_YY":"1956","DATA_END_YY":"2023","STATBL_CMMT":"출처: OECD 통계 「http://stats.oecd.org」","SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T223643007051928.do"},{"CATE_FULLNM":"국제통계>주요 경제지표","STATBL_ID":"T228743007099398","STATBL_NM":"OECD 은행간 금리","DTACYCLE_NM":"분기,월","TOP_ORG_NM":"국회예산정책처","ORG_NM":None,"USR_NM":"관리자","LOAD_DATE":"2024-01-14","OPEN_DATE":"2022-04-27","DATA_START_YY":"1956","DATA_END_YY":"2023","STATBL_CMMT":"출처: OECD 통계 「http://stats.oecd.org」","SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T228743007099398.do"},{"CATE_FULLNM":"국제통계>주요 경제지표","STATBL_ID":"T224553007089343","STATBL_NM":"OECD 수입액","DTACYCLE_NM":"분기,월","TOP_ORG_NM":"국회예산정책처","ORG_NM":None,"USR_NM":"관리자","LOAD_DATE":"2024-01-28","OPEN_DATE":"2022-04-27","DATA_START_YY":"1955","DATA_END_YY":"2023","STATBL_CMMT":"출처: OECD 통계 「http://stats.oecd.org」","SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T224553007089343.do"},{"CATE_FULLNM":"국제통계>주요 경제지표","STATBL_ID":"T222913007004629","STATBL_NM":"OECD 총 제조","DTACYCLE_NM":"분기","TOP_ORG_NM":"국회예산정책처","ORG_NM":None,"USR_NM":"관리자","LOAD_DATE":"2024-01-07","OPEN_DATE":"2022-04-27","DATA_START_YY":"1919","DATA_END_YY":"2023","STATBL_CMMT":"출처: OECD 통계 「http://stats.oecd.org」","SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T222913007004629.do"},{"CATE_FULLNM":"국제통계>주요 경제지표","STATBL_ID":"T222273007067508","STATBL_NM":"OECD 소매판매","DTACYCLE_NM":"분기","TOP_ORG_NM":"국회예산정책처","ORG_NM":None,"USR_NM":"관리자","LOAD_DATE":"2023-10-01","OPEN_DATE":"2022-04-27","DATA_START_YY":"1957","DATA_END_YY":"2023","STATBL_CMMT":"출처: OECD 통계 「http://stats.oecd.org」","SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T222273007067508.do"},{"CATE_FULLNM":"인구·사회통계>인구","STATBL_ID":"T211463006939573","STATBL_NM":"출생(등록)자·사망(말소)자 ","DTACYCLE_NM":"년","TOP_ORG_NM":"국회예산정책처","ORG_NM":None,"USR_NM":"관리자","LOAD_DATE":"2023-04-01","OPEN_DATE":"2021-12-08","DATA_START_YY":"1970","DATA_END_YY":"2022","STATBL_CMMT":"자료: 통계청,「인구동향조사」","SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T211463006939573.do"},{"CATE_FULLNM":"인구·사회통계>인구","STATBL_ID":"T203963006925762","STATBL_NM":"총인구 성장률(주민등록인구)","DTACYCLE_NM":"년","TOP_ORG_NM":"국회예산정책처","ORG_NM":None,"USR_NM":"관리자","LOAD_DATE":"2023-07-17","OPEN_DATE":"2020-09-25","DATA_START_YY":"1992","DATA_END_YY":"2022","STATBL_CMMT":"자료: 행정안전부,「주민등록인구현황」","SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T203963006925762.do"},{"CATE_FULLNM":"공공기관 통계>지정현황","STATBL_ID":"T203683006884284","STATBL_NM":"부처별 공공기관현황","DTACYCLE_NM":"년","TOP_ORG_NM":"국회예산정책처","ORG_NM":None,"USR_NM":"관리자","LOAD_DATE":None,"OPEN_DATE":"2020-06-15","DATA_START_YY":None,"DATA_END_YY":None,"STATBL_CMMT":None,"SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T203683006884284.do"},{"CATE_FULLNM":"국제통계>주요 경제지표","STATBL_ID":"T222813007426744","STATBL_NM":"OECD 경기선행지수","DTACYCLE_NM":"월","TOP_ORG_NM":"국회예산정책처","ORG_NM":None,"USR_NM":"관리자","LOAD_DATE":"2023-10-17","OPEN_DATE":"2022-04-27","DATA_START_YY":"1957","DATA_END_YY":"2023","STATBL_CMMT":"출처: OECD 통계 「http://stats.oecd.org」","SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T222813007426744.do"},{"CATE_FULLNM":"국제통계>주요 경제지표","STATBL_ID":"T221403007113161","STATBL_NM":"OECD 총수출입액","DTACYCLE_NM":"분기,월","TOP_ORG_NM":"국회예산정책처","ORG_NM":None,"USR_NM":"관리자","LOAD_DATE":"2024-01-28","OPEN_DATE":"2022-04-27","DATA_START_YY":"1955","DATA_END_YY":"2023","STATBL_CMMT":"출처: OECD 통계 「http://stats.oecd.org」","SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T221403007113161.do"},{"CATE_FULLNM":"국제통계>주요 경제지표","STATBL_ID":"T223023007105802","STATBL_NM":"OECD 수출액","DTACYCLE_NM":"분기,월","TOP_ORG_NM":"국회예산정책처","ORG_NM":None,"USR_NM":"관리자","LOAD_DATE":"2024-01-21","OPEN_DATE":"2022-04-27","DATA_START_YY":"1955","DATA_END_YY":"2023","STATBL_CMMT":"출처: OECD 통계 「http://stats.oecd.org」","SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T223023007105802.do"},{"CATE_FULLNM":"국제통계>주요 경제지표","STATBL_ID":"T221993007019771","STATBL_NM":"OECD 건설","DTACYCLE_NM":"월","TOP_ORG_NM":"국회예산정책처","ORG_NM":None,"USR_NM":"관리자","LOAD_DATE":"2024-01-07","OPEN_DATE":"2022-04-27","DATA_START_YY":"1955","DATA_END_YY":"2023","STATBL_CMMT":"출처: OECD 통계 「http://stats.oecd.org」","SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T221993007019771.do"},{"CATE_FULLNM":"조세통계>기초통계","STATBL_ID":"T188383000323998","STATBL_NM":"조세부담률 및 국민부담률","DTACYCLE_NM":"년","TOP_ORG_NM":"기획재정부","ORG_NM":None,"USR_NM":"국회예산정책처","LOAD_DATE":"2023-12-01","OPEN_DATE":"2018-08-31","DATA_START_YY":"2000","DATA_END_YY":"2022","STATBL_CMMT":"주: 1. SNA 2015년 기준 경상 GDP 성장률을 적용하여 산출2. 반올림으로 인한 단수차 존재\r\n자료: 기획재정부, 행정안전부, 한국은행","SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T188383000323998.do"},{"CATE_FULLNM":"공공기관 통계>지정현황","STATBL_ID":"T185203003736933","STATBL_NM":"공공기관 지정 현황","DTACYCLE_NM":"년","TOP_ORG_NM":"기획재정부","ORG_NM":None,"USR_NM":"국회예산정책처","LOAD_DATE":"2023-07-27","OPEN_DATE":"2018-07-20","DATA_START_YY":"2011","DATA_END_YY":"2023","STATBL_CMMT":"1. 2021년 현황은 해산된 기관을 포함한 2021년 말 기준임\r\n2. 2023. 1. 30 기준","SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T185203003736933.do"},{"CATE_FULLNM":"공공기관 통계>지정현황","STATBL_ID":"T184313001426172","STATBL_NM":"공공기관 지정 및 분류기준","DTACYCLE_NM":"년","TOP_ORG_NM":"국회예산정책처","ORG_NM":None,"USR_NM":"관리자","LOAD_DATE":None,"OPEN_DATE":"2018-07-09","DATA_START_YY":None,"DATA_END_YY":None,"STATBL_CMMT":None,"SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T184313001426172.do"},{"CATE_FULLNM":"재정통계>재정총량","STATBL_ID":"T189693001617414","STATBL_NM":"총수입·총지출(총량)","DTACYCLE_NM":"년","TOP_ORG_NM":"기획재정부","ORG_NM":None,"USR_NM":"국회예산정책처","LOAD_DATE":"2024-01-18","OPEN_DATE":"2018-07-09","DATA_START_YY":"2010","DATA_END_YY":"2024","STATBL_CMMT":"예산 총수입·총지출은 추경 기준","SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T189693001617414.do"},{"CATE_FULLNM":"경제통계>국민계정","STATBL_ID":"T192213006109866","STATBL_NM":"국내총생산 및 경제성장률(GDP,2015년 기준)","DTACYCLE_NM":"년","TOP_ORG_NM":"한국은행","ORG_NM":None,"USR_NM":"국회예산정책처","LOAD_DATE":"2023-07-28","OPEN_DATE":"2019-06-24","DATA_START_YY":"1953","DATA_END_YY":"2022","STATBL_CMMT":None,"SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T192213006109866.do"},{"CATE_FULLNM":"조세통계>기초통계","STATBL_ID":"T205073006409130","STATBL_NM":"국세수입실적(연간)","DTACYCLE_NM":"년","TOP_ORG_NM":"국회예산정책처","ORG_NM":None,"USR_NM":"세제분석2과01","LOAD_DATE":"2023-09-14","OPEN_DATE":"2020-02-17","DATA_START_YY":"2008","DATA_END_YY":"2022","STATBL_CMMT":"자료: 기획재정부\r\n주:  소득세 항목 중 연금소득세는 별도 표시하지 않음","SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T205073006409130.do"},{"CATE_FULLNM":"조세통계>기초통계","STATBL_ID":"T206873006418249","STATBL_NM":"국세수입실적(월별 누계)","DTACYCLE_NM":"월","TOP_ORG_NM":"국회예산정책처","ORG_NM":None,"USR_NM":"관리자","LOAD_DATE":"2023-12-29","OPEN_DATE":"2020-02-17","DATA_START_YY":"2014","DATA_END_YY":"2023","STATBL_CMMT":"자료: 기획재정부\r\n*누계 기준","SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T206873006418249.do"},{"CATE_FULLNM":"인구·사회통계>인구","STATBL_ID":"T188273000249112","STATBL_NM":"출생아수와 합계출산율","DTACYCLE_NM":"년","TOP_ORG_NM":"통계청","ORG_NM":None,"USR_NM":"국회예산정책처","LOAD_DATE":"2023-07-17","OPEN_DATE":"2018-06-17","DATA_START_YY":"1997","DATA_END_YY":"2022","STATBL_CMMT":"자료 : 통계청(101003호, 인구동향조사)\r\n  1) 합계출산율(가임여성1명당 명)\r\n  2) 연령별 출산율(가임여성인구 1천명당 명)","SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T188273000249112.do"},{"CATE_FULLNM":"경제통계>국민계정","STATBL_ID":"T188843000667480","STATBL_NM":"경제전망","DTACYCLE_NM":"년","TOP_ORG_NM":"국회예산정책처","ORG_NM":None,"USR_NM":"관리자","LOAD_DATE":None,"OPEN_DATE":"2018-06-21","DATA_START_YY":None,"DATA_END_YY":None,"STATBL_CMMT":None,"SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T188843000667480.do"},{"CATE_FULLNM":"공공기관 통계>지정현황","STATBL_ID":"T186723001411489","STATBL_NM":"공공기관 지정 변경 현황","DTACYCLE_NM":"년","TOP_ORG_NM":"기획재정부","ORG_NM":None,"USR_NM":"국회예산정책처","LOAD_DATE":None,"OPEN_DATE":"2018-07-09","DATA_START_YY":None,"DATA_END_YY":None,"STATBL_CMMT":None,"SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T186723001411489.do"},{"CATE_FULLNM":"경제통계>국민계정","STATBL_ID":"T183793000671157","STATBL_NM":"IMF 세계경제 전망","DTACYCLE_NM":"년","TOP_ORG_NM":"국회예산정책처","ORG_NM":None,"USR_NM":"관리자","LOAD_DATE":None,"OPEN_DATE":"2018-06-21","DATA_START_YY":None,"DATA_END_YY":None,"STATBL_CMMT":None,"SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T183793000671157.do"},{"CATE_FULLNM":"공공기관 통계>지정현황","STATBL_ID":"T189453001204814","STATBL_NM":"공공기관 지정 상세 목록","DTACYCLE_NM":"년","TOP_ORG_NM":"국회예산정책처","ORG_NM":None,"USR_NM":"관리자","LOAD_DATE":None,"OPEN_DATE":"2018-07-05","DATA_START_YY":None,"DATA_END_YY":None,"STATBL_CMMT":None,"SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T189453001204814.do"},{"CATE_FULLNM":"재정통계>재정총량","STATBL_ID":"T188723004802681","STATBL_NM":"총수입(항목별)","DTACYCLE_NM":"년","TOP_ORG_NM":"기획재정부","ORG_NM":None,"USR_NM":"국회예산정책처","LOAD_DATE":"2024-01-18","OPEN_DATE":"2018-08-01","DATA_START_YY":"2010","DATA_END_YY":"2024","STATBL_CMMT":"예산(추경) 기준","SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T188723004802681.do"},{"CATE_FULLNM":"조세통계>기초통계","STATBL_ID":"T203863006421880","STATBL_NM":"진도율(월별 누계)","DTACYCLE_NM":"월","TOP_ORG_NM":"국회예산정책처","ORG_NM":None,"USR_NM":"관리자","LOAD_DATE":"2023-12-29","OPEN_DATE":"2020-02-17","DATA_START_YY":"2014","DATA_END_YY":"2023","STATBL_CMMT":"2022년까지는 결산 대비, 2023년은 예산대비 값임\r\n자료: 기획재정부 「월간 재정동향」 등 자료를 바탕으로 재작성","SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T203863006421880.do"},{"CATE_FULLNM":"조세통계>기초통계","STATBL_ID":"T203603006436445","STATBL_NM":"진도율(전년동기대비)","DTACYCLE_NM":"월","TOP_ORG_NM":"국회예산정책처","ORG_NM":None,"USR_NM":"관리자","LOAD_DATE":"2023-12-29","OPEN_DATE":"2020-02-17","DATA_START_YY":"2016","DATA_END_YY":"2023","STATBL_CMMT":"자료: 기획재정부 「월간 재정동향」 월별실적을 바탕으로 재작성","SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T203603006436445.do"},{"CATE_FULLNM":"재정통계>재정총량","STATBL_ID":"T182633004812603","STATBL_NM":"총지출(항목별)","DTACYCLE_NM":"년","TOP_ORG_NM":"기획재정부","ORG_NM":None,"USR_NM":"국회예산정책처","LOAD_DATE":"2024-01-18","OPEN_DATE":"2018-08-01","DATA_START_YY":"2010","DATA_END_YY":"2024","STATBL_CMMT":"예산(추경) 기준","SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T182633004812603.do"},{"CATE_FULLNM":"경제통계>국민계정","STATBL_ID":"T183553001146446","STATBL_NM":"OECD 세계경제 전망","DTACYCLE_NM":"년","TOP_ORG_NM":"국회예산정책처","ORG_NM":None,"USR_NM":"관리자","LOAD_DATE":None,"OPEN_DATE":"2018-07-05","DATA_START_YY":None,"DATA_END_YY":None,"STATBL_CMMT":None,"SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T183553001146446.do"},{"CATE_FULLNM":"재정통계>재정총량","STATBL_ID":"T183213000709195","STATBL_NM":"재정수지","DTACYCLE_NM":"년","TOP_ORG_NM":"기획재정부","ORG_NM":None,"USR_NM":"국회예산정책처","LOAD_DATE":"2024-01-27","OPEN_DATE":"2020-07-23","DATA_START_YY":"1970","DATA_END_YY":"2022","STATBL_CMMT":"1) 중앙정부 기준\r\n2) 결산기준\r\n3) `04~`09년 자료는 공자기금과 외평기금간의 이자거래를 금융활동의 일환으로 판단하여 제거한 수치","SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T183213000709195.do"},{"CATE_FULLNM":"경제통계>국민계정","STATBL_ID":"T207903006384949","STATBL_NM":"World Bank 세계경제전망","DTACYCLE_NM":"년","TOP_ORG_NM":"국회예산정책처","ORG_NM":None,"USR_NM":"관리자","LOAD_DATE":None,"OPEN_DATE":"2020-01-29","DATA_START_YY":None,"DATA_END_YY":None,"STATBL_CMMT":None,"SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T207903006384949.do"},{"CATE_FULLNM":"재정통계>재정총량","STATBL_ID":"T191673005927817","STATBL_NM":"GDP 대비 국가채무 비율","DTACYCLE_NM":"년","TOP_ORG_NM":"기획재정부","ORG_NM":None,"USR_NM":"국회예산정책처","LOAD_DATE":"2023-07-28","OPEN_DATE":"2019-01-03","DATA_START_YY":"1974","DATA_END_YY":"2022","STATBL_CMMT":"1) 국가채무는 결산기준\r\n2) 2000년 이후 GDP는 2015년이 기준년도\r\n3) 1996년부터 지방정부 순채무 포함","SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T191673005927817.do"},{"CATE_FULLNM":"재정통계>재정총량","STATBL_ID":"T189473000723971","STATBL_NM":"국가채무(성질별)","DTACYCLE_NM":"년","TOP_ORG_NM":"기획재정부","ORG_NM":None,"USR_NM":"국회예산정책처","LOAD_DATE":"2024-01-27","OPEN_DATE":"2020-07-23","DATA_START_YY":"1997","DATA_END_YY":"2027","STATBL_CMMT":"주: 2022년은 잠정치","SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T189473000723971.do"},{"CATE_FULLNM":"조세통계>기초통계","STATBL_ID":"T181573000303448","STATBL_NM":"국세 세목별 수입구조","DTACYCLE_NM":"년","TOP_ORG_NM":"국회예산정책처","ORG_NM":None,"USR_NM":"관리자","LOAD_DATE":"2023-07-12","OPEN_DATE":"2022-06-21","DATA_START_YY":"2017","DATA_END_YY":"2022","STATBL_CMMT":"주 : 구성 항목별 합계는 소수점 이하 단수조정으로 상이할 수 있음\r\n자료 : 기획재정부 자료를 토대로 국회예산정책처 작성","SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T181573000303448.do"},{"CATE_FULLNM":"재정통계>재정총량","STATBL_ID":"T188763004825040","STATBL_NM":"국가채무(항목별)","DTACYCLE_NM":"년","TOP_ORG_NM":"기획재정부","ORG_NM":None,"USR_NM":"국회예산정책처","LOAD_DATE":"2024-01-27","OPEN_DATE":"2020-07-23","DATA_START_YY":"1997","DATA_END_YY":"2027","STATBL_CMMT":"주: 2022년은 잠정치(지방정부 순채무가 지방정부 결산 이후 확정)","SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T188763004825040.do"},{"CATE_FULLNM":"경제통계>국민계정","STATBL_ID":"T185763004099320","STATBL_NM":"지역내총생산(GRDP)(2015년 기준)","DTACYCLE_NM":"년","TOP_ORG_NM":"통계청","ORG_NM":None,"USR_NM":"국회예산정책처","LOAD_DATE":"2024-01-27","OPEN_DATE":"2020-07-23","DATA_START_YY":"1985","DATA_END_YY":"2022","STATBL_CMMT":"출처: 통계청 「지역소득」\r\n단위: 당해년가격기준\r\n기준년: 2015년\r\n매년 12월말 전년도 잠정자료 발표, 국세, 지방세 등 기초통계자료를 보완하여 익년 6월말 확정자료 DB수록\r\n","SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T185763004099320.do"},{"CATE_FULLNM":"재정통계>재정총량","STATBL_ID":"T201033006361599","STATBL_NM":"일반정부 부채(D2)(2015년 기준)","DTACYCLE_NM":"년","TOP_ORG_NM":"기획재정부","ORG_NM":None,"USR_NM":"국회예산정책처","LOAD_DATE":"2024-01-19","OPEN_DATE":"2020-01-16","DATA_START_YY":"2011","DATA_END_YY":"2022","STATBL_CMMT":None,"SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T201033006361599.do"},{"CATE_FULLNM":"조세통계>기초통계","STATBL_ID":"T207393006441886","STATBL_NM":"총 조세 대비 지방세 비중","DTACYCLE_NM":"년","TOP_ORG_NM":"기획재정부","ORG_NM":None,"USR_NM":"국회예산정책처","LOAD_DATE":"2023-12-02","OPEN_DATE":"2021-12-08","DATA_START_YY":"1980","DATA_END_YY":"2022","STATBL_CMMT":"자료: 국세청･관세청, e-나라지표: 징수보고서; 행정안전부, 지방세통계연감(지방세정연감), 각 연도를 바탕으로 국회예산정책처 작성","SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T207393006441886.do"},{"CATE_FULLNM":"재정통계>재정총량","STATBL_ID":"T206453006375099","STATBL_NM":"공공부문 부채(D3)(2015년 기준)","DTACYCLE_NM":"년","TOP_ORG_NM":"기획재정부","ORG_NM":None,"USR_NM":"국회예산정책처","LOAD_DATE":"2024-01-19","OPEN_DATE":"2020-01-16","DATA_START_YY":"2011","DATA_END_YY":"2022","STATBL_CMMT":None,"SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T206453006375099.do"},{"CATE_FULLNM":"재정통계>재정총량","STATBL_ID":"T187183000538818","STATBL_NM":"부처별 총지출","DTACYCLE_NM":"년","TOP_ORG_NM":"기획재정부","ORG_NM":None,"USR_NM":"국회예산정책처","LOAD_DATE":None,"OPEN_DATE":"2018-07-11","DATA_START_YY":None,"DATA_END_YY":None,"STATBL_CMMT":"자료: 기획재정부","SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T187183000538818.do"},{"CATE_FULLNM":"재정통계>재정총량","STATBL_ID":"T186313000755905","STATBL_NM":"국가보증채무","DTACYCLE_NM":"년","TOP_ORG_NM":"대한민국 정부","ORG_NM":None,"USR_NM":"국회예산정책처","LOAD_DATE":"2022-05-30","OPEN_DATE":"2018-06-30","DATA_START_YY":"2011","DATA_END_YY":"2024","STATBL_CMMT":"주:2021~2024년은 전망치\r\n자료: 대한민국 정부, 2021~2025년 국가보증채무관리계획","SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T186313000755905.do"},{"CATE_FULLNM":"북한통계>남북협력기금","STATBL_ID":"T182573005409426","STATBL_NM":"남북협력기금 조성","DTACYCLE_NM":"년","TOP_ORG_NM":"통계청","ORG_NM":None,"USR_NM":"국회예산정책처","LOAD_DATE":"2023-08-07","OPEN_DATE":"2018-08-12","DATA_START_YY":"1991","DATA_END_YY":"2022","STATBL_CMMT":"출처: 통일부「http://www.unikorea.go.kr>주요통계자료」","SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T182573005409426.do"},{"CATE_FULLNM":"북한통계>남북협력기금","STATBL_ID":"T189633005413020","STATBL_NM":"남북협력기금 집행","DTACYCLE_NM":"년","TOP_ORG_NM":"통계청","ORG_NM":None,"USR_NM":"국회예산정책처","LOAD_DATE":"2023-07-18","OPEN_DATE":"2018-08-12","DATA_START_YY":"1994","DATA_END_YY":"2022","STATBL_CMMT":"출처: 통일부「http://www.unikorea.go.kr>주요통계자료」\r\n\r\n1994년 자료는 91년~94년까지의 합계임","SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T189633005413020.do"},{"CATE_FULLNM":"국제통계>부의 분배지표","STATBL_ID":"T226473007137511","STATBL_NM":"OECD 가구당 평균 금융자산(현재가)","DTACYCLE_NM":"년","TOP_ORG_NM":"국회예산정책처","ORG_NM":None,"USR_NM":"관리자","LOAD_DATE":"2023-09-24","OPEN_DATE":"2022-04-27","DATA_START_YY":"2009","DATA_END_YY":"2019","STATBL_CMMT":"출처: OECD 통계 「http://stats.oecd.org」","SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T226473007137511.do"},{"CATE_FULLNM":"국제통계>부의 분배지표","STATBL_ID":"T221883007188473","STATBL_NM":"OECD 가구당 평균 부채(현재 가격)","DTACYCLE_NM":"년","TOP_ORG_NM":"국회예산정책처","ORG_NM":None,"USR_NM":"관리자","LOAD_DATE":"2023-09-24","OPEN_DATE":"2022-04-27","DATA_START_YY":"2009","DATA_END_YY":"2019","STATBL_CMMT":"출처: OECD 통계 「http://stats.oecd.org」","SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T221883007188473.do"},{"CATE_FULLNM":"국제통계>부의 분배지표","STATBL_ID":"T222333007162944","STATBL_NM":"OECD 가구의 소득 대비 부채 비율 중앙값","DTACYCLE_NM":"년","TOP_ORG_NM":"국회예산정책처","ORG_NM":None,"USR_NM":"관리자","LOAD_DATE":"2023-09-24","OPEN_DATE":"2022-04-27","DATA_START_YY":"2009","DATA_END_YY":"2019","STATBL_CMMT":"출처: OECD 통계 「http://stats.oecd.org」","SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T222333007162944.do"},{"CATE_FULLNM":"국제통계>부의 분배지표","STATBL_ID":"T227183007157690","STATBL_NM":"OECD 가구당 평균 순자산(현재 가격)","DTACYCLE_NM":"년","TOP_ORG_NM":"국회예산정책처","ORG_NM":None,"USR_NM":"관리자","LOAD_DATE":"2023-09-24","OPEN_DATE":"2022-04-27","DATA_START_YY":"2009","DATA_END_YY":"2019","STATBL_CMMT":"출처: OECD 통계 「http://stats.oecd.org」","SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T227183007157690.do"},{"CATE_FULLNM":"국제통계>부의 분배지표","STATBL_ID":"T226943007142400","STATBL_NM":"OECD 1인당 평균 순자산(현재 가격)","DTACYCLE_NM":"년","TOP_ORG_NM":"국회예산정책처","ORG_NM":None,"USR_NM":"관리자","LOAD_DATE":"2023-09-24","OPEN_DATE":"2022-04-27","DATA_START_YY":"2009","DATA_END_YY":"2019","STATBL_CMMT":"출처: OECD 통계 「http://stats.oecd.org」","SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T226943007142400.do"},{"CATE_FULLNM":"조세통계>국제비교","STATBL_ID":"T186143000334166","STATBL_NM":"OECD 국가의 국민부담률","DTACYCLE_NM":"년","TOP_ORG_NM":"OECD","ORG_NM":None,"USR_NM":"국회예산정책처","LOAD_DATE":"2023-10-10","OPEN_DATE":"2018-07-18","DATA_START_YY":"1965","DATA_END_YY":"2022","STATBL_CMMT":"자료: OECD Revenue Statistics\r\n주1) 우리나라 조세부담률은 신계열 명목 GDP반영(2010년→2015년으로 기준년 개편)","SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T186143000334166.do"},{"CATE_FULLNM":"북한통계>남북한교류","STATBL_ID":"T185933005382245","STATBL_NM":"분야별 남북회담 개최","DTACYCLE_NM":"년","TOP_ORG_NM":"통계청","ORG_NM":None,"USR_NM":"국회예산정책처","LOAD_DATE":"2023-12-23","OPEN_DATE":"2018-08-12","DATA_START_YY":"1992","DATA_END_YY":"2022","STATBL_CMMT":"출처: 통일부「http://www.unikorea.go.kr>주요통계자료」\r\n\r\n1992년은 1971년부터 1992년까지의 회담 개최 수의 합계임\r\n\r\n정치(장차관급 회담 등)/군사(장성급·군사실무회담 등)/경제(경제협력추진위 등)\r\n\r\n/인도·사회(적십자·체육 회담 등)","SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T185933005382245.do"},{"CATE_FULLNM":"재정통계>세입세출통계","STATBL_ID":"T184703004345091","STATBL_NM":"세출예산규모(본예산기준)","DTACYCLE_NM":"년","TOP_ORG_NM":"국회예산정책처","ORG_NM":None,"USR_NM":"관리자","LOAD_DATE":"2024-01-18","OPEN_DATE":"2018-07-27","DATA_START_YY":"1948","DATA_END_YY":"2024","STATBL_CMMT":"(舊)원: 1948~1952, 환: 1953~1962, 100 (舊)원 = 1환, 10환 = 1원","SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T184703004345091.do"},{"CATE_FULLNM":"재정통계>세입세출통계","STATBL_ID":"T183483004332601","STATBL_NM":"세출예산규모(추경기준)","DTACYCLE_NM":"년","TOP_ORG_NM":"국회예산정책처","ORG_NM":None,"USR_NM":"관리자","LOAD_DATE":"2023-08-04","OPEN_DATE":"2018-07-27","DATA_START_YY":"2010","DATA_END_YY":"2023","STATBL_CMMT":"(舊)원: 1948~1952, 환: 1953~1962, 100 (舊)원 = 1환, 10환 = 1원","SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T183483004332601.do"},{"CATE_FULLNM":"공공기관 통계>인력현황","STATBL_ID":"T184833004126869","STATBL_NM":"공공기관 임직원 현황(정원)","DTACYCLE_NM":"년","TOP_ORG_NM":"기획재정부","ORG_NM":None,"USR_NM":"국회예산정책처","LOAD_DATE":"2023-08-02","OPEN_DATE":"2018-07-26","DATA_START_YY":"2013","DATA_END_YY":"2022","STATBL_CMMT":" 공공기관(부설기관 포함)의 임원, 정규직에 대한 총 정원","SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T184833004126869.do"},{"CATE_FULLNM":"조세통계>국제비교","STATBL_ID":"T208923006467320","STATBL_NM":"OECD 국가의 조세부담률","DTACYCLE_NM":"년","TOP_ORG_NM":"OECD","ORG_NM":None,"USR_NM":"국회예산정책처","LOAD_DATE":"2023-10-10","OPEN_DATE":"2020-02-18","DATA_START_YY":"1965","DATA_END_YY":"2022","STATBL_CMMT":"자료 : OECD Revenue Statistics\r\n주: 1) 조세부담률은 조세수입의 명목GDP 대비 비율\r\n2) 우리나라 조세부담률은 신계열 명목GDP 반영(2010년→2015년으로 기준년 개편)\r\n3) 2018년 OECD 평균은 미제출국가(호주, 일본) 전년수준 가정","SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T208923006467320.do"},{"CATE_FULLNM":"조세통계>국제비교","STATBL_ID":"T186633000344135","STATBL_NM":"OECD 국가의 세목별 GDP 대비 비중","DTACYCLE_NM":"년","TOP_ORG_NM":"OECD","ORG_NM":None,"USR_NM":"국회예산정책처","LOAD_DATE":"2023-07-14","OPEN_DATE":"2018-07-18","DATA_START_YY":"1965","DATA_END_YY":"2021","STATBL_CMMT":"자료: OECD statistics, Revenue Statistics\r\n주: 개인소득세 1100, 법인세 1200, 사회보장기여금 2000, 급여세 3000, 재산세 4000, 일반소비세 5110, 개별소비세 5120, 기타 6000","SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T186633000344135.do"},{"CATE_FULLNM":"조세통계>국제비교","STATBL_ID":"T188153000357469","STATBL_NM":"OECD 국가의 세목별 총조세 대비 비중","DTACYCLE_NM":"년","TOP_ORG_NM":"OECD","ORG_NM":None,"USR_NM":"국회예산정책처","LOAD_DATE":"2023-07-14","OPEN_DATE":"2018-07-18","DATA_START_YY":"1965","DATA_END_YY":"2021","STATBL_CMMT":"자료: OECD statistics, Revenue Statistics\r\n주: 개인소득세 1100, 법인세 1200, 사회보장기여금 2000, 급여세 3000, 재산세 4000, 일반소비세 5110, 개별소비세 5120, 기타 6000","SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T188153000357469.do"},{"CATE_FULLNM":"공공기관 통계>인력현황","STATBL_ID":"T198613006077346","STATBL_NM":"공공기관 신규채용 현황","DTACYCLE_NM":"년","TOP_ORG_NM":"기획재정부","ORG_NM":None,"USR_NM":"국회예산정책처","LOAD_DATE":"2023-08-02","OPEN_DATE":"2019-05-07","DATA_START_YY":"2013","DATA_END_YY":"2022","STATBL_CMMT":None,"SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T198613006077346.do"},{"CATE_FULLNM":"재정통계>세입세출통계","STATBL_ID":"T184173004318491","STATBL_NM":"세출결산규모","DTACYCLE_NM":"년","TOP_ORG_NM":"국회예산정책처","ORG_NM":None,"USR_NM":"관리자","LOAD_DATE":"2023-08-03","OPEN_DATE":"2018-07-27","DATA_START_YY":"1948","DATA_END_YY":"2022","STATBL_CMMT":"(舊)원: 1948~1952, 환: 1953~1962, 100 (舊)원 = 1환, 10환 = 1원","SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T184173004318491.do"},{"CATE_FULLNM":"조세통계>국제비교","STATBL_ID":"T185363000773228","STATBL_NM":"OECD 국가의 소득세 명목최고세율","DTACYCLE_NM":"년","TOP_ORG_NM":"OECD","ORG_NM":None,"USR_NM":"국회예산정책처","LOAD_DATE":"2023-07-17","OPEN_DATE":"2018-06-30","DATA_START_YY":"2000","DATA_END_YY":"2021","STATBL_CMMT":"자료: OECD Tax Database, 2021.10.를 바탕으로 국회예산정책처 작성\r\n주 1) 지방세율을 포함한 세율임\r\n    2) OECD는 소득세 최고세율을 2020년까지 집계･발표하고 있어 이를 반영\r\n    3) G7국가: 미국·영국·프랑스·독일·이탈리아·캐나다·일본 \r\n    4) 콜롬비아 추가","SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T185363000773228.do"},{"CATE_FULLNM":"재정통계>세입세출통계","STATBL_ID":"T188213004298116","STATBL_NM":"세입결산규모","DTACYCLE_NM":"년","TOP_ORG_NM":"국회예산정책처","ORG_NM":None,"USR_NM":"관리자","LOAD_DATE":"2023-08-03","OPEN_DATE":"2018-07-27","DATA_START_YY":"1948","DATA_END_YY":"2022","STATBL_CMMT":"(舊)원: 1948~1952, 환: 1953~1962, 100 (舊)원 = 1환, 10환 = 1원","SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T188213004298116.do"},{"CATE_FULLNM":"공공기관 통계>인력현황","STATBL_ID":"T194473006083911","STATBL_NM":"공공기관 기관장 평균연봉","DTACYCLE_NM":"년","TOP_ORG_NM":"기획재정부","ORG_NM":None,"USR_NM":"국회예산정책처","LOAD_DATE":"2023-08-02","OPEN_DATE":"2019-05-07","DATA_START_YY":"2013","DATA_END_YY":"2022","STATBL_CMMT":" 공공기관(부설기관 포함)의 상임기관장 평균 연봉","SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T194473006083911.do"},{"CATE_FULLNM":"조세통계>국제비교","STATBL_ID":"T187453000786735","STATBL_NM":"OECD 국가의 법인세 명목최고세율","DTACYCLE_NM":"년","TOP_ORG_NM":"OECD","ORG_NM":None,"USR_NM":"국회예산정책처","LOAD_DATE":"2023-07-11","OPEN_DATE":"2018-06-30","DATA_START_YY":"2000","DATA_END_YY":"2023","STATBL_CMMT":"자료: OECD Tax Database를 바탕으로 국회예산정책처 작성\r\n주: 1) 지방세율을 포함한 세율임\r\n2) OECD 평균: 2020년 가입한 콜롬비아를 포함한 37개국 기준\r\n3) G7국가: 미국·영국·프랑스·독일·이탈리아·캐나다·일본 ","SRV_URL":"http://www.nabostats.go.kr/portal/stat/easyStatPage/T187453000786735.do"}]}]}
    url = f"https://www.nabostats.go.kr/openapi/Sttsapitbl.do?Type=json&KEY={os.getenv('ASSEMBLY_STAT_KEY')}"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    data = json.loads(response.text)
    #
    return {
        "data": [x for (i, x) in enumerate(data["Sttsapitbl"][1]["row"]) if
                 i in [0, 2, 3, 4, 14, 15, 43, 50, 51, 55, 57, 62, 65, 72, 79, 80, 87, 90]][::-1]
        # "data": data["Sttsapitbl"][1]["row"][70:]
    }


@router.get("/stat/data")
async def get_stat_Data(statbl_id: str):
    print(statbl_id)
    url = f"https://www.nabostats.go.kr/openapi/Sttsapitbldata.do?STATBL_ID={statbl_id}&DTACYCLE_CD=YY&Type=json&KEY={os.getenv('ASSEMBLY_STAT_KEY')}&pSize=1000"
    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    data = json.loads(response.text)

    print([x for x in data["Sttsapitbldata"][1]["row"] if x["DTA_VAL"] != None])

    def applyfunc(x):
        if x['CLS_NM'] is not None and x['CLS_NM'] != "":
            x["ITM_NM"] = f'{x["ITM_NM"]}({x["CLS_NM"]})'
        return x

    if "Sttsapitbldata" in data:
        return {
            "data": [applyfunc(x) for x in data["Sttsapitbldata"][1]["row"] if x["DTA_VAL"] != None]
        }
    else:
        return {
            "data": []
        }


class GptInput(BaseModel):
    statbl_id: str
    prompt: str
    stat_data: list


class EditGptInput(BaseModel):
    statbl_id: str
    prompt: str
    stat_data: list
    graph_type: int
    template_index : int


@router.post("/stat/gpt/range")
async def gpt_range(gpt_input: GptInput):
    global df
    df = pd.DataFrame(gpt_input.stat_data)
    df = df.rename(columns={"year": "연도", "name": "항목", "unit": "단위", "value": "값"})

    client = openai.OpenAI(api_key=os.getenv('OPEN_AI_KEY'))

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": """You are using Python pandas library.
        Name of dataframe is 'df', which has the following columns:
        '연도', '항목', '단위', '값'.
        After processing the data, you should save the result as 'df'.
        Just provide Python code without description. You don't need to import library or print result.
        Example : df = df[(df['연도'] >= 1980)]
        """},
            {"role": "user", "content": gpt_input.prompt},
        ]
    )

    gpt_result = response.choices[0].message.content
    gpt_result = gpt_result.replace("```python\n", "").replace("\n```", "")
    print(gpt_result)
    loc = {}

    exec(gpt_result, globals(), loc)
    df = loc["df"]

    df['연도'] = df['연도'].astype(str)
    df = df.rename(columns={"연도": "WRTTIME_IDTFR_ID", "항목": "ITM_NM", "단위": "UI_NM", "값": "DTA_VAL"})

    return {
        "data": json.loads(df.to_json(orient='records'))
    }


@router.post("/stat/gpt/edit")
async def gpt_edit(gpt_input: EditGptInput, api_response: Response):
    global df
    import matplotlib.font_manager as fm
    import socket


    if socket.gethostname()[:7] == "DESKTOP":
        font_name = "Malgun Gothic"
    else:
        font_location = './static/NanumGothic.ttf'  # 폰트 위치

        font_name = fm.FontProperties(fname=font_location).get_name()




    plt.rc("font", family=font_name)
    sns.set(font=font_name,
            rc={"axes.unicode_minus": False}, style='white')

    df = pd.DataFrame(gpt_input.stat_data)

    df_str = str(df.values.tolist())

    df = df.rename(columns={"year": "연도", "name": "항목", "unit": "단위", "value": "값"})

    template_code = ""

    if gpt_input.graph_type == 0:
        if gpt_input.template_index == 0:
            template_code = """You should include below source code between chevrons.
<<<
import seaborn as sns
import matplotlib.pyplot as plt

max_value_index = df['값'].idxmax()
clrs = ['grey' if (x < max_value_index) else 'yellow' for x in df.index]

fig = plt.figure(figsize=(10,6))
sns.barplot(x='연도', y='값', data=df, palette=clrs)
>>>
"""
        elif gpt_input.template_index == 1:
            template_code = """You should include below source code between chevrons.
            <<<
import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(10,6))
fig = sns.barplot(x='연도', y='값', data=df, color='orange')
plt.ylim(min(df['값']) * 0.95, max(df['값'])+1)
plt.show()
            >>>
            """

        elif gpt_input.template_index == 2:
            template_code = """You should include below source code between chevrons.
            <<<
import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(10,6))
fig = sns.barplot(x='연도', y='값', data=df, palette='rainbow')
plt.show()
            
            >>>
            """
        elif gpt_input.template_index == 3:
            template_code = """You should include below source code between chevrons.
            <<<
import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
fig = sns.barplot(data=df, x='연도', y='값', hue='항목', palette=['white'])
fig.grid(False)
fig.set_facecolor('lightgrey')

# Changing bar border color and hatch
for rectangle in fig.patches:
    rectangle.set_hatch('/')
    rectangle.set_edgecolor('black')
    rectangle.set_linewidth(2)
            >>>
            """

    client = openai.OpenAI(api_key=os.getenv('OPEN_AI_KEY'))

    prompt_dict = {
        0: "막대 그래프를 그려줘.",
        1: "꺾은선 그래프를 그려줘.",
        2: "원그래프를 그려줘."
    }

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": f"""You are using Python pandas and seaborn library.
        Name of dataframe is 'df', which has the following columns:
        '연도'(int), '항목'(string), '단위'(string), '값'(double).
        Below is the data you provided.
        [
        {df_str}
        ]
        {template_code}
        Just provide Python code without description. Save the chart variable as 'fig'.
      
        """},
            {"role": "user", "content": prompt_dict[gpt_input.graph_type] + gpt_input.prompt},
        ]
    )

    gpt_result = response.choices[0].message.content
    gpt_result = gpt_result.replace("```python\n", "").replace("\n```", "")

    if not('a' <= gpt_result[0] <= "z" or 'A' <= gpt_result[0] <='Z'):
        gpt_result = "# " + gpt_result

    loc = {}
    print(gpt_result)

    is_error = False
    try:
        exec(gpt_result, globals(), loc)
        fig = loc["fig"]
        plt.legend(fontsize=5)

    except Exception as e:
        print(e)
        is_error = True
    # print(loc)

    if is_error is False:

        import io
        import base64
        # my_stringIObytes = io.BytesIO()
        import uuid

        uuid = str(uuid.uuid4())
        fig.figure.savefig("./result/images/" + uuid + ".jpg", format='jpg')
        # my_stringIObytes.seek(0)
        # my_base64_jpgData = base64.b64encode(my_stringIObytes.read()).decode()
        # print(my_base64_jpgData)
        print(uuid)
        return {
            "data": uuid + ".jpg",
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    else:
        raise HTTPException(status_code=404, detail="invalid name")
    # df['연도'] = df['연도'].astype(str)
    # df = df.rename(columns={"연도": "WRTTIME_IDTFR_ID", "항목": "ITM_NM", "단위": "UI_NM", "값": "DTA_VAL"})
    #
    # return {
    #     "data": json.loads(df.to_json(orient='records'))
    # }


@router.get("/download/photo/{photo_url}")
async def download_photo(photo_url: str):
    return FileResponse("./result/images/" + photo_url)

@router.get("/template/{photo_url}")
async def download_template_image(photo_url: str):
    return FileResponse("./result/templates/" + photo_url)
