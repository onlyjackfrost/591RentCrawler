from crawler.crawler import getFullHouseList
import copy

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

def crawTaipeiHouseList():
    option1 = get_basicOption()
    option1['kind'] = 1 #整層住家
    houseList1 = getFullHouseList(taipei_region_code, option1)
    
    option2 = get_basicOption()
    option2['kind'] = 2 #獨立套房
    houseList2 = getFullHouseList(taipei_region_code, option2)
    # pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(house_list[0])
    return houseList1 + houseList2