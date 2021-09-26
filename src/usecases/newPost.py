import pprint
from crawler.facade import crawTaipeiHouseList


def sendNewRentPost():
    def filter_posttime_in_hours(houseList):
        print(houseList[0])
        return [house for house in houseList if '分鐘' in house['posttime']]

    post_list = crawTaipeiHouseList(filter_posttime_in_hours)
    # pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint([house['posttime'] for house in post_list])

    post_ids = [int(p.post_id) for p in post_list]
    post_id_sent = get_post_id_in_hours()
    new_post_ids = list(set(post_ids).difference(set(post_id_sent)))

    # get detail of new_post_ids
    to_send = []
    for new_post_id in new_post_ids:
        detail = crawHouseDetail(new_post_id)
        to_send.append(detail)

    # transfer to Line message view
    to_send = [toLineNotifyView(houseObj) for houseObj in to_send]


def get_post_id_in_hours():
    return []


# /crawler
def crawHouseDetail(post_id):
    pass


def toLineNotifyView(house):
    return house