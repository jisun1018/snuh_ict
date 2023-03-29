import requests
from bs4 import BeautifulSoup

def get_weather(where):
    weather = ""
    url = "https://search.naver.com/search.naver?query={}+날씨".format(where)
    r = requests.get(url)
    bs = BeautifulSoup(r.text, "lxml")

    # 날씨정보가 제공되는 큰 박스를 찾습니다.
    w_box = bs.select_one("div.weather_info > div.status_wrap")

    if w_box:
        # 온도가 표시된 div 를 찾습니다. 여기서는 select_one 함수를 사용해서
        # 요소를 1개만 선택합니다.
        temp = w_box.select_one("div.temperature_text")
        # 온도 정보 박스 내부에는 span 태그에 '현재 온도' 글자와 ° 문자가 있는데
        # 이 정보는 필요없는 정보 입니다. 그걸 삭제 하기 위해서
        # 먼저 span 태그를 선택합니다. 여기서는 select() 함수를 사용했으므로
        # 모든 span 태그가 복수개로 선택됩니다.
        spans = temp.select("span")
        # span 갯수만큼 반복하며 decompose() 함수를 사용하면 해당 요소가 삭제되는데
        # 이 삭제는 원본 w_box 에서 아예 사라지게 됩니다.
        [s.decompose() for s in spans]
        # 그래서 다시 temp 에서 select_one 을 수행하면 삭제된 상태의 결과에서
        # 선택되므로 span 이 제거된 결과를 얻게 됩니다.
        temperature = temp.select_one("strong").text
        
        # 어제비교 날씨 정보를 구하기 위해 div 를 선택하고 text 값을 추출합니다.
        w_text = w_box.select_one("div.temperature_info").text
        # text 값을 보면 띄어쓰기가 연속적으로 된 것들이 있어 이를 제거 하기위해
        # split 후 다시 join 합니다.
        w_text = ' '.join(w_text.split())

        # 미세먼지, 초미세먼지... 등의 정보가 담긴 ul > li 요소를 선택합니다.
        # 이 요소는 여러개로 존재하기 때문에 select() 함수로 선택합니다.
        lists = w_box.select("ul.today_chart_list > li")
        w_list = []
        # li 요소를 반복합니다.
        for li in lists:
            # li 요소 하위에 a 태그의 내용에 필요한 정보가 담겨 있습니다.
            # a 태그의 text 값을 구합니다.
            w_string = li.select_one("a").text.strip()
            w_list.append(w_string)
        
        # 최종 결과 문자열 값을 설정합니다.
        weather = "{}℃\r\n{}\r\n{}".format(temperature, w_text, "\n".join(w_list))
    return weather
