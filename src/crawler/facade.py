from pprint import pprint
from crawler.crawler import getFullHouseList, getHouseDetailHtml
import copy
import json

taipei_region_code = 1
newtaipei_region_code = 3


def get_basicOption():
    basicOption = {
        'type': 1,
        #  'searchtype': 1,
        'role': 1,  #屋主刊登
        'multiPrice': ['10000_20000', '20000_30000'],
        'orderType': 'desc',
        'multiNotice': 'not_cover',
        'not_cover': 1,
        'totalRows': 90
    }
    return copy.deepcopy(basicOption)


def crawTaipeiHouseList(filter_func=None):
    option1 = get_basicOption()
    option1['kind'] = 1  #整層住家
    houseList1 = getFullHouseList(taipei_region_code, option1, filter_func)

    option2 = get_basicOption()
    option2['kind'] = 2  #獨立套房
    houseList2 = getFullHouseList(taipei_region_code, option2, filter_func)
    # pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(house_list[0])
    return houseList1 + houseList2


def test():
    # option1 = get_basicOption()
    # option1['kind'] = 1  #整層住家
    # houseList1 = getFullHouseList(taipei_region_code, option1)
    # //*[@id="rightConFixed"]/section/div[2]/div/div[1]/span[2]
    soup = getHouseDetailHtml(taipei_region_code)
    rightConFixed = soup.find("div", {"id": "rightConFixed"})
    print(rightConFixed)
    contact = rightConFixed.find("contact")
    print('======================')
    print(contact)
    # house_dict = json.loads(html_text)
    # pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(houseList1)