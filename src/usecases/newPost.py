import pprint
from crawler.facade import crawTaipeiHouseList


def sendNewRentPost():
    def filter_posttime_in_hours(houseList):
        print(houseList[0])
        return [house for house in houseList if '分鐘' in house['posttime']]

    post_list = crawTaipeiHouseList(filter_posttime_in_hours)
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint([house['posttime'] for house in post_list])
    
    post_ids = [int(p.post_id) for p in post_list]


def toLineNotifyView()