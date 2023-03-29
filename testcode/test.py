import os
import requests
from bs4 import BeautifulSoup
from urllib3.packages.six import b 

def get_dir_lsit(dir):
    str_lsit=""
    if os.path.exists(dir):
        file_list = os.listdir(dir)
        file_list.sort()
        for f in file_list:
            full_path = os.path.join(dir, f)
            if os.path.isdir(full_path):
                f = "["+f+"]"
            str_lsit +=f
            str_lsit +="\n"
    str_lsit.strip()
    return str_lsit

#날씨를 구해보자
def get_weather(where):
    weather = ""
    url = "https://search.naver.com/search.naver?query={}+날씨".format(where)
    r = requests.get(url)
    bs = BeautifulSoup(r.text, "lxml")
    w_box = bs.select("div.today_area._mainTabContent > div.main_info")
    
    if len(w_box) > 0 :
        temperature = bs.select("div.info_data > p.info_temperature > span.todaytemp")
        cast_text = bs.select("#main_pack > section.sc_new.cs_weather._weather > div > div.api_cs_wrap > div.weather_box > div.weather_area._mainArea > div.today_area._mainTabContent > div.main_info > div > ul > li:nth-child(1) > p")
        indicator  = bs.select("#main_pack > section.sc_new.cs_weather._weather > div > div.api_cs_wrap > div.weather_box > div.weather_area._mainArea > div.today_area._mainTabContent > div.main_info > div > ul > li:nth-child(3) > span")
        
        if len(temperature) >0 and len(cast_text)>0 and len(indicator)>0:
            temperature = temperature[0].text.strip()
            indicator = indicator[0].text.strip()
            txt = cast_text[0].text.strip()

            print(temperature, indicator, cast_text)

            weather = "{}℃ \r\n{}\r\n{}".format(temperature, indicator, txt)
    return weather

#환율정보 구하기

MONEY_NAME = {
    "유로" : "유럽연합 EUR",
    "엔" : "일본 JPY (100엔)",
    "위안" : "중국 CNY",
    "홍콩달라" :  "홍콩 HKD",
    "타이완달라" : "대만 TWD",
    "파운드" : "영국 GBP",
    "달라" : "미국 USD"
}

def get_exchange_info():
    EXCHANGE_LIST = {}
    url = "https://finance.naver.com//marketindex/exchangeList.nhn"
    r = requests.get(url)
    bs = BeautifulSoup(r.text, "lxml")
    trs = bs.select("body > div > table > tbody > tr")
    for tr in trs:
        tds = tr.select("td")
        name  = tds[0].text.strip()
        value = tds[1].text.replace(",", "").strip()
        EXCHANGE_LIST[name] =value
    return EXCHANGE_LIST

def mony_transalte(keword):
    EXCHANGE_LIST = get_exchange_info()
    kewords = []
    for m in MONEY_NAME.keys():
        if m in keword:
            kewords.append(keword[0:keword.find(m)].strip())
            kewords.append(m)
            break
    
    if kewords[1] in MONEY_NAME:
        country = MONEY_NAME[kewords[1]]

        if country in EXCHANGE_LIST:
            money = float(EXCHANGE_LIST[country])
            if country == "일본 JPY (100엔)":
                money /=100
            
            money = format(round(float(money) * float(kewords[0]),3),",")
            output = "{}원".format(money)
            return output


print(mony_transalte("150달라"))




