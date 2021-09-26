from crawler.utils import checkStatusCode, getHouseList, getTotalNumber
from crawler.singleton import session, csrf_Token
from crawler.logger import logCrawlProgress
import time
import pprint


#api範例:
#https://rent.591.com.tw/home/search/rsList?is_new_list=1&type=1&kind=0&searchtype=1&region=3&firstRow=30&totalRows=9005
#https://rent.591.com.tw/home/search/rsList?is_new_list=1&type=1&kind=0&searchtype=1&region=3&firstRow=60&totalRows=9010
#......
#https://rent.591.com.tw/home/search/rsList?is_new_list=1&type=1&kind=0&searchtype=1&region=3&firstRow=9000&totalRows=9011
#根據地區碼和資料行數發送一次request, 回傳的純HTML包含三十筆房屋資料
def getHouseListHtml(session, region_code, row_Number, options):
    url_getHouseListApi = 'https://rent.591.com.tw/home/search/rsList'
    options['firstRow'] = row_Number

    my_headers = {'X-CSRF-TOKEN': csrf_Token}
    # pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(my_headers)
    response = session.get(url_getHouseListApi,
                           headers=my_headers,
                           params=options,
                           cookies={'urlJumpIp': str(region_code)})

    if checkStatusCode(response.status_code) is False:
        return ""

    html_text = response.text
    return html_text


def getFullHouseList(region_code, options, filter_func=None):
    number = 0
    totalNumber = 0
    loop = 0
    houseList = []
    # print('11111')
    while number <= totalNumber:
        if loop > 20:
            break
        loop += 1
        html_text = getHouseListHtml(session, region_code, number, options)
        # print(html_text)

        if html_text == "":
            logCrawlProgress("failure, fuck\n")
            break

        house_list = getHouseList(html_text)
        if filter_func:
            house_list = filter_func(house_list)
        houseList += house_list

        number += 30
        totalNumber = getTotalNumber(html_text)
        print(totalNumber, number)
        timeString = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime())
        logCrawlProgress("{0}  {1}-{2}  {3}\n".format(timeString, number - 30,
                                                      number, totalNumber))
    return houseList