from crawler.crawler import getFullHouseList
import copy

taipei_region_code = 1
newtaipei_region_code = 3


def basicQueryString():
    queryString = {
        'type': 1,
        #  'searchtype': 1,
        'role': 1,  #屋主刊登
        # 'multiPrice': ['10000_20000', '20000_30000'],  #租金
        'multiPrice': '10000_20000,20000_30000',  #租金
        'orderType': 'desc',  # 最新
        'multiNotice': 'not_cover',  # 排除頂加
        'not_cover': 1,
        'totalRows': 90,
        'shType': 'host'
    }
    return copy.deepcopy(queryString)


def QueryStringPrice(option, price):
    prices = {10000: '10000_20000', 20000: '20000_30000'}
    option['multiPrice'] = prices[price]
    return option


def crawTaipeiHouseList(filter_func=None):
    option1 = basicQueryString()
    option1['kind'] = 1  #整層住家
    QueryStringPrice(option1, 10000)
    houseList1 = getFullHouseList(taipei_region_code, option1, filter_func)
    QueryStringPrice(option1, 20000)
    houseList2 = getFullHouseList(taipei_region_code, option1, filter_func)

    option2 = basicQueryString()
    option2['kind'] = 2  #獨立套房
    option2['other'] = 'lift'  #有電梯
    QueryStringPrice(option2, 10000)
    houseList3 = getFullHouseList(taipei_region_code, option2, filter_func)
    QueryStringPrice(option2, 20000)
    houseList4 = getFullHouseList(taipei_region_code, option2, filter_func)

    return houseList1 + houseList2 + houseList3 + houseList4
