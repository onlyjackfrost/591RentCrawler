from crawler.utils import checkStatusCode, getHouseList, getTotalNumber
from crawler.singleton import session, csrf_Token
from logger.logger import logCrawlProgress


def getHouseListHtml(session, region_code, row_Number, options):
    url_getHouseListApi = 'https://rent.591.com.tw/home/search/rsList'
    options['firstRow'] = row_Number

    my_headers = {'X-CSRF-TOKEN': csrf_Token}
    response = session.get(url_getHouseListApi,
                           headers=my_headers,
                           params=options,
                           cookies={'urlJumpIp': str(region_code)})
    if checkStatusCode(response.status_code) is False:
        return ""

    html_text = response.text
    print(html_text[:30])
    return html_text


def getFullHouseList(region_code, options, filter_func=None):
    number = 0
    totalNumber = 1
    loop = 0
    houseList = []
    while number < totalNumber:
        if loop > 20:
            break
        loop += 1
        html_text = getHouseListHtml(session, region_code, number, options)

        if html_text == "":
            logCrawlProgress("failure, fuck\n")
            break

        house_list = getHouseList(html_text)
        number += len(house_list)
        if filter_func:
            house_list = filter_func(house_list)
        houseList += house_list

        totalNumber = getTotalNumber(html_text)
        logCrawlProgress("{0}-{1}  {2}\n".format(number - 30, number,
                                                 totalNumber))
    return houseList