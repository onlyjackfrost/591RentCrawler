from click.decorators import option
from crawler.crawler import getFullHouseList
import copy

taipei_region_code = 1
newtaipei_region_code = 3


def basicQueryString():
    queryString = {
        'type': 1,
        'orderType': 'desc',  # 最新
        'multiNotice': 'not_cover',  # 排除頂加
        'not_cover': 1,
        'totalRows': 90,
        'shType': 'host',
    }
    return copy.deepcopy(queryString)


def QueryStringPrice(option, price):
    prices = {10000: '10000_20000', 20000: '20000_30000'}
    option['multiPrice'] = prices[price]


def crawTaipeiHouseList(filter_func=None, options=None):
    option1 = basicQueryString()
    if options:
        option1.update(options)
    option1['kind'] = 1  #整層住家
    QueryStringPrice(option1, 10000)
    houseList1 = getFullHouseList(taipei_region_code, option1, filter_func)
    QueryStringPrice(option1, 20000)
    houseList2 = getFullHouseList(taipei_region_code, option1, filter_func)

    option2 = basicQueryString()
    if options:
        option1.update(options)
    option2['kind'] = 2  #獨立套房
    option2['other'] = 'lift'  #有電梯
    QueryStringPrice(option2, 10000)
    houseList3 = getFullHouseList(taipei_region_code, option2, filter_func)
    QueryStringPrice(option2, 20000)
    houseList4 = getFullHouseList(taipei_region_code, option2, filter_func)

    return houseList1 + houseList2 + houseList3 + houseList4


def crawNewTaipeiLocationsHouseList(filter_func=None, locations=[], options=None):
    def query_by_location(filter_func=None, location=0, options=None):
        house_list = []
        option = basicQueryString()
        # option['region'] = 3
        option['section'] = location  # 位置
        option['searchtype'] = 1  # 猜測是跟section同時出現的query string
        #整層住家 & 1~2w 2~3w
        option['kind'] = 1
        QueryStringPrice(option, 10000)
        if options:
            option.update(options)
        houses = getFullHouseList(newtaipei_region_code, option, filter_func)
        house_list += houses
        QueryStringPrice(option, 20000)
        houses = getFullHouseList(newtaipei_region_code, option, filter_func)
        house_list += houses

        option['kind'] = 2  #獨立套房
        option['other'] = 'lift'  #有電梯
        QueryStringPrice(option, 10000)
        if options:
            option.update(options)
        houses = getFullHouseList(newtaipei_region_code, option, filter_func)
        house_list += houses
        QueryStringPrice(option, 20000)
        houses = getFullHouseList(newtaipei_region_code, option, filter_func)
        house_list += houses
        return house_list

    house_list = []
    for location in locations:
        try:
            houses = query_by_location(filter_func=filter_func,
                                       location=location)
            house_list += houses
        except:
            continue
    return house_list
