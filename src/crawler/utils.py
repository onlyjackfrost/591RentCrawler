
import json, requests


#請求狀態等於200就回傳true
def checkStatusCode(status_code):
    return status_code == requests.codes.ok

#傳入純HTML, 解析出其中的三十筆房屋資料的id
def getHouseList(html_text):
    house_dict = json.loads(html_text)  #house_dict是完整的json檔
    house_list = house_dict['data']['data']  #house_list是三十筆房屋資料形成的List
    return house_list


#傳入純HTML, 解析出該地區資料總筆數(總筆數會浮動)
def getTotalNumber(html_text):
    house_dict = json.loads(html_text)  #house_dict是完整的json檔
    totalNumber = house_dict['records']
    return int(totalNumber.replace(',', ''))


def parseDataCared(house_list):
    attr_cares = ['id', 'address', 'price']
    for house in house_list:
        print(house)
