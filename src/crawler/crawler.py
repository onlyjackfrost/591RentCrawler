from crawler.utils import checkStatusCode, getHouseList, getTotalNumber
from crawler.singleton import session_591
from logger.logger import logCrawlProgress


def session():
    return session_591.session


def token():
    return session_591.token


def getHouseListHtml(region_code, row_Number, options):
    url_getHouseListApi = 'https://rent.591.com.tw/home/search/rsList'
    options['firstRow'] = row_Number

    my_headers = {'X-CSRF-TOKEN': token(), 'User-Agent': 'Custom'}
    response = session().get(url_getHouseListApi,
                             headers=my_headers,
                             params=options,
                             cookies={'urlJumpIp': str(region_code)})
    if response.status_code == 419:
        session_591.update_token()
        my_headers['X-CSRF-TOKEN'] = token()
        print('csrf-token updated')
        response = session().get(url_getHouseListApi,
                                 headers=my_headers,
                                 params=options,
                                 cookies={'urlJumpIp': str(region_code)})
    if checkStatusCode(response.status_code) is False:
        return ""

    html_text = response.text
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
        html_text = getHouseListHtml(region_code, number, options)
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